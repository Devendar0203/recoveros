import os
import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment


ACTIONS = [
    "RETRY_NOW",
    "RETRY_LATER",
    "SEND_REMINDER",
    "SUGGEST_ALTERNATIVE_PAYMENT",
    "OFFER_INCENTIVE",
    "ESCALATE_TO_HUMAN",
]


def generate_training_data():

    print("\nGenerating simulator-aligned training data...")

    df = pd.read_csv(
        "data/training_events.csv"
    )

    environment = RecoveryEnvironment(
        seed=42
    )

    training_rows = []

    for _, row in df.iterrows():

        event = row.to_dict()

        for action in ACTIONS:

            result = environment.execute_action(
                event,
                action
            )

            training_rows.append({
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "failure_reason": event["failure_reason"],
                "amount": float(event["amount"]),
                "retry_count": int(event["retry_count"]),
                "previous_contact_count": int(
                    event["previous_contact_count"]
                ),
                "customer_lifetime_value": float(
                    event["customer_lifetime_value"]
                ),
                "previous_success_rate": float(
                    event["previous_success_rate"]
                ),
                "customer_engagement": float(
                    event["customer_engagement"]
                ),
                "hours_since_event": float(
                    event["hours_since_event"]
                ),
                "action": action,
                "success": int(
                    result["success"]
                ),
                "recovered_amount": float(
                    result["recovered_amount"]
                ),
            })

    training_df = pd.DataFrame(
        training_rows
    )

    os.makedirs(
        "data",
        exist_ok=True
    )

    output_path = (
        "data/recovery_training_data_v3.csv"
    )

    training_df.to_csv(
        output_path,
        index=False
    )

    print("\n" + "=" * 60)
    print(
        "RECOVEROS SIMULATOR-ALIGNED "
        "TRAINING DATA"
    )
    print("=" * 60)

    print(
        f"\nTraining events: "
        f"{len(df)}"
    )

    print(
        f"Total training examples: "
        f"{len(training_df)}"
    )

    print(
        f"\nActions per event: "
        f"{len(ACTIONS)}"
    )

    print(
        f"\nSaved to:\n{output_path}"
    )

    print("\nSuccess rate by action:")

    success_rates = (
        training_df
        .groupby("action")["success"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    for action, rate in success_rates.items():

        print(
            f"{action:30} "
            f"{rate:.2%}"
        )

    print("=" * 60)


if __name__ == "__main__":
    generate_training_data()