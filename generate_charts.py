import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean, professional visual style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 14})

# Connect to database
conn = sqlite3.connect("banking_ops.db")

# --- CHART 1: REGIONAL STP RATES BAR CHART ---
print("Generating Regional STP Rate chart...")
q_regional = """
SELECT region, 
       ROUND(CAST(SUM(CASE WHEN stp_indicator = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS stp_rate
FROM transactions
GROUP BY region
ORDER BY stp_rate DESC;
"""
df_regional = pd.read_sql_query(q_regional, conn)

plt.figure(figsize=(8, 5))
ax1 = sns.barplot(x="region", y="stp_rate", data=df_regional, palette="Blues_r")

for p in ax1.patches:
    ax1.annotate(f"{p.get_height():.2f}%", 
                 (p.get_x() + p.get_width() / 2., p.get_height() - 8), 
                 ha='center', va='center', color='white', fontweight='bold')

plt.title("APAC Regional Straight-Through Processing (STP) Rates", pad=15, fontweight='bold')
plt.xlabel("Operational Region Hub")
plt.ylabel("STP Rate (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig("regional_stp_rates.png", dpi=300)
plt.close()


# --- CHART 2: CHANNEL FAILURE PARETO CHART ---
print("Generating Channel Failure Rate chart...")
q_channel = """
SELECT channel,
       ROUND(CAST(SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS failure_rate
FROM transactions
GROUP BY channel
ORDER BY failure_rate DESC;
"""
df_channel = pd.read_sql_query(q_channel, conn)

plt.figure(figsize=(9, 5))
ax2 = sns.barplot(x="failure_rate", y="channel", data=df_channel, palette="Oranges_r")

for p in ax2.patches:
    ax2.annotate(f" {p.get_width():.2f}%", 
                 (p.get_width() + 0.2, p.get_y() + p.get_height() / 2.), 
                 va='center', fontweight='bold')

plt.title("Processing Channel Vulnerability & Failure Rates", pad=15, fontweight='bold')
plt.xlabel("Failure Rate (%)")
plt.ylabel("Ingestion Channel")
plt.xlim(0, max(df_channel['failure_rate']) + 3)
plt.tight_layout()
plt.savefig("channel_failures.png", dpi=300)
plt.close()

conn.close()
print("✅ Done! 'regional_stp_rates.png' and 'channel_failures.png' created successfully.")

