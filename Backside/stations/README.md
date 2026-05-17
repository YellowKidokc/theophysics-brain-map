# Backside Stations

**What this is:** Reusable single-purpose NLP/service steps called by workflows.
**Owner:** shared
**Status:** live map
**Last updated:** 2026-05-16

Stations are smaller than workflows. A workflow chains stations; a station does one job well.

Folder names end in `.station`:

```text
claim-extract.station
facts-extract.station
timeline-build.station
paper-proximity.station
contradiction-scan.station
math-clarify.station
```

## Planned station lanes

| Station | Uses |
|---|---|
| `facts-extract.station` | `facts.model` |
| `timeline-build.station` | `timeline.model` |
| `paper-proximity.station` | `paper-citation.model` |
| `claim-extract.station` | `mistral-7b-instruct.model` |
| `contradiction-scan.station` | `deberta-v3-large.model` |
| `math-clarify.station` | Math Translation Layer |

Do not promote a station to workflow just because it is useful. Promote only when it has its own intake, run lifecycle, output contract, and dashboard tile.
