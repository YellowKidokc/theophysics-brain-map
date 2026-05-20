create extension if not exists vector;

create table if not exists lcc_documents (
  doc_id uuid primary key,
  vault_id text not null,
  source_path text,
  first_seen_at timestamptz not null default now()
);

create table if not exists lcc_audit_runs (
  run_id uuid primary key,
  vault_id text not null,
  doc_id uuid not null,
  note_version text not null,
  content_hash text not null,
  started_at timestamptz not null default now(),
  pipeline_version text not null default '0.1.0'
);

create table if not exists lcc_audit_snapshots (
  audit_snapshot_id uuid primary key,
  run_id uuid not null references lcc_audit_runs(run_id) deferrable initially deferred,
  vault_id text not null,
  doc_id uuid not null,
  note_version text not null,
  content_hash text not null,
  address text not null,
  vector jsonb not null,
  semantic_hash text not null,
  master_equation_uuid uuid,
  artifact jsonb not null,
  created_at timestamptz not null default now()
);

alter table lcc_audit_snapshots
  add column if not exists master_equation_uuid uuid;

create table if not exists lcc_blocks (
  block_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  doc_id uuid not null,
  section_id text not null,
  ordinal integer not null,
  block_type text not null,
  content_hash text not null,
  text text not null,
  embedding vector(384),
  payload jsonb not null
);

create table if not exists lcc_claims (
  claim_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  block_id uuid not null,
  doc_id uuid not null,
  surface_claim text not null,
  buried_claim text,
  operational_claim text,
  domain_badges text[] not null default '{}',
  payload jsonb not null
);

create table if not exists lcc_equations (
  equation_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  block_id uuid not null,
  doc_id uuid not null,
  equation text not null,
  status text not null,
  payload jsonb not null
);

create table if not exists lcc_evidence (
  evidence_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  block_id uuid not null,
  doc_id uuid not null,
  primary_source text,
  gap text,
  payload jsonb not null
);

create table if not exists lcc_repair_items (
  repair_item_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  block_id uuid,
  doc_id uuid not null,
  repair_type text not null,
  status text not null default 'open',
  payload jsonb not null
);

create table if not exists lcc_semantic_tags (
  tag_id uuid primary key,
  audit_snapshot_id uuid not null references lcc_audit_snapshots(audit_snapshot_id) on delete cascade,
  doc_id uuid not null,
  block_id uuid,
  tag_type text not null,
  label text not null,
  chi_vars text[] not null default '{}',
  master_equation_uuid uuid not null,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists lcc_snapshots_doc_hash_idx on lcc_audit_snapshots(doc_id, content_hash);
create index if not exists lcc_blocks_snapshot_type_idx on lcc_blocks(audit_snapshot_id, block_type);
create index if not exists lcc_claims_doc_idx on lcc_claims(doc_id);
create index if not exists lcc_snapshots_artifact_gin on lcc_audit_snapshots using gin (artifact);
create index if not exists lcc_semantic_tags_doc_type_idx on lcc_semantic_tags(doc_id, tag_type);
create index if not exists lcc_semantic_tags_chi_vars_idx on lcc_semantic_tags using gin (chi_vars);
