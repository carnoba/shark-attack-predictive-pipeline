import pandas as pd
import sqlite3

# 1. Database se connect karein
conn = sqlite3.connect('master_sharks.db')

# 2. Data ko read karein (Sharks table se)
df = pd.read_sql('SELECT * FROM sharks', conn)

# 3. CSV mein save karein
df.to_csv('sharks_cleaned.csv', index=False)

conn.close()
print("✅sharks_cleaned.csv")