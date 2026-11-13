import pandas as pd
df = pd.read_csv("data/202508_Generation_MD.csv")
print(df.shape)
print(df.iloc[:3, :8])
print(df["Fuel_Code"].unique())
print(df["Trading_Date"].nunique())

print(df["Fuel_Code"].value_counts())

odd = df[df["Fuel_Code"].isin(["ELE", "HYD", "GEO", "SOL"])]
print(odd[["Site_Code", "Gen_Code", "Fuel_Code", "Tech_Code"]].drop_duplicates())

# 统一 Fuel_Code 写法
fuel_map = {"HYD": "Hydro", "GEO": "Geo", "SOL": "Solar", "ELE": "Battery"}
df["Fuel"] = df["Fuel_Code"].replace(fuel_map)
print(df["Fuel"].value_counts())