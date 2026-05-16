# Backside Architecture — the workhorse layer

**Owner:** David Lowe · canon-locked 2026-05-16
**Status:** live · phased migration from current X:\ layout
**Last updated:** 2026-05-16

The 3-tier topology under `X:\Backside\`. Models are atoms, stations are reusable skills, workflows are end-to-end pipelines, all bound by env-var portability and a uniform state contract.

---

## The three tiers

```
X:\Backside\                                  ← env-var: BRAIN_ROOT\Backside
│
├── _models/                                  ← raw artifacts (weights, configs only)
│     ├── moon-streak/                        ← e.g. theopoetic-style fine-tune
│     │     ├── moon-streak.gguf
│     │     ├── tokenizer.json
│     │     └── card.json                     ← {name, size, quant, license, anchor_role}
│     ├── deepseek-coder/
│     ├── clip-vision/
│     ├── deberta-v3-large/
│     ├── mistral-7b-instruct/
│     └── whisper-large-v3/
│
├── stations/                                 ← reusable skill services (called by workflows)
│     ├── claim-extract/
│     ├── ME-tag-paragraph/                   ← paragraph-level Master Equation tagger
│     ├── axiom-hit/
│     ├── fruits-score/
│     ├── seven-q-score/
│     ├── contradiction-scan/
│     ├── describe-figure/                    ← clip-vision + Mistral describer
│     ├── deconstruct-picture/                ← look at picture → return prompt to replicate
│     ├── math-clarify/                       ← Math Translation Layer as service
│     ├── theopoetic-format/                  ← moon-streak-driven style emitter
│     └── lossless-summarize/                 ← canonical lossless format
│
├── workflows/                                ← end-to-end pipelines (clicked from GUI)
│     ├── grade-paper/                        ← what PPG becomes
│     ├── refresh-axiom-snapshot/             ← what axioms NLP becomes
│     ├── route-and-convert/                  ← what knowledge-refinery becomes
│     ├── build-ai-portal/
│     ├── handoff-session/
│     ├── pull-link/
│     └── deconstruct-picture/                ← one-for-one workflows live here too
│
├── _state/                                   ← cross-workflow run registry
│     ├── active_runs.json                    ← list of in-flight runs (GUI polls this)
│     └── history/                            ← finalized run records (date-rolled)
│
└── _archive/                                 ← what X:\Backside\ holds today
      ├── phase-logs/
      ├── scratch/
      ├── apps/
      └── root-leftovers/
```

---

## Every workflow folder has this shape

```
workflows/<workflow-name>/
  README.md                  ← human-facing (Layer 1 + Layer 2)
  _AGENT_BRIEF.md            ← AI-facing mission card
  RUN.bat                    ← click-button entry (defaults to configs/default.json)
  RUN_AGENT.bat              ← loads PRIMER + AGENT_BRIEF → LLM session
  health_check.bat           ← read-only probe (0=pass, 1=fail, 2=warn)
  pipeline.py                ← reads --config <name>, orchestrates stations
  dependencies.json          ← static declaration of what stations COULD be called
  configs/                   ← saved compositions (named workflow variants)
    default.json
    minus-lossless.json
    deep.json                ← any number, user-creatable from the GUI
  STATE/                     ← per-run state.json files, polled by GUI
    <run_id>.json
  prompts/                   ← prompt templates this workflow's pipeline.py loads
  00_DROP/                   ← intake
  OUTPUT/                    ← results
  ARCHIVE/                   ← processed inputs
```

## Every station folder has this shape

```
stations/<station-name>/
  README.md
  _AGENT_BRIEF.md
  station.py                 ← the service (callable from any workflow)
  prompt.md                  ← the prompt template
  health_check.bat
  uses-model.txt             ← single line: which model this station uses (e.g. "moon-streak")
  config.json
```

## Every model folder has this shape

```
_models/<model-name>/
  <weights>.gguf             ← or .safetensors, .bin, etc.
  tokenizer.json             ← or equivalent
  card.json                  ← metadata
