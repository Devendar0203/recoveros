
class DiagnosisEngine:
    """
    RecoverOS Root Cause Diagnosis Engine.

    Converts gateway/payment failure information
    into a normalized root-cause category.

    This is intentionally deterministic and explainable.
    """

    DIAGNOSES = {
        "INSUFFICIENT_FUNDS": {
            "category": "CUSTOMER_FUNDS",
            "confidence": 0.96,
            "actions": [
                "RETRY_LATER",
                "SUGGEST_ALTERNATIVE_PAYMENT",
            ],
        },

        "PAYMENT_TIMED_OUT": {
            "category": "TEMPORARY_TECHNICAL",
            "confidence": 0.94,
            "actions": [
                "RETRY_LATER",
                "RETRY_NOW",
            ],
        },

        "CARD_EXPIRED": {
            "category": "PAYMENT_METHOD",
            "confidence": 0.98,
            "actions": [
                "SUGGEST_ALTERNATIVE_PAYMENT",
            ],
        },

        "AUTHENTICATION_FAILED": {
            "category": "PAYMENT_AUTHENTICATION",
            "confidence": 0.95,
            "actions": [
                "SUGGEST_ALTERNATIVE_PAYMENT",
                "SEND_REMINDER",
            ],
        },

        "ISSUER_DOWN": {
            "category": "ISSUER_DEGRADATION",
            "confidence": 0.93,
            "actions": [
                "RETRY_LATER",
            ],
        },

        "NETWORK_ERROR": {
            "category": "TEMPORARY_TECHNICAL",
            "confidence": 0.90,
            "actions": [
                "RETRY_LATER",
            ],
        },

        "BANK_TEMPORARY_FAILURE": {
            "category": "TEMPORARY_TECHNICAL",
            "confidence": 0.92,
            "actions": [
                "RETRY_LATER",
            ],
        },

        "MANDATE_FAILURE": {
            "category": "SUBSCRIPTION_PAYMENT",
            "confidence": 0.94,
            "actions": [
                "RETRY_LATER",
                "SUGGEST_ALTERNATIVE_PAYMENT",
            ],
        },

        "PAYMENT_METHOD_UNAVAILABLE": {
            "category": "PAYMENT_METHOD",
            "confidence": 0.91,
            "actions": [
                "SUGGEST_ALTERNATIVE_PAYMENT",
            ],
        },

        "CUSTOMER_DELAY": {
            "category": "INVOICE_COLLECTION",
            "confidence": 0.90,
            "actions": [
                "SEND_REMINDER",
            ],
        },

        "INVOICE_DISPUTE": {
            "category": "INVOICE_COLLECTION",
            "confidence": 0.93,
            "actions": [
                "ESCALATE_TO_HUMAN",
                "SEND_REMINDER",
            ],
        },

        "FORGOTTEN_INVOICE": {
            "category": "INVOICE_COLLECTION",
            "confidence": 0.95,
            "actions": [
                "SEND_REMINDER",
            ],
        },

        "UNKNOWN": {
            "category": "UNKNOWN",
            "confidence": 0.40,
            "actions": [
                "ESCALATE_TO_HUMAN",
            ],
        },
    }

    REASON_ALIASES = {
        "insufficient_funds":
            "INSUFFICIENT_FUNDS",

        "payment_timed_out":
            "PAYMENT_TIMED_OUT",

        "payment_timeout":
            "PAYMENT_TIMED_OUT",

        "timed_out":
            "PAYMENT_TIMED_OUT",

        "timeout":
            "PAYMENT_TIMED_OUT",

        "card_expired":
            "CARD_EXPIRED",

        "expired_card":
            "CARD_EXPIRED",

        "authentication_failed":
            "AUTHENTICATION_FAILED",

        "issuer_down":
            "ISSUER_DOWN",

        "network_error":
            "NETWORK_ERROR",

        "technical_error":
            "NETWORK_ERROR",

        "temporary_bank_failure":
            "BANK_TEMPORARY_FAILURE",

        "mandate_failed":
            "MANDATE_FAILURE",

        "payment_method_unavailable":
            "PAYMENT_METHOD_UNAVAILABLE",

        "customer_delay":
            "CUSTOMER_DELAY",

        "invoice_dispute":
            "INVOICE_DISPUTE",

        "forgotten_invoice":
            "FORGOTTEN_INVOICE",
    }

    def diagnose(self, event):
        """
        Diagnose the root cause of a payment failure.
        """

        reason = str(
            event.get(
                "failure_reason",
                event.get(
                    "reason",
                    "unknown"
                )
            )
        ).lower().strip()

        normalized = self.REASON_ALIASES.get(
            reason,
            "UNKNOWN"
        )

        diagnosis = self.DIAGNOSES.get(
            normalized,
            self.DIAGNOSES["UNKNOWN"]
        )

        return {
            "root_cause": normalized,

            "category":
                diagnosis["category"],

            "confidence":
                diagnosis["confidence"],

            "recommended_actions":
                diagnosis["actions"],

            "raw_failure_reason":
                reason,

            "diagnosis_source":
                "RULE_BASED_GATEWAY_TAXONOMY",
        }
