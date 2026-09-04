from simulator.ml_action_scorer import MLActionScorer


def main():

    print()
    print("=" * 60)
    print("RECOVEROS ML ACTION SCORER")
    print("=" * 60)

    event = {
        "event_type": "payment_failure",
        "failure_reason": "insufficient_funds",
        "amount": 2988.57,
        "retry_count": 1,
        "customer_lifetime_value": 15000.0,

        "previous_success_rate": 0.5,
        "customer_engagement": 0.5,
        "previous_contact_count": 0,
        "hours_since_event": 24.0,
    }

    print()
    print("EVENT:")

    print(
        f"Event type: "
        f"{event['event_type']}"
    )

    print(
        f"Failure reason: "
        f"{event['failure_reason']}"
    )

    print(
        f"Amount: "
        f"₹{event['amount']:,.2f}"
    )

    print()
    print("ACTION SCORES:")
    print()

    scorer = MLActionScorer()

    scores = scorer.score_actions(event)

    for score in scores:

        print(
            f"{score['action']:<30} "
            f"Probability: "
            f"{score['success_probability']:.2%} | "
            f"Gross EV: "
            f"₹{score['gross_expected_value']:,.2f} | "
            f"Cost: "
            f"₹{score['action_cost']:,.2f} | "
            f"Net EV: "
            f"₹{score['net_expected_value']:,.2f}"
        )

    best_action = scorer.recommend_action(event)

    print()
    print("-" * 60)

    print(
        f"BEST ACTION: "
        f"{best_action['action']}"
    )

    print(
        f"EXPECTED NET VALUE: "
        f"₹{best_action['net_expected_value']:,.2f}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()