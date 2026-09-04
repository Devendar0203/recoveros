import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment
from simulator.intelligent_strategy import IntelligentRecoveryStrategy


df = pd.read_csv("data/revenue_events.csv")

environment = RecoveryEnvironment(seed=42)

strategy = IntelligentRecoveryStrategy()


total_revenue_at_risk = 0
total_recovered = 0

successful_recoveries = 0
failed_recoveries = 0
stopped_events = 0

action_counts = {}


for _, row in df.iterrows():

    event = row.to_dict()

    amount = float(event["amount"])

    total_revenue_at_risk += amount

    action = strategy.choose_action(event)

    action_counts[action] = (
        action_counts.get(action, 0) + 1
    )

    if action == "STOP":
        stopped_events += 1

    result = environment.execute_action(
        event,
        action
    )

    total_recovered += result["recovered_amount"]

    if result["success"]:
        successful_recoveries += 1
    else:
        failed_recoveries += 1


event_recovery_rate = (
    successful_recoveries / len(df)
) * 100


revenue_recovery_rate = (
    total_recovered / total_revenue_at_risk
) * 100


print("\n" + "=" * 55)
print("RECOVEROS INTELLIGENT STRATEGY V1")
print("=" * 55)

print(f"\nEvents processed: {len(df)}")

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
    f"Stopped by policy: "
    f"{stopped_events}"
)

print("\nACTIONS TAKEN:")

for action, count in sorted(action_counts.items()):
    print(f"{action}: {count}")

print("\n" + "=" * 55)