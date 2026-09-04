import hashlib
import random


class RecoveryEnvironment:
    """
    Deterministic counterfactual recovery simulator.

    The same event + action + seed will always
    produce the same simulated outcome.

    This allows fair comparison between strategies.
    """

    ACTION_SUCCESS_MULTIPLIERS = {
        "RETRY_NOW": 0.65,
        "RETRY_LATER": 0.80,
        "SEND_REMINDER": 0.55,
        "SUGGEST_ALTERNATIVE_PAYMENT": 0.75,
        "OFFER_INCENTIVE": 0.60,
        "ESCALATE_TO_HUMAN": 0.85,
        "STOP": 0.0,
    }

    def __init__(self, seed=42):
        self.seed = seed

    def _get_deterministic_random(
        self,
        event_id,
        action
    ):
        """
        Generate a deterministic random value.

        Same event + action + seed
        always returns the same value.
        """

        key = (
            f"{self.seed}|"
            f"{event_id}|"
            f"{action}"
        )

        hash_value = hashlib.sha256(
            key.encode()
        ).hexdigest()

        integer_value = int(
            hash_value[:16],
            16
        )

        rng = random.Random(
            integer_value
        )

        return rng.random()

    def _calculate_success_probability(
        self,
        event,
        action
    ):
        """
        Calculate simulated probability of recovery.
        """

        event_type = event["event_type"]

        failure_reason = event["failure_reason"]

        retry_count = int(
            event.get(
                "retry_count",
                0
            )
        )

        engagement = float(
            event.get(
                "customer_engagement",
                0.5
            )
        )

        previous_success_rate = float(
            event.get(
                "previous_success_rate",
                0.5
            )
        )

        base_probability = (
            self.ACTION_SUCCESS_MULTIPLIERS
            .get(action, 0.30)
        )

        # -----------------------------
        # EVENT-SPECIFIC ADJUSTMENTS
        # -----------------------------

        if (
            failure_reason == "insufficient_funds"
            and action == "RETRY_LATER"
        ):
            base_probability += 0.15

        if (
            failure_reason in [
                "card_expired",
                "payment_method_unavailable",
            ]
            and action == "SUGGEST_ALTERNATIVE_PAYMENT"
        ):
            base_probability += 0.20

        if (
            event_type == "checkout_abandonment"
            and action == "SEND_REMINDER"
        ):
            base_probability += 0.15

        if (
            event_type == "invoice_overdue"
            and action == "ESCALATE_TO_HUMAN"
        ):
            base_probability += 0.10

        # -----------------------------
        # CUSTOMER SIGNALS
        # -----------------------------

        base_probability += (
            engagement - 0.5
        ) * 0.20

        base_probability += (
            previous_success_rate - 0.5
        ) * 0.20

        # -----------------------------
        # RETRY PENALTY
        # -----------------------------

        base_probability -= (
            retry_count * 0.05
        )

        # Keep probability valid

        base_probability = max(
            0.01,
            min(
                base_probability,
                0.95
            )
        )

        return base_probability

    def execute_action(
        self,
        event,
        action
    ):
        """
        Execute a deterministic simulated recovery action.
        """

        amount = float(
            event["amount"]
        )

        event_id = str(
            event.get(
                "event_id",
                "unknown_event"
            )
        )

        # -----------------------------
        # STOP NEVER ATTEMPTS RECOVERY
        # -----------------------------

        if action == "STOP":
            return {
                "success": False,
                "recovered_amount": 0.0,
                "success_probability": 0.0,
                "probability": 0.0,
                "random_value": None,
            }

        # -----------------------------
        # CALCULATE SUCCESS PROBABILITY
        # -----------------------------

        success_probability = (
            self._calculate_success_probability(
                event,
                action
            )
        )

        # -----------------------------
        # DETERMINISTIC RANDOM VALUE
        # -----------------------------

        random_value = (
            self._get_deterministic_random(
                event_id,
                action
            )
        )

        # -----------------------------
        # DETERMINE SUCCESS
        # -----------------------------

        success = (
            random_value
            < success_probability
        )

        # -----------------------------
        # RECOVERED AMOUNT
        # -----------------------------

        recovered_amount = (
            amount
            if success
            else 0.0
        )

        # -----------------------------
        # RETURN RESULT
        # -----------------------------

        return {
            "success": success,
            "recovered_amount": recovered_amount,
            "success_probability": round(
                success_probability,
                4
            ),
            "probability": round(
                success_probability,
                4
            ),
            "random_value": round(
                random_value,
                4
            ),
        }