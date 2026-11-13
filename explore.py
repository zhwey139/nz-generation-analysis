import plotly.express as px
import matplotlib.pyplot as plt
import os
import pandas as pd

# Load the data
df = pd.read_csv("data/202508_Generation_MD.csv")
print(df.shape)
print(df.iloc[:3, :8])
print(df["Fuel_Code"].unique())
print(df["Trading_Date"].nunique())

# Look at fuel codes and find inconsistent labels
print(df["Fuel_Code"].value_counts())

odd = df[df["Fuel_Code"].isin(["ELE", "HYD", "GEO", "SOL"])]
print(odd[["Site_Code", "Gen_Code", "Fuel_Code", "Tech_Code"]].drop_duplicates())

# Unify Fuel_Code labels (checked against Tech_Code)
fuel_map = {"HYD": "Hydro", "GEO": "Geo", "SOL": "Solar", "ELE": "Battery"}
df["Fuel"] = df["Fuel_Code"].replace(fuel_map)
print(df["Fuel"].value_counts())

# Daily generation per unit = sum of TP1-TP50 (TP49-TP50 are only used on daylight saving days)
tp_cols = [f"TP{i}" for i in range(1, 51)]
df["Daily_kWh"] = df[tp_cols].sum(axis=1)

# Total by date and fuel type, in GWh
daily = df.groupby(["Trading_Date", "Fuel"])["Daily_kWh"].sum().unstack()
daily_gwh = daily / 1e6

print(daily_gwh.head())
print(daily_gwh.sum().sort_values(ascending=False))

# Prepare data for plotting
daily_gwh = daily_gwh.fillna(0)                      # no records on a day = 0
daily_gwh = daily_gwh.loc[:, daily_gwh.sum() > 0]    # drop fuel types with zero output all month
order = daily_gwh.sum().sort_values(ascending=False).index
daily_gwh = daily_gwh[order]                         # largest fuel type at the bottom
daily_gwh.index = pd.to_datetime(daily_gwh.index)

# Stacked area chart
ax = daily_gwh.plot(kind="area", figsize=(12, 6))
ax.set_title("NZ daily grid generation by fuel type, August 2025")
ax.set_xlabel("Date")
ax.set_ylabel("Generation (GWh/day)")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()

os.makedirs("figures", exist_ok=True)
plt.savefig("figures/daily_generation_by_fuel.png", dpi=150)
print("Saved figures/daily_generation_by_fuel.png")

# Interactive chart (open the HTML file in a browser)
fig = px.area(
    daily_gwh,
    title="NZ daily grid generation by fuel type, August 2025 (interactive)",
    labels={"value": "Generation (GWh/day)", "Trading_Date": "Date", "Fuel": "Fuel type"},
)
fig.update_layout(hovermode="x unified")
fig.update_traces(hovertemplate="%{y:.1f} GWh")
fig.write_html("figures/daily_generation_by_fuel.html")
print("Saved figures/daily_generation_by_fuel.html")