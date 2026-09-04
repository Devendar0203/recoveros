
import joblib
import pandas as pd

from simulator.fallback_policy import FallbackPolicy
from simulator.diagnosis_engine import DiagnosisEngine


class MLActionScorer:
    """
    RecoverOS ML Action Scorer.

    Responsibilities:
    1. Score all recovery actions using ML.
    2. Calculate expected net value.
    3. Select the best action.
    4. Fall back safely if ML fails.
    5. Attach root-cause diagnosis to the decision.
    6. Provide explainable decision reasoning.
    """

    ACTIONS = [
        "RETRY_NOW",
        "RETRY_LATER",
        "SEND_REMINDER",
        "OFFER_INCENTIVE",
        "ESCALATE_TO_HUMAN",
        "SUGGEST_ALTERNATIVE_PAYMENT",
    ]

    ACTION_COSTS = {
        "RETRY_NOW": 5.0,
        "RETRY_LATER": 10.0,
        "SEND_REMINDER": 3.0,
        "OFFER_INCENTIVE": 500.0,
        "ESCALATE_TO_HUMAN": 1500.0,
        "SUGGEST_ALTERNATIVE_PAYMENT": 8.0,
    }

    def __init__(
        self,
        model_path="models/recovery_action_model.joblib"
    ):
        self.model = joblib.load(model_path)

        self.fallback_policy = FallbackPolicy()
        self.diagnosis_engine = DiagnosisEngine()

    # =====================================================
    # FEATURE PREPARATION
    # =====================================================

    def _prepare_features(self, event, action):

        features = {
            "event_type": str(
                event.get(
                    "event_type",
                    "unknown"
                )
            ),

            "failure_reason": str(
                event.get(
                    "failure_reason",
                    "unknown"
                )
            ),

            "amount": float(
                event.get(
                    "amount",
                    0.0
                )
            ),

            "retry_count": int(
                event.get(
                    "retry_count",
                    0
                )
            ),

            "customer_lifetime_value": float(
                event.get(
                    "customer_lifetime_value",
                    0.0
                )
            ),

            "previous_success_rate": float(
                event.get(
                    "previous_success_rate",
                    0.5
                )
            ),

            "customer_engagement": float(
                event.get(
                    "customer_engagement",
                    0.5
                )
            ),

            "previous_contact_count": int(
                event.get(
                    "previous_contact_count",
                    0
                )
            ),

            "hours_since_event": float(
                event.get(
                    "hours_since_event",
                    24.0
                )
            ),

            "action": str(action),
        }

        return pd.DataFrame([features])

    # =====================================================
    # SCORE ONE ACTION
    # =====================================================

    def score_action(self, event, action):

        X = self._prepare_features(
            event,
            action
        )

        probabilities = self.model.predict_proba(X)

        probability = float(
            probabilities[0][1]
        )

        amount = float(
            event.get(
                "amount",
                0.0
            )
        )

        gross_expected_value = (
            probability * amount
        )

        action_cost = float(
            self.ACTION_COSTS.get(
                action,
                0.0
            )
        )

        net_expected_value = (
            gross_expected_value
            - action_cost
        )

        return {
            "action": action,

            "probability": probability,

            "success_probability": probability,

            "gross_expected_value":
                gross_expected_value,

            "expected_recovery":
                gross_expected_value,

            "action_cost":
                action_cost,

            "net_expected_value":
                net_expected_value,

            "decision_source":
                "ML",

            "fallback_used":
                False,
        }

    # =====================================================
    # SCORE ALL ACTIONS
    # =====================================================

    def score_actions(self, event):

        scores = []

        for action in self.ACTIONS:

            result = self.score_action(
                event,
                action
            )

            scores.append(result)

        scores.sort(
            key=lambda score:
                score["net_expected_value"],
            reverse=True
        )

        return scores

    # =====================================================
    # FALLBACK RESULT
    # =====================================================

    def _fallback_result(self, event):

        fallback = (
            self.fallback_policy.choose_action(
                event
            )
        )

        amount = float(
            event.get(
                "amount",
                0.0
            )
        )

        action = fallback["action"]

        action_cost = float(
            self.ACTION_COSTS.get(
                action,
                0.0
            )
        )

        return {
            "action": action,

            "probability": 0.0,

            "success_probability": 0.0,

            "gross_expected_value": 0.0,

            "expected_recovery": 0.0,

            "action_cost": action_cost,

            "net_expected_value":
                -action_cost,

            "decision_source":
                "FALLBACK_POLICY",

            "fallback_used":
                True,

            "fallback_reason":
                fallback["reason"],

            "amount":
                amount,
        }

    # =====================================================
    # RECOMMEND ACTION
    # =====================================================

    def recommend_action(self, event):

        try:

            # Deterministic root-cause diagnosis.
            diagnosis = (
                self.diagnosis_engine.diagnose(
                    event
                )
            )

            # Existing ML scoring remains unchanged.
            scores = self.score_actions(
                event
            )

            if not scores:

                return self._fallback_result(
                    event
                )

            best = scores[0]

            # Attach diagnosis to the final
            # ML recommendation.
            best["diagnosis"] = diagnosis

            # Explain why the ML action was selected.
            best["reasoning"] = (
                f"Root cause: "
                f"{diagnosis['root_cause']}. "
                f"Category: "
                f"{diagnosis['category']}. "
                f"ML selected "
                f"{best['action']} because it "
                f"has the highest expected net "
                f"value among the evaluated "
                f"recovery actions."
            )

            return best

        except Exception as error:

            fallback = self._fallback_result(
                event
            )

            fallback["ml_error"] = str(
                error
            )

            return fallback

    # =====================================================
    # BACKWARD COMPATIBILITY
    # =====================================================

    def choose_best_action(self, event):

        return self.recommend_action(
            event
        )