```

`card.json` schema:
```json
{
  "name": "moon-streak",
  "anchor_role": "theopoetic-style-emitter",
  "base_model": "mistral-7b-instruct-v0.3",
  "quant": "Q4_K_M",
  "size_gb": 4.1,
  "license": "Apache-2.0",
  "fine_tuned": true,
  "fine_tune_dataset": "X:\\Backside\\_models\\moon-streak\\dataset-200-theopoetic-examples.jsonl",
  "trained_at": "2026-05-XX"
}
```

---

## Portability — drive-agnostic by contract

No hardcoded `X:\` anywhere. Every script reads `BRAIN_ROOT`.

**Batch script preamble:**
```batch
@echo off
if not defined BRAIN_ROOT (
  for %%i in ("%~dp0..\..\..\..") do set "BRAIN_ROOT=%%~fi"
)
:: now use %BRAIN_ROOT%\Backside\_models\..., etc.
```

**Python preamble:**
```python
import os, pathlib
BRAIN_ROOT = pathlib.Path(os.environ.get(
    "BRAIN_ROOT",
    pathlib.Path(__file__).resolve().parents[3]
))
```

Move `Backside/` to `B:\` or `D:\` — set `BRAIN_ROOT=B:\Backside` once, everything keeps working.

---

## State manifest — the contract that powers the GUI

Every workflow run writes one JSON to `STATE/<run_id>.json` and updates `_state/active_runs.json`.

```json
{
  "run_id": "2026-05-16T20-15-04_grade-paper_a7f3",
  "workflow": "grade-paper",
  "config": "default",
  "started_at": "2026-05-16T20:15:04Z",
  "ended_at": null,
  "status": "running",
  "inputs": [{"path": "00_DROP/foo.pdf", "type": "pdf", "size": 12345}],
  "outputs": [],
  "stations_called": [
    {"id": "claim-extract", "started_at": "...", "status": "done"},
    {"id": "axiom-hit", "started_at": "...", "status": "running"}
  ],
  "metrics": {},
  "errors": []
}
```

GUI polls `_state/active_runs.json` for the dashboard view, drills into individual run JSONs for detail.

---

## Workflow config schema — named compositions

`workflows/<workflow>/configs/<name>.json`:

```json
{
  "name": "default",
  "description": "Full grading with lossless summary and figure descriptions",
  "extends": null,
  "stations": [
    {"id": "claim-extract", "enabled": true, "params": {}},
    {"id": "ME-tag-paragraph", "enabled": true, "params": {"confidence_floor": 0.6}},
    {"id": "axiom-hit", "enabled": true},
    {"id": "fruits-score", "enabled": true},
    {"id": "seven-q-score", "enabled": true},
    {"id": "describe-figure", "enabled": true},
    {"id": "math-clarify", "enabled": true},
    {"id": "contradiction-scan", "enabled": true, "scope": ["internal", "canon"]},
    {"id": "lossless-summarize", "enabled": true}
  ],
  "outputs": ["html-axioms", "html-7q", "excel-workbook", "lossless-md", "vault-md"]
}
```

`minus-lossless.json` extends `default.json` and toggles one station off:
```json
{"name": "minus-lossless", "extends": "default",
 "stations": [{"id": "lossless-summarize", "enabled": false}],
 "outputs": ["html-axioms", "html-7q", "excel-workbook", "vault-md"]}
```

---

## Dependencies declaration

`workflows/<workflow>/dependencies.json`:

```json
{
  "stations": ["claim-extract", "ME-tag-paragraph", "axiom-hit", "fruits-score",
               "seven-q-score", "describe-figure", "math-clarify",
               "contradiction-scan", "lossless-summarize"],
  "models": [],
  "external_services": [
    {"name": "qdrant", "endpoint": "http://192.168.1.177:6333"},
    {"name": "postgres", "endpoint": "192.168.1.177:2665"}
  ],
  "sinks": ["proof-explorer", "qdrant:paper_proof_grader", "vault:O:\\_Theophysics_v5\\"]
}
```

The root health-check (`X:\CHECKS\RUN_ALL.bat`) reads every `dependencies.json` and verifies every claimed station/service is reachable.

---

## Migration map (current → new)

| Current path | New path |
|---|---|
| `X:\paper-proof-grader\` | `Backside/workflows/grade-paper/` |
| `X:\axioms\` | `Backside/workflows/refresh-axiom-snapshot/` (logic → `stations/axiom-hit/`) |
| `X:\knowledge-refinery\` | `Backside/workflows/route-and-convert/` (model-stations → real `stations/`) |
| `X:\ai-portal-generator\` | `Backside/workflows/build-ai-portal/` |
| `X:\session-handoff-drop\` | `Backside/workflows/handoff-session/` |
| `X:\link-pull-drop\` | `Backside/workflows/pull-link/` |
| `X:\models\` | `Backside/_models/` |
| `X:\proof-architecture\`, `X:\proof-explorer\` | stay at `X:\` root (these are output sinks, not workflows) |
| `X:\Backside\` (current archive) | `Backside/_archive/` |
| `D:\GitHub\Math-Translation-Layer\` | `Backside/stations/math-clarify/` (move + repackage) |

---

## Related

- `THEOPHYSICS_PRIMER.md` — framework anchor (load first in every AI session)
- `FOLDER_CONVENTIONS.md` — universal 3-layer folder contract
- `ARCHITECTURE.md` — the wider X:\ system map (Mermaid diagrams)
- `00_WORKFLOWS/prompts/x-drive-reorg/4e_pyside_workflow_composer.md` — the GUI spec that consumes this architecture
