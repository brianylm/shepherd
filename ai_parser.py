import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def parse_shipping_info(email_text):
    # We tell Gemini specifically to look for the FORWARDED info
    prompt = f"""
    The following text is a forwarded email. 
    Find the ORIGINAL shipping information from the sender (like Lazada or Shopee).
    Extract the courier name and tracking number.
    
    Format: Courier: [Name], Tracking: [Number]
    If not found, return 'No tracking info found'.

    Text: {email_text}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    
    return response.text