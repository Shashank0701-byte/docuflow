import re
from typing import Optional
from .data_models import InvoiceData

def clean_currency(amount_str: str) -> Optional[float]:
    if not amount_str:
        return None
    clean_str = re.sub(r'[$,\s]', '', amount_str)
    try:
        return float(clean_str)
    except ValueError:
        return None

def parse_invoice_text(raw_text: str) -> InvoiceData:
    data = InvoiceData()
    
    # 1. FIND TOTAL AMOUNT
    total_pattern = r'(?:Total|Amount|Balance)\s*(?:Due)?\s*:?\s*[\$]?\s*([0-9,]+\.[0-9]{2})'
    total_match = re.search(total_pattern, raw_text, re.IGNORECASE)
    if total_match:
        data.total_amount = clean_currency(total_match.group(1))

    # 2. FIND INVOICE DATE
    date_pattern = r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})'
    date_match = re.search(date_pattern, raw_text)
    if date_match:
        data.invoice_date = date_match.group(1)

    # 3. FIND INVOICE NUMBER
    inv_num_pattern = r'(?:[Il1]nvoice|Inv|Quote)\s*(?:Number|#|No)?\.?\s*:?\s*([A-Za-z0-9-]+)'
    inv_num_match = re.search(inv_num_pattern, raw_text, re.IGNORECASE)
    if inv_num_match:
        data.invoice_number = inv_num_match.group(1)
        
    # 4. FIND VENDOR
    # Filter out empty lines AND lines that start with '---' (our page separators)
    lines = [
        line.strip() for line in raw_text.split('\n') 
        if line.strip() and not line.strip().startswith('---')
    ]
    
    # Indentation Fixed: This block MUST align with 'lines = ...'
    if lines:
        data.vendor_name = lines[0]

    return data