from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import date as dt_date
from typing import Optional

Base = declarative_base()
metadata = Base.metadata

class Transaction(Base):
    """SQLAlchemy-модель для транзакций."""
    __tablename__ = 'transactions'
    id: int = Column(Integer, primary_key=True)
    date: dt_date = Column(Date, nullable=False)
    amount: float = Column(Float, nullable=False)
    description: str = Column(String, nullable=False)
    category: str = Column(String, default="Uncategorized") 