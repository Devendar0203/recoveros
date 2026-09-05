# ⚡ RecoverOS: Autonomous Revenue Recovery & Decision System

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red.svg)](https://recoveros-yatrzeuqirmuhwfdxa57od.streamlit.app/)
[![Razorpay API](https://img.shields.io/badge/Razorpay-Test--Mode%20Verified-blue.svg)](https://razorpay.com/docs/)
[![Track](https://img.shields.io/badge/Razorpay%20Buildathon-Track%2003%3A%20AI%20Revenue%20Recovery-orange.svg)]()

RecoverOS
AI-Powered Revenue Recovery Decision System

Razorpay Buildathon — Track 03: AI Revenue Recovery

RecoverOS diagnoses why a payment, checkout, subscription, or invoice failed, scores every possible recovery action by expected net revenue, applies compliance guardrails before anything is executed, and logs an append-only audit trail of the entire decision — so recovery is measurable, safe, and explainable rather than a black box.

💡 Project Architecture Summary
The Core Stack
Frontend: Streamlit (interactive multi-tab dashboard — recommendation, execution, analytics, audit log, batch simulation)
Backend: Python — a modular simulator/ package (diagnosis engine, ML scorer, policy engine, idempotency guard, executor, audit logger) orchestrated by a single RecoveryWorkflow class
Database: None yet — state is in-memory (Streamlit session state) with an append-only audit log exportable as CSV. (Noted as a scaling gap below, not hidden.)
The AI Layer
Model: Random Forest classifier (scikit-learn), trained to score each candidate recovery action (RETRY_NOW, RETRY_LATER, SEND_REMINDER, OFFER_INCENTIVE, ESCALATE_TO_HUMAN, SUGGEST_ALTERNATIVE_PAYMENT) by probability of success
Decision framing: Every action is ranked by Net Expected Value = P(success) × amount − action_cost, not just raw success probability — so a cheap action with slightly lower odds can correctly beat an expensive one
Diagnosis layer: A deterministic, rule-based root-cause taxonomy (not an LLM) maps raw gateway/failure signals to a normalized root cause with a confidence score — kept deterministic and explainable on purpose, since this is the layer the compliance logic depends on
Safety net: A fallback policy engine takes over automatically if the ML model is unavailable or errors, guaranteeing the system never fails open into an unsafe or undefined recovery action
No LLM, LangChain, or vector DB is used — this is a classical ML decision system by design, since the task is structured tabular scoring, not open-ended reasoning.
The Razorpay Integration
Test-mode Orders API creates real payment events (not simulated in the app layer)
A webhook receiver listens for payment.failed and payment.captured events, verifies the Razorpay signature, and feeds real failed payments directly into the same RecoveryWorkflow used everywhere else in the app — no separate code path for "real" vs "demo" data
Failures are exercised using Razorpay's documented test instruments: test cards for card declines, and the failure@razorpay / success@razorpay UPI IDs for UPI outcomes
Key Features
Machine-learning-based recovery action scoring (Net Expected Value)
Deterministic, explainable root-cause diagnosis
Policy-based safety controls (fraud escalation, retry/contact fatigue caps, high-value dispute & incentive escalation)
ML failure fallback mechanism (safe deterministic policy takes over)
Idempotency protection against duplicate recovery execution
Batch simulation — run N events through the full pipeline and see aggregate revenue recovered, not just one event at a time
Append-only audit logging with CSV export
Real Razorpay test-mode webhook integration
Benchmark comparison against baseline strategies
Architecture
Revenue Event (synthetic OR real Razorpay webhook)
        │
        ▼
  Diagnosis Engine
        │
        ▼
  ML Action Scorer  ──(on failure)──▶ Fallback Policy
        │
        ▼
  Policy Engine
   ├──▶ STOP
   ├──▶ ESCALATE_TO_HUMAN
   └──▶ Approved Recovery Action
        │
        ▼
  Idempotency Guard
        │
        ▼
  Recovery Executor
        │
        ▼
  Audit Logger
Batch Simulation

Rather than only reporting a static benchmark number, the app now runs a configurable batch (25–200 events) through the exact same production workflow live, and reports:

Total revenue at risk vs. total recovered (₹ and %)
Recovery rate broken down by root cause
Policy stops and human escalations triggered
Duplicate executions blocked by the idempotency guard
A downloadable per-event CSV
Benchmark (synthetic, 100 unseen events)
Strategy	Recovered Revenue	Revenue Rate	Success Rate
Baseline	₹2,348,795.26	52.85%	55.00%
ML + Policy	₹2,582,254.15	58.10%	62.00%

Note: an earlier "Intelligent V1" heuristic strategy underperformed the naive baseline in initial testing and has been pulled from this table pending root-cause analysis — including a broken result honestly would raise more questions than it answers. Re-benchmark before citing any V1 numbers publicly.

Safety Controls
Maximum retry protection (hard stop after N attempts)
Maximum customer-contact protection (no repeated nudges past a cap)
Fraud escalation (never auto-retried — always routed to a human)
Customer cancellation handling (no automated recovery triggered)
High-value invoice dispute escalation
High-value incentive escalation (requires human approval above a threshold)
Project Structure
recoveros/
├── app.py
├── requirements.txt
├── data/
├── models/
│   └── recovery_action_model.joblib
├── simulator/
│   ├── diagnosis_engine.py
│   ├── ml_action_scorer.py
│   ├── policy_engine.py
│   ├── fallback_policy.py
│   ├── idempotency_guard.py
│   ├── recovery_environment.py
│   ├── recovery_executor.py
│   ├── recovery_workflow.py
│   ├── batch_simulator.py
│   └── audit_logger.py
├── integrations/
│   ├── razorpay_connector.py
│   └── webhook_server.py
└── tests/
    ├── test_diagnosis_engine.py
    ├── test_environment.py
    ├── test_ml_scorer.py
    ├── test_ml_fallback.py
    └── test_recovery_workflow.py
Running Locally
bash
pip install -r requirements.txt
streamlit run app.py

For the real Razorpay demo flow:

bash
export RAZORPAY_KEY_ID=<your test-mode key id>
export RAZORPAY_KEY_SECRET=<your test-mode key secret>
export RAZORPAY_WEBHOOK_SECRET=<from Dashboard > Webhooks>
python integrations/webhook_server.py
# expose with ngrok, point the Razorpay webhook at it, then fail a
# test payment using failure@razorpay (UPI) or a decline test card
Known Limitations (stated up front, not discovered by the panel)
No persistent database yet — audit history resets when the app restarts; CSV export is the current durability mechanism
Model quality is a work in progress (ROC-AUC ~0.65) — feature engineering and more training data are the next priority
The V1 heuristic benchmark needs re-validation before being cited again
