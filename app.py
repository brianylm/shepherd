from flask import Flask, render_template, redirect, url_for
import sqlite3
import main as shepherd_main  # Ensure your main.py is in the same folder

app = Flask(__name__)

# THIS IS THE MISSING PIECE:
def get_db_connection():
    conn = sqlite3.connect('parcels.db')
    conn.row_factory = sqlite3.Row  # This lets us use parcel['status'] instead of parcel[4]
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        parcels = conn.execute('SELECT * FROM parcels ORDER BY last_updated DESC').fetchall()
        conn.close()
        return render_template('index.html', parcels=parcels)
    except sqlite3.OperationalError:
        # This handles cases where the database hasn't been created yet
        return "Database not found. Please run a sync first!"

@app.route('/sync')
def sync():
    print("Manual Sync Triggered...", flush=True) # Check if this prints!
    import main
    main.main() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)