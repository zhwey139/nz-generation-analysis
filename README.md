# NZ Electricity Generation Data Analysis

Python analysis of New Zealand half-hourly grid generation data from the Electricity Authority (EMI).

**Status: work in progress**

## Background
In a RESE421 tutorial, I analysed one day of half-hourly generation data (22 August 2025) in Excel. This project extends that to the full month of August 2025 using Python, with data checks and visualisation.

## Data
- Source: Electricity Authority EMI, Generation output (`202508_Generation_MD.csv`)
- One row per generating unit per day; columns TP1–TP50 are half-hour trading periods (kWh)
- 2,807 rows, 31 days

## What `explore.py` does
1. Reads the CSV with pandas
2. Checks fuel labels and finds inconsistent codes (`HYD` vs `Hydro`, `GEO` vs `Geo`, `SOL` vs `Solar`). Each was checked against `Tech_Code` before merging. `ELE` units are batteries (`Tech_Code` = `BAT`), grouped as Battery
3. Sums TP1–TP50 to get daily generation per unit, then totals by date and fuel type (GWh)
4. Plots a stacked area chart

## What `checks.py` does
Processes the data in daily batches and runs automatic checks:
1. Duplicate records (same connection point, network, unit and day): 0
2. Missing half-hour values (TP1–TP48): 0
3. Negative values: 0
4. Units with fewer than 31 days of records: 4 (Highbank 30, Huntly coal 24, Huntly P40 gas 15, Kawerau TOPP2 10)
5. Daily total compared with the previous day, flagged if it changes by more than 10%: 1 flag (4 August, a Monday after the weekend, so a real change rather than a data error)

## Result
![Daily generation by fuel type](figures/daily_generation_by_fuel.png)

August 2025 total: about 3,914 GWh (about 126 GWh per day). Hydro 58%, geothermal 22%, gas 11%, wind 7%, coal 2%.

## Data issues found
- Inconsistent fuel codes (fixed as above)
- 4 units have fewer than 31 days of records. This may be because they were not running on those days (e.g. Huntly units are often used only when needed), so they are flagged rather than changed
- My first duplicate check found 248 rows. On checking, these were 4 plants recorded under two network codes at the same connection point, with different values (one often zero), so they are not true duplicates. I added `Nwk_Code` to the check
- Diesel and wood units recorded zero generation all month

## Next steps
- [x] Process the data in daily batches
- [x] Automatic checks: duplicates, missing values, negative values, units with missing days, large day-to-day changes
- [ ] Check for sudden jumps within each unit's half-hourly data
- [ ] Evening peak (TP43) comparison across the month
- [ ] Add more months
- [ ] Interactive dashboard

## How to run
```
pip install pandas matplotlib
python3 explore.py
python3 checks.py
```