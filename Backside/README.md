# Backside

System-side storage for root cleanup, archived leftovers, app fragments, logs, scratch material, model cards, stations, workflows, and prompt packs.

This folder exists to keep `X:\` readable without deleting potentially useful files.

## Folders

- `_models` - model/NLP registry. Stores model cards and routing contracts; large weights stay off git and live on X:\.
- `_state` - shared runtime state used by workflow dashboards and intake engines.
- `brain_dashboard` - current dashboard MVP.
- `conversion_lib` - shared source/URL to canonical Markdown conversion library.
- `station_lab` - safe bench for tuning paper-grader stations before full workflow integration.
- `stations` - target home for reusable station services; folder names end in `.station`.
- `workflows` - target home for end-to-end pipelines; folder names end in `.workflow`.
- `prompts` - target home for reusable assignment/system prompt packs; folder names end in `.prompt-pack`.
- `archives` - zip files, websets, extracted bundles, and old import payloads.
- `apps` - small app/plugin fragments not part of the live root workflow.
- `logs` - old/root logs moved out of the top level.
- `root-leftovers` - legacy folders that were not active workflow roots.
- `scratch` - temporary material moved out of the top level.

## Rule

If something here becomes an active user-facing workflow, expose it through `X:\00_WORKFLOWS\`, `X:\DROP_HERE\`, `X:\EXPORTS\`, or the dashboard. Do not scatter new NLP folders at X:\ root.

## Naming

Backside is allowed to be the messy workbench, but every folder should name its type:

```text
<name>.model        model card / local model runtime contract
<name>.workflow     end-to-end process with 00_DROP, RUN.bat, OUTPUT, ARCHIVE
<name>.station      reusable station called by one or more workflows
<name>.prompt-pack  reusable prompts meant to be handed to AI partners
```

That gives David a fast read: what it is, not just what it is called.
