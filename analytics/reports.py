"""
Модуль для генерации отчётов: cashflow, тренды, SMA-прогноз.
"""

from typing import List, Dict, Tuple
from datetime import date
import matplotlib.pyplot as plt
from collections import defaultdict
from finance_app.data.parser import Transaction
from matplotlib.figure import Figure

def generate_cashflow_report(transactions: List[Transaction]) -> Dict[str, Tuple[float, float]]:
    """
    Возвращает {месяц: (доход, расход)}
    """
    report = defaultdict(lambda: [0.0, 0.0])  # {month: [income, expense]}
    for tx in transactions:
        month = tx.date.strftime('%Y-%m')
        if tx.amount > 0:
            report[month][0] += tx.amount
        else:
            report[month][1] += tx.amount
    # Преобразуем расходы в положительные значения
    return {m: (inc, abs(exp)) for m, (inc, exp) in report.items()}

def plot_trends(transactions: List[Transaction]) -> Figure:
    """
    Строит график трендов по категориям (месяц→сумма) и возвращает Figure
    """
    data = defaultdict(lambda: defaultdict(float))  # {category: {month: sum}}
    for tx in transactions:
        month = tx.date.strftime('%Y-%m')
        data[tx.category][month] += tx.amount
    fig, ax = plt.subplots()
    for category, month_data in data.items():
        months = sorted(month_data)
        values = [month_data[m] for m in months]
        ax.plot(months, values, label=category)
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Сумма')
    ax.set_title('Тренды по категориям')
    ax.legend()
    fig.tight_layout()
    return fig

def forecast_sma(transactions: List[Transaction], category: str = None) -> Dict[str, float]:
    """
    Прогнозирует сумму по скользящему среднему (SMA, 3 месяца) для всех или выбранной категории.
    Возвращает {месяц: sma}
    """
    # Группируем по месяцам
    sums = defaultdict(float)
    for tx in transactions:
        if category and tx.category != category:
            continue
        month = tx.date.strftime('%Y-%m')
        sums[month] += tx.amount
    months = sorted(sums)
    values = [sums[m] for m in months]
    sma = {}
    for i in range(2, len(values)):
        avg = sum(values[i-2:i+1]) / 3
        sma[months[i]] = avg
    return sma

def plot_sma(sma: Dict[str, float]) -> Figure:
    fig, ax = plt.subplots()
    ax.plot(list(sma.keys()), list(sma.values()), marker='o')
    ax.set_title('SMA (3 месяца)')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Скользящее среднее')
    fig.tight_layout()
    return fig 