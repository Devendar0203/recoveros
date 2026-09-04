import os

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


FEATURES = [
    "event_type",
    "failure_reason",
    "amount",
    "retry_count",
    "previous_contact_count",
    "customer_lifetime_value",
    "previous_success_rate",
    "customer_engagement",
    "hours_since_event",
    "action",
]

TARGET = "success"


def train_model():

    # -------------------------------
    # LOAD DATA
    # -------------------------------

    df = pd.read_csv(
        "data/recovery_training_data_v3.csv"
    )

    X = df[FEATURES]
    y = df[TARGET]

    # -------------------------------
    # EVENT-LEVEL TRAIN / TEST SPLIT
    # -------------------------------

    groups = df["event_id"]

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=42
    )

    train_index, test_index = next(
        splitter.split(
            X,
            y,
            groups=groups
        )
    )

    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]

    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]

    # -------------------------------
    # FEATURE TYPES
    # -------------------------------

    categorical_features = [
        "event_type",
        "failure_reason",
        "action",
    ]

    numeric_features = [
        "amount",
        "retry_count",
        "previous_contact_count",
        "customer_lifetime_value",
        "previous_success_rate",
        "customer_engagement",
        "hours_since_event",
    ]

    # -------------------------------
    # PREPROCESSING
    # -------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    # -------------------------------
    # MODEL
    # -------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        class_weight="balanced"
    )

    # -------------------------------
    # PIPELINE
    # -------------------------------

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # -------------------------------
    # TRAIN
    # -------------------------------

    print("\nTraining ML model...")

    pipeline.fit(
        X_train,
        y_train
    )

    # -------------------------------
    # EVALUATE
    # -------------------------------

    predictions = pipeline.predict(
        X_test
    )

    probabilities = pipeline.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    auc = roc_auc_score(
        y_test,
        probabilities
    )

    print("\n" + "=" * 55)
    print("RECOVEROS ML MODEL — EVENT-LEVEL TEST RESULTS")
    print("=" * 55)

    print(
        f"\nTraining examples: {len(X_train)}"
    )

    print(
        f"Test examples: {len(X_test)}"
    )

    print(
        f"\nAccuracy: {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall: {recall:.4f}"
    )

    print(
        f"ROC-AUC: {auc:.4f}"
    )

    # -------------------------------
    # SAVE MODEL
    # -------------------------------

    os.makedirs(
        "models",
        exist_ok=True
    )

    model_path = (
        "models/recovery_action_model.joblib"
    )

    joblib.dump(
        pipeline,
        model_path
    )

    print(
        f"\nModel saved to:\n{model_path}"
    )

    print("\n" + "=" * 55)


if __name__ == "__main__":
    train_model()