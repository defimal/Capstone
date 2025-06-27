import pandas as pd

# Load data
csv_path = 'data/processed/output.csv'
df = pd.read_csv(csv_path)

# Start report
print("\n📊 PROJECT DATA REPORT\n" + "="*50)

# 1. Basic Overview
print(f"\n✅ Total Records: {len(df)}")
print(f"✅ Columns: {', '.join(df.columns)}")

# 2. Preview
print("\n🧾 First 5 Entries:\n")
print(df.head(5).to_string(index=False))

# 3. Stats (only for numeric columns)
numeric_cols = df.select_dtypes(include=['number'])
if not numeric_cols.empty:
    print("\n📈 Numeric Column Summary:\n")
    print(numeric_cols.describe().to_string())
else:
    print("\nℹ️ No numeric columns to summarize.")

# 4. Optional: Export to a TXT report
with open("data/processed/project_report.txt", "w") as f:
    f.write("📊 PROJECT DATA REPORT\n" + "="*50 + "\n\n")
    f.write(f"✅ Total Records: {len(df)}\n")
    f.write(f"✅ Columns: {', '.join(df.columns)}\n\n")
    f.write("🧾 First 5 Entries:\n")
    f.write(df.head(5).to_string(index=False) + "\n\n")
    if not numeric_cols.empty:
        f.write("📈 Numeric Column Summary:\n")
        f.write(numeric_cols.describe().to_string())
    else:
        f.write("ℹ️ No numeric columns to summarize.")
print("\n✅ Report written to: project_report.txt")
