# COSC301 — Canadian Housing Price Index Analysis
**By:** Fraser Muller & Branden Kennedy

**Course:** COSC 301 - Introduction to Data Analytics

Data analytics pipeline looking at housing price trends across Canada using data from 1981 - 2024.

**Course**: COSC301 | **Project Type**: Information Extraction

---

## Analytics Question

How have new housing price indexes changed across Canadian regions over time, and what relationships exist between growth, volatility, speculation, and market cycles?

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Python (pandas) | ETL, data cleaning, analysis, querying |
| SQLite | Storage of raw and cleaned data in separate tables |
| Tableau | Interactive dashboards and visualization |

---

## Dataset

- **Source**: [New Housing Price Indexes — Statistics Canada via Kaggle](https://www.kaggle.com/datasets/noeyislearning/housing-price-indexes)
- **File**: `data/housing_price_indexes.csv`
- **Size**: 63,120 rows × 15 columns
- **Coverage**: Canada-wide, 40 geographic regions, January 1981 - 2024.
- **Unit**: Index (December 2016 = 100)
- **License**: Statistics Canada Open Licence

## Important Note on Dataset

This project uses the New Housing Price Index (NHPI), which measures changes in the selling prices of newly built homes. The data is reported as an index with December 2016 = 100, meaning values represent relative price levels rather than actual housing prices in dollars.

As a result, the dataset does not reflect average home prices or resale market values. Instead, it captures how the prices of newly constructed homes change over time.

---

## Project Pipeline
```

data/housing_price_indexes.csv
        │
        ▼
1_setup_database.py           → loads raw CSV into SQLite (raw_housing table)
        │
        ▼
2_raw_data_cleaning.py        → cleans data, saves to SQLite (cleaned_housing table)
        │
        ▼
3_growth_analysis.py          → long-term growth by region (1981–2024)
        │
        ▼
4_recent_growth_analysis.py   → recent growth by region (2020–2024)
        │
        ▼
5_land_premium.py             → land vs house index ratio (speculation detection)
        │
        ▼
6_yoy_change.py               → month-over-month % change vs same month last year
        │
        ▼
7_boom_crash.py               → labels each month as Boom / Crash / Stable
        │
        ▼
8_peak_analysis.py            → all-time peak per region + current drawdown
        │
        ▼
9_volatility_analysis.py      → measures market instability using standard deviation of year over year changes
        │
        ▼
10_correlation_analysis.py    → analyzes relationships between growth, volatility, land premium, drawdown
        │
        ▼
11_market_classification.py   → categorizes regions into market types based on growth, volatility, drawdown
        │
        ▼
     Tableau                  → dashboards and visualizations

```

## Key Findings

- **Housing prices increased significantly across most regions**, with particularly strong growth observed between 2020–2024, suggesting a widespread surge in demand during this period.

- **Growth patterns vary greatly by region**, with some areas experiencing rapid increases while others show more moderate, steady trends.

- **Market volatility differs across regions**, as some housing markets exhibit large year-over-year swings while others remain relatively stable.

- **Higher-growth regions tend to be slightly more volatile**, indicating that rapid price increases may come with increased uncertainty.

- **Speculation (land value vs house value) does not strongly explain growth**, as regions with higher land premiums do not consistently show higher price increases.

- **More volatile regions are more likely to decline from their peak**, suggesting that unstable markets carry greater downside risk.

- **Most regions remain at or near their historical peak prices**, though a small number show signs of decline, indicating uneven market cooling.

- **Canadian housing markets can be grouped into distinct types**, including high-growth stable markets, high-growth volatile markets, moderate-growth regions, and declining markets.

---

## Folder Structure

```

COSC301-Canadian-Housing-Analysis/
├── data/
│   ├── housing_price_indexes.csv              # Raw dataset (do not modify)
│   ├── housing_data.db                        # SQLite database (raw + cleaned tables)
│   ├── 3_growth_by_region.csv                 # output for script 3
│   ├── 4_recent_growth_by_region.csv          # output for script 4
│   ├── 5_land_premium.csv                     # output for script 5
│   ├── 6_yoy_change.csv                       # output for script 6
│   ├── 7_boom_crash_labels.csv                # output for script 7
│   ├── 8_peak_analysis.csv                    # output for script 8
│   ├── 9_volatility_by_region.csv             # output for script 9
│   ├── 10_regional_correlation_metrics.csv    # merged regional matrix for analysis and tableau visualization for script 10 
│   ├── 10_regional_correlation_matrix.csv     # correlation between key housing indicators for script 10
│   └── 11_market_classification.csv           # output for script 11
├── scripts/
│   ├── 1_setup_database.py                    # load raw CSV into SQLite
│   ├── 2_raw_data_cleaning.py                 # clean data and store in SQLite
│   ├── 3_growth_analysis.py                   # long-term growth by region
│   ├── 4_recent_growth_analysis.py            # recent growth (2020-2024)
│   ├── 5_land_premium.py                      # land vs house speculation ratio
│   ├── 6_yoy_change.py                        # year-over-year % change
│   ├── 7_boom_crash.py                        # boom/crash labels
│   ├── 8_peak_analysis.py                     # all-time peak + drawdown
│   ├── 9_volatility_analysis.py               # volatility using standard deviation of year over year changes
│   ├── 10_correlation_analysis.py             # relationships between growth, volatility, land premium, drawdown
│   └── 11_market_classification.py            # classify regions into market types
├── README.md
├── requirements.txt
└── run_all_scripts.py                         # runs all scripts with terminal command python run_all_scripts.py

```
---

## How to Reproduce

```bash
# 1. Clone the repo
git clone https://github.com/branden6/COSC301-Canadian-Housing-Analysis.git
cd COSC301-Canadian-Housing-Analysis

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the run_all_scripts script, which runs all scripts in order 
python run_all_scripts.py
```

---

## Data Dictionary (Cleaned Table)

| Column | Type | Description |
|--------|------|-------------|
| `ref_date` | string | Date of observation (YYYY-MM) |
| `year` | int | Year extracted from ref_date |
| `month` | int | Month extracted from ref_date |
| `geo` | string | Geographic region (e.g., Canada, Ontario, Vancouver) |
| `price_category` | string | Index type: Total (house and land), House only, Land only |
| `value` | float | Price index value (base value: Dec 2016 = 100, so 38.2 would mean prices were about 38% of their December 2016 level) |
| `status` | string | Data quality flag: `normal`, `E` (estimate), `..` (not available), `x` (suppressed) |

---

## Cleaning Decisions

| Decision | Reason |
|----------|---------|
| Dropped `SYMBOL`, `TERMINATED` | completely empty |
| Dropped `UOM`, `UOM_ID`, `SCALAR_FACTOR`, `SCALAR_ID`, `DECIMALS` | same value in every single row |
| Dropped `DGUID`, `VECTOR`, `COORDINATE` | internal Stats Canada IDs, not useful for analysis |
| Converted `VALUE` to float | raw CSV stores it as a string |
| Converted `REF_DATE` to datetime, split into year/month | easier to filter and group by time |
| Filled null `STATUS` with `"normal"` | null just means the data point is fine |
| Kept rows where `value` is missing | these are suppressed/unavailable data points, still want them tracked |
