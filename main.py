import json
import gmail_client
import ai_parser
import database # This is your file containing init_db and upsert_parcel

def main():
    database.init_db()
    
    print("Searching Gmail...")
    service = gmail_client.get_gmail_service()
    
    emails = gmail_client.fetch_emails(service, "order")
   
    if not emails:
        print("❌ No emails found. Try a different search term or check your inbox!")
        return  # Stop the function here

    print(f"✅ Found {len(emails)} emails! Starting AI analysis...")

    for body in emails:
        ai_response = ai_parser.parse_shipping_info(body)
        
        if "NO_TRACKING" in ai_response:
            continue
            
        try:
            # Convert Gemini's text into a Python Dictionary
            parcel_data = json.loads(ai_response)
            
            # Use your existing function!
            database.upsert_parcel(parcel_data)
        except Exception as e:
            print(f"Error processing email: {e}")

if __name__ == "__main__":
    main()