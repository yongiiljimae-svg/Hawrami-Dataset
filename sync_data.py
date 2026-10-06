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

    # فیلتر هوشمند: فقط ردیف‌هایی را قبول کن که واقعاً ترجمه شده‌اند
    valid_records = []
    for row in records:
        if table == "vocabulary":
            if row.get("word_hac") and str(row.get("word_hac")).strip():
                valid_records.append(row)
        else:
            if row.get("hac_translation") and str(row.get("hac_translation")).strip():
                valid_records.append(row)

    if not valid_records:
        print(f"No fully translated records found in {table}.")
        continue
        
    os.makedirs("dataset", exist_ok=True)
    filename = f"dataset/{table}.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode="a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=valid_records[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(valid_records)
        
    print(f"Added {len(valid_records)} records to {filename}")
    
    # پاک کردن فقط ردیف‌های دارای ترجمه از سوپابیس
    ids_to_delete = [row["id"] for row in valid_records]
    supabase.table(table).delete().in_("id", ids_to_delete).execute()
    print(f"Deleted {len(valid_records)} records from Supabase {table}.")
