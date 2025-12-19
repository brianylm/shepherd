import sqlite3
import datetime

DB_NAME = "parcels.db"

def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # For development ease, we'll try to add columns if they don't exist, 
    # but for a clean state, you might want to delete parcels.db.
    # Here uses the user-defined schema:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parcels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            product_name TEXT,
            sku_asin TEXT,
            tracking_id TEXT UNIQUE,
            courier TEXT,
            destination_address TEXT,
            delivery_type TEXT,
            expiry_date TEXT,
            status TEXT DEFAULT 'Shipped',
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def upsert_parcel(data):
    """
    Insert a new parcel or update the status if tracking_id exists.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    now = datetime.datetime.now()
    
    # Check if exists
    cursor.execute("SELECT id FROM parcels WHERE tracking_id = ?", (data['tracking_id'],))
    row = cursor.fetchone()
    
    if row:
        # Update status and last_updated. 
        # Optionally update other fields if they are present and not null? 
        # For now, let's keep it simple and just update status/expiry as requested implicitly.
        cursor.execute('''
            UPDATE parcels 
            SET status = ?, last_updated = ?, expiry_date = ?
            WHERE tracking_id = ?
        ''', (data.get('status'), now, data.get('expiry_date'), data['tracking_id']))
        print(f"Updated status for {data['tracking_id']}")
    else:
        # Insert
        cursor.execute('''
            INSERT INTO parcels (
                platform, product_name, sku_asin, tracking_id, courier, 
                destination_address, delivery_type, expiry_date, status, last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('platform'),
            data.get('product_name'),
            data.get('sku_asin'),
            data.get('tracking_id'),
            data.get('courier'),
            data.get('destination_address'),
            data.get('delivery_type'),
            data.get('expiry_date'),
            data.get('status', 'Shipped'),
            now
        ))
        print(f"Inserted new parcel {data['tracking_id']}")
        
    conn.commit()
    conn.close()
