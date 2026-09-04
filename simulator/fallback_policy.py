class FallbackPolicy:
    """
    Safe deterministic recovery policy used when
    the ML model is unavailable or fails.

    The fallback policy is:
    - deterministic
    - explainable
    - bounded
    - safe
    """

    MAX_RETRIES = 3
    MAX_CONTACTS = 3

    def choose_action(self, event):
        """
        Select a safe recovery action using deterministic rules.
        """

        event_type = str(
            event.get(
                "event_type",
                "unknown"
            )
        )

        failure_reason = str(
            event.get(
                "failure_reason",
                "unknown"
            )
        )

        retry_count = int(
            event.get(
                "retry_count",
                0
            )
        )

        previous_contact_count = int(
            event.get(
                "previous_contact_count",
                0
            )
        )

        amount = float(
            event.get(
                "amount",
                0.0
            )
        )

        # ==================================================
        # RULE 1 — INVALID REVENUE
        # ==================================================

        if amount <= 0:

            return {
                "action": "STOP",
                "reason": (
                    "Revenue amount is zero or invalid. "
                    "Recovery execution is not allowed."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 2 — MAXIMUM RETRIES
        # ==================================================

        if retry_count >= self.MAX_RETRIES:

            return {
                "action": "ESCALATE_TO_HUMAN",
                "reason": (
                    "Maximum retry limit has been reached. "
                    "Further automated retries are blocked."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 3 — MAXIMUM CUSTOMER CONTACTS
        # ==================================================

        if previous_contact_count >= self.MAX_CONTACTS:

            return {
                "action": "STOP",
                "reason": (
                    "Maximum customer contact limit has "
                    "been reached. Automated outreach stopped."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 4 — CARD / PAYMENT METHOD PROBLEM
        # ==================================================

        if failure_reason in [
            "authentication_failed",
            "card_expired",
        ]:

            return {
                "action": "SUGGEST_ALTERNATIVE_PAYMENT",
                "reason": (
                    "The failure indicates a payment-method "
                    "problem. An alternative payment method "
                    "is safer than an immediate retry."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 5 — TEMPORARY TECHNICAL FAILURE
        # ==================================================

        if failure_reason in [
            "technical_error",
            "payment_timeout",
            "timeout",
            "network_error",
        ]:

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "The failure appears temporary or technical. "
                    "A delayed retry is preferred over an "
                    "immediate retry."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 6 — INSUFFICIENT FUNDS
        # ==================================================

        if failure_reason == "insufficient_funds":

            return {
                "action": "RETRY_LATER",
                "reason": (
                    "Insufficient funds may be temporary. "
                    "A delayed retry is selected instead of "
                    "an immediate retry."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 7 — PAYMENT DECLINED
        # ==================================================

        if failure_reason == "payment_declined":

            return {
                "action": "SUGGEST_ALTERNATIVE_PAYMENT",
                "reason": (
                    "The payment was declined. An alternative "
                    "payment method is safer than repeated "
                    "immediate retries."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 8 — CUSTOMER CANCELLATION
        # ==================================================

        if failure_reason == "customer_cancelled":

            return {
                "action": "STOP",
                "reason": (
                    "The customer explicitly cancelled the "
                    "transaction. Automated recovery is stopped."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 9 — CHECKOUT ABANDONMENT
        # ==================================================

        if event_type == "checkout_abandonment":

            return {
                "action": "SEND_REMINDER",
                "reason": (
                    "Checkout was abandoned. A reminder is "
                    "the safest bounded recovery action."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 10 — SUBSCRIPTION CANCELLATION
        # ==================================================

        if event_type == "subscription_cancellation":

            return {
                "action": "SEND_REMINDER",
                "reason": (
                    "The subscription event requires a "
                    "non-invasive recovery attempt before "
                    "escalation."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # RULE 11 — OVERDUE INVOICE
        # ==================================================

        if event_type == "invoice_overdue":

            return {
                "action": "SEND_REMINDER",
                "reason": (
                    "The invoice is overdue. A reminder is "
                    "selected as the bounded first recovery action."
                ),
                "decision_source": "FALLBACK_POLICY",
                "fallback_used": True,
            }

        # ==================================================
        # DEFAULT SAFE ACTION
        # ==================================================

        return {
            "action": "SEND_REMINDER",
            "reason": (
                "The ML recommendation was unavailable and "
                "no specialized recovery rule matched. "
                "Using the default safe recovery action."
            ),
            "decision_source": "FALLBACK_POLICY",
            "fallback_used": True,
        }