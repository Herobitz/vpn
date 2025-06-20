import pytest
from finance_app.data import parser
from unittest.mock import patch
from datetime import date

def test_parse_screenshot_extracts_transactions():
    fake_text = """
    01.01.2024  -100,00  Magnit
    02.01.2024  -200,00  Yandex.Taxi
    """
    with patch('pytesseract.image_to_string', return_value=fake_text):
        with patch('PIL.Image.open'):
            txs = parser.parse_screenshot('fake_path.png')
    assert len(txs) == 2
    assert txs[0].date == date(2024, 1, 1)
    assert txs[0].amount == -100.0
    assert 'Magnit' in txs[0].description

    # Add more assertions as needed 