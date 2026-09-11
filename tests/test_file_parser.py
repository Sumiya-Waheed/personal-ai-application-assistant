from utils.file_parser import extract_text

def test_txt_extraction():
    assert "hello" in extract_text("sample.txt", b"hello world")

def test_empty_txt_rejected():
    try:
        extract_text("empty.txt", b"")
        assert False
    except ValueError as exc:
        assert "empty" in str(exc).lower()
