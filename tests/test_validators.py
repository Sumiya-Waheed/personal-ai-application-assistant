from utils.validators import validate_upload

def test_valid_upload():
    assert validate_upload("cv.pdf", 100)[0]

def test_bad_extension():
    ok, msg = validate_upload("cv.exe", 100)
    assert not ok and "Unsupported" in msg
