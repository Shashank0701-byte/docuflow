from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# 1. Connection String (User:Pass@Host:Port/DB)
# We use 'localhost' because we are running Python on Windows, talking to Docker
DB_URL = os.getenv("DATABASE_URL", "postgresql://docuflow:docuflow_pass@localhost:5432/docuflow_db")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define the Table
class InvoiceDB(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    invoice_number = Column(String, nullable=True)
    vendor_name = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    invoice_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Store the raw text just in case we need to debug later
    raw_text = Column(Text, nullable=True)

# 3. Create Tables
def init_db():
    print("🗄️  Initializing Database Tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables Created!")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()