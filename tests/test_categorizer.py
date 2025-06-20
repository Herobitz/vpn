import pytest
import tempfile
import os
from finance_app.logic import categorizer
from finance_app.data.parser import Transaction
from datetime import date

def test_categorize_auto():
    tx = Transaction(date=date(2024, 1, 1), amount=-100.0, description='Magnit магазин')
    assert categorizer.categorize(tx) == 'Еда'

def test_rules_json(tmp_path):
    rules = {r"Test": "Тест"}
    path = tmp_path / 'rules.json'
    with open(path, 'w', encoding='utf-8') as f:
        import json
        json.dump(rules, f)
    categorizer.load_rules_from_json(str(path))
    assert any(c == 'Тест' for c in categorizer.RULES.values())
    categorizer.save_rules_to_json(str(path))
    assert os.path.exists(path) 