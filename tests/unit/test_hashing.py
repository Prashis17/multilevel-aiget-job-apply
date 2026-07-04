from app.utils.hashing import stable_hash


def test_stable_hash_is_normalized() -> None:
    assert stable_hash(" Company ", "Role") == stable_hash("company", " role ")

