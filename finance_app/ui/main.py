import PySimpleGUI as sg
from finance_app.data.parser import parse_screenshot, Transaction
from finance_app.logic.categorizer import categorize, load_rules_from_json, save_rules_to_json, RULES
from finance_app.analytics.reports import generate_cashflow_report, plot_trends, forecast_sma, plot_sma
from finance_app.db.models import Transaction as DBTransaction, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import csv
import os
import matplotlib.pyplot as plt
# import gspread  # Для Google Sheets (опционально)

DB_PATH = 'finance.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def select_files() -> list:
    files = sg.popup_get_file('Выберите скриншоты выписок', multiple_files=True, file_types=(('PNG', '*.png'), ('JPG', '*.jpg'), ('Все файлы', '*.*')))
    if not files:
        return []
    return files.split(';') if isinstance(files, str) else files

def display_transactions(window, transactions):
    table_data = [[tx.date.strftime('%d.%m.%Y'), tx.amount, tx.description, tx.category] for tx in transactions]
    window['-TABLE-'].update(values=table_data)

def save_transactions_to_db(transactions):
    session = Session()
    for tx in transactions:
        db_tx = DBTransaction(date=tx.date, amount=tx.amount, description=tx.description, category=tx.category)
        session.add(db_tx)
    session.commit()
    session.close()

def load_transactions_from_db():
    session = Session()
    txs = session.query(DBTransaction).all()
    session.close()
    return [Transaction(date=tx.date, amount=tx.amount, description=tx.description, category=tx.category) for tx in txs]

def update_categories_in_db(transactions):
    session = Session()
    for tx in transactions:
        db_tx = session.query(DBTransaction).filter_by(date=tx.date, amount=tx.amount, description=tx.description).first()
        if db_tx:
            db_tx.category = tx.category
    session.commit()
    session.close()

def export_to_csv(transactions, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Дата', 'Сумма', 'Описание', 'Категория'])
        for tx in transactions:
            writer.writerow([tx.date.strftime('%d.%m.%Y'), tx.amount, tx.description, tx.category])

def manual_edit_category(window, transactions, row_idx):
    tx = transactions[row_idx]
    new_cat = sg.popup_get_text(f'Изменить категорию для: {tx.description}', default_text=tx.category)
    if new_cat and new_cat != tx.category:
        # Добавить новое правило: часть описания → категория
        import re
        pattern = re.escape(tx.description.split()[0])  # Пример: по первому слову
        from finance_app.logic.categorizer import RULES, save_rules_to_json
        RULES[re.compile(pattern)] = new_cat
        save_rules_to_json()
        tx.category = new_cat
        update_categories_in_db(transactions)
        display_transactions(window, transactions)
        sg.popup('Новое правило добавлено и сохранено в rules.json')

def main():
    sg.theme('LightBlue')
    layout = [
        [sg.Text('Домашняя финансовая система')],
        [sg.Button('Импорт'), sg.Button('Категоризация'), sg.Button('Отчёты'), sg.Button('Экспорт')],
        [sg.Table(values=[], headings=['Дата', 'Сумма', 'Описание', 'Категория'], key='-TABLE-', auto_size_columns=True, justification='left', enable_events=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Загрузить правила из JSON')]
    ]
    window = sg.Window('Домашняя финансовая система', layout, finalize=True)
    transactions = load_transactions_from_db()
    display_transactions(window, transactions)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Импорт':
            files = select_files()
            new_txs = []
            for f in files:
                new_txs.extend(parse_screenshot(f))
            save_transactions_to_db(new_txs)
            transactions = load_transactions_from_db()
            display_transactions(window, transactions)
        elif event == 'Категоризация':
            for tx in transactions:
                tx.category = categorize(tx)
            update_categories_in_db(transactions)
            transactions = load_transactions_from_db()
            display_transactions(window, transactions)
        elif event == 'Отчёты':
            if not transactions:
                sg.popup('Нет данных для отчёта')
                continue
            report = generate_cashflow_report(transactions)
            msg = '\n'.join([f'{m}: Доход {inc:.2f}, Расход {exp:.2f}' for m, (inc, exp) in sorted(report.items())])
            sg.popup('Cashflow', msg)
            fig1 = plot_trends(transactions)
            fig1.show()
            sma = forecast_sma(transactions)
            fig2 = plot_sma(sma)
            fig2.show()
        elif event == 'Экспорт':
            path = sg.popup_get_file('Сохранить как CSV', save_as=True, file_types=(('CSV', '*.csv'),))
            if path:
                export_to_csv(transactions, path)
                sg.popup('Экспорт завершён')
        elif event == 'Загрузить правила из JSON':
            path = sg.popup_get_file('Выберите JSON с правилами', file_types=(('JSON', '*.json'),))
            if path:
                load_rules_from_json(path)
                sg.popup('Правила обновлены')
        elif event == '-TABLE-':
            if values['-TABLE-']:
                row_idx = values['-TABLE-'][0]
                manual_edit_category(window, transactions, row_idx)
    window.close()

if __name__ == '__main__':
    main() 