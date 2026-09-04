"""Smoke tests for RecoverOS safety-critical workflow paths."""

from simulator.recovery_workflow import RecoveryWorkflow


class FakeScorer:
    def score_actions(self, event):
        return [{
            "action": "RETRY_NOW",
            "success_probability": 0.8,
            "gross_expected_value": 800.0,
            "action_cost": 5.0,
            "net_expected_value": 795.0,
        }]


class FakeExecutor:
    def execute(self, event, action, score):
        return {"success": True, "recovered_amount": event["amount"]}


def event(**overrides):
    value = {
        "event_id": "test-event",
        "event_type": "payment_failure",
        "failure_reason": "technical_error",
        "gateway_signal": "timeout",
        "amount": 1000.0,
        "retry_count": 0,
        "previous_contact_count": 0,
    }
    value.update(overrides)
    return value


def main():
    workflow = RecoveryWorkflow(FakeScorer(), FakeExecutor())

    fraud = workflow.analyze(event(gateway_signal="fraud_suspected"))
    assert fraud["policy"]["final_action"] == "ESCALATE_TO_HUMAN"
    assert workflow.execute(fraud)["status"] == "PENDING_REVIEW"

    exhausted = workflow.analyze(event(retry_count=3))
    assert exhausted["policy"]["final_action"] == "STOP"
    assert workflow.execute(exhausted)["status"] == "STOPPED"

    fallback = workflow.analyze(event(simulate_model_failure=True))
    assert fallback["fallback_used"] is True
    assert fallback["proposed"]["action"] == "RETRY_LATER"
    print("Recovery workflow safety checks passed.")


if __name__ == "__main__":
    main()
