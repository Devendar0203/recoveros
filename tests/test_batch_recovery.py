"""Checks that batch measurement produces comparable, exportable metrics."""

import pandas as pd

from simulator.batch_recovery import BatchRecoverySimulator


class FakeScorer:
    def choose_best_action(self, event):
        return {"action": "RETRY_LATER"}


class FakePolicy:
    def evaluate(self, event, action):
        if int(event["retry_count"]) >= 3:
            return {"final_action": "STOP", "reason": "Retry limit"}
        return {"final_action": action, "reason": "Approved"}


def main():
    events = pd.DataFrame([
        {
            "event_id": "batch-1",
            "event_type": "payment_failure",
            "failure_reason": "insufficient_funds",
            "amount": 1000.0,
            "retry_count": 0,
            "customer_engagement": 0.5,
            "previous_success_rate": 0.5,
        },
        {
            "event_id": "batch-2",
            "event_type": "payment_failure",
            "failure_reason": "technical_error",
            "amount": 500.0,
            "retry_count": 3,
            "customer_engagement": 0.5,
            "previous_success_rate": 0.5,
        },
    ])

    simulator = BatchRecoverySimulator(FakeScorer(), FakePolicy())
    baseline = simulator.run_baseline(events)
    ml_policy = simulator.run_ml_policy(events)

    assert baseline["events"] == 2
    assert ml_policy["events"] == 2
    assert ml_policy["policy_stops"] == 1
    assert len(ml_policy["details"]) == 2
    assert set(ml_policy["details"]) >= {
        "event_id", "proposed_action", "final_action", "recovered_amount"
    }
    print("Batch recovery checks passed.")


if __name__ == "__main__":
    main()
