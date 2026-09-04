from simulator.fallback_policy import FallbackPolicy


def main():

    policy = FallbackPolicy()

    print()
    print("=" * 60)
    print("RECOVEROS FALLBACK POLICY TEST")
    print("=" * 60)

    test_events = [

        {
            "event_id": "TEST-001",
            "event_type": "payment_failure",
            "failure_reason": "insufficient_funds",
            "amount": 50000,
            "retry_count": 0,
            "previous_contact_count": 0,
        },

        {
            "event_id": "TEST-002",
            "event_type": "payment_failure",
            "failure_reason": "technical_error",
            "amount": 25000,
            "retry_count": 1,
            "previous_contact_count": 0,
        },

        {
            "event_id": "TEST-003",
            "event_type": "payment_failure",
            "failure_reason": "authentication_failed",
            "amount": 15000,
            "retry_count": 0,
            "previous_contact_count": 0,
        },

        {
            "event_id": "TEST-004",
            "event_type": "payment_failure",
            "failure_reason": "insufficient_funds",
            "amount": 10000,
            "retry_count": 3,
            "previous_contact_count": 0,
        },

        {
            "event_id": "TEST-005",
            "event_type": "payment_failure",
            "failure_reason": "unknown",
            "amount": 10000,
            "retry_count": 0,
            "previous_contact_count": 3,
        },

    ]

    for event in test_events:

        result = policy.choose_action(event)

        print()
        print("Event:", event["event_id"])
        print(
            "Failure:",
            event["failure_reason"]
        )
        print(
            "Retry Count:",
            event["retry_count"]
        )
        print(
            "Selected Action:",
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
            result["reason"]
        )

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()