import pytest
from hashing import compute_hash

def test_same_file_hash(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")

    hash1 = compute_hash(file_path)
    hash2 = compute_hash(file_path)

    assert hash1 == hash2

def test_known_hash(tmp_path):
    file_path = tmp_path / "known.txt"
    file_path.write_text("abc")

    digest = compute_hash(file_path)

    assert digest == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

def test_missing_file_error():
    with pytest.raises(FileNotFoundError):
        compute_hash("does_not_exist.txt")