import pandas as pd

from simulator.recovery_environment import (
    RecoveryEnvironment
)


def main():

    df = pd.read_csv(
        "data/evaluation_events.csv"
    )

    event = df.iloc[0].to_dict()

    environment = RecoveryEnvironment(
        seed=42
    )

    result_1 = environment.execute_action(
        event,
        "RETRY_LATER"
    )

    result_2 = environment.execute_action(
        event,
        "RETRY_LATER"
    )

    print("\n" + "=" * 60)
    print("RECOVEROS DETERMINISTIC ENVIRONMENT TEST")
    print("=" * 60)

    print(
        "\nEvent ID:",
        event["event_id"]
    )

    print("\nAction: RETRY_LATER")

    print("\nRun 1:")
    print(result_1)

    print("\nRun 2:")
    print(result_2)

    print("\nDeterministic:")

    print(
        result_1 == result_2
    )

    print("=" * 60)


if __name__ == "__main__":
    main()