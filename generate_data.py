import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Initialize Faker and seed for reproducibility
fake = Faker(['en_US'])
Faker.seed(42)
random.seed(42)

# --- CONFIGURATION (Per Blueprint Specifications) ---
NUM_TRANSACTIONS = 2000
START_DATE = datetime(2026, 1, 1) # Set in current operational year

# Regional distribution profile [cite: 38]
REGIONS = ["SG", "MY", "TH", "ID"]
REGION_PROBS = [0.40, 0.25, 0.20, 0.15] 

REGION_METRICS = {
    "SG": {"currency": "SGD", "base_fail_rate": 0.07}, # Lower failure, high automation
    "MY": {"currency": "MYR", "base_fail_rate": 0.11},
    "TH": {"currency": "THB", "base_fail_rate": 0.14},
    "ID": {"currency": "IDR", "base_fail_rate": 0.16}  # Higher failure, legacy infrastructure
}

CATEGORIES = ["CASA", "Payment", "Loan", "FX"]
CHANNELS = ["Mobile App", "Internet Banking", "ATM", "SWIFT/Corporate Gateway", "Branch"]

# 5 Core Bank Operational Failure Codes [cite: 38]
FAILURE_REASONS = {
    "FAIL_001": "Insufficient Funds / Limit Exceeded",
    "FAIL_002": "Sanction Screening Match / Compliance Hold",
    "FAIL_003": "Invalid Beneficiary Account / Routing Error",
    "FAIL_004": "Clearing House Timeout / Network Dropout",
    "FAIL_005": "FX Rate Expired / Cross-Currency Discrepancy"
}

transactions = []

# --- GENERATE DATA ---
for i in range(NUM_TRANSACTIONS):
    tx_id = f"TXN{2026}{100000 + i}" # 2026 transaction series
    
    # 1. Geographic & Regional Mapping [cite: 38]
    region = random.choices(REGIONS, weights=REGION_PROBS, k=1)[0]
    currency = REGION_METRICS[region]["currency"]
    
    # 2. Category & Channel Selection [cite: 38]
    category = random.choice(CATEGORIES)
    channel = random.choices(CHANNELS, weights=[0.45, 0.30, 0.10, 0.10, 0.05], k=1)[0]
    
    # 3. Base Amount (highly dependent on category)
    if category == "CASA":
        amount = round(random.uniform(10, 8000), 2)
    elif category == "Payment":
        amount = round(random.uniform(5, 25000), 2)
    elif category == "Loan":
        amount = round(random.uniform(1000, 150000), 2)
    elif category == "FX":
        amount = round(random.uniform(500, 500000), 2)

    # 4. Generate Date/Time Component spread across a rolling period [cite: 38]
    tx_timestamp = START_DATE + timedelta(
        days=random.randint(0, 150),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    # 5. Injecting Failure Risk & Exception Patterns [cite: 20, 38]
    # Adjust failure chance slightly based on legacy channels (SWIFT/Branch)
    fail_chance = REGION_METRICS[region]["base_fail_rate"]
    if channel in ["SWIFT/Corporate Gateway", "Branch"]:
        fail_chance += 0.05 
        
    is_failed = random.random() < fail_chance
    
    if is_failed:
        status = "Failed"
        stp_indicator = "No" # Did not go Straight-Through
        # Assign realistic failure code
        if category == "FX":
            failure_code = "FAIL_005"
        else:
            failure_code = random.choice(list(FAILURE_REASONS.keys()))
        failure_description = FAILURE_REASONS[failure_code]
        
        # Exception Resolution Days: Normal distribution skewed by severity [cite: 38]
        if failure_code == "FAIL_002":  # Compliance holds take longer
            resolution_days = int(max(2, round(random.normalvariate(7.5, 2.0))))
        else:
            resolution_days = int(max(0, round(random.normalvariate(3.2, 1.5))))
            
        resolution_status = random.choices(["Resolved", "Pending Escalation"], weights=[0.85, 0.15], k=1)[0]
    else:
        status = "Success"
        stp_indicator = "Yes" # Clean processing
        failure_code = "None"
        failure_description = "None"
        resolution_days = 0
        resolution_status = "N/A"

    # 6. Simulated FX Column (Realism factor) [cite: 38]
    # Standardize cross-currency reference vs USD for dashboard analytics
    fx_rate_to_usd = round(random.uniform(0.7, 1.4), 4) if currency != "SGD" else 0.74

    transactions.append({
        "transaction_id": tx_id,
        "timestamp": tx_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "region": region,
        "currency": currency,
        "category": category,
        "channel": channel,
        "amount": amount,
        "fx_rate_to_usd": fx_rate_to_usd,
        "status": status,
        "stp_indicator": stp_indicator,
        "failure_code": failure_code,
        "failure_description": failure_description,
        "resolution_days": resolution_days,
        "resolution_status": resolution_status
    })

# --- DATA EXPORT & PERSISTENCE ---
df = pd.DataFrame(transactions)

# 1. Export to CSV for visualizers [cite: 21]
csv_filename = "apac_banking_transactions.csv"
df.to_csv(csv_filename, index=False)

# 2. Export to SQLite to write your 8-10 BA SQL queries 
db_filename = "banking_ops.db"
conn = sqlite3.connect(db_filename)
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()

print(f"✅ Success! Generated {len(df)} transactions.")
print(f"📊 CSV saved as: '{csv_filename}'")
print(f"🗄️ SQLite Database saved as: '{db_filename}'")
print("\n--- Operational Sample (First 5 Transactions) ---")
print(df[['transaction_id', 'region', 'category', 'channel', 'status', 'stp_indicator']].head())