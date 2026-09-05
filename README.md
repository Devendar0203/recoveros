# ⚡ RecoverOS: Autonomous Revenue Recovery & Decision Engine

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-red.svg)](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-12%20Passing-brightgreen.svg)]()
[![Track](https://img.shields.io/badge/Razorpay%20Buildathon-Track%2003%3A%20AI%20Revenue%20Recovery-orange.svg)]()

> **"ML recommends; policy controls; execution records the outcome."**  
> A production-hardened revenue recovery system designed to diagnose payment failures, optimize Net Expected Value ($EV_{net}$) via calibrated ML, enforce deterministic policy guardrails, and execute bounded actions with distributed idempotency locks.

---

## 📌 Executive Summary & Problem Taste

Revenue leakage in modern digital payments is rarely a one-step failure. It manifests through subtle degradations: 3DS authentication drop-offs, transient network drops, low account balances during mandate runs, and bank switch outages.

Most recovery mechanisms fail in production by applying naive heuristics (e.g., *"retry immediately"*), leading to:
1. **Fee Burn:** Repeating retries against down issuer switches eats merchant margins.
2. **Double-Debits:** Concurrency collisions between automated retries and manual customer checkouts.
3. **Ghost Recoveries:** Misinterpreting delayed captures (the 45-second bank lag) as drop-offs.

**RecoverOS** frames revenue recovery as an exact economic optimization problem bounded by deterministic state machine safety.

---

## 📊 Benchmark Results (100 Unseen Held-Out Events)

Evaluated strictly on held-out test events to measure real financial uplift:

| Recovery Strategy | Total Recovered | Recovery Rate (%) | Success Rate (%) | Operational Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline (Static Retries/Reminders)** | ₹2,348,795.26 | 52.85%[cite: 1] | 55.00%[cite: 1] | Burns retry counts blindly[cite: 1] |
| **RecoverOS (Calibrated ML + Policy Gate)** | **₹2,560,470.85** | **57.61%** | **60.00%** | **+₹211,675.59 Net Uplift (+9.01%)** |

* **Policy-Enforced Safety Stops:** 15 unsafe actions blocked (preventing fee burn & user spam)[cite: 1].
* **High-Touch Human Escalations:** 6 cases escalated only when justified by high-margin $EV_{net}$[cite: 1].
* **Brier Calibration Loss:** Reduced to `0.2089` (resolving Random Forest score clustering).

---

## 🏗️ System Architecture

```text
[ Incoming Payment Failure / Webhook ]
                  │
                  ▼
       [ Event Diagnosis Engine ]
                  │
                  ▼
       [ Calibrated ML Scorer ]
   (Isotonic Regression | Brier: 0.2089)
                  │
                  ▼
    [ Net Expected Value Formulation ]
  EV_net = (P_calibrated × Amount) - (Cost × λ_risk)
                  │
                  ▼
     [ Deterministic Policy Gate ] ◄─── [ Downtime Registry ]
    - Attempt Caps & Cool-downs           (Forces P=0 on Bank Outage)
    - Margin Tripwires
                  │
                  ▼
   [ 2-Phase Atomic State Executor ]
   - Distributed Lock (SET NX with TTL)
   - Deterministic Idempotency Key: rec_{id}_att_{n}
                  │
                  ▼
    [ Razorpay Gateway API Engine ]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
[ Immutable Audit Trail ]  [ Reconciliation Worker ]
(audit_log.csv)            (Late Webhook & Orphan Cleaner)
