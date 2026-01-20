import pandas as pd
import sqlite3
import os

def ingest_data(csv_file, db_name):
    print(f"Starting ingestion of {csv_file}")
    
    try:
        # User specified: encoding='cp1252' and on_bad_lines='skip'
        df = pd.read_csv(csv_file, encoding='cp1252', on_bad_lines='skip')
        
        # Initial stats
        raw_count = len(df)
        print(f"Read {raw_count} rows from CSV.")
        
        # Clean column names for SQLite (remove spaces, dots, and trailing spaces)
        df.columns = [c.strip().replace(' ', '_').replace('.', '').replace('/', '_').replace('?', '').replace('(', '').replace(')', '') for c in df.columns]
        
        # Connect to SQLite
        conn = sqlite3.connect(db_name)
        df.to_sql('raw_attacks', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"Successfully converted to {db_name}. table name: 'raw_attacks'")
        return True
    except Exception as e:
        print(f"Failed to ingest data: {e}")
        return False

if __name__ == "__main__":
    csv_path = 'GSAF5.csv'
    db_path = 'master_sharks.db'
    ingest_data(csv_path, db_path)
