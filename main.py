import json
import time
import gmail_client
import ai_parser
import database 

def main():
    database.init_db()
    
    print("Searching Gmail...")
    service = gmail_client.get_gmail_service()

    # Optimized search query
    query = "tracking OR courier OR 'shipped' OR 'ninja van' OR 'j&t' OR 'speedpost' OR 'parcel'"
    emails = gmail_client.fetch_emails(service, query)
   
    if not emails:
        print("❌ No emails found.")
        return 

    print(f"✅ Found {len(emails)} emails! Starting AI analysis...")

    for i, body in enumerate(emails):
        print(f"\n--- Analyzing Email #{i+1} ---", flush=True)
        
        # 1. Respect the API Rate Limit (wait 3s between requests)
        if i > 0: 
            print("⏳ Waiting 3 seconds to respect API quota...")
            time.sleep(3) 

        try:
            # 2. Call the AI once per email
            ai_response = ai_parser.parse_shipping_info(body)
            print(f"AI Result: {ai_response}")

            # 3. Check for the skip signal
            if "NO_TRACKING" in ai_response:
                print("⏭️  Decision: Skipped (No tracking found)")
                continue
                
            # 4. Save to database
            parcel_data = json.loads(ai_response)
            database.upsert_parcel(parcel_data)
            print(f"🎉 Success! {parcel_data.get('tracking_id')} saved.")

        except Exception as e:
            if "429" in str(e):
                print("❌ Quota hit! Please wait a minute before syncing again.")
                break 
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()