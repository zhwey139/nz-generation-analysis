import pandas as pd

df = pd.read_csv("data/202508_Generation_MD.csv")
tp_cols = [f"TP{i}" for i in range(1, 49)]  # August has 48 trading periods per day

# Check 1: duplicate records (same connection point, network, unit and day)
key = ["POC_Code", "Nwk_Code", "Gen_Code", "Trading_Date"]
dups = df[df.duplicated(subset=key, keep=False)]
print("Check 1 - duplicate unit-days:", len(dups))

# Check 2: missing values in TP1-TP48
missing = df[tp_cols].isna().sum().sum()
print("Check 2 - missing half-hour values:", missing)

# Check 3: negative values
negative = (df[tp_cols] < 0).sum().sum()
print("Check 3 - negative values:", negative)

# Check 4: units with fewer than 31 days of records
days = df.groupby(["POC_Code", "Gen_Code", "Fuel_Code"])["Trading_Date"].nunique()
print("Check 4 - units with fewer than 31 days:")
print(days[days < 31])

# Check 5: process the data day by day and compare each day's total with the previous day
prev = None
for date, day in df.groupby("Trading_Date"):
    total = day[tp_cols].sum().sum() / 1e6
    flag = ""
    if prev is not None and abs(total - prev) / prev > 0.10:
        flag = "  <-- changed more than 10% from previous day"
    print(f"{date}: {len(day)} rows, {total:.1f} GWh{flag}")
    prev = total