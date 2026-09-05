# ⚡ RecoverOS: Autonomous Revenue Recovery & Decision System

<div align="center">

[![Live Demo](https://img.shields.io/badge/⚡_Live_Prototype-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)

[![Razorpay Buildathon](https://img.shields.io/badge/Razorpay_Buildathon-Track_03:_AI_Revenue_Recovery-0C2340?style=for-the-badge&logo=razorpay&logoColor=3395FF)](https://razorpay.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

### 🚀 **[Click Here to Launch the Live Interactive Dashboard](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)**

</div>

> **Core Architectural Principle:** *"ML recommends; policy controls; execution records the outcome."*  
> RecoverOS is an AI-driven revenue recovery decision engine that diagnoses why transactions fail, ranks candidate recovery interventions by **Net Expected Value ($EV_{net}$)**, enforces deterministic compliance and stopping guardrails, executes bounded actions with 2-phase idempotency locks, and maintains an append-only audit trail—with zero unconstrained LLM hallucinations.

---

## 📌 Problem Statement & Design Philosophy

Payment failures rarely happen in one clean step. Revenue leaks through 3DS authentication timeouts, issuer switch degradation, low account balances during mandate runs, and user drop-offs.

Traditional recovery approaches rely on naive immediate retries, causing:
* **Fee Burn:** Retrying against down issuer switches burns processing fees and damages merchant standing.
* **Customer Fatigue:** Uncontrolled messaging cascades across SMS/WhatsApp trigger churn and disputes.
* **Double-Debits:** Concurrency collisions between background retries and manual customer checkout attempts.

**RecoverOS rejects generic LLM wrapper patterns.** Structured tabular recovery decisions demand classical, calibrated machine learning bounded by deterministic finite-state machine (FSM) safeguards.

---

## 💡 The Solution We Built: RecoverOS

To solve these failure modes, RecoverOS implements a production-grade resilience layer separating prediction from authorization:

```text
[ Revenue Event: Synthetic Batch OR Real Razorpay Webhook ]
                           │
                           ▼
                 [ Diagnosis Engine ] 
           (Deterministic Root-Cause Mapping)
                           │
                           ▼
                 [ ML Action Scorer ] ──(Pipeline Error)──► [ Fallback Policy ][cite: 1]
         (Isotonic Calibrated Random Forest)                   (Deterministic Safety)
                           │
                           ▼
                  [ Policy Engine ] ◄─── [ Downtime Registry ]
           ├──▶ [ STOP ] (DOWNTIME_VETO / Fatigue Tripwires)
           ├──▶ [ ESCALATE_TO_HUMAN ] (Fraud / High Margin)
           └──▶ [ Approved Recovery Action ]
                           │
                           ▼
              [ Idempotency & Lock Guard ]
         (SET NX Lease + Deterministic Key Hash)
                           │
                           ▼
             [ 2-Phase Recovery Executor ]
            (Razorpay API Gateway Actions)
                           │
        ┌──────────────────┴──────────────────┐
        ▼                                     ▼
[ Immutable Audit Logger ]        [ Reconciliation Worker ]
(audit_log.csv Append-Only)   (45s Late Webhook & Orphan Cleaner)


Core Components of the Solution:

Probability Calibration & Regularized EV Scorer (ml_action_scorer.py):

Eliminates Random Forest score clustering (0.40–0.60) via CalibratedClassifierCV using Isotonic Regression (Brier loss: 0.2089).

Optimizes Net Expected Value with risk multipliers ($\lambda_{risk}$):

$$EV_{net} = (P_{calibrated} \times \text{Amount at Risk}) - (\text{Cost} \times \lambda_{risk})$$

Enforces $\lambda_{risk} = 1.5$ for human escalations and $\lambda_{risk} = 1.1$ for retries to penalize operational overhead and retry fatigue.

Infrastructure Downtime Veto Gate (****fallback_policy.py & policy_engine.py****):

Uses a thread-safe DowntimeRegistry singleton listening to bank degradation webhooks (payment.downtime.started).

If a route is down (e.g., HDFC UPI), the policy immediately vetoes the attempt (p_success = 0.0, status = DOWNTIME_VETO, action = STOP), preventing fee burn.

Atomic 2-Phase Executor & Idempotency Guard (recovery_executor.py):

Implements a distributed lock lease (SET NX with 30s TTL) and deterministic key generation:

X-Razorpay-Idempotency-Key: rec_{event_id}_att_{attempt_count}

Eliminates race conditions between automated retries and manual customer checkout.

Reconciliation Worker & Late-Webhook Handler (reconciliation_worker.py):

Reconciles late payment.captured webhooks (the 45-second bank lag) to RECOVERED_LATE_CAPTURE and auto-cancels active recovery payment links to prevent double debits.

Scans for stranded IN_PROGRESS transactions and polls gateway status to self-heal.

📊 Benchmark Results (100 Unseen Held-Out Events)

Evaluated against an independent held-out evaluation batch of 100 unseen payment failure events:

Strategy

Recovered Capital

Recovery Rate (%)

Success Rate (%)

Operational Profile

Baseline (Static Rules)









₹2,348,795.26



52.85%



55.00%



Naive retries & static nudges

RecoverOS (Calibrated ML + Policy)



₹2,582,254.15



58.10%



62.00%



+₹233,458.89 (+9.94%) Net Lift

Calibration Quality: Isotonic regression dropped Brier Score Loss to 0.2089 (ROC-AUC ~0.66).

Policy Stops: 15 unsafe or degrading actions halted before hitting the gateway.

High-Touch Escalations: 6 high-value accounts routed to human support based on positive expected net yield.

V1 Strategy Disclosure: An early experimental heuristic variant ("Intelligent V1") underperformed the baseline (34.53% recovery rate) and was removed pending deeper feature re-engineering[cite: 1].

💡 Architecture & Component Breakdown

1. The Core Stack

Frontend: Streamlit multi-tab analytics terminal[cite: 1] (Real-time Recommendation, Execution, Benchmark Analytics, Audit Ledger, Batch Simulator).

Backend: Python runtime structured as a modular engine[cite: 1] orchestrated via RecoveryWorkflow.

State & Durability: In-memory runtime session state backed by append-only ledger tracking (data/audit_log.csv)[cite: 1].

2. The Decision Layer

ML Action Scorer: Multi-class Random Forest model (scikit-learn)[cite: 1] scoring candidate actions: RETRY_NOW[cite: 1], RETRY_LATER[cite: 1], SEND_REMINDER[cite: 1], OFFER_INCENTIVE[cite: 1], ESCALATE_TO_HUMAN[cite: 1], and SUGGEST_ALTERNATIVE_PAYMENT[cite: 1].

Deterministic Root-Cause Diagnosis: Normalizes error payloads (insufficient funds, 3DS timeouts, mandate dropouts) into standardized failure taxonomies[cite: 1].

Circuit-Breaker Fallback: If inference errors occur, FallbackPolicy assumes control to enforce safe, bounded behaviors without halting transactions (fallback_used = True)[cite: 1].

3. The Razorpay Gateway Integration

Orders API: Generates native test-mode payment transactions.

Webhook Ingestion: Ingests and HMAC-verifies payment.failed and payment.captured webhooks using RAZORPAY_WEBHOOK_SECRET.

Unified Pipeline: Live incoming webhooks execute through the same RecoveryWorkflow used by batch simulations.

Header Contract: Outbound calls transmit a deterministic idempotency header:

HTTP

X-Razorpay-Idempotency-Key: rec_{event_id}_att_{attempt_count}


Test Instrument Validation: Validated against Razorpay test suites (failure@razorpay, success@razorpay, and card decline profiles).

🛡️ Policy Controls & Safety Guardrails

Retry Fatigue Cap: Absolute upper boundary on retry frequency per transaction lifecycle.

Contact Cadence Guard: Rate limits messaging frequency across customer channels to eliminate notification spam.

Fraud Isolation: High-risk or fraud-flagged transactions bypass auto-retry entirely and route to compliance review.

Dispute & Margin Safeguards: High-value concessions and discounts require explicit human approval thresholds.

Idempotency Guard: Leases state to block collisions between background retries and manual checkouts.

📂 Project Structure

Plaintext

recoveros/
├── app.py                             # Interactive Streamlit dashboard[cite: 1]
├── requirements.txt                   # Environment dependencies
├── data/
│   ├── revenue_events.csv             # Simulated event baseline[cite: 1]
│   ├── evaluation_events.csv          # Held-out benchmark dataset[cite: 1]
│   └── audit_log.csv                  # Immutable decision ledger[cite: 1]
├── models/
│   └── recovery_action_model.joblib   # Persisted ML scoring pipeline[cite: 1]
├── simulator/
│   ├── diagnosis_engine.py            # Deterministic root-cause mapping
│   ├── ml_action_scorer.py            # Expected Net Value ranker with lambda penalties[cite: 1]
│   ├── policy_engine.py               # Compliance rules & DOWNTIME_VETO gate
│   ├── fallback_policy.py             # Circuit breakers & DowntimeRegistry[cite: 1]
│   ├── idempotency_guard.py           # Duplicate execution prevention
│   ├── recovery_executor.py           # 2-Phase atomic executor & distributed locks[cite: 1]
│   ├── reconciliation_worker.py       # Late webhook handler (45s lag) & orphan cleaner
│   ├── recovery_workflow.py           # Unified pipeline orchestrator
│   ├── batch_simulator.py             # Configurable batch runner
│   └── audit_logger.py                # Append-only audit logger[cite: 1]
├── integrations/
│   ├── razorpay_connector.py          # Native API client
│   └── webhook_server.py              # HMAC-verified webhook listener
└── tests/
    ├── test_diagnosis_engine.py       # Taxonomy mapping unit tests
    ├── test_environment.py            # Execution simulation tests
    ├── test_ml_scorer.py              # EV_net calculation tests[cite: 1]
    ├── test_ml_fallback.py            # Failure circuit-breaker tests[cite: 1]
    ├── test_calibrated_scorer.py      # Isotonic calibration tests
    ├── test_downtime_veto.py          # Bank downtime interception tests
    ├── test_atomic_executor.py        # Lock & idempotency tests
    └── test_recovery_workflow.py      # End-to-end integration tests


🚀 Quickstart & Local Setup

1. Clone & Set Up Virtual Environment

Bash

git clone [https://github.com/your-username/recoveros.git](https://github.com/your-username/recoveros.git)
cd recoveros
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


2. Run Test Suite (12 Tests Passed)

Bash

python -m unittest discover tests


3. Launch Dashboard

Bash

streamlit run app.py


4. Run Webhook Server

Bash

export RAZORPAY_KEY_ID="rzp_test_..."
export RAZORPAY_KEY_SECRET="..."
export RAZORPAY_WEBHOOK_SECRET="..."

python integrations/webhook_server.py


Expose via ngrok http 5000 and map the URL inside the Razorpay Dashboard under Webhooks.

🔍 Upfront Engineering Disclosures

Persistence Layer: Audit history is maintained in session state with append-only CSV persistence (data/audit_log.csv)[cite: 1]. Production deployment requires migration to a relational store with row-level locks (e.g., PostgreSQL).

Model Optimization: Current pipeline achieves ROC-AUC ~0.66 with Isotonic Brier Score calibration at 0.2089[cite: 1]. Future iterations will incorporate expanded feature engineering and automated hyperparameter sweeps.
