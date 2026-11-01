// Read-only AST audit: remove exactly the declared additions in memory, then
// compare the remaining Rust syntax with pristine source. Never writes source.
use quote::ToTokens;
use std::{error::Error, fs, path::Path};
use syn::{Expr, File, ImplItemFn, Item, ItemFn, Stmt, visit_mut::VisitMut};

type Result<T> = std::result::Result<T, Box<dyn Error>>;

struct ExpectedHook {
    method: &'static str,
    helper: ItemFn,
    call: Expr,
    cancellable: bool,
    seen: usize,
}

impl ExpectedHook {
    fn load(bundle: &Path, method: &'static str, file: &str, call: &str) -> Result<Self> {
        Ok(Self {
            method,
            helper: syn::parse_str(&fs::read_to_string(bundle.join(file))?)?,
            call: syn::parse_str(call)?,
            cancellable: false,
            seen: 0,
        })
    }

}

struct RemoveHooks {
    hooks: Vec<ExpectedHook>,
    error: Option<String>,
}

impl VisitMut for RemoveHooks {
    fn visit_impl_item_fn_mut(&mut self, method: &mut ImplItemFn) {
        for hook in &mut self.hooks {
            if method.sig.ident != hook.method {
                continue;
            }
            hook.seen += 1;
            let helper = &hook.helper;
            let call = &hook.call;
            let expected: Stmt = if hook.cancellable {
                syn::parse_quote! {
                    if let ::core::ops::ControlFlow::Break(__horizon_mixins_return) = {
                        #helper
                        #call
                    } { return __horizon_mixins_return; }
                }
            } else {
                syn::parse_quote! { { #helper #call }; }
            };
            let matches = method.block.stmts.first().is_some_and(|actual| stmt_text(actual) == stmt_text(&expected));
            if matches {
                method.block.stmts.remove(0);
            } else {
                self.error = Some(format!("Unexpected generated head in {}", hook.method));
            }
        }
        syn::visit_mut::visit_impl_item_fn_mut(self, method);
    }
}

fn tokens(value: &impl ToTokens) -> String {
    value.to_token_stream().to_string()
}

fn item_text(item: &Item) -> String {
    prettyplease::unparse(&File { shebang: None, attrs: Vec::new(), items: vec![item.clone()] })
}

fn stmt_text(stmt: &Stmt) -> String {
    let body = syn::Block { brace_token: Default::default(), stmts: vec![stmt.clone()] };
    let function: ItemFn = syn::parse_quote!(fn audit_head() #body);
    item_text(&Item::Fn(function))
}

fn parse(path: &Path) -> Result<File> {
    Ok(syn::parse_file(&fs::read_to_string(path)?)?)
}

fn audit(source: &Path, stage: &Path, bundle: &Path, file: &str, kind: &str) -> Result<()> {
    let original = parse(&source.join(file))?;
    let mut generated = parse(&stage.join(file))?;
    let hooks = if kind == "game" {
        for (name, payload) in [("right_click_crops", "runtime.rs"), ("right_click_crops_gameplay", "gameplay.rs")] {
        let runtime = parse(&bundle.join(payload))?;
        let modules: Vec<_> = generated.items.iter().enumerate().filter_map(|(i, item)| {
            match item {
                Item::Mod(module) if module.ident == name => Some(i),
                _ => None,
            }
        }).collect();
        if modules.len() != 1 {
            return Err("Expected exactly one bundle module".into());
        }
        let Item::Mod(module) = generated.items.remove(modules[0]) else { unreachable!() };
        let Some((_, items)) = module.content else {
            return Err("Expected an inline bundle module".into());
        };
        if items.len() != runtime.items.len()
            || items.iter().zip(&runtime.items).any(|(a, b)| item_text(a) != item_text(b))
            || tokens(&module.vis) != "pub (crate)"
            || !module.attrs.is_empty()
        {
            let mismatch = items.iter().zip(&runtime.items).position(|(a,b)| item_text(a) != item_text(b));
            if let Some(index) = mismatch {
                eprintln!("Module {name}: item {index} differs after canonical printing");
            }
            return Err(format!("Generated module {name} differs from bundle source (item {mismatch:?})").into());
        }
        }
        Vec::new()
    } else if kind == "native" {
        vec![
            ExpectedHook::load(bundle, "native_tick", "startup.rs", "startup(&*self)")?,
            ExpectedHook::load(bundle, "native_mods", "register.rs", "register(mods)")?,
            ExpectedHook::load(
                bundle,
                "native_settings",
                "settings_list.rs",
                "settings_list(&mut *self, mod_id, buttons)",
            )?,
            ExpectedHook::load(
                bundle,
                "native_settings_click",
                "settings_click.rs",
                "settings_click(&mut *self, mod_id, button)",
            )?,
            ExpectedHook::load(
                bundle,
                "native_use_item_on",
                "use_item_on.rs",
                "use_item_on(&mut *self, pos, claimed)",
            )?,
            ExpectedHook::load(
                bundle,
                "native_use_item",
                "use_item.rs",
                "use_item(&*self, claimed)",
            )?,
            ExpectedHook::load(
                bundle,
                "native_right_click_block",
                "right_click_block.rs",
                "right_click_block(&mut *self, pos, canceled)",
            )?,
        ]
    } else {
        return Err(format!("Unknown audit kind: {kind}").into());
    };
    let mut visitor = RemoveHooks { hooks, error: None };
    visitor.visit_file_mut(&mut generated);
    if let Some(error) = visitor.error { return Err(error.into()); }
    if visitor.hooks.iter().any(|hook| hook.seen != 1) {
        return Err("Each expected method must occur exactly once".into());
    }
    // Canonical printing normalizes insignificant layout/trailing punctuation
    // that differs when the same runtime is nested inside the game module.
    if prettyplease::unparse(&original) != prettyplease::unparse(&generated) {
        return Err(format!("Original AST was not preserved in {file}").into());
    }
    println!("AST preserved: {file}");
    Ok(())
}

fn main() -> Result<()> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if args.len() != 3 { return Err("Usage: audit-bundle SOURCE STAGE BUNDLE".into()); }
    let (source, stage, bundle) = (Path::new(&args[0]), Path::new(&args[1]), Path::new(&args[2]));
    audit(source, stage, bundle, "crates/horizon-client/src/game.rs", "game")?;
    audit(source, stage, bundle, "crates/horizon-client/src/game/native_hooks.rs", "native")?;
    println!("Verified seven declared native-hook heads and two unchanged support modules.");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn visitor() -> RemoveHooks {
        RemoveHooks {
            hooks: vec![ExpectedHook {
                method: "action",
                helper: syn::parse_str("fn hook() {}").unwrap(),
                call: syn::parse_str("hook()").unwrap(),
                cancellable: false,
                seen: 0,
            }],
            error: None,
        }
    }

    #[test]
    fn removes_only_the_expected_head() {
        let original = syn::parse_file("impl Sample { fn action() { let kept = 42; } }").unwrap();
        let mut staged = syn::parse_file(
            "impl Sample { fn action() { { fn hook() {} hook() }; let kept = 42; } }",
        ).unwrap();
        let mut check = visitor();
        check.visit_file_mut(&mut staged);
        assert!(check.error.is_none());
        assert_eq!(check.hooks[0].seen, 1);
        assert_eq!(prettyplease::unparse(&original), prettyplease::unparse(&staged));
    }

    #[test]
    fn rejects_an_altered_helper() {
        let mut staged = syn::parse_file(
            "impl Sample { fn action() { { fn hook() { let extra = 1; } hook() }; } }",
        ).unwrap();
        let mut check = visitor();
        check.visit_file_mut(&mut staged);
        assert!(check.error.is_some());
    }

    #[test]
    fn verifies_cancellation_and_rejects_an_altered_return() {
        for (returned, valid) in [("__horizon_mixins_return", true), ("42", false)] {
            let mut staged = syn::parse_file(&format!(
                "impl Sample {{ fn action() {{ if let ::core::ops::ControlFlow::Break(__horizon_mixins_return) = {{ fn hook() {{}} hook() }} {{ return {returned}; }} let kept = 42; }} }}"
            )).unwrap();
            let mut check = visitor();
            check.hooks[0].cancellable = true;
            check.visit_file_mut(&mut staged);
            assert_eq!(check.error.is_none(), valid);
        }
    }

    #[test]
    fn retains_unrelated_body_changes_for_comparison_to_reject() {
        let original = syn::parse_file("impl Sample { fn action() { let kept = 42; } }").unwrap();
        let mut staged = syn::parse_file(
            "impl Sample { fn action() { { fn hook() {} hook() }; let kept = 99; } }",
        ).unwrap();
        let mut check = visitor();
        check.visit_file_mut(&mut staged);
        assert!(check.error.is_none());
        assert_ne!(prettyplease::unparse(&original), prettyplease::unparse(&staged));
    }

    #[test]
    fn does_not_treat_a_missing_method_as_an_audited_hook() {
        let mut staged = syn::parse_file("impl Sample { fn different() {} }").unwrap();
        let mut check = visitor();
        check.visit_file_mut(&mut staged);
        assert_eq!(check.hooks[0].seen, 0);
    }
}
