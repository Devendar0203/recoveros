class RecoveryPolicyEngine:
    """
    Safety and compliance layer for RecoverOS.

    The policy engine decides whether an action
    can be automated, should be escalated,
    or must be stopped.
    """

    MAX_RETRIES = 3
    MAX_CONTACTS = 3

    def evaluate(self, event, proposed_action):

        event_type = event["event_type"]

        retry_count = int(event["retry_count"])
        contact_count = int(event["previous_contact_count"])

        amount = float(event["amount"])

        reason = event["failure_reason"]
        gateway_signal = event.get("gateway_signal")
        if (
            reason == "fraud_suspected"
            or gateway_signal == "fraud_suspected"
        ):
            return {
                "allowed": False,
                "final_action": "ESCALATE_TO_HUMAN",
                "reason": "Fraud suspicion requires human review"
            }

        if reason == "customer_cancelled":
            return {
                "allowed": False,
                "final_action": "STOP",
                "reason": "Customer cancellation must not trigger automated recovery"
            }

        # --------------------------------------
        # HARD STOP: RETRY FATIGUE
        # --------------------------------------

        if (
            proposed_action in ["RETRY_NOW", "RETRY_LATER"]
            and retry_count >= self.MAX_RETRIES
        ):
            return {
                "allowed": False,
                "final_action": "STOP",
                "reason": "Maximum retry limit reached"
            }

        # --------------------------------------
        # CONTACT FATIGUE
        # --------------------------------------

        if (
            proposed_action in [
                "SEND_REMINDER",
                "OFFER_INCENTIVE"
            ]
            and contact_count >= self.MAX_CONTACTS
        ):
            return {
                "allowed": False,
                "final_action": "STOP",
                "reason": "Maximum customer contact limit reached"
            }

        # --------------------------------------
        # HIGH VALUE DISPUTES
        # --------------------------------------

        if (
            reason == "invoice_dispute"
            and amount >= 50000
        ):
            return {
                "allowed": False,
                "final_action": "ESCALATE_TO_HUMAN",
                "reason": "High-value invoice dispute"
            }

        # --------------------------------------
        # HIGH VALUE RECOVERY
        # --------------------------------------

        if (
            amount >= 100000
            and proposed_action == "OFFER_INCENTIVE"
        ):
            return {
                "allowed": False,
                "final_action": "ESCALATE_TO_HUMAN",
                "reason": "High-value incentive requires approval"
            }

        # --------------------------------------
        # DEFAULT
        # --------------------------------------

        return {
            "allowed": True,
            "final_action": proposed_action,
            "reason": "Action approved by policy"
        }
