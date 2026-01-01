import os
from google import genai
from dotenv import load_dotenv
import json # Add this at the top

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_shipping_info(email_text):
    # We ask for JSON now so it's easy to plug into your dictionary-based upsert_parcel function
    prompt = f"""
    You are a logistics data extractor. Analyze the email text below.
    
    CRITICAL INSTRUCTIONS:
    1. Look for the SPECIFIC PRODUCT NAME. Check order summaries, item descriptions, or lines starting with 'Item:'. 
    2. If there are multiple items, summarize them (e.g., 'Keyboard + 2 others').
    3. If it is truly a gift or the name is hidden, use a generic category like 'Parcel'.
    4. If the email is travel-related (flights/hotels) or bank alerts, return ONLY: {{"tracking_id": "NO_TRACKING"}}

    Return a JSON object with these EXACT keys:
    {{
        "platform": "e.g. Lazada, Shopee",
        "product_name": "Be as specific as possible",
        "tracking_id": "the actual tracking number",
        "courier": "e.g. NinjaVan, J&T",
        "destination_address": "if found",
        "delivery_type": "Standard/Express",
        "expiry_date": null,
        "status": "Shipped"
    }}

    If no tracking number is found, return {{"tracking_id": "NO_TRACKING"}}.

    Text: {email_text}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    # Clean the response in case Gemini adds markdown backticks
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return clean_json