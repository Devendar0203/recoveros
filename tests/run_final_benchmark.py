import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment
from simulator.ml_action_scorer import MLActionScorer
from simulator.policy_engine import RecoveryPolicyEngine


def run_strategy(
    df,
    strategy_name,
    action_selector,
    seed=42
):
    """
    Run one strategy on the same unseen events.
    """

    environment = RecoveryEnvironment(
        seed=seed
    )

    total_at_risk = 0
    total_recovered = 0

    successful = 0
    failed = 0

    stops = 0
    escalations = 0

    action_counts = {}

    for _, row in df.iterrows():

        event = row.to_dict()

        total_at_risk += float(
            event["amount"]
        )

        final_action = action_selector(
            event
        )

        result = environment.execute_action(
            event,
            final_action
        )

        total_recovered += float(
            result["recovered_amount"]
        )

        if result["success"]:
            successful += 1
        else:
            failed += 1

        if final_action == "STOP":
            stops += 1

        if final_action == "ESCALATE_TO_HUMAN":
            escalations += 1

        action_counts[final_action] = (
            action_counts.get(
                final_action,
                0
            )
            + 1
        )

    return {
        "strategy": strategy_name,
        "events": len(df),
        "revenue_at_risk": total_at_risk,
        "revenue_recovered": total_recovered,
        "event_recovery_rate":
            (successful / len(df)) * 100,
        "revenue_recovery_rate":
            (total_recovered / total_at_risk)
            * 100,
        "successful": successful,
        "failed": failed,
        "stops": stops,
        "escalations": escalations,
        "action_counts": action_counts
    }


def baseline_action(event):
    """
    Original simple baseline.
    """

    if (
        event["event_type"]
        == "payment_failure"
    ):
        return "RETRY_NOW"

    return "SEND_REMINDER"


def intelligent_v1_action(event):
    """
    Your V1 heuristic strategy.
    """

    event_type = event["event_type"]

    retry_count = int(
        event["retry_count"]
    )

    failure_reason = (
        event["failure_reason"]
    )

    amount = float(
        event["amount"]
    )

    if retry_count >= 3:
        return "STOP"

    if (
        failure_reason
        == "insufficient_funds"
    ):
        return "RETRY_LATER"

    if (
        failure_reason
        in [
            "card_expired",
            "payment_method_unavailable"
        ]
    ):
        return (
            "SUGGEST_ALTERNATIVE_PAYMENT"
        )

    if (
        event_type
        == "checkout_abandonment"
    ):
        return "SEND_REMINDER"

    if (
        amount > 100000
    ):
        return "ESCALATE_TO_HUMAN"

    return "SEND_REMINDER"


def main():

    df = pd.read_csv(
        "data/evaluation_events.csv"
    )

    print("\n" + "=" * 70)
    print(
        "RECOVEROS FINAL BENCHMARK — "
        "100 UNSEEN EVENTS"
    )
    print("=" * 70)

    # -----------------------------------
    # BASELINE
    # -----------------------------------

    baseline_results = run_strategy(
        df=df,
        strategy_name="Baseline",
        action_selector=baseline_action,
        seed=42
    )

    # -----------------------------------
    # ML + POLICY
    # -----------------------------------

    scorer = MLActionScorer()

    policy_engine = RecoveryPolicyEngine()

    def ml_policy_action(event):

        ml_decision = (
            scorer.choose_best_action(
                event
            )
        )

        proposed_action = (
            ml_decision["action"]
        )

        policy_result = (
            policy_engine.evaluate(
                event,
                proposed_action
            )
        )

        return policy_result[
            "final_action"
        ]

    ml_policy_results = run_strategy(
        df=df,
        strategy_name="ML + Policy",
        action_selector=ml_policy_action,
        seed=42
    )

    # The final comparison is intentionally limited to the
    # fixed baseline and production ML + Policy strategy.
    # Intelligent V1 remains an exploratory, retired heuristic.
    results = [baseline_results, ml_policy_results]

    print(
        "\nSTRATEGY COMPARISON\n"
    )

    print(
        f"{'Strategy':<20}"
        f"{'Recovered':>18}"
        f"{'Revenue Rate':>18}"
        f"{'Success Rate':>18}"
    )

    print("-" * 74)

    for result in results:

        print(
            f"{result['strategy']:<20}"
            f"₹{result['revenue_recovered']:>16,.2f}"
            f"{result['revenue_recovery_rate']:>17.2f}%"
            f"{result['event_recovery_rate']:>17.2f}%"
        )

    print("\n" + "-" * 74)

    baseline_recovered = (
        baseline_results[
            "revenue_recovered"
        ]
    )

    ml_recovered = (
        ml_policy_results[
            "revenue_recovered"
        ]
    )

    improvement = (
        (
            ml_recovered
            - baseline_recovered
        )
        / baseline_recovered
    ) * 100

    additional_revenue = (
        ml_recovered
        - baseline_recovered
    )

    print(
        "\nML + POLICY IMPACT"
    )

    print(
        f"Additional revenue recovered: "
        f"₹{additional_revenue:,.2f}"
    )

    print(
        f"Improvement over baseline: "
        f"{improvement:.2f}%"
    )

    print(
        f"\nPolicy stops: "
        f"{ml_policy_results['stops']}"
    )

    print(
        f"Human escalations: "
        f"{ml_policy_results['escalations']}"
    )

    print(
        "\nML + POLICY FINAL ACTIONS:"
    )

    for action, count in sorted(
        ml_policy_results[
            "action_counts"
        ].items()
    ):
        print(
            f"{action}: {count}"
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
