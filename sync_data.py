import os
import csv
from supabase import create_client, Client

# گرفتن اطلاعات اتصال از متغیرهای محیطی
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set.")
    exit(1)

supabase: Client = create_client(url, key)

tables = ["vocabulary", "sentences", "literary_texts"]

for table in tables:
    print(f"\n--- Checking {table} ---")
    
    try:
        # دریافت داده‌های تایید شده
        response = supabase.table(table).select("*").eq("status", "approved").execute()
        records = response.data
        
        if not records:
            print(f"No new approved data for {table}.")
            continue

        # فیلتر هوشمند: جداسازی داده‌های کامل از داده‌های بدون ترجمه
        valid_records = []
        invalid_ids = []
        
        for row in records:
            if table == "vocabulary":
                if row.get("word_hac") and str(row.get("word_hac")).strip():
                    valid_records.append(row)
                else:
                    invalid_ids.append(row["id"])
            else:
                if row.get("hac_translation") and str(row.get("hac_translation")).strip():
                    valid_records.append(row)
                else:
                    invalid_ids.append(row["id"])

        # اگر داده‌ای تایید شده اما ترجمه ندارد، وضعیتش را به pending برگردان تا مسدود نشود
        if invalid_ids:
            print(f"Found {len(invalid_ids)} items approved without translation. Reverting to 'pending'...")
            for invalid_id in invalid_ids:
                supabase.table(table).update({"status": "pending"}).eq("id", invalid_id).execute()

        if not valid_records:
            print(f"No fully translated records found to export for {table}.")
            continue
            
        # ساخت پوشه و فایل CSV برای ذخیره در گیت‌هاب
        os.makedirs("dataset", exist_ok=True)
        filename = f"dataset/{table}.csv"
        file_exists = os.path.isfile(filename)
        
        with open(filename, mode="a", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=valid_records[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(valid_records)
            
        print(f"✅ Added {len(valid_records)} records to {filename}")
        
        # پاک کردن ردیف‌های منتقل شده از سوپابیس برای سبک شدن دیتابیس
        ids_to_delete = [row["id"] for row in valid_records]
        supabase.table(table).delete().in_("id", ids_to_delete).execute()
        print(f"🗑️ Deleted {len(valid_records)} exported records from Supabase {table}.")
        
    except Exception as e:
        print(f"❌ Error processing table {table}: {e}")
