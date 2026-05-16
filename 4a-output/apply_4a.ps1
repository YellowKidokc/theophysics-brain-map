$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$XRoot = "X:\"

Write-Host "Applying 4a generated artifacts to $XRoot"

# Stage 1 README copies
$readmeFolders = @(
  'C4C','C4C-wiki','captures','digests','embeddings','FAP','github','link-pull-drop','models','ollama','proof-architecture','proof-explorer','ratings','session-handoff-drop','theophysics-comms-hub'
)
foreach ($f in $readmeFolders) {
  $src = Join-Path $RepoRoot "$f\README.md"
  $dst = Join-Path $XRoot "$f\README.md"
  if (Test-Path $src) { Copy-Item $src $dst -Force }
}

# Stage 4 NLP files
$active = @('axioms','knowledge-refinery','paper-proof-grader','link-pull-drop','session-handoff-drop','ai-portal-generator','ollama')
foreach ($nlp in $active) {
  $srcBase = Join-Path $RepoRoot $nlp
  $dstBase = Join-Path $XRoot $nlp
  Copy-Item (Join-Path $srcBase '_AGENT_BRIEF.md') (Join-Path $dstBase '_AGENT_BRIEF.md') -Force
  Copy-Item (Join-Path $srcBase 'RUN_AGENT.bat') (Join-Path $dstBase 'RUN_AGENT.bat') -Force
  Copy-Item (Join-Path $srcBase 'health_check.bat') (Join-Path $dstBase 'health_check.bat') -Force
  if (-not (Test-Path (Join-Path $dstBase 'prompts'))) { New-Item -ItemType Directory -Path (Join-Path $dstBase 'prompts') | Out-Null }
  Copy-Item (Join-Path $srcBase 'prompts\.gitkeep') (Join-Path $dstBase 'prompts\.gitkeep') -Force
}

# Stage 2 junction commands (queued/executed locally)
cmd /c mklink /J "X:\axioms\00_INBOX_DROP_PAPERS_HERE" "X:\axioms\00_DROP"
cmd /c mklink /J "X:\knowledge-refinery\00_INTAKE" "X:\knowledge-refinery\00_DROP"
cmd /c mklink /J "X:\paper-proof-grader\INPUT" "X:\paper-proof-grader\00_DROP"
cmd /c mklink /J "X:\paper-proof-grader\DROP_PAPERS_HERE" "X:\paper-proof-grader\00_DROP"
cmd /c mklink /J "X:\session-handoff-drop\DROP_HERE" "X:\session-handoff-drop\00_DROP"

Write-Host "Done. Review _4a_LOG.md before executing in production."
