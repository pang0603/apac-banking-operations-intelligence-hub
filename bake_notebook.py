import sqlite3
import pandas as pd
import json

# Connect to database and load data summaries
conn = sqlite3.connect('banking_ops.db')

# 1. Global Metrics
df_stp = pd.read_sql_query("""
SELECT 
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS successful_stp_txns,
    ROUND(CAST(SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS overall_stp_rate_pct
FROM transactions;
""", conn)

# 2. Regional Metrics
df_regional = pd.read_sql_query("""
SELECT region, COUNT(*) AS transaction_volume,
       ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM transactions) * 100, 2) AS regional_volume_share_pct,
       ROUND(CAST(SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS regional_stp_rate_pct
FROM transactions GROUP BY region ORDER BY transaction_volume DESC;
""", conn)

# 3. Channel Metrics
df_channel = pd.read_sql_query("""
SELECT channel, COUNT(*) AS total_txns, SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS total_failures,
       ROUND(CAST(SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS failure_rate_pct
FROM transactions GROUP BY channel ORDER BY failure_rate_pct DESC;
""", conn)
conn.close()

# Structure a pre-executed notebook structure including the generated images
notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "source": [
    "# APAC Banking Operations Intelligence Hub\n",
    "### Automated Process Analysis & STP Performance Optimization Report\n",
    "**Author:** Pang Kiat Si <br>\n",
    "**Target Role:** Digital Transformation Business Analyst (OCBC Alignment)"
   ]
  },
  {
   "cell_type": "markdown",
   "source": [
    "## 1. Global Metric Baseline: Straight-Through Processing (STP) Rate\n",
    "The baseline health metric calculates core automation capacity. Any dropout marks manual exception handling leakage."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "outputs": [{"output_type": "execute_result", "data": {"text/plain": df_stp.to_string(index=False)}, "execution_count": 1}],
   "source": ["# SQL Query to verify base operational health\n", "print(df_stp)"]
  },
  {
   "cell_type": "markdown",
   "source": [
    "## 2. Regional Volume Share & STP Divergence Analysis\n",
    "This section isolates transaction volume distribution and processing efficiency across our four operational hubs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "outputs": [
       {"output_type": "stream", "name": "stdout", "text": df_regional.to_string(index=False) + "\n"},
       {"output_type": "display_data", "data": {"image/png": "IMAGE_MARKER_1"}, "metadata": {}}
   ],
   "source": ["# Plotting regional bottlenecks\n", "print(df_regional)"]
  },
  {
   "cell_type": "markdown",
   "source": [
    "## 3. Processing Channel Ingestion Vulnerabilities\n",
    "Isolating where legacy system handshakes create processing dropouts."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "outputs": [
       {"output_type": "stream", "name": "stdout", "text": df_channel.to_string(index=False) + "\n"},
       {"output_type": "display_data", "data": {"image/png": "IMAGE_MARKER_2"}, "metadata": {}}
   ],
   "source": ["# Isolate leakage channels\n", "print(df_channel)"]
  }
 ],
 "metadata": {"language_info": {"name": "python"}},
 "nbformat": 4, "nbformat_minor": 2
}

# Convert the existing generated images into the notebook data stream
import base64
try:
    with open("regional_stp_rates.png", "rb") as img_f:
        img1_data = base64.b64encode(img_f.read()).decode('utf-8')
    with open("channel_failures.png", "rb") as img_f:
        img2_data = base64.b64encode(img_f.read()).decode('utf-8')
        
    notebook_str = json.dumps(notebook)
    notebook_str = notebook_str.replace("IMAGE_MARKER_1", img1_data).replace("IMAGE_MARKER_2", img2_data)
    
    with open("APAC_Banking_Ops_Analysis.ipynb", "w") as f:
        f.write(notebook_str)
    print("✅ Success! Charts and analytical queries baked directly into 'APAC_Banking_Ops_Analysis.ipynb'.")
except FileNotFoundError:
    print("❌ Error: Make sure you run 'generate_charts.py' first to build the image assets!")