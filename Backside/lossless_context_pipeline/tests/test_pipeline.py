from pathlib import Path

from Backside.lossless_context_pipeline.pipeline import build_artifact


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "sample_article.md"


def test_build_artifact_has_required_ids_and_address():
    artifact = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert artifact.ids.vault_id == "test-vault"
    assert artifact.ids.doc_id
    assert artifact.ids.run_id
    assert artifact.ids.audit_snapshot_id
    assert " :: " in artifact.address
    assert artifact.vector_string.startswith("G")
    assert artifact.recovery_key.startswith("LCC-")


def test_extracts_core_protocol_objects():
    artifact = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert artifact.blocks
    assert artifact.claim_arch
    assert artifact.evidence_chain
    assert artifact.kill_arch
    assert artifact.eq_sem
    assert artifact.domain_boundary
    assert artifact.mechanism_graph
    assert artifact.four_score_dashboard.Academic_Readiness.score >= 0
    assert "7. Overstatement gap" in artifact.eight_gaps


def test_stable_ids_for_same_content():
    first = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")
    second = build_artifact(SAMPLE, vault_id="test-vault", embeddings="none")

    assert first.ids.doc_id == second.ids.doc_id
    assert first.ids.content_hash == second.ids.content_hash
    assert [b.block_id for b in first.blocks] == [b.block_id for b in second.blocks]
