import gmail_client
import ai_parser

def main():
    print("Connecting to Gmail...")
    service = gmail_client.get_gmail_service()
    
    # We're searching for ANY email with these words to be sure it finds something
    print("Searching for ANY emails containing 'Lazada', 'Shopee', or 'Order'...")
    query = "Lazada OR Shopee OR Order" 
    emails = gmail_client.fetch_emails(service, query)
    
    if not emails:
        print("!!! Still no emails found. Check if you have these words in your inbox. !!!")
        return

    print(f"--- Found {len(emails)} potential emails! Sending to Gemini... ---")
    
    for i, body in enumerate(emails):
        print(f"Reading Email #{i+1}...")
        info = ai_parser.parse_shipping_info(body)
        print(f"Gemini says: {info}")
        print("-" * 30)

if __name__ == "__main__":
    main()