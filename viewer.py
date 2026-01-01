import sqlite3

def display_all_parcels():
    conn = sqlite3.connect('parcels.db')
    cursor = conn.cursor()
    
    # Fetch the important columns
    cursor.execute("SELECT platform, product_name, tracking_id, courier, status FROM parcels")
    rows = cursor.fetchall()
    
    print("\n📦 CURRENT SHIPPING MANIFEST")
    print("-" * 80)
    print(f"{'PLATFORM':<12} | {'ITEM':<20} | {'TRACKING ID':<20} | {'COURIER':<15}")
    print("-" * 80)
    
    for row in rows:
        platform = row[0] if row[0] else "Unknown"
        item = row[1] if row[1] else "N/A"
        print(f"{platform:<12} | {item:<20} | {row[2]:<20} | {row[3]:<15}")
    
    print("-" * 80)
    conn.close()

if __name__ == "__main__":
    display_all_parcels()