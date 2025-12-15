from main import main
from hashing import compute_hash

def test_cli_hash_success(tmp_path):
    file_path = tmp_path / "cli.txt"
    file_path.write_text("cli test")

    exit_code = main(["hash", str(file_path)])

    assert exit_code == 0

def test_cli_verify_mismatch(tmp_path):
    file_path = tmp_path / "cli.txt"
    file_path.write_text("original")

    expected = compute_hash(file_path)

    file_path.write_text("altered")

    exit_code = main(["verify", str(file_path), expected])

    assert exit_code == 2