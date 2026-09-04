from simulator.ml_action_scorer import MLActionScorer


def main():

    print()
    print("=" * 60)
    print("RECOVEROS ML FAILURE → FALLBACK TEST")
    print("=" * 60)

    scorer = MLActionScorer()

    # Deliberately replace the ML model with
    # an object that will fail during prediction.
    class BrokenModel:

        def predict_proba(self, X):

            raise RuntimeError(
                "Simulated ML model failure"
            )

    scorer.model = BrokenModel()

    event = {
        "event_id": "FALLBACK-TEST-001",
        "event_type": "payment_failure",
        "failure_reason": "insufficient_funds",
        "amount": 50000,
        "retry_count": 0,
        "customer_lifetime_value": 100000,
        "previous_success_rate": 0.50,
        "customer_engagement": 0.50,
        "previous_contact_count": 0,
        "hours_since_event": 24,
    }

    result = scorer.choose_best_action(
        event
    )

    print()
    print("EVENT:")
    print(
        "Failure reason:",
        event["failure_reason"]
    )

    print()
    print("ML MODEL:")
    print("INTENTIONALLY FAILED")

    print()
    print("FALLBACK RESULT:")
    print(
        "Action:",
        result["action"]
    )

    print(
        "Decision Source:",
        result["decision_source"]
    )

    print(
        "Fallback Used:",
        result["fallback_used"]
    )

    print(
        "Reason:",
        result["fallback_reason"]
    )

    print()

    if result["fallback_used"] is True:

        print(
            "STATUS: PASS"
        )

        print(
            "ML failure was handled safely."
        )

    else:

        print(
            "STATUS: FAIL"
        )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()