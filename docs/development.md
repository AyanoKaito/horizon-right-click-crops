# Development preparation

## Current stage

The user authorized actual wheat implementation on 2026-10-30 after the successful foundation smoke test. The source for `0.1.0-dev.2` now includes a standalone-tested payment core and revision-pinned game adapters; native build and gameplay validation are recorded in [wheat-validation.md](wheat-validation.md). Read the [integration contract](../specs/001-wheat-harvest/contracts.md) for current boundaries. The preparation history below describes earlier gates, not a continuing prohibition on this authorized work.

The user's subsequent continuation covered additional isolated single-player verification: paired ordinary-game loot comparisons, authoritative Fortune/Silk Touch fixtures, nonempty seedless loot, ground-seed exclusion and item persistence, ordinary berries and restart-disabled actions. No gameplay source change or native rebuild was needed for those additional checks. Twenty-four Python tests now include the standalone observation verifier. Third-party protection/capability work, default-speed growth timing and multiplayer remain separate unverified scope.

## Foundation and preparation history

The harmless `dev.1` native foundation compiled against the pinned Horizon source on Windows, and its four tests passed both standalone and inside the game test binary. A separately approved isolated default-server-thread smoke test also passed, including the mod row, survival block-use logging, and disabling across a process restart. The test games were closed. At that stage, there was no harvesting implementation or release `.hnmod`; foundation checks were not harvest acceptance.

The [harmless `dev.1` native foundation](native-foundation.md) contained a dependency-free standalone library, three non-cancelling hooks, and a shared runtime. It targets Nightly `64e2989` and Mixins `3f99a5c...`; this exact pair passed foundation compilation, not gameplay compatibility testing. See [foundation-only tasks](../specs/001-wheat-harvest/foundation-tasks.md). That earlier version contained no harvesting, loot calculation, inventory payment, or crop mutation.

The user explicitly approved missing source/tool downloads, compilation, and Rust tests, but not game launch. The 15 structural checks, four standalone runtime tests, exact Mixins tool build, real target resolution, pristine-source check, AST audit, and four audit-tool tests passed. The first native compile exposed an incorrect hit type in the observer; it was corrected to `crate::game::Hit`, restaged through Mixins, and re-audited. The repeat native build and all four embedded runtime tests then passed. The other 159 upstream binary tests were filtered out. See [native-validation.md](native-validation.md) for commands, Windows staging limitations, and the local executable receipt.

The user subsequently granted game-launch approval. The smoke test used fresh homes under ignored `.local/runs/`, an explicit read path to already-prepared Nightly resources, and no account/session import. An offscreen game was driven through its own authenticated local control endpoint; control tokens were not printed. Setup used creative commands, then an actual right-click was performed in survival. Full product scenarios and no-cheat/non-OP claims remain untested.

The user approved the revised [wheat prototype specification](../specs/001-wheat-harvest/spec.md), covering held-click behavior, inventory fallback, and the test-setup clarification. Its [requirements quality checklist](../specs/001-wheat-harvest/checklists/requirements.md) records document review, not gameplay test results. The user then authorized technical planning: [plan.md](../specs/001-wheat-harvest/plan.md) began as a proposal, backed by [pinned-source research](../specs/001-wheat-harvest/research.md). At that earlier gate, gameplay implementation had not yet been approved; the later authorization and implementation status are recorded above. The ignored local `.specify/feature.json` points to `specs/001-wheat-harvest`.

The user approved the staged order and proceeding with launcher inspection and an isolated test profile. Launcher CLI version 0.2.26 was confirmed, and the empty `wheat-prototype` instance was created under ignored `.local/wheat-test-environment/`. See [test-environment.md](test-environment.md) for isolation boundaries and actual diagnostics. Exact source/tool pins, downloads, native execution trust, and gameplay implementation remain separate gates; no game/toolchain was installed or built during this preparation.

A subsequent user-authorized read-only inspection confirmed that the ordinary launcher already has Rust/Cargo 1.99.1, MinGW, Mixins `0d6b103...`, dependency/build caches, a ready native build, and the candidate Nightly game/resources. The earlier missing-toolchain observation was scoped to the fresh isolated cache. Do not propose a full redownload without checking actual missing components; first agree on safe reuse of the installed tools/resources while keeping test saves and generated outputs separate.

## Language and local review

All Git-tracked files, code, comments, commit messages, and GitHub-facing text must be English. Conversation and local review material may be Russian. Keep that material under ignored `.local/review/`; never force-add it.

Byte-identical snapshots of eight Russian documents are preserved locally under `.local/review/ru-before-english/`. They predate the latest held-click, inventory-fallback, and test-setup decisions and are historical backups, not current requirements. The exact original brief is included there; `docs/original-brief.md` is its English archival translation. A current Russian review summary is kept locally in `.local/review/wheat-harvest.ru.md`, not linked as a dependency of published documentation.

On 2026-10-29, the user explicitly authorized replacing the original Russian-containing history of `main` with an English-only root commit. The previous complete history is preserved in the verified local bundle `.local/history-backup/before-english-rewrite.bundle`, excluded from Git. The authorized replacement push must use force-with-lease against the previously checked remote commit rather than an unguarded force push. This one-time approval does not authorize future history rewrites.

