import pandas as pd

from simulator.ml_action_scorer import MLActionScorer
from simulator.recovery_executor import RecoveryExecutor


def main():

    events = pd.read_csv(
        "data/evaluation_events.csv"
    )

    event = events.iloc[0].to_dict()

    scorer = MLActionScorer()

    best_action = scorer.choose_best_action(
        event
    )

    executor = RecoveryExecutor()

    result = executor.execute(
        event=event,
        action=best_action["action"],
        score=best_action
    )

    print()
    print("=" * 60)
    print("RECOVEROS RECOVERY EXECUTION TEST")
    print("=" * 60)

    print(f"\nEvent ID: {result['event_id']}")

    print(
        f"Recommended Action: "
        f"{result['action']}"
    )

    print(
        f"Success Probability: "
        f"{result['success_probability']:.2%}"
    )

    print(
        f"Execution Random Value: "
        f"{result['random_value']}"
    )

    print(f"\nRecovery Success: {result['success']}")

    print(
        f"Amount Recovered: "
        f"₹{result['recovered_amount']:,.2f}"
    )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()