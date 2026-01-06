import os
from core.ocr import extract_text_from_pdf

def main():
    # 1. Define the path to our test file relative to this script
    # We go 'up' one level (..) then into data/raw
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_path = os.path.join(base_dir, "data", "raw", "sample_invoice.pdf")

    # 2. Run the OCR
    print("-" * 30)
    print("🚀 Starting DocuFlow v0.1")
    print("-" * 30)
    
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # 3. Show results
    print("\n" + "="*30)
    print("RESULTS:")
    print("="*30)
    print(extracted_text)
    print("="*30)

if __name__ == "__main__":
    main()