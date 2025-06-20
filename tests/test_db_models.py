import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finance_app.db.models import Base, Transaction
from datetime import date

def test_transaction_model():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    tx = Transaction(date=date(2024, 1, 1), amount=100.0, description='Test', category='Еда')
    session.add(tx)
    session.commit()
    loaded = session.query(Transaction).first()
    assert loaded.date == date(2024, 1, 1)
    assert loaded.amount == 100.0
    assert loaded.category == 'Еда' 