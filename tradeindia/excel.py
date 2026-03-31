import os
import re
import random
import pandas as pd
from tradeindia.db_config import con  # assumes `con` is your DB connection

# Step 1: Clean function for Excel-safe strings
def clean_cell(value):
    if isinstance(value, str):
        return re.sub(r'[\x00-\x1F\x7F]', '', value)
    return value

# Step 2: Setup export folder
folder_path = r"D:\tradeindia_File"
os.makedirs(folder_path, exist_ok=True)

t_name=f"profile_data_12102025"
# Step 3: Fetch all data into DataFrame
query = f"SELECT * FROM {t_name}"
print("Fetching all records from DB...")
df = pd.read_sql_query(query, con)
print(f"Total rows fetched: {len(df)}")

# Step 4: Clean data
df = df.applymap(clean_cell)
df['Service_meta_data'] = df['Service_meta_data'].apply(lambda x: None if x == [] else x)

# Drop 'id' column if exists
if 'id' in df.columns:
    df.drop('id', axis=1, inplace=True)

# Close the DB connection
con.close()

# Step 5: Chunking logic
total_rows = len(df)
start_idx = 0
file_num = 1

no=0
while start_idx < total_rows:
    # Random chunk size between 250k and 300k
    chunk_size = random.randint(190000, 195000)
    end_idx = min(start_idx + chunk_size, total_rows)

    chunk_df = df.iloc[start_idx:end_idx]

    if no!=0:
        output_file = os.path.join(folder_path, f"{t_name}_extra_{file_num}.xlsx")
    else:
        output_file = os.path.join(folder_path, f"{t_name}.xlsx")

    print(f"Exporting rows {start_idx+1} to {end_idx} --> {output_file}")
    chunk_df.to_excel(output_file, index=False, engine='openpyxl')

    start_idx = end_idx
    file_num += 1
    no+=1

print("✅ All chunks exported successfully.")
