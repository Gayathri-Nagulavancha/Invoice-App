from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base, engine
from datetime import datetime

def create_tables():
    Base.metadata.create_all(bind=engine)


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

