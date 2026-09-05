# ⚡ RecoverOS: Autonomous Payment Recovery & Revenue Protection Engine

<div align="center">

[![Live Demo](https://img.shields.io/badge/⚡_Live_Dashboard-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Devendar0203/recoveros)
[![Razorpay Buildathon](https://img.shields.io/badge/Razorpay_Buildathon-Track_03:_AI_Revenue_Recovery-0C2340?style=for-the-badge&logo=razorpay&logoColor=3395FF)](https://razorpay.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

### 🚀 **[Click Here to Launch the Live Interactive Dashboard](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)**

</div>

---

## 📖 Overview

**RecoverOS** is an autonomous revenue recovery decision engine built for payment aggregators and subscription platforms. Instead of relying on naive, blind retry loops that burn merchant fees, RecoverOS uses **calibrated machine learning** bounded by a **deterministic policy engine** to evaluate payment failures, select the optimal recovery action based on **Net Expected Value ($EV_{net}$)**, and record an immutable audit ledger.

> **Core Architectural Principle:** *"ML recommends; policy controls; execution records the outcome."*

---

## 🔗 Demo & Links

| Resource | Access Point |
| :--- | :--- |
| **🚀 Live Dashboard** | [recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/) |
| **💻 Source Code** | [github.com/Devendar0203/recoveros](https://github.com/Devendar0203/recoveros) |
| **🎥 Pitch Video** | *Coming soon / Add pitch video link here* |
| **📄 Track Focus** | **Razorpay Buildathon — Track 03: AI Revenue Recovery** |

```
Payment Failure ──► Root Cause Diagnosis ──► ML Action Scoring ──► Expected Net Value ──► Policy & Safety Guardrails ──► Recovery Execution ──► Audit & Revenue Measurement
📌 The ProblemPayment failures do not necessarily mean permanently lost revenue. Transactions degrade and drop across complex banking rails for distinct reasons:  Customer Funds: Insufficient account balances during recurring mandate debits.  Switch Degradation: Core bank switch or issuer downtime causing 5xx dropouts[cite: 1].Authentication Drop-offs: 3DS timeouts and customer dropouts during 2FA challenges[cite: 1].Stale Instruments: Expired cards and revoked e-mandates[cite: 1].The Danger of Naive Retry LoopsMost recovery systems use brute-force retries:PlaintextPayment Failed ──► Immediate Retry ──► Immediate Retry Again ──► Churn / Failure
This causes severe operational damage:💸 Fee Burn: Repeating retries against down issuer switches burns transaction fees.😓 Customer Fatigue: Repetitive automated SMS/WhatsApp alerts trigger churn and chargebacks.⚠️ Double-Debits: Concurrency collisions between background retries and manual user checkouts.🎯 Poor Decision Quality: A static retry cannot fix an expired card or revoked mandate[cite: 1].💡 The RecoverOS SolutionRecoverOS models recovery as an economic decision problem governed by strict state boundaries[cite: 1]:Plaintext               PAYMENT EVENT
                     │
                     ▼
           ┌───────────────────┐
           │ Idempotency Guard │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │   Failure Reason  │
           │   Normalization   │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │    Root Cause     │
           │     Diagnosis     │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │  ML Action Scorer │ ──(ML Failure)──► [ Fallback Policy ][cite: 1]
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │    Expected Net   │
           │       Value       │
           └─────────┬─────────┘
                     │
                     ▼
           ┌───────────────────┐
           │   Policy Engine   │
           │   & Guardrails    │[cite: 1]
           └─────────┬─────────┘
                     │
            ┌────────┴────────┐
            │ ALLOW           │ BLOCK
            ▼                 ▼
     ┌─────────────┐   [ STOP / ESCALATE_TO_HUMAN ][cite: 1]
     │  Executor   │
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │  Audit Log  │[cite: 1]
     └──────┬──────┘
            │
            ▼
   REVENUE RECOVERED[cite: 1]

       
🧠 How It Works1. Root Cause DiagnosisConverts raw payment error payloads into structured, explainable root causes with associated confidence metrics:  PlaintextRaw Failure: insufficient_funds
  └──► Root Cause: INSUFFICIENT_FUNDS
  └──► Category: CUSTOMER_FUNDS
  └──► Confidence: 96%
  └──► Candidate Actions: RETRY_LATER, SUGGEST_ALTERNATIVE_PAYMENT


Failure CategoryExample Root CauseOptimal Action StrategyCustomer FundsInsufficient balance at mandate runRETRY_LATER (Align with pay cycle)Temporary TechnicalGateway/3DS auth timeoutRETRY_NOW (Dynamic exponential backoff)Payment MethodExpired card / canceled mandateSUGGEST_ALTERNATIVE_PAYMENTAuthenticationCustomer dropped out during 2FASEND_REMINDER (Direct recovery link)Gateway / IssuerCore banking switch degradationRETRY_LATER / Wait for downtime clearanceUnknown / High RiskUnmapped failure code / fraud flagESCALATE_TO_HUMAN  2. Machine Learning Action ScoringA calibrated multi-class Random Forest model predicts the historical success probability $P(\text{success})$ for every candidate intervention:  SUGGEST_ALTERNATIVE_PAYMENT: 62.16%  RETRY_LATER: 57.40%  SEND_REMINDER: 52.02%  RETRY_NOW: 50.14%  OFFER_INCENTIVE: 52.46%  ESCALATE_TO_HUMAN: 60.46%  3. Net Expected Value OptimizationRecoverOS selects actions by maximizing economic yield rather than raw probability:
  $$\text{Gross EV} = P(\text{success}) \times \text{Amount at Risk}$$  $$\text{Net EV} = \text{Gross EV} - \text{Action Cost}$$  PlaintextAction: SUGGEST_ALTERNATIVE_PAYMENT
### 🎯 Candidate Action Scoring & Cost Matrix

## 🎯 Candidate Action Scoring & Cost Matrix

## 🎯 Candidate Action Scoring & Cost Matrix
```
| Candidate Recovery Action | Historical Success P(Success) | Typical Cost | Operational Focus |
| :--- | :--- | :--- | :--- |
| **`SUGGEST_ALTERNATIVE_PAYMENT`** | 62.16% | ₹8.00 | Contextual switch prompts (UPI, Cards, Netbanking) |
| **`ESCALATE_TO_HUMAN`** | 60.46% | ₹1,500.00 | High-touch operations desk for enterprise accounts |
| **`RETRY_LATER`** | 57.40% | ₹10.00 | Dynamic backoff / salary cycle synchronization |
| **`OFFER_INCENTIVE`** | 52.46% | ₹500.00 | Margin-deducted concession for cart abandonment |
| **`SEND_REMINDER`** | 52.02% | ₹3.00 | Low-cost automated SMS/WhatsApp payment link |
| **`RETRY_NOW`** | 50.14% | ₹5.00 | Immediate gateway retry on network glitch |

---

## 📈 Machine Learning Evaluation Metrics

| Metric | Score | Evaluation Context |
| :--- | :--- | :--- |
| **🎯 Model Accuracy** | 65.00% | Multiclass classification across discrete recovery actions |
| **🔍 Model Precision** | 75.84% | Precision across approved positive recovery decisions |
| **📡 Model Recall** | 70.19% | Identification rate of recoverable failed events |
| **📉 ROC-AUC** | ~65.83% | Baseline discrimination capacity on unseen test splits |
| **⚖️ Brier Score Loss** | 0.2089 | Calibration quality index via Isotonic Regression |
```

ActionCost ProfileEconomic PurposeRETRY_NOW  ₹5.00  Immediate API retry on transient network dropsRETRY_LATER  ₹10.00  Scheduled backoff retry for fund recoverySEND_REMINDER  ₹3.00  Automated low-cost SMS/WhatsApp payment link dispatchSUGGEST_ALTERNATIVE_PAYMENT  ₹8.00  Contextual switch prompt (UPI / Netbanking / Card)OFFER_INCENTIVE  ₹500.00  Margin-deducted concession for high-LTV cart recoveryESCALATE_TO_HUMAN  ₹1,500.00  High-touch operations desk for enterprise accounts  4. Policy Engine & Safety GuardrailsML models provide recommendations; the policy engine enforces deterministic constraints:  Retry Caps: Hard boundary blocking retries beyond maximum attempt limits.  Contact Limits: Frequency ceilings preventing notification fatigue across customer channels.  Dispute & Fraud Isolation: High-risk transactions skip automation and route directly to compliance desks.  Margin Validation: Expensive interventions (OFFER_INCENTIVE, ESCALATE_TO_HUMAN) are blocked unless the transaction value supports the overhead.  5. Idempotency & Distributed Execution SafetyDuplicate webhooks or concurrent checkout attempts are intercepted using deterministic execution hashes (rec_{event_id}_att_{attempt_count}) and state lease locking, preventing race conditions and double charges.6. Deterministic Execution EnvironmentEvery run pairs seeded simulation behavior with isolated execution tracking, ensuring benchmarks are reproducible across identical failure parameters.  7. ML Circuit-Breaker FallbackIf model inference throws exceptions, timeouts, or data corruption errors, the system engages FallbackPolicy. The transaction is safely routed to bounded deterministic rules (fallback_used = True) rather than failing open.  8. End-to-End AuditabilityEvery decision—from diagnostic classification to ML probability rankings, policy approvals, and API response states—is committed to an immutable append-only ledger (data/audit_log.csv).  📊 Benchmark Results — 100 Unseen EventsEvaluated on an independent, held-out evaluation batch of 100 unseen payment failure events:  StrategyTotal Revenue RecoveredRevenue Recovery Rate (%)Event Success Rate (%)Operational NotesBaseline (Static Rules)₹2,348,795.26  52.85%  55.00%  Blind retries & static notifications  RecoverOS (ML + Policy)₹2,582,254.15  58.10%  62.00%  Calibrated EV optimization  Business & Operational ImpactIncremental Revenue Recovered: +₹233,458.89 net capital preserved.  Relative Revenue Uplift: +9.94% improvement over static approaches.  Policy Stops Enforced: 15 unsafe attempts halted (saving merchant fees and stopping user spam).  Human Escalations: 6 accounts routed to high-touch workflows based on positive unit economics.  ML Model Performance (Scoring Layer Only)Accuracy: 65.00%  Precision: 75.84%  Recall: 70.19%  ROC-AUC: ~0.6583  🏗️ Technology StackCore Execution: Python 3.11, Pandas, NumPy, Scikit-learn, Joblib, Streamlit.  Machine Learning Pipeline: Multi-class Random Forest with probability calibration, stratified preprocessing, and expected net value optimization.  Decision Framework: Root-cause diagnosis taxonomy, ML action ranking, deterministic policy engine, fallback circuit breakers, idempotency locks, and audit logging.  Dashboard: Streamlit dark-mode analytics terminal covering live event drilldown, held-out batch testing, and ledger exports.  💳 Razorpay Gateway ArchitecturePlaintextRazorpay Gateway Event ──► Webhook Validation ──► Idempotency Guard ──► Failure Normalization ──► Root Cause Diagnosis ──► ML Action Scoring ──► Expected Net Value ──► Policy Gate ──► Bounded Execution ──► Immutable Audit Trail
Test-Mode API Integration: Interacts with Razorpay Orders and Payment Links endpoints.Webhook Authentication: Inbound events are validated using HMAC-SHA256 signature verification (RAZORPAY_WEBHOOK_SECRET).Test Instrument Validation: Validated against Razorpay test suites (failure@razorpay, success@razorpay, and card decline profiles).📂 Project StructurePlaintextrecoveros/
├── app.py                             # Interactive Streamlit dashboard
├── requirements.txt                   # Project runtime dependencies
├── data/
│   ├── revenue_events.csv             # 500 baseline transaction events
│   ├── training_events.csv            # 400 training split events
│   ├── evaluation_events.csv          # 100 held-out evaluation events
│   └── audit_log.csv                  # Immutable execution decision ledger
├── models/
│   └── recovery_action_model.joblib   # Serialized ML scoring pipeline
├── simulator/
│   ├── diagnosis_engine.py            # Rule-based root-cause normalizer
│   ├── ml_action_scorer.py            # Expected Net Value ranker[cite: 1]
│   ├── policy_engine.py               # Deterministic compliance & stopping rules[cite: 1]
│   ├── fallback_policy.py             # Circuit-breaker fallback handler[cite: 1]
│   ├── idempotency_guard.py           # Concurrency & lock management
│   ├── recovery_executor.py           # Action execution module[cite: 1]
│   ├── recovery_workflow.py           # Unified orchestrator class
│   ├── batch_simulator.py             # Configurable batch runner
│   └── audit_logger.py                # Append-only audit logger[cite: 1]
├── integrations/
│   ├── razorpay_connector.py          # Razorpay API client
│   └── webhook_server.py              # HMAC webhook listener service
└── tests/
    ├── test_diagnosis_engine.py       # Taxonomy validation tests
    ├── test_environment.py            # Deterministic simulation tests[cite: 1]
    ├── test_ml_scorer.py              # EV calculation tests[cite: 1]
    ├── test_ml_fallback.py            # Safety fallback unit tests[cite: 1]
    └── test_recovery_workflow.py      # End-to-end integration tests
🚀 Quickstart & Reproduction1. Clone & Set Up Virtual EnvironmentBashgit clone [https://github.com/Devendar0203/recoveros.git](https://github.com/Devendar0203/recoveros.git)
cd recoveros

python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
2. Retrain the Scoring PipelineBashpython simulator/train_ml_model.py
3. Run the Complete Verification SuiteBashpython -m unittest discover tests
4. Launch the Interactive DashboardBashstreamlit run app.py
Access the local interface at http://localhost:8501 or use the hosted Live Dashboard.5. Webhook Server Configuration (Optional for Live Gateway)Bashexport RAZORPAY_KEY_ID="rzp_test_..."
export RAZORPAY_KEY_SECRET="..."
export RAZORPAY_WEBHOOK_SECRET="..."

python integrations/webhook_server.py
Forward port 5000 via ngrok http 5000, configure the webhook URL in the Razorpay Dashboard, and fire test payments.---

## ⚙️ Production Design Principles

* **Separation of Concerns:** Diagnosis $\neq$ Prediction $\neq$ Policy $\neq$ Execution[cite: 1]. Prediction never dictates execution directly[cite: 1].
* **Fail-Safe by Default:** Any ML pipeline failure routes immediately to deterministic fallback policies[cite: 1]. The system never fails open[cite: 1].
* **Idempotency Guarantee:** Cryptographic attempt identifiers prevent duplicate debits from concurrent runs or webhook retries.
* **Unit Economic Alignment:** Actions optimize for net recovered capital after operational costs and margin friction[cite: 1].

---

## 🚦 System Status & Roadmap

| Layer | Component | Status | Notes |
| :--- | :--- | :---: | :--- |
| **Ingestion** | Failure Normalization & Root Cause | 🟢 Ready | Deterministic diagnostic taxonomy |
| **Intelligence** | Calibrated ML Action Scoring ($EV_{net}$) | 🟢 Ready[cite: 1] | Random Forest + Isotonic Calibration[cite: 1] |
| **Governance** | Policy Engine & Safety Guardrails | 🟢 Ready[cite: 1] | Contact caps & retry limit tripwires[cite: 1] |
| **Resilience** | Fallback Circuit Breaker | 🟢 Ready[cite: 1] | Automatic fail-safe policy handoff[cite: 1] |
| **Concurrency** | Idempotency & State Locking | 🟢 Ready | Deterministic key collision guard |
| **Observability** | Append-Only Audit Trail | 🟢 Ready[cite: 1] | Full trace logging (`audit_log.csv`)[cite: 1] |
| **Interface** | Streamlit Operations Dashboard | 🟢 Ready[cite: 1] | Multi-tab event inspector & batch runner[cite: 1] |
| **Gateway** | Razorpay Test-Mode Integration | 🟡 Verified | Orders API & webhook receiver tested |
| **Scale** | Persistent Relational Store | ⚪ Roadmap | Migration from CSV to PostgreSQL with row locks |

---

## 🔍 Engineering Disclosures

* **State Durability:** Audit state currently commits to session cache and local append-only CSV ledgers (`data/audit_log.csv`)[cite: 1]. Production deployment requires migrating to a transactional database (e.g., PostgreSQL with row-level locks).
* **Model Quality:** The decision scoring model currently achieves ROC-AUC ~0.6583 with an Isotonic Brier score of 0.2089[cite: 1]. Future iterations will incorporate expanded feature stores and automated retraining sweeps.

---

<div align="center">

### Built for Razorpay Buildathon — Track 03: AI Revenue Recovery

**Devendar Bandaru**  
*ML recommends. Policy controls. Execution records.*[cite: 1]

[![License: MIT](https://img.shields.io/badge/License-MIT-gray.svg?style=flat-square)](LICENSE)

</div>
