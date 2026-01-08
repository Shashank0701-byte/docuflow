import os
import json
import logging
import requests
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_invoice(text):
    """
    Extracts data using the Gemini REST API directly.
    Bypasses SDK versioning issues.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("❌ GEMINI_API_KEY is missing!")
        return {}

    # Endpoint: Using Gemini 2.5 Flash (current recommended model as of 2026)
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    # Prompt
    prompt_text = f"""
    Extract the following fields from the OCR text below and return ONLY valid JSON.
    Do not add Markdown formatting (no ```json).
    
    Fields:
    - vendor (string): Issuer name.
    - invoice_number (string): Identifier. Use "UNK-000" if missing.
    - date (string): YYYY-MM-DD format. Use today if missing.
    - total_amount (float): Final amount (number only).

    OCR Text:
    {text}
    """

    # Payload
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        logger.info("🤖 Sending Raw REST Request to Gemini 2.5 Flash...")
        
        response = requests.post(
            url, 
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            },
            json=payload
        )

        # Check for HTTP Errors (404, 400, 500)
        if response.status_code != 200:
            logger.error(f"❌ API Error {response.status_code}: {response.text}")
            return fallback_data()

        # Parse Response
        response_json = response.json()
        
        # Safe Extraction Logic
        try:
            raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
            
            # Clean Markdown (Standard cleanup)
            clean_json = raw_text.strip()
            if clean_json.startswith("```json"): clean_json = clean_json[7:]
            if clean_json.startswith("```"): clean_json = clean_json[3:]
            if clean_json.endswith("```"): clean_json = clean_json[:-3]
            
            data = json.loads(clean_json)
            logger.info(f"✅ AI Extraction Success: {data}")
            return data

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"❌ Failed to parse AI JSON response: {e}")
            return fallback_data()

    except Exception as e:
        logger.error(f"❌ Connection Failed: {e}")
        return fallback_data()

def fallback_data():
    return {
        "vendor": "AI_ERROR", 
        "total_amount": 0.0, 
        "invoice_number": "ERR", 
        "date": datetime.now().strftime('%Y-%m-%d')
    }