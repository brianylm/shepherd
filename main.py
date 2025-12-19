import os
import getpass
from database import init_db, upsert_parcel
from gmail_client import authenticate_gmail, search_shipping_emails, get_email_body
from ai_parser import configure_gemini, parse_email_content

def main():
    print("Initializing Parcel Tracker...")
    
    # 1. Setup Database
    init_db()

    # Pre-check for credentials.json
    if not os.path.exists('credentials.json'):
        print("ERROR: credentials.json not found in current directory.")
        print("Please download it from Google Cloud Console and place it here.")
        return
    
    # 2. Setup Gemini
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found in environment variables.")
        api_key = getpass.getpass("Please enter your Google Gemini API Key: ")
    
    if not api_key:
        print("API Key required. Exiting.")
        return

    configure_gemini(api_key)
    
    # 3. Authenticate Gmail
    print("Authenticating with Gmail...")
    service = authenticate_gmail()
    if not service:
        print("Failed to authenticate.")
        return

    # 4. Search Emails
    print("Searching for shipping emails...")
    messages = search_shipping_emails(service)
    
    if not messages:
        print("No emails found.")
        return
        
    print(f"Found {len(messages)} emails. Processing...")
    
    for msg in messages:
        msg_id = msg['id']
        print(f"Processing email {msg_id}...")
        
        # Get Body
        body = get_email_body(service, msg_id)
        if not body:
            print("  No body content found. Skipping.")
            continue
            
        # Parse with Gemini
        print("  Extracting info with Gemini...")
        data = parse_email_content(body[:10000]) # Limit body size for token limits
        
        if data:
            print(f"  Extracted: {data}")
            if data.get('tracking_id'):
                upsert_parcel(data)
            else:
                print("  No tracking ID found in extracted data.")
        else:
            print("  Failed to extract data.")

    print("Done!")

if __name__ == "__main__":
    main()
