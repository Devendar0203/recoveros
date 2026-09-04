import random


class RecoveryEnvironment:
    """
    Simulates whether a recovery action succeeds.

    The agent does NOT directly know the exact probabilities.
    """

    def __init__(self, seed=42):
        self.random = random.Random(seed)

    def get_success_probability(self, event, action):
        """
        Hidden environment logic.

        Returns the probability that a chosen recovery
        action will successfully recover the revenue.
        """

        event_type = event["event_type"]
        failure_reason = event["failure_reason"]

        probability = 0.20

        # -----------------------------------
        # PAYMENT FAILURE
        # -----------------------------------

        if event_type == "payment_failure":

            if failure_reason == "temporary_bank_failure":

                if action == "RETRY_LATER":
                    probability = 0.85

                elif action == "RETRY_NOW":
                    probability = 0.45

                elif action == "SEND_REMINDER":
                    probability = 0.20

            elif failure_reason == "insufficient_funds":

                if action == "RETRY_LATER":
                    probability = 0.75

                elif action == "SEND_REMINDER":
                    probability = 0.60

                elif action == "RETRY_NOW":
                    probability = 0.20

            elif failure_reason == "authentication_failed":

                if action == "SUGGEST_ALTERNATIVE_PAYMENT":
                    probability = 0.85

                elif action == "SEND_REMINDER":
                    probability = 0.65

            elif failure_reason == "payment_timeout":

                if action == "RETRY_NOW":
                    probability = 0.70

                elif action == "RETRY_LATER":
                    probability = 0.50

            elif failure_reason == "technical_error":

                if action == "RETRY_LATER":
                    probability = 0.80

                elif action == "RETRY_NOW":
                    probability = 0.55

        # -----------------------------------
        # CHECKOUT ABANDONMENT
        # -----------------------------------

        elif event_type == "checkout_abandonment":

            if failure_reason == "payment_method_unavailable":

                if action == "SUGGEST_ALTERNATIVE_PAYMENT":
                    probability = 0.80

                elif action == "SEND_REMINDER":
                    probability = 0.40

            elif failure_reason == "price_hesitation":

                if action == "OFFER_INCENTIVE":
                    probability = 0.75

                elif action == "SEND_REMINDER":
                    probability = 0.45

            elif failure_reason == "high_friction":

                if action == "SEND_REMINDER":
                    probability = 0.50

                elif action == "SUGGEST_ALTERNATIVE_PAYMENT":
                    probability = 0.60

        # -----------------------------------
        # SUBSCRIPTION FAILURE
        # -----------------------------------

        elif event_type == "subscription_failure":

            if failure_reason == "mandate_failed":

                if action == "RETRY_LATER":
                    probability = 0.80

                elif action == "SEND_REMINDER":
                    probability = 0.55

            elif failure_reason == "card_expired":

                if action == "SUGGEST_ALTERNATIVE_PAYMENT":
                    probability = 0.90

                elif action == "SEND_REMINDER":
                    probability = 0.70

            elif failure_reason == "insufficient_funds":

                if action == "RETRY_LATER":
                    probability = 0.75

                elif action == "SEND_REMINDER":
                    probability = 0.60

        # -----------------------------------
        # OVERDUE INVOICE
        # -----------------------------------

        elif event_type == "overdue_invoice":

            if failure_reason == "forgotten_invoice":

                if action == "SEND_REMINDER":
                    probability = 0.85

                elif action == "ESCALATE_TO_HUMAN":
                    probability = 0.40

            elif failure_reason == "invoice_dispute":

                if action == "ESCALATE_TO_HUMAN":
                    probability = 0.85

                elif action == "SEND_REMINDER":
                    probability = 0.30

            elif failure_reason == "cash_flow_issue":

                if action == "RETRY_LATER":
                    probability = 0.65

                elif action == "ESCALATE_TO_HUMAN":
                    probability = 0.55

        # -----------------------------------
        # CUSTOMER BEHAVIOR MODIFIERS
        # -----------------------------------

        success_rate = float(event["previous_success_rate"])
        engagement = float(event["customer_engagement"])

        probability += (success_rate - 0.5) * 0.15
        probability += (engagement - 0.5) * 0.10

        # Retry fatigue
        retry_count = int(event["retry_count"])

        if retry_count >= 3 and action in [
            "RETRY_NOW",
            "RETRY_LATER"
        ]:
            probability -= 0.20

        # Contact fatigue
        contact_count = int(
            event["previous_contact_count"]
        )

        if contact_count >= 3 and action in [
            "SEND_REMINDER",
            "OFFER_INCENTIVE"
        ]:
            probability -= 0.15

        # Keep probability valid
        probability = max(0.01, min(probability, 0.95))

        return probability

    def execute_action(self, event, action):
        """
        Executes an action inside the hidden environment.
        """

        if action == "STOP":
            return {
                "success": False,
                "recovered_amount": 0,
                "probability": 0
            }

        probability = self.get_success_probability(
            event,
            action
        )

        success = (
            self.random.random() < probability
        )

        recovered_amount = (
            float(event["amount"])
            if success
            else 0
        )

        return {
            "success": success,
            "recovered_amount": recovered_amount,
            "probability": round(probability, 3)
        }