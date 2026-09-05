# ⚡ RecoverOS: Autonomous Revenue Recovery & Decision System

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red.svg)](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)
[![Razorpay API](https://img.shields.io/badge/Razorpay-Test--Mode%20Verified-blue.svg)](https://razorpay.com/docs/)
[![Track](https://img.shields.io/badge/Razorpay%20Buildathon-Track%2003%3A%20AI%20Revenue%20Recovery-orange.svg)]()

> **Core Architectural Principle:** *"ML recommends; policy controls; execution records the outcome."*  
> RecoverOS is a decision engine that diagnoses why payments, subscriptions, or invoices fail, ranks candidate recovery actions by **Net Expected Value ($EV_{net}$)**, validates decisions against deterministic compliance and stopping rules, and records an append-only audit trail—with zero unconstrained LLM hallucinations.

---

## 📌 Problem Statement & Design Philosophy

Revenue loss in payment infrastructure rarely happens in a single step. It manifests through subtle degradations: issuer downtime, customer authorization drop-offs, mandate friction, and transient network errors. 

Naive retry mechanisms introduce critical risks:
* **Fee Burn:** Repeating retries against degraded bank switches wastes merchant capital.
* **Customer Fatigue:** Uncoordinated messaging across channels triggers churn and disputes.
* **Double Charges:** Concurrency collisions between automated retry workers and customer manual checkouts.

**RecoverOS rejects generic generative wrappers.** It relies on classical machine learning for structured tabular scoring, bounded by deterministic rule-based safety gates.

```text
[ Revenue Event: Synthetic Batch OR Real Razorpay Webhook ]
                           │
                           ▼
                 [ Diagnosis Engine ] 
           (Deterministic Root-Cause Mapping)
                           │
                           ▼
                 [ ML Action Scorer ] ──(Pipeline Failure)──► [ Fallback Policy ]
              (Isotonic Random Forest)                          (Safe Recovery)
                           │
                           ▼
                  [ Policy Engine ]
           ├──▶ [ STOP ] (Fatigue / Policy Tripwires)
           ├──▶ [ ESCALATE_TO_HUMAN ] (Fraud / High Value)
           └──▶ [ Approved Recovery Action ]
                           │
                           ▼
                 [ Idempotency Guard ]
             (Prevents Concurrency Collisions)
                           │
                           ▼
                 [ Recovery Executor ]
            (Razorpay API Gateway Actions)
                           │
                           ▼
                  [ Audit Logger ]
          (Append-Only Ledger with CSV Export)
📊 Benchmark Results (100 Unseen Held-Out Events)Evaluated against an independent held-out evaluation batch (100 unseen events) to verify real financial impact:  StrategyRecovered RevenueRevenue Recovery Rate (%)Success Rate (%)Architectural BehaviorBaseline (Static Rules)₹2,348,795.26  52.85%  55.00%  Immediate retries, static reminders  RecoverOS (ML + Policy)₹2,582,254.15  58.10%  62.00%  +₹233,458.89 (+9.94%) Net Revenue Lift  Deterministic Stopping Interventions: 15 actions safely blocked by policy gates.  Targeted Escalations: 6 high-value, complex cases routed directly to human support.  Transparency Note: An earlier experimental heuristic strategy ("Intelligent V1") underperformed the baseline during initial runs and was pulled from evaluation pending deeper feature re-engineering.  💡 Architecture & Component Breakdown1. The Core StackFrontend: Streamlit interactive multi-tab dashboard (Action Recommendation, Execution, Live Analytics, Audit Ledger, Batch Runner).Backend: Modular Python runtime orchestrated by a unified RecoveryWorkflow pipeline.Durability Layer: Streamlit session state accompanied by an immutable, append-only CSV audit ledger (data/audit_log.csv).  2. The Decision LayerML Action Scorer: A multi-class Random Forest model (scikit-learn) predicting probability of success across six candidate actions: RETRY_NOW, RETRY_LATER, SEND_REMINDER, OFFER_INCENTIVE[cite: 1], ESCALATE_TO_HUMAN[cite: 1], and SUGGEST_ALTERNATIVE_PAYMENT[cite: 1].  Economic Objective Function: Actions are ranked strictly by Net Expected Value ($EV_{net}$), preventing margin erosion from expensive interventions[cite: 1]:
$$EV_{net} = (P(\text{success}) \times \text{Revenue at Risk}) - \text{Action Cost}$$Deterministic Diagnosis: A rule-based root-cause taxonomy standardizes raw failure codes (insufficient funds, 3DS timeouts, mandate dropouts) with confidence indicators[cite: 1].Circuit Breaker Fallback: If ML scoring throws an exception or experiences service degradation, FallbackPolicy automatically assumes control, selecting safe, bounded fallback actions (fallback_used = True)[cite: 1].3. The Razorpay IntegrationOrders API: Generates native test-mode payment transactions.HMAC Signature Verification: Verifies inbound payment.failed and payment.captured webhooks using RAZORPAY_WEBHOOK_SECRET.Zero Disconnect: Live webhook events flow directly into the exact same RecoveryWorkflow engine powering simulated batches.Test Instrument Validation: Thoroughly tested using documented test instruments (failure@razorpay, success@razorpay, and declining test card profiles).🛡️ Policy Controls & Safety GuardrailsRetry Fatigue Cap: Hard stopping rule enforcing a maximum attempt ceiling per transaction.Customer Contact Safeguard: Rate-limits communication frequency to eliminate user spam.Fraud Isolation: Suspicious or fraud-flagged events are strictly excluded from automated retries and routed to compliance review.Dispute & Incentive Ceilings: Discounts and high-value invoices exceed autonomous thresholds and mandate human authorization.Idempotency Guard: Protects against race conditions between automated retries and manual customer payments.📂 Project StructurePlaintextrecoveros/
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
│   ├── ml_action_scorer.py            # Expected Net Value ranker[cite: 1]
│   ├── policy_engine.py               # Compliance rules & stopping tripwires
│   ├── fallback_policy.py             # Circuit breaker failure handlers[cite: 1]
│   ├── idempotency_guard.py           # Duplicate execution prevention
│   ├── recovery_executor.py           # Action execution module[cite: 1]
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
    └── test_recovery_workflow.py      # End-to-end integration tests
🚀 Quickstart & Local Setup1. Installation & EnvironmentBashgit clone [https://github.com/your-username/recoveros.git](https://github.com/your-username/recoveros.git)
cd recoveros
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Run the Verification SuiteBashpython -m unittest discover tests
3. Launch the DashboardBashstreamlit run app.py
4. Running the Razorpay Webhook ReceiverBashexport RAZORPAY_KEY_ID="rzp_test_..."
export RAZORPAY_KEY_SECRET="..."
export RAZORPAY_WEBHOOK_SECRET="..."

python integrations/webhook_server.py
Expose port 5000 using ngrok http 5000, register the URL in the Razorpay Dashboard under Webhooks (payment.failed, payment.captured), and trigger failures via test instruments.🔍 Upfront Engineering DisclosuresState Persistence: Audit state currently writes to session memory and append-only CSV files[cite: 1]. Production deployment requires migrating this interface to an external transactional database (e.g., PostgreSQL with row-level locks).Model Regularization: Model ROC-AUC is currently ~0.66[cite: 1]. Further expansion of training feature sets and hyperparameter optimization will follow
