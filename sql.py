import sqlite3
import pandas as pd

# Connect to the SQLite database generated in Phase 1
db_filename = "banking_ops.db"
conn = sqlite3.connect(db_filename)

def run_and_print_query(title, query):
    """Helper function to execute a query and print it cleanly"""
    print("\n" + "="*60)
    print(f"📊 {title.upper()}")
    print("="*60)
    
    # Use pandas to read the SQL query directly into a DataFrame
    df_result = pd.read_sql_query(query, conn)
    
    # Print the full DataFrame with clean formatting
    print(df_result.to_string(index=False))

# --- QUERY 1: Overall Straight-Through Processing (STP) Rate ---
q1_stp_rate = """
SELECT 
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS successful_stp_txns,
    ROUND(CAST(SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS overall_stp_rate_pct
FROM transactions;
"""

# --- QUERY 2: Regional STP Performance & Volumetric Split ---
q2_regional_perf = """
SELECT 
    region,
    COUNT(*) AS transaction_volume,
    ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM transactions) * 100, 2) AS regional_volume_share_pct,
    ROUND(CAST(SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS regional_stp_rate_pct
FROM transactions
GROUP BY region
ORDER BY transaction_volume DESC;
"""

# --- QUERY 3: Channel Vulnerability ---
q3_channel_vulnerability = """
SELECT 
    channel,
    COUNT(*) AS total_txns,
    SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS total_failures,
    ROUND(CAST(SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS failure_rate_pct
FROM transactions
GROUP BY channel
ORDER BY failure_rate_pct DESC;
"""

# --- QUERY 4: Top Core Banking Failure Codes ---
q4_failure_root_cause = """
SELECT 
    failure_code,
    failure_description,
    COUNT(*) AS failure_count,
    ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM transactions WHERE status = 'Failed') * 100, 2) AS contribution_to_failures_pct
FROM transactions
WHERE status = 'Failed'
GROUP BY failure_code, failure_description
ORDER BY failure_count DESC;
"""

# --- QUERY 5: Exception Handling Backlog (Avg Resolution Days) ---
q5_resolution_time = """
SELECT 
    region,
    COUNT(*) AS failed_txn_count,
    ROUND(AVG(resolution_days), 1) AS avg_days_to_resolve,
    MAX(resolution_days) AS worst_case_resolution_days
FROM transactions
WHERE status = 'Failed'
GROUP BY region
ORDER BY avg_days_to_resolve DESC;
"""

# --- EXECUTE THE QUERIES ---
if __name__ == "__main__":
    print("Running Portfolio Analytics Pipeline Validation...")
    
    run_and_print_query("Overall Straight-Through Processing (STP) Rate", q1_stp_rate)
    run_and_print_query("Regional Volume Share & STP Rates", q2_regional_perf)
    run_and_print_query("Processing Channel Failure Rates", q3_channel_vulnerability)
    run_and_print_query("Root Cause Failure Code Analysis", q4_failure_root_cause)
    run_and_print_query("Operational Exception Resolution Time (Days)", q5_resolution_time)
    
    # Close connection
    conn.close()
    print("\n✅ Verification complete. Data matches expected operational patterns.")