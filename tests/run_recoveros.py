import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment
from simulator.intelligent_strategy import IntelligentRecoveryStrategy
from simulator.policy_engine import RecoveryPolicyEngine
from simulator.audit_logger import AuditLogger


df = pd.read_csv("data/revenue_events.csv")

environment = RecoveryEnvironment(seed=42)

strategy = IntelligentRecoveryStrategy()

policy_engine = RecoveryPolicyEngine()

audit_logger = AuditLogger(
    output_path="data/audit_log.csv"
)


total_revenue_at_risk = 0
total_recovered = 0

successful_recoveries = 0
failed_recoveries = 0

policy_stops = 0
escalations = 0


for _, row in df.iterrows():

    event = row.to_dict()

    amount = float(event["amount"])

    total_revenue_at_risk += amount


    # -----------------------------
    # 1. INTELLIGENCE
    # -----------------------------

    proposed_action = strategy.choose_action(
        event
    )


    # -----------------------------
    # 2. POLICY CHECK
    # -----------------------------

    policy_result = policy_engine.evaluate(
        event,
        proposed_action
    )

    final_action = (
        policy_result["final_action"]
    )


    # -----------------------------
    # 3. EXECUTION
    # -----------------------------

    execution_result = (
        environment.execute_action(
            event,
            final_action
        )
    )


    # -----------------------------
    # 4. AUDIT LOG
    # -----------------------------

    audit_logger.log(
        event=event,
        proposed_action=proposed_action,
        policy_result=policy_result,
        execution_result=execution_result
    )


    # -----------------------------
    # 5. METRICS
    # -----------------------------

    total_recovered += (
        execution_result["recovered_amount"]
    )

    if execution_result["success"]:
        successful_recoveries += 1
    else:
        failed_recoveries += 1

    if final_action == "STOP":
        policy_stops += 1

    if final_action == "ESCALATE_TO_HUMAN":
        escalations += 1


event_recovery_rate = (
    successful_recoveries / len(df)
) * 100


revenue_recovery_rate = (
    total_recovered /
    total_revenue_at_risk
) * 100


print("\n" + "=" * 60)
print("RECOVEROS — AUDITABLE RECOVERY RUN")
print("=" * 60)

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
    f"{escalations}"
)

print(
    "\nAudit log saved to:"
)

print(
    "data/audit_log.csv"
)

print("\n" + "=" * 60)