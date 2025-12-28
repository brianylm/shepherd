import os
from google import genai
from dotenv import load_dotenv
import json # Add this at the top

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_shipping_info(email_text):
    # We ask for JSON now so it's easy to plug into your dictionary-based upsert_parcel function
    prompt = f"""
    Extract shipping details from this email. Return ONLY a JSON object with these keys:
    "platform" (e.g., Lazada, Shopee, Amazon),
    "product_name",
    "tracking_id",
    "courier",
    "destination_address",
    "delivery_type",
    "expiry_date" (if found, else null),
    "status" (default to 'Shipped')

    If any field is missing, use null. If no tracking_id is found, return "NO_TRACKING".

    Text: {email_text}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    # Clean the response in case Gemini adds markdown backticks
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return clean_json