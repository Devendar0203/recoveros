import pandas as pd

from sklearn.model_selection import train_test_split


def split_events():

    df = pd.read_csv(
        "data/revenue_events_v2.csv"
    )

    train_events, evaluation_events = (
        train_test_split(
            df,
            test_size=0.20,
            random_state=42
        )
    )

    train_events.to_csv(
        "data/training_events.csv",
        index=False
    )

    evaluation_events.to_csv(
        "data/evaluation_events.csv",
        index=False
    )

    print("\n" + "=" * 55)
    print("RECOVEROS EVENT SPLIT")
    print("=" * 55)

    print(
        f"\nTotal events: {len(df)}"
    )

    print(
        f"Training events: {len(train_events)}"
    )

    print(
        f"Evaluation events: {len(evaluation_events)}"
    )

    print(
        "\nSaved:"
    )

    print(
        "data/training_events.csv"
    )

    print(
        "data/evaluation_events.csv"
    )

    print("\n" + "=" * 55)


if __name__ == "__main__":
    split_events()