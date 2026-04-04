import os

scripts = [
    "scripts/1_setup_database.py",
    "scripts/2_raw_data_cleaning.py",
    "scripts/3_growth_analysis.py",
    "scripts/4_recent_growth_analysis.py",
    "scripts/5_land_premium.py",
    "scripts/6_yoy_change.py",
    "scripts/7_boom_crash.py",
    "scripts/8_peak_analysis.py",
    "scripts/9_volatility_analysis.py",
    "scripts/10_correlation_analysis.py",
    "scripts/11_market_classification.py"
]

for script in scripts:
    print(f"\nRunning {script}...\n")
    os.system(f"python {script}")