import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment
from simulator.ml_action_scorer import MLActionScorer
from simulator.policy_engine import RecoveryPolicyEngine
from simulator.audit_logger import AuditLogger


def main():

    df = pd.read_csv(
        "data/revenue_events.csv"
    )

    environment = RecoveryEnvironment(
        seed=42
    )

    scorer = MLActionScorer()

    policy_engine = RecoveryPolicyEngine()

    audit_logger = AuditLogger(
        output_path="data/ml_policy_audit_log.csv"
    )

    total_revenue_at_risk = 0
    total_recovered = 0

    successful_recoveries = 0
    failed_recoveries = 0

    policy_stops = 0
    human_escalations = 0

    action_counts = {}


    for _, row in df.iterrows():

        event = row.to_dict()

        total_revenue_at_risk += float(
            event["amount"]
        )

        # ---------------------------------
        # 1. ML SCORES ALL ACTIONS
        # ---------------------------------

        best_decision = (
            scorer.choose_best_action(
                event
            )
        )

        proposed_action = (
            best_decision["action"]
        )

        # ---------------------------------
        # 2. POLICY ENGINE
        # ---------------------------------

        policy_result = (
            policy_engine.evaluate(
                event,
                proposed_action
            )
        )

        final_action = (
            policy_result["final_action"]
        )

        # ---------------------------------
        # 3. EXECUTE ACTION
        # ---------------------------------

        execution_result = (
            environment.execute_action(
                event,
                final_action
            )
        )

        # ---------------------------------
        # 4. AUDIT
        # ---------------------------------

        audit_logger.log(
            event=event,
            proposed_action=proposed_action,
            policy_result=policy_result,
            execution_result=execution_result
        )

        # ---------------------------------
        # 5. METRICS
        # ---------------------------------

        total_recovered += float(
            execution_result["recovered_amount"]
        )

        if execution_result["success"]:
            successful_recoveries += 1
        else:
            failed_recoveries += 1

        if final_action == "STOP":
            policy_stops += 1

        if final_action == "ESCALATE_TO_HUMAN":
            human_escalations += 1

        action_counts[final_action] = (
            action_counts.get(
                final_action,
                0
            )
            + 1
        )


    event_recovery_rate = (
        successful_recoveries / len(df)
    ) * 100

    revenue_recovery_rate = (
        total_recovered /
        total_revenue_at_risk
    ) * 100


    print("\n" + "=" * 65)
    print("RECOVEROS V3 — ML + POLICY STRATEGY")
    print("=" * 65)

    print(
        f"\nEvents processed: {len(df)}"
    )

    print(
        f"Total revenue at risk: "
        f"₹{total_revenue_at_risk:,.2f}"
    )

    print(
        f"Revenue recovered: "
        f"₹{total_recovered:,.2f}"
    )

    print(
        f"Event recovery rate: "
        f"{event_recovery_rate:.2f}%"
    )

    print(
        f"Revenue recovery rate: "
        f"{revenue_recovery_rate:.2f}%"
    )

    print(
        f"Successful recoveries: "
        f"{successful_recoveries}"
    )

    print(
        f"Failed recoveries: "
        f"{failed_recoveries}"
    )

    print(
        f"Policy stops: "
        f"{policy_stops}"
    )

    print(
        f"Human escalations: "
        f"{human_escalations}"
    )

    print("\nFINAL ACTIONS:")

    for action, count in sorted(
        action_counts.items()
    ):
        print(
            f"{action}: {count}"
        )

    print(
        "\nAudit log saved to:"
    )

    print(
        "data/ml_policy_audit_log.csv"
    )

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()