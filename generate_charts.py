import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set professional corporate style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.size': 10, 
    'axes.labelsize': 11, 
    'axes.titlesize': 13,
    'font.family': 'sans-serif'
})

# Connect to database
conn = sqlite3.connect("banking_ops.db")

# -------------------------------------------------------------------------
# CHART 1: FAILURE RATE HEATMAP (CHANNEL × REGION)
# -------------------------------------------------------------------------
print("Generating Regional Failure Rate Heatmap...")
q_heatmap = """
SELECT channel, region,
       ROUND(CAST(SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 1) AS failure_rate
FROM transactions
GROUP BY channel, region;
"""
df_heatmap = pd.read_sql_query(q_heatmap, conn)

# Pivot data using verified database structural pillars
pivot_df = df_heatmap.pivot(index='channel', columns='region', values='failure_rate')

plt.figure(figsize=(9, 5))
sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap="YlOrRd", cbar=True, 
            annot_kws={'weight': 'bold'}, linewidths=0.5)

plt.title("FAILURE RATE HEATMAP — CHANNEL × OPERATIONAL REGION (%)", pad=15, fontweight='bold', loc='left')
plt.xlabel("Operational Hub Region")
plt.ylabel("Ingestion Channel")
plt.tight_layout()
plt.savefig("dashboard_heatmap.png", dpi=300)
plt.close()


# -------------------------------------------------------------------------
# CHART 2: FAILURE CODE BREAKDOWN & LATENCY
# -------------------------------------------------------------------------
print("Generating Failure Code Analysis Charts...")
q_code_count = """
SELECT failure_code, COUNT(*) as volume
FROM transactions
WHERE status = 'Failed' AND failure_code IS NOT NULL
GROUP BY failure_code
ORDER BY volume DESC;
"""
df_code_count = pd.read_sql_query(q_code_count, conn)

q_code_latency = """
SELECT failure_code, ROUND(AVG(resolution_days), 1) as avg_days
FROM transactions
WHERE status = 'Failed' AND failure_code IS NOT NULL
GROUP BY failure_code
ORDER BY avg_days DESC;
"""
df_code_latency = pd.read_sql_query(q_code_latency, conn)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Left plot: Volume
sns.barplot(x="volume", y="failure_code", data=df_code_count, palette="Reds_r", ax=ax1)
ax1.set_title("FAILURE CODE BREAKDOWN (TOTAL EXCEPTIONS)", fontweight='bold', loc='left')
ax1.set_xlabel("Volume Count")
ax1.set_ylabel("")
for p in ax1.patches:
    ax1.annotate(f" {int(p.get_width())}", (p.get_width(), p.get_y() + p.get_height()/2), va='center', fontweight='bold')

# Right plot: Days
sns.barplot(x="avg_days", y="failure_code", data=df_code_latency, palette="Oranges_r", ax=ax2)
ax2.set_title("AVG RESOLUTION DAYS BY EXCEPTION CODE", fontweight='bold', loc='left')
ax2.set_xlabel("Operational Days")
ax2.set_ylabel("")
for p in ax2.patches:
    ax2.annotate(f" {p.get_width()}d", (p.get_width(), p.get_y() + p.get_height()/2), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig("dashboard_breakdown.png", dpi=300)
plt.close()

conn.close()
print("✅ Done! 'dashboard_heatmap.png' and 'dashboard_breakdown.png' generated successfully.")
