import os
import csv
from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

tables = ["vocabulary", "sentences", "literary_texts"]

for table in tables:
    print(f"Checking {table}...")
    response = supabase.table(table).select("*").eq("status", "approved").execute()
    records = response.data
    
    if not records:
        print(f"No new approved data for {table}.")
        continue
        
    os.makedirs("dataset", exist_ok=True)
    filename = f"dataset/{table}.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode="a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(records)
        
    print(f"Added {len(records)} records to {filename}")
    
    # پاک کردن ردیف‌های دانلود شده از سوپابیس
    ids_to_delete = [row["id"] for row in records]
    supabase.table(table).delete().in_("id", ids_to_delete).execute()
    print(f"Deleted {len(records)} records from Supabase {table}.")
