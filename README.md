# APAC Banking Operations Intelligence Hub
**Candidate Portfolio Asset** | Target Role: Digital Transformation Business Analyst (OCBC Alignment)  
**Author:** Chelsea Pang Kiat Si

---

## 1. Executive Summary & Operational Problem Statement
This repository hosts a self-contained operational intelligence pipeline designed to simulate, analyze, and optimize core cross-border payment processing across major APAC hubs (**Singapore, Malaysia, Thailand, and Indonesia**). 

### The Core Automation Gap
Our regional payment infrastructure is currently tracking an overall transaction failure rate of **11.1%** (221 failed transactions out of a 2,000 baseline volume). While consumer-facing digital ingestion channels operate cleanly with an aggregate **90.1% Straight-Through Processing (STP) rate**, legacy system friction and file format mismatches across our corporate gateways push **18.1% of all failures directly into prolonged Pending Escalation queues**. 

This operational bottleneck traps significant transactional liquidity and forces high manual exception handling overhead. This project isolates the systemic root causes of these process dropouts and establishes a clear data-driven roadmap to recover lost efficiency.

---

## 2. Core Repository Architecture & Technical Stack
The asset utilizes a modular data architecture to demonstrate data engineering fluency, relational database logic, and executive-ready reporting structures:

* **`generate_data.py`**: A Python simulation engine using the `Faker` library to synthesize a 2,000-transaction relational ledger complete with unique alpha-numeric tracking IDs, processing channels, geographic metadata, and targeted system dropouts.
* **`sql.py`**: An analytics data suite executing advanced relational queries (conditional aggregations, volumetric market shares, failure rates) against an underlying SQLite asset (`banking_ops.db`).
* **`APAC_Banking_Ops_Analysis.ipynb`**: An interactive, fully executed Jupyter Notebook that pairs our analytical data scripts and automated visual plots side-by-side with professional business narratives.

---

## 3. Key Analytical Insights & Executive Breakdown (Analyst-Grade)

### 📊 Macro Operational Health Baseline
Our pipeline captures an overall failure rate of **11.1%** (221 failures). While digital channels handle volume with high efficiency (**9.9% failure rate or lower**), traditional networks introduce significant manual friction, causing an operational tail where **18.1% of all processing faults sit stalled in escalated states**.

---

### 🔍 Deep-Dive Diagnostic Pillars

#### A. FAIL_005 (FX Rate Expiry) Concentrated in High-Value Tiers
* **The Trend:** `FAIL_005` represents our single largest operational leak, driving **81 individual failures** (accounting for 37% of the total exception pool). 
* **The Risk:** Crucially, **87% of these failures** sit squarely within our top-25% highest transaction value band (exceeding SGD 114,000). This is not a low-impact volume glitch; it represents a major friction point concentrated inside our highest-value enterprise and premier client accounts.
* **The Root Cause:** High-value transactions require longer multi-tier internal compliance checks, causing the underlying currency FX rate cards to time out and expire before final trade execution.

#### B. The SWIFT Corporate Ingestion Bottleneck
* **The Trend:** The **SWIFT/Corporate Gateway** exhibits an alarming **18.1% failure rate**—which is **2.3x higher** than our consumer-facing Mobile App average (8.6%). 
* **The Intersection:** When mapped across product categories via our dimensional heatmap, SWIFT failures are heavily concentrated within **Current Account Savings Accounts (CASA) at 26.7%** and **Foreign Exchange (FX) at 24.1%**. 
* **The Takeaway:** This indicates systematic data field mismatch and validation leakage occurring during automated bulk B2B file transmissions from corporate clients.

#### C. Regional Infrastructure Maturity Gaps
* **The Trend:** **Indonesia (15.5%)** and **Thailand (14.2%)** suffer from processing failure rates nearly **double** that of **Singapore (7.8%)**, despite handling lower overall relative transaction volumes.
* **The Context:** This structural performance gap persists uniformly across all banking product lines (CASA, FX, Loans, Payments), identifying a fundamental infrastructure maturity gap in regional processing networks rather than an isolated product issue.

#### D. Liquidity Trapped in Pending Escalations
* **The Trend:** Transactions currently caught in **Pending Escalation** hold a massive average value of **SGD 139,313**, compared to an average value of **SGD 82,683** for cases cleanly resolved at the operational desk.
* **The Consequence:** The operational bottlenecks are disproportionately delaying our most critical corporate accounts, creating compounding relationship risk at the exact moment they are most exposed.

#### E. Stagnant Month-Over-Month Performance Trends
* **The Trend:** Historical trend evaluation across Jan–May 2026 shows a completely flat failure ceiling, fluctuating narrowly between **10.2% and 11.9%**.
* **The Takeaway:** The complete absence of a downward trend proves that current business-as-usual operations are failing to drive structural improvements, confirming that the current systems have reached their maximum capacity and require direct automation intervention.

---

## 4. Visualized Operational Performance

## 4. Visualized Operational Performance

### A. Failure Rate Heatmap (Channel × Product Line Matrix)
The visualization maps where critical process handshakes break down. Data fields show a profound risk correlation inside our corporate lines, where **SWIFT transfers face a 26.7% failure rate within CASA products and 24.1% in FX processing**:

![Failure Rate Heatmap Matrix](dashboard_heatmap.png)

### B. Core Vulnerability Profile & Resolution Latency
This analysis isolates the raw volume of failures against the total business days required for operations desks to manually investigate and resolve them:

![Failure Profiles and Latencies](dashboard_breakdown.png)

*Detailed code parameters, execution blocks, and raw data frames can be reviewed directly inside the [Interactive Analytical Notebook](./APAC_Banking_Ops_Analysis.ipynb).*

---

## 5. Target Digital Transformation Roadmap

To bridge our automation deficit and recover operational cost leakage, this portfolio outlines three key data-driven solutions aligned with digital banking goals:

1. **Upstream Validation APIs on Corporate SWIFT Gateways:** Intercept bulk corporate B2B payment payloads and validate accounting field inputs *before* ingestion into the core banking ledger. This will eliminate structural file parsing errors on CASA and FX lines, compressing the 18.1% SWIFT failure rate down toward digital baselines.
2. **Real-Time Treasury Desk RPA Integration:** Deploy Robotic Process Automation or real-time API pricing buffers to automatically refresh or extend currency rate cards for transactions exceeding SGD 114,000. This directly neutralizes the impact of `FAIL_005` exceptions on our premier customer tiers.
3. **AI-Driven Compliance Triage for Risk Holds:** Introduce machine learning classifiers to flag and instantly clear historical false-positives within our sanction screening (`FAIL_002`) queues. This will alleviate manual investigative volume on the regional risk desk, accelerating resolution times for high-value trapped liquidity.
