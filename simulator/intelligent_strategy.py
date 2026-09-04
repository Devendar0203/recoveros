class IntelligentRecoveryStrategy:
    """
    Version 1 of RecoverOS intelligence.

    Uses event context, failure reason,
    customer behavior, and stopping rules
    to choose a recovery action.
    """

    def choose_action(self, event):

        event_type = event["event_type"]
        reason = event["failure_reason"]

        retry_count = int(event["retry_count"])
        contact_count = int(event["previous_contact_count"])

        success_rate = float(event["previous_success_rate"])
        engagement = float(event["customer_engagement"])

        # ----------------------------------
        # STOPPING RULES
        # ----------------------------------

        # Too many retries
        if retry_count >= 3 and event_type in [
            "payment_failure",
            "subscription_failure"
        ]:
            return "STOP"

        # Too many contacts
        if contact_count >= 3 and event_type in [
            "checkout_abandonment",
            "overdue_invoice"
        ]:
            return "STOP"

        # Very low probability customer
        if success_rate < 0.25 and engagement < 0.20:
            return "STOP"

        # ----------------------------------
        # PAYMENT FAILURE
        # ----------------------------------

        if event_type == "payment_failure":

            if reason == "temporary_bank_failure":
                return "RETRY_LATER"

            elif reason == "insufficient_funds":
                return "RETRY_LATER"

            elif reason == "authentication_failed":
                return "SUGGEST_ALTERNATIVE_PAYMENT"

            elif reason == "payment_timeout":
                return "RETRY_NOW"

            elif reason == "technical_error":
                return "RETRY_LATER"

        # ----------------------------------
        # CHECKOUT ABANDONMENT
        # ----------------------------------

        elif event_type == "checkout_abandonment":

            if reason == "payment_method_unavailable":
                return "SUGGEST_ALTERNATIVE_PAYMENT"

            elif reason == "price_hesitation":
                return "OFFER_INCENTIVE"

            elif reason == "high_friction":

                if engagement > 0.50:
                    return "SUGGEST_ALTERNATIVE_PAYMENT"

                return "SEND_REMINDER"

            else:
                return "SEND_REMINDER"

        # ----------------------------------
        # SUBSCRIPTION FAILURE
        # ----------------------------------

        elif event_type == "subscription_failure":

            if reason == "mandate_failed":
                return "RETRY_LATER"

            elif reason == "card_expired":
                return "SUGGEST_ALTERNATIVE_PAYMENT"

            elif reason == "insufficient_funds":
                return "RETRY_LATER"

            elif reason == "authentication_failed":
                return "SUGGEST_ALTERNATIVE_PAYMENT"

        # ----------------------------------
        # OVERDUE INVOICE
        # ----------------------------------

        elif event_type == "overdue_invoice":

            if reason == "forgotten_invoice":
                return "SEND_REMINDER"

            elif reason == "invoice_dispute":
                return "ESCALATE_TO_HUMAN"

            elif reason == "cash_flow_issue":
                return "RETRY_LATER"

            elif reason == "customer_delay":

                if contact_count < 2:
                    return "SEND_REMINDER"

                return "ESCALATE_TO_HUMAN"

        return "STOP"