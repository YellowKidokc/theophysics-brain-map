# theophysics-brain-map

The map of the Theophysics brain — David Lowe's `X:\` working drive. Maps, conventions, prompts, and automation scripts that organize the brain. **Not the brain itself** — vault content, model weights, NLP code, and pipeline data stay off git.

**Source of truth:** `X:\` on the NAS (`\\dlowenas\brain\`). This repo mirrors the organizational layer.
**Owner:** David Lowe (POF 2828)
**Last synced:** 2026-05-16
**Plan that drove this:** [`plan/yes-i-want-togo-agile-puddle.md`](plan/yes-i-want-togo-agile-puddle.md)

---

## What's in here

| Path | What it is |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | The X:\ brain system map — 11 Mermaid diagrams of zones, workflows, intake/output flow |
| [`FOLDER_CONVENTIONS.md`](FOLDER_CONVENTIONS.md) | The 3-layer folder contract every folder on X:\ honors (L1 universal · L2 workflow · L3 NLP-specific) |
| [`THEOPHYSICS_PRIMER.md`](THEOPHYSICS_PRIMER.md) | Framework anchor doc — every AI partner loads this at session start (Master Equation, 10 Laws, Boundary Proof, Theopoetic format, R-rules, glossary) |
| [`BRAIN_README.md`](BRAIN_README.md) | The signpost README at `X:\` root — human front door for the drive itself |
| [`00_WORKFLOWS/`](00_WORKFLOWS/) | Workflow lane docs, healthcheck infrastructure, root maps, and the Codex prompt bank |
| [`00_WORKFLOWS/prompts/x-drive-reorg/`](00_WORKFLOWS/prompts/x-drive-reorg/) | **The Codex prompts.** 4a–4g + Phase 5. Start at [`00_INDEX.md`](00_WORKFLOWS/prompts/x-drive-reorg/00_INDEX.md). |
| [`Backside/`](Backside/) | Phase logs (1a/1b/path-fix), dedup reference implementation (`phase2_dedup.ps1`), cleanup records |
| [`plan/`](plan/) | The plan doc that David approved 2026-05-16 — phased restructure with Option A (BIL move to X:) locked |
| `RUN_*.bat` | Top-level click-buttons David uses today (FAP pipeline, public article refinery) |

## What's NOT in here (by design)

- **Vault content** — `X:\C4C\`, `X:\C4C-wiki\`, `X:\FAP\` (the Obsidian vaults and pipeline scaffolds — primary copy lives in `O:\_Theophysics_v5\`)
- **NLP source code** — `X:\paper-proof-grader\`, `X:\knowledge-refinery\`, `X:\axioms\`, etc. (each is its own repo or stays local)
- **Model weights and embeddings** — `X:\models\`, `X:\embeddings\` (gigabytes; not git-friendly)
- **Pipeline data** — `X:\captures\`, `X:\digests\`, `X:\ratings\` (ephemeral)
- **Logs** — `X:\_LOGS\` (volume + churn)

If you need any of the above, work directly on the NAS at `\\dlowenas\brain\` (mounted as `X:\` on David's box).

---

## How to use this repo

### As an AI partner walking in cold

1. Load `THEOPHYSICS_PRIMER.md` as system context — that's the framework floor.
2. Read `ARCHITECTURE.md` to know what zone you're in.
3. Read `FOLDER_CONVENTIONS.md` for the contract you must honor when touching X:\.
4. For workflow-specific work: each NLP has its own `_AGENT_BRIEF.md` on X:\ (loaded by that workflow's `RUN_AGENT.bat`).
5. Check `00_WORKFLOWS/prompts/x-drive-reorg/00_INDEX.md` if you're picking up Codex work in the X-drive reorg.

### As a human walking in cold

1. Open `BRAIN_README.md` — that's the X:\ signpost.
2. Open `ARCHITECTURE.md` — pretty Mermaid diagrams of how it all fits.
3. The plan that organized this: `plan/yes-i-want-togo-agile-puddle.md`.

### To make changes

Edits to map/convention/prompt files happen on `X:\` first (canonical source), then a sync push updates this repo. Never edit this repo as the source of truth — it's a mirror.

---

## Phase status (as of 2026-05-16)

| Phase | Scope | Status |
|---|---|---|
| 1a — Flatten `X:\brain\` nest | Promote `C4C`, `C4C-wiki`, `FAP`, `ollama` to root; drop dupes | **Done** |
| 1b — Pull in D:\ targets | `D:\C4C-wiki`, `D:\FAP` → `X:\` | **Done** |
| 2 — Redundancy sweep | Cross-X: dedup; symlinks resolved | **Done** (see `Backside/phase2_dedup.ps1` + `DEDUP_REPORT_20260516.md` on X:) |
| 3 — Push to GitHub | This repo | **In progress (this commit)** |
| 4a — Folder convention rollout | 15 READMEs + `00_DROP/` rename + `_AGENT_BRIEF` + `RUN_AGENT.bat` + `health_check.bat` per NLP | **Queued for Codex** |
| 4b — Root simplification | Move 9 NLPs under `00_WORKFLOWS/`, junctions at old paths | Queued (depends on 4a) |
| 4c — Batch-script path sweep | Rewrite `D:\BIL\*` + `D:\FAP` refs across 10 BIL files + Task Scheduler | Queued for Codex |
| 4d — Intake engine | Watchdog + Mistral classifier + router | Queued for Codex |
| 4e — PySide 6 dashboard | GUI for brain state | Queued (depends on 4d) |
| 4f — Conversion layer | MarkItDown + Whisper + OCR unified | Queued for Codex |
| 4g — Root health-check master | `X:\CHECKS\RUN_ALL.bat` | Queued (depends on 4a) |
| 5 — BIL + FAP migration | `robocopy /MOVE D:\BIL → X:\BIL` + Task Scheduler re-import | Queued (depends on 4c) |

---

## Related

- **Comms hub:** `https://comms.dlowehomelab.com` — Theophysics multi-AI coordination
- **Operating manual:** `C:\Users\lowes\AppData\Local\Programs\Warp\CLAUDE.md` (Claude Code workspace)
- **Primary vault:** `O:\_Theophysics_v5\` (Obsidian, canon-locked)
- **Public axioms:** `D:\PUB_AXIOM_FOUNDATIONS\` (22 axioms v2.1)
- **Technical axioms:** `D:\01_Axioms\_001-188\` (188 axioms; PostgreSQL mirror @ 192.168.1.177:2665)
