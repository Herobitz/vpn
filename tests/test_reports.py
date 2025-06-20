import pytest
from finance_app.analytics import reports
from finance_app.data.parser import Transaction
from datetime import date

def sample_transactions():
    return [
        Transaction(date=date(2024, 1, 1), amount=1000.0, description='Зарплата', category='Доход'),
        Transaction(date=date(2024, 1, 2), amount=-200.0, description='Magnit', category='Еда'),
        Transaction(date=date(2024, 2, 1), amount=1000.0, description='Зарплата', category='Доход'),
        Transaction(date=date(2024, 2, 2), amount=-300.0, description='Magnit', category='Еда'),
        Transaction(date=date(2024, 3, 1), amount=1000.0, description='Зарплата', category='Доход'),
        Transaction(date=date(2024, 3, 2), amount=-400.0, description='Magnit', category='Еда'),
    ]

def test_generate_cashflow_report():
    txs = sample_transactions()
    report = reports.generate_cashflow_report(txs)
    assert '2024-01' in report
    assert report['2024-01'][0] == 1000.0
    assert report['2024-01'][1] == 200.0

def test_plot_trends():
    txs = sample_transactions()
    fig = reports.plot_trends(txs)
    assert fig is not None
    assert hasattr(fig, 'show')

def test_forecast_sma_and_plot():
    txs = sample_transactions()
    sma = reports.forecast_sma(txs, category='Еда')
    assert isinstance(sma, dict)
    fig = reports.plot_sma(sma)
    assert fig is not None
    assert hasattr(fig, 'show') 