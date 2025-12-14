from hashing import compute_hash, verify_hash

def test_verify_match(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world!")

    expected = compute_hash(file_path)
    match, actual = verify_hash(file_path, expected)

    assert match is True
    assert expected == actual

def test_verify_mismatch(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("original file")

    expected = compute_hash(file_path)

    file_path.write_text("new changed file")

    match, actual = verify_hash(file_path, expected)

    assert match is False
    assert actual != expected

def test_verify_normalize(tmp_path):
    file_path = tmp_path / "text.txt"
    file_path.write_text("normalize me")

    expected = compute_hash(file_path)
    messy = f"  {expected.upper()}   \n"

    match, _ = verify_hash(file_path, messy)

    assert match is True

