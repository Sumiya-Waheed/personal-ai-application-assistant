from utils.text_processor import clean_text, chunk_text

def test_clean_text():
    assert clean_text(" a  b\n\n\n c ") == "a b\n\nc"

def test_chunk_text():
    chunks = chunk_text("Paragraph one.\n\nParagraph two.", chunk_size=20, overlap=5)
    assert chunks
    assert all(c.strip() for c in chunks)
