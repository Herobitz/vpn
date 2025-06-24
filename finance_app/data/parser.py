import re
from typing import List
from dataclasses import dataclass
from PIL import Image
import pytesseract
from datetime import datetime, date

@dataclass
class Transaction:
    """Модель транзакции, извлекаемой из банковской выписки."""
    date: date
    amount: float
    description: str
    category: str = "Uncategorized"

line_pattern = re.compile(
    r"(?P<date>\d{2}\.\d{2}\.\d{4})\s+(?P<amount>-?\d+,\d{2})\s+(?P<desc>.+)"
)

def parse_screenshot(path: str) -> List[Transaction]:
    """
    Парсит скриншот банковской выписки и возвращает список транзакций.
    Args:
        path (str): Путь к изображению.
    Returns:
        List[Transaction]: Список транзакций.
    """
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='rus')
    transactions: List[Transaction] = []
    for line in text.splitlines():
        m = line_pattern.match(line.strip())
        if m:
            try:
                dt = datetime.strptime(m.group('date'), "%d.%m.%Y").date()
                amount = float(m.group('amount').replace(',', '.'))
                desc = m.group('desc').strip()
                transactions.append(Transaction(date=dt, amount=amount, description=desc))
            except Exception:
                continue
    return transactions 