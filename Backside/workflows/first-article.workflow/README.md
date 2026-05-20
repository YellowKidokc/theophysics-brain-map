# First Article Workflow

**What this is:** the first practical X-drive workflow for an article/file packet.

It chains the reusable pieces that already exist:

```text
source
-> conversion / canonical Markdown
-> executive summary + overview + math layer
-> image notes / quote context
-> lossless context JSON + HTML
-> manifest
```

## Front Door

```text
X:\Backside\workflows\first-article.workflow\00_DROP
```

Drop a Markdown, text, HTML, or image file there, then run:

```text
X:\Backside\workflows\first-article.workflow\RUN.bat
```

Or run one explicit file:

```powershell
python X:\Backside\workflows\first-article.workflow\pipeline.py --input "path\to\file.html"
```

Batch a folder:

```powershell
python X:\Backside\workflows\first-article.workflow\pipeline.py --input-root "path\to\folder" --glob "gtq-*.html"
```

GTQ root-series runner:

```text
X:\Backside\workflows\first-article.workflow\RUN_GTQ_ROOT_SERIES.bat
```

## Outputs

Final reproducible exports go to:

```text
X:\EXPORTS\first-article-workflow\<run_id>\
```

Internal state goes to:

```text
X:\Backside\_state\first-article-workflow\<run_id>\
```

## Stations

| Station | Status | Output |
|---|---|---|
| conversion | wired | `source.canonical.md` |
| executive-summary | wrapped from station lab | `stations/<run>/executive-summary.md` |
| overview | wrapped from station lab | `stations/<run>/overview.md` |
| math-layer | wrapped from station lab | `stations/<run>/math-layer.md` |
| image-notes | first deterministic pass | `image-notes.md` |
| lossless-context | wired | `lossless/*.json`, `lossless/*.html` |

## Boundary

Image notes use file metadata, dimensions, alt/title text, and nearby caption/quote context. They do not yet use a true image-caption model. That is intentional: the workflow should not pretend metadata is vision.
