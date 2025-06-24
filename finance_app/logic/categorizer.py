import re
from typing import TYPE_CHECKING, Dict, Pattern
import json
if TYPE_CHECKING:
    from finance_app.data.parser import Transaction

RULES: Dict[Pattern, str] = {
    re.compile(r"Magnit|Пятёрочка"): "Еда",
    re.compile(r"Yandex\\.Taxi"): "Транспорт",
    # Добавьте другие шаблоны по необходимости
}

RULES_PATH = 'rules.json'

def categorize(tx: 'Transaction') -> str:
    """Категоризирует транзакцию по описанию."""
    for pattern, cat in RULES.items():
        if pattern.search(tx.description):
            return cat
    return "Uncategorized"

def load_rules_from_json(path: str = RULES_PATH) -> None:
    """Загружает правила категоризации из JSON-файла."""
    global RULES
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    RULES = {re.compile(p): c for p, c in data.items()}

def save_rules_to_json(path: str = RULES_PATH) -> None:
    """Сохраняет текущие правила категоризации в JSON-файл."""
    rules_dict = {p.pattern: c for p, c in RULES.items()}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(rules_dict, f, ensure_ascii=False, indent=2) 