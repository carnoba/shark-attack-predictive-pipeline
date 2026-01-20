import pandas as pd
import sqlite3
import re
from datetime import datetime

def master_pipeline(csv_file, db_name):
    print(f"--- Phase 1: Ingestion ---")
    try:
        # Read with user parameters
        df = pd.read_csv(csv_file, encoding='cp1252', on_bad_lines='skip')
        print(f"Total rows read: {len(df)}")
        
        # Clean column names immediately
        df.columns = [c.strip().replace(' ', '_').replace('.', '').replace('/', '_').replace('?', '').replace('(', '').replace(')', '') for c in df.columns]
        
        print(f"--- Phase 2: Cleaning (@the-janitor) ---")
        
        # 1. Clean 'Fatal' and create 'is_fatal'
        # The column is often named 'Fatal_Y_N' or similar after cleaning
        fatal_col = 'Fatal_Y_N' if 'Fatal_Y_N' in df.columns else 'Fatal'
        if fatal_col in df.columns:
            df['is_fatal'] = df[fatal_col].astype(str).str.upper().str.strip()
            df['is_fatal'] = df['is_fatal'].apply(lambda x: 1 if x == 'Y' else (0 if x == 'N' else None))
            # Fill missing is_fatal with 0 (assuming non-fatal if not specified, or we can drop)
            df['is_fatal'] = df['is_fatal'].fillna(0).astype(int)
            print("Created 'is_fatal' column.")
        
        # 2. Clean 'Date' and extract 'Month'
        if 'Date' in df.columns:
            def extract_month(date_str):
                date_str = str(date_str).lower()
                months = {
                    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                }
                for m_str, m_num in months.items():
                    if m_str in date_str:
                        return m_num
                return None
            
            df['Month'] = df['Date'].apply(extract_month)
            # Fill missing months with a placeholder or drop? Let's use 0 for unknown
            df['Month'] = df['Month'].fillna(0).astype(int)
            print("Extracted 'Month' from 'Date'.")
            
        # 3. Clean 'Country' and 'Activity'
        for col in ['Country', 'Activity']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.title()
                df[col] = df[col].replace('Nan', 'Unknown')
                print(f"Cleaned '{col}' column.")
                
        # 4. Final DB Conversion
        print(f"Saving to {db_name}...")
        conn = sqlite3.connect(db_name)
        df.to_sql('sharks', conn, if_exists='replace', index=False)
        conn.close()
        print("Pipeline completed successfully.")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    master_pipeline('GSAF5.csv', 'master_sharks.db')
