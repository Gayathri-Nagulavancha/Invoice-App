from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime

app = FastAPI()

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class InvoiceBase(OurBaseModel):
    id:int
    number: str
    amount: float
    status: str
    date: datetime

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/addinvoices/', response_model=Invoice, status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    new_invoice = models.Invoice(
        number=invoice.number,
        amount=invoice.amount,
        status=invoice.status,
        date=invoice.date
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@app.get('/invoices/', response_model=List[Invoice], status_code=status.HTTP_200_OK)
def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()

@app.get('/invoicebyid/{invoice_id}', response_model=Invoice, status_code=status.HTTP_200_OK)
def get_invoice_by_id(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice

@app.put('/invoices/{invoice_id}', response_model=Invoice, status_code=status.HTTP_202_ACCEPTED)
def update_invoice(invoice_id: int, invoice: InvoiceUpdate, db: Session = Depends(get_db)):
    existing_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if existing_invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    
    existing_invoice.number = invoice.number
    existing_invoice.amount = invoice.amount
    existing_invoice.status = invoice.status
    existing_invoice.date = invoice.date
    
    db.commit()
    db.refresh(existing_invoice)
    return existing_invoice

@app.delete('/invoices/{invoice_id}', response_model=Invoice, status_code=status.HTTP_200_OK)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    
    db.delete(invoice)
    db.commit()
    return invoice
