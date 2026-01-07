import re
from datetime import datetime

def parse_invoice(text):
    """
    Parses OCR text to extract metadata using Regex:
    - Invoice Number
    - Date
    - Vendor Name
    - Total Amount
    """
    data = {}
    
    # Clean text
    clean_text = text.strip()
    lines = [line.strip() for line in clean_text.split('\n') if line.strip()]

    # 1. Vendor Name (Heuristic: First non-empty line is usually the vendor)
    if lines:
        data['vendor'] = lines[0]
    else:
        data['vendor'] = "Unknown Vendor"

    # 2. Invoice Number
    # Looks for: "Invoice #123", "Inv: 123", "Invoice Number: 123"
    inv_match = re.search(r'(?i)(invoice\s*#|inv\.|invoice\s*number)[:\s]*([a-zA-Z0-9-]+)', text)
    if inv_match:
        data['invoice_number'] = inv_match.group(2)
    else:
        # Fallback if not found
        data['invoice_number'] = f"UNK-{datetime.now().strftime('%H%M%S')}"

    # 3. Date
    # Looks for dates like: 12/05/2023, 2023-05-12, 12-05-2023
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})', text)
    if date_match:
        data['date'] = date_match.group(1)
    else:
        data['date'] = datetime.now().strftime('%Y-%m-%d')

    # 4. Total Amount
    # Looks for: "Total: $1,200.50", "Amount Due: 500"
    # Matches patterns with currency symbols optionally
    amount_match = re.search(r'(?i)(total|amount|due|balance|grand\s*total)[:\s]*[\$€£]?\s*([\d,]+\.?\d{0,2})', text)
    
    if amount_match:
        try:
            # Remove commas (e.g., "1,200.00" -> "1200.00")
            amount_str = amount_match.group(2).replace(',', '')
            data['total_amount'] = float(amount_str)
        except ValueError:
            data['total_amount'] = 0.0
    else:
        data['total_amount'] = 0.0

    return data