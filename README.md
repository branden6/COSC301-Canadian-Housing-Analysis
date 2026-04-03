# COSC301 — Canadian Housing Price Index Analysis

Data analytics pipeline looking at housing price trends across Canada using data from 1981 - 2024.

**Course**: COSC301 | **Project Type**: Information Extraction

---

## Analytics Question

TBD fill this out later once we start with the our actual scripts

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
3_growth_analysis.py          → exploratory long-term NHPI comparison (1981 - 2024)
        │
        ▼
4_recent_growth_analysis.py   → post COVID growth analysis (2020-2024)
        │
        ▼
     Tableau                  → dashboards and visualizations

```

---

## Analysis Scripts

### 3_growth_analysis.py

Explores long-term changes in the New Housing Price Index (NHPI) across Canadian regions.

- Aggregates monthly data into yearly averages  
- Compares earliest and latest available values per region  
- Computes percentage growth  

**Note:**  
Due to the indexed nature of the NHPI (December 2016 = 100), long-term comparisons may produce unintuitive results and are used for exploratory context only.

---

### 4_recent_growth_analysis.py

Analyzes recent growth in new housing prices across Canadian regions (2020–2024).

- Filters data to recent years (2020+)  
- Computes yearly averages per region  
- Calculates percentage growth from 2020 to latest available year (2024)
- Ranks regions by growth 


---

## Folder Structure

```
Change this throughout project whenever you add something new

COSC301-Canadian-Housing-Analysis/
├── data/
│   ├── housing_price_indexes.csv     # Raw dataset (do not modify)
│   └── housing_data.db               # SQLite database (raw + cleaned tables)
├── scripts/
│   ├── 1_setup_database.py           # Step 1: Load raw CSV into SQLite
│   ├── 2_raw_data_cleaning.py        # Step 2: Clean data and store in SQLite
│   ├── 3_growth_analysis.py          # Exploratory long-term comparison
│   ├── 4_recent_growth_analysis.py   # post COVID growth analysis (2020-2024)
├── README.md
└── requirements.txt

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

# 4. Run the pipeline in order
python scripts/1_setup_database.py
python scripts/2_raw_data_cleaning.py
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
