# COSC301 — Canadian Housing Price Index Analysis

Data analytics pipeline looking at new housing price trends across Canada using Statistics Canada data going back to 1981.

**Course**: COSC301 | **Project Type**: Information Extraction

---

## Analytics Question

How have housing price indexes changed across Canadian regions over time, and which regions have seen the biggest increases?

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Python (pandas) | ETL, data cleaning, analysis, querying |
| SQLite | Storage of raw and cleaned data in separate tables |
| Tableau | Interactive dashboards and visualization |

---

## Dataset

- **Source**: [New Housing Price Indexes — Statistics Canada via Kaggle](https://www.kaggle.com/)
- **File**: `data/housing_price_indexes.csv`
- **Size**: 63,120 rows × 15 columns
- **Coverage**: Canada-wide, 40 geographic regions, January 1981 onwards
- **Unit**: Index (December 2016 = 100)
- **License**: Statistics Canada Open Licence

---

## Project Pipeline

```
data/housing_price_indexes.csv
        │
        ▼
1_setup_database.py       → loads raw CSV into SQLite (raw_housing table)
        │
        ▼
2_raw_data_cleaning.py    → cleans data, saves to SQLite (cleaned_housing table)
        │
        ▼
[EDA & Analysis scripts]  → queries and analysis NOT IN YET
        │
        ▼
Tableau                   → dashboards and visualizations
```

---

## Folder Structure

```
COSC301-Canadian-Housing-Analysis/
├── data/
│   ├── housing_price_indexes.csv     # Raw dataset (do not modify)
│   └── housing_data.db               # SQLite database (raw + cleaned tables)
├── scripts/
│   ├── 1_setup_database.py           # Step 1: Load raw CSV into SQLite
│   └── 2_raw_data_cleaning.py        # Step 2: Clean data and store in SQLite
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
| `value` | float | Price index value (base: Dec 2016 = 100) |
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
