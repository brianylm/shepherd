import gmail_client
try:
    print("Trying to start the Gmail service...")
    service = gmail_client.get_gmail_service()
    print("Success! Service created.")
except Exception as e:
    print(f"An error occurred: {e}")
