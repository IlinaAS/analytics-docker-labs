from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import time

time.sleep(5)

DB_USER = os.getenv("DB_USER", "support_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "support_pass")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "support_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    urgency = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Support Tickets API", version="1.0")

class TicketCreate(BaseModel):
    description: str = Field(..., min_length=5, max_length=500)
    urgency: str = Field(..., pattern="^(low|medium|high|critical)$")
    author: str = Field(..., min_length=2, max_length=100)

class TicketUpdate(BaseModel):
    status: str = Field(..., pattern="^(open|in_progress|resolved|closed)$")

class TicketResponse(BaseModel):
    id: int
    description: str
    urgency: str
    author: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

@app.get("/tickets", response_model=list[TicketResponse])
def get_tickets(status: str = None):
    db = SessionLocal()
    try:
        if status:
            return db.query(Ticket).filter(Ticket.status == status).all()
        return db.query(Ticket).all()
    finally:
        db.close()

@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate):
    db = SessionLocal()
    try:
        new_ticket = Ticket(**ticket.dict())
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return new_ticket
    finally:
        db.close()

@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(ticket_id: int, update: TicketUpdate):
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        ticket.status = update.status
        db.commit()
        db.refresh(ticket)
        return ticket
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "support-tickets-backend"}

