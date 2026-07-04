from app.services.dedupe import email_dedupe_hash


def test_email_dedupe_hash_changes_by_role() -> None:
    first = email_dedupe_hash("hr@example.com", "Acme", "AI Engineer")
    second = email_dedupe_hash("hr@example.com", "Acme", "Backend Engineer")
    assert first != second

