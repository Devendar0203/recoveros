@"
# RecoverOS

## AI-Powered Revenue Recovery Decision System

RecoverOS is an AI-powered revenue recovery decision system designed to intelligently select recovery actions for failed payment and revenue events.

The system combines machine learning, deterministic diagnosis, policy controls, fallback decision-making, idempotency protection, recovery execution, and audit logging.

## Key Features

- Machine-learning-based recovery action scoring
- Deterministic root-cause diagnosis
- Policy-based safety controls
- ML failure fallback mechanism
- Idempotency protection against duplicate recovery attempts
- Deterministic recovery simulation
- Recovery execution and revenue measurement
- Append-only audit logging
- Streamlit interactive dashboard
- Benchmark comparison against baseline strategies

## Architecture

Revenue Event
    |
    v
Diagnosis Engine
    |
    v
ML Action Scorer
    |
    v
Policy Engine
    |
    +----> STOP
    |
    +----> ESCALATE_TO_HUMAN
    |
    +----> Approved Recovery Action
                  |
                  v
          Idempotency Guard
                  |
                  v
          Recovery Executor
                  |
                  v
             Audit Logger

## Machine Learning

The recovery action model uses a Random Forest classifier with categorical feature encoding.

The model evaluates recovery actions using event information such as:

- Event type
- Failure reason
- Transaction amount
- Retry count
- Previous contact count
- Customer lifetime value
- Previous success rate
- Customer engagement
- Hours since event
- Candidate recovery action

## Safety Controls

RecoverOS applies deterministic policy controls before executing recovery actions.

Examples include:

- Maximum retry protection
- Maximum customer-contact protection
- Fraud escalation
- Customer cancellation handling
- High-value invoice dispute escalation
- High-value incentive escalation

## Fallback Strategy

If the ML model becomes unavailable, RecoverOS automatically uses a deterministic fallback policy.

This ensures that an ML outage does not result in unsafe or undefined recovery behavior.

## Live Batch Measurement

The Streamlit dashboard includes a **Batch Simulation** tab. It runs the
ML + Policy strategy and a fixed baseline across the same 100 unseen events
and displays recovered revenue, improvement, recovery rate, policy stops,
human escalations, per-event decisions, and a CSV export in real time.

Results are **counterfactual simulation metrics**, not real payment revenue:
the deterministic environment holds the event cohort and random seed constant
so the action-selection strategies can be compared fairly.

## Final Benchmark

Evaluation on 100 unseen events:

| Strategy | Recovered Revenue | Revenue Rate | Success Rate |
|---|---:|---:|---:|
| Baseline | ₹2,348,795.26 | 52.85% | 55.00% |
| ML + Policy | ₹2,582,254.15 | 58.10% | 62.00% |

### ML + Policy Impact

- Additional revenue recovered: ₹233,458.89
- Improvement over baseline: 9.94%
- Policy stops: 15
- Human escalations: 6

### Why the earlier heuristic is not a comparator

An exploratory rules-only heuristic ("Intelligent V1") recovered less than
the fixed baseline (34.53% vs 52.85%) on this cohort. It is retained only as
historical learning, not presented as a production strategy or part of the
final benchmark. The production comparison is deliberately limited to the
fixed baseline and the ML + Policy system.

## Project Structure

```text
recoveros/
├── app.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── revenue_events.csv
│   ├── recovery_training_data_v3.csv
│   └── ...
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
│   └── audit_logger.py
└── tests/
    ├── test_diagnosis_engine.py
    ├── test_environment.py
    ├── test_ml_scorer.py
    ├── test_ml_fallback.py
    └── test_recovery_workflow.py
