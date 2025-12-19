import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def configure_gemini(api_key):
    genai.configure(api_key=api_key)

def parse_email_content(email_body):
    """
    Sends email body to Gemini and extracts parcel details.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a data extraction assistant analyzing shipping emails.
    Please extract the following information in JSON format:
    
    - platform: The e-commerce platform (e.g., 'Lazada', 'Shopee', 'Amazon', 'Keychron').
    - product_name: A concise, friendly name of the product (e.g. "Keychron M6 Mouse").
    - sku_asin: The SKU or Amazon ASIN if available, else null.
    - tracking_id: The tracking number. If not found, use null.
    - courier: The courier name (e.g., NinjaVan, SPX, Com1Express, J&T).
    - destination_address: The delivery address.
    - delivery_type: Either 'Home/Office' or 'PickLocker' based on context (e.g., if it mentions a locker code or collection point, use 'PickLocker').
    - expiry_date: If it's a locker delivery, the deadline for collection. Else null.
    - status: Current status (e.g., 'Shipped', 'Out for Delivery').

    Email Body:
    {email_body}
    
    Output JSON only. No markdown.
    """
    
    try:
        response = model.generate_content(
            prompt,
             safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        text = response.text.strip()
        # Clean up json if it has markdown backticks
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
            
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error parsing with Gemini: {e}")
        return None
