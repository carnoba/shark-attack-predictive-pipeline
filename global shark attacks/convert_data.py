import pandas as pd
import sqlite3
import os

def convert_csv_to_sqlite(csv_file, db_name):
    log_file = "conversion_log.txt"
    with open(log_file, "w") as log:
        log.write(f"Starting conversion of {csv_file}\n")
        try:
            # Try latin-1 first
            log.write("Trying latin-1 encoding...\n")
            df = pd.read_csv(csv_file, encoding='latin-1')
            log.write("Successfully read CSV.\n")
            log.write("Columns: " + str(df.columns.tolist()) + "\n")
            log.write("Data Head:\n" + str(df.head()) + "\n")
            
            # Clean column names
            df.columns = [c.strip().replace(' ', '_').replace('.', '').replace('/', '_').replace('?', '') for c in df.columns]
            
            log.write(f"Converting to {db_name}...\n")
            conn = sqlite3.connect(db_name)
            df.to_sql('attacks', conn, if_exists='replace', index=False)
            conn.close()
            log.write("Conversion complete!\n")
            
        except Exception as e:
            log.write(f"Error: {e}\n")

if __name__ == "__main__":
    csv_path = 'GSAF5.csv'
    db_path = 'shark_attacks.db'
    convert_csv_to_sqlite(csv_path, db_path)

