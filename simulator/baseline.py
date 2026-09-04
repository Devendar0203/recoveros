class BaselineRecoveryStrategy:
    """
    Traditional rule-based recovery strategy.

    This represents a simple system without
    intelligent decision-making.
    """

    def choose_action(self, event):

        event_type = event["event_type"]

        if event_type == "payment_failure":
            return "RETRY_NOW"

        elif event_type == "checkout_abandonment":
            return "SEND_REMINDER"

        elif event_type == "subscription_failure":
            return "RETRY_NOW"

        elif event_type == "overdue_invoice":
            return "SEND_REMINDER"

        return "STOP"