import sys
import os
import pytest

# Add 'src' to the Python path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.parser import parse_invoice_text

# --- TEST CASES ---

def test_perfect_invoice():
    """Test a standard invoice with clear data."""
    raw_text = """
    INVOICE #INV-2024-001
    Date: 2024-01-15
    Vendor: TechCorp Solutions
    
    Services Rendered:
    - Cloud Consulting: $1,000.00
    - Storage Costs: $250.50
    
    Total Amount: $1,250.50
    """
    
    data = parse_invoice_text(raw_text)
    
    assert data.is_valid is True
    assert data.total_amount == 1250.50
    assert data.invoice_number == "INV-2024-001"
    assert data.invoice_date == "2024-01-15"

def test_messy_ocr_scan():
    """Test text that might come from a bad scan (extra spaces, typos)."""
    raw_text = """
    lnvoice   Number:   999-XYZ
    Date: 12/05/2023
    
    Balance   Due :   $ 500.00
    """
    
    data = parse_invoice_text(raw_text)
    
    assert data.total_amount == 500.00
    assert data.invoice_number == "999-XYZ"

def test_missing_total():
    """Test that the system flags invoices with no total."""
    raw_text = """
    Quote #Q-100
    This is not a bill.
    Est: $100.00
    """
    
    data = parse_invoice_text(raw_text)
    
    # This should be False because there is no "Total: " line
    assert data.is_valid is False
    assert data.total_amount is None

def test_currency_formats():
    """Test different currency formats ($1000 vs 1,000.00)."""
    text_comma = "Total: $1,200.50"
    text_plain = "Total: 1200.50"
    
    assert parse_invoice_text(text_comma).total_amount == 1200.50
    assert parse_invoice_text(text_plain).total_amount == 1200.50