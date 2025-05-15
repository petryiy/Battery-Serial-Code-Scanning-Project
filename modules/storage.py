import sqlite3
import os

DB_PATH = "data/battery_pack.db"


def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS battery_pack (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pack_serial TEXT UNIQUE,
            bms_serial TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_latest_serial_with_prefix(prefix):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT pack_serial FROM battery_pack WHERE pack_serial LIKE ? ORDER BY pack_serial DESC LIMIT 1", (prefix + '%',))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None


def save_record_to_db(pack_serial, bms_serial):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO battery_pack (pack_serial, bms_serial) VALUES (?, ?)", (pack_serial, bms_serial))
    conn.commit()
    conn.close()


def save_record_to_csv(record, filename):
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ["pack_serial", "bms_serial", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "pack_serial": record["pack_serial"],
            "bms_serial": record["bms_serial"],
            "timestamp": record["timestamp"]
        })
    print(f"Data saved to CSV: {filename}")