Replacing branch history removes old commits from the branch's reachable history, but does not guarantee erasure from GitHub's caches or unreachable-object storage. No old-history branch or tag should be published as part of this rewrite.

## Tools

- Python 3.12 is suitable for Spec Kit.
- Spec Kit CLI is pinned to `1.2.5` from the official PyPI package `specify-cli`; the [installation guide](https://github.github.io/spec-kit/installation.html) lists this as an official distribution channel.
- `.tools/spec-kit/` is an isolated project-local Python environment excluded from Git. Do not change system dependencies or neighboring projects.
- OpenCode commands are in `.opencode/commands/`; shared infrastructure is in `.specify/`. Extra extension/workflow packages and runtime events are not needed for this stage.
- Do not store passwords, tokens, account data, or game resources in documentation or commits.

Spec Kit 1.2.5 is installed and initialized with PowerShell scripts, the bundled OpenCode integration, and `--events false`. Generated commands/templates are tracked; local tools are not. No separate Rust skills have been installed.

### Recreating the tooling environment

From the repository root in PowerShell:

```powershell
python -m venv .tools/spec-kit
.\.tools\spec-kit\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements-tools.txt
.\.tools\spec-kit\Scripts\specify.exe version
.\.tools\spec-kit\Scripts\specify.exe integration status --json
.\.tools\spec-kit\Scripts\python.exe -m pip check
```

Do not repeat `specify init --force` in an existing clone: infrastructure is already tracked. The original initialization command is recorded for audit, not for rerunning over edits:

```powershell
.\.tools\spec-kit\Scripts\specify.exe init --here --force --non-interactive --integration opencode --script ps '--integration-options=--events false'
```

The CLI version is pinned, but its complete transitive dependency graph is not locked yet. These are development tools, not the mod's runtime dependencies. The standalone Rust foundation uses only the standard library; its manually prepared lockfile passed an actual locked, offline Cargo test run. The AST audit has a separate development-only lockfile. Integration uses the exact source/tool pins recorded in `compatibility.json`, validated for foundation compilation only, not gameplay compatibility.

## Test preparation versus test execution

1. Use an isolated test world, never a real player save.
2. Creative mode and commands may provide farmland, crops, tools, seeds, and bone meal. Bone meal may prepare mature crops quickly; no survival resource grind is required for fixture preparation.
3. Before harvest assertions, switch the acting player back to survival. Record inventory contents and mode so creative item behavior or instant block breaking cannot mask a defect.
4. Test payment from loot, then controlled no-seed loot with an inventory seed, then no suitable seed in either source. Record inventory changes, ground drops, and the crop/farmland result separately. Preparing seeds in creative does not authorize free seeds during the survival harvest.
5. Check natural growth separately. Bone meal proves bone meal behavior, not random-tick growth. Report natural-growth checks as pending if not actually completed.
6. Distinguish setup privileges from runtime privileges. Survival checks in a command-enabled world do not by themselves prove a cheats-disabled world or non-OP multiplayer account was tested. Record the actual conditions before making a compatibility or permission claim.
7. Commands and cheat-dependent actions must never be part of the mod's normal harvesting path. Creative/adventure harvesting behavior remains undecided; creative fixture preparation does not approve it.

These are planned practices, not tests already run. Exact preparation commands and fixtures will be selected only after compatible revisions and a safe native build are agreed.

## Review gates

Requirements -> approved technical plan -> small testable tasks -> implementation -> actual checks. Spec Kit stores the process but does not guarantee safety or replace approval.

Do not run an automatic whole-mod implementation chain. After preparation, the first technical result is a reproducible minimal native foundation using isolated data, only after compatible revisions are selected and the user explicitly trusts the native build.

### Initial local preparation checks - 2026-10-29

- `specify integration status --json`: `ok`; managed files present and unmodified.
- `pip check`: no broken installed dependencies.
- Six PowerShell scripts passed syntax parsing; this does not validate every execution path.
- Local documentation links, ignore rules for tools/secrets/player data, and staged whitespace checks passed.
- A limited staged-content scan found no known key/token patterns; this is not a guarantee that every possible secret is absent.
- No shell-expansion blocks were found in the ten installed OpenCode commands. During initial installation, no specification or implementation was generated by running those commands.

At the preparation-only gate, gameplay checks had not run. The later wheat implementation and its partial game verification are recorded in [wheat-validation.md](wheat-validation.md). `.specify/memory/constitution.md` remains a draft for separate review.

## Before sending changes to GitHub

Local work does not require GitHub login. Creating a private remote requires the user's GitHub CLI authentication; never ask them to share credentials. Before pushing, inspect staged files, exclude local/game data, confirm English-only content, and verify the target repository.

Initial authentication and Git author blockers are resolved. The user authenticated and approved a GitHub noreply identity configured only in this repository; global settings were not changed.

The private repository is https://github.com/AyanoKaito/horizon-right-click-crops with remote `origin`. Private storage is not a public release. Making the repository public or publishing a release requires separate approval.
