
"""The recoverable, policy-gated RecoverOS decision workflow."""

from simulator.diagnosis_engine import DiagnosisEngine
from simulator.policy_engine import RecoveryPolicyEngine
from simulator.idempotency_guard import IdempotencyGuard


class RecoveryWorkflow:
    """Coordinates diagnosis, scoring, policy gating, and safe execution."""

    FALLBACK_ACTIONS = {
        "insufficient_funds": "RETRY_LATER",
        "card_expired": "SUGGEST_ALTERNATIVE_PAYMENT",
        "technical_error": "RETRY_LATER",
        "payment_declined": "SUGGEST_ALTERNATIVE_PAYMENT",
        "customer_cancelled": "STOP",
        "fraud_suspected": "ESCALATE_TO_HUMAN",
    }

    def __init__(
        self,
        scorer,
        executor,
        diagnosis_engine=None,
        policy_engine=None,
        idempotency_guard=None
    ):
        self.scorer = scorer
        self.executor = executor

        self.diagnosis_engine = (
            diagnosis_engine or DiagnosisEngine()
        )

        self.policy_engine = (
            policy_engine or RecoveryPolicyEngine()
        )

        self.idempotency_guard = (
            idempotency_guard or IdempotencyGuard()
        )

    def analyze(self, event):

        diagnosis = self.diagnosis_engine.diagnose(
            event
        )

        # Preserve the original event values for the
        # existing ML model. Normalized diagnosis is
        # stored separately in the decision result.
        enriched_event = dict(event)

        fallback_used = bool(
            event.get(
                "simulate_model_failure",
                False
            )
        )

        try:

            if fallback_used:
                raise RuntimeError(
                    "Simulated ML model outage"
                )

            scores = self.scorer.score_actions(
                enriched_event
            )

            proposed = scores[0]

            decision_source = (
                "ML action scorer"
            )

        except Exception as error:

            action = self.FALLBACK_ACTIONS.get(
                diagnosis["raw_failure_reason"],
                diagnosis["recommended_actions"][0]
                if diagnosis["recommended_actions"]
                else "ESCALATE_TO_HUMAN"
            )

            proposed = {
                "action": action,
                "success_probability": 0.0,
                "gross_expected_value": 0.0,
                "action_cost": 0.0,
                "net_expected_value": 0.0,
            }

            scores = [proposed]

            fallback_used = True

            decision_source = (
                f"Safe fallback policy ({error})"
            )

        policy = self.policy_engine.evaluate(
            enriched_event,
            proposed["action"]
        )

        explanation = [
            (
                f"Diagnosis: "
                f"{diagnosis['root_cause']} "
                f"({diagnosis['confidence']:.0%} "
                f"confidence from "
                f"{diagnosis['diagnosis_source']})."
            ),

            (
                f"{decision_source} "
                f"proposed {proposed['action']}."
            ),

            (
                f"Policy selected "
                f"{policy['final_action']}: "
                f"{policy['reason']}."
            ),
        ]

        if not fallback_used:

            explanation.insert(
                2,
                (
                    f"Expected net value: "
                    f"₹{proposed['net_expected_value']:,.2f}."
                )
            )

        return {
            "event": enriched_event,
            "diagnosis": diagnosis,
            "scores": scores,
            "proposed": proposed,
            "policy": policy,
            "fallback_used": fallback_used,
            "explanation": explanation,
        }

    def execute(self, decision):

        final_action = (
            decision["policy"]["final_action"]
        )

        if final_action == "STOP":

            return {
                "event_id":
                    decision["event"]["event_id"],

                "action":
                    final_action,

                "success":
                    False,

                "recovered_amount":
                    0.0,

                "status":
                    "STOPPED",

                "message":
                    "No recovery action was executed "
                    "because policy stopped it.",
            }

        if final_action == "ESCALATE_TO_HUMAN":

            return {
                "event_id":
                    decision["event"]["event_id"],

                "action":
                    final_action,

                "success":
                    False,

                "recovered_amount":
                    0.0,

                "status":
                    "PENDING_REVIEW",

                "message":
                    "No automated money action was "
                    "taken; the event is awaiting "
                    "human review.",
            }

        # -------------------------------------------------
        # IDEMPOTENCY / CONCURRENCY GUARD
        # -------------------------------------------------

        event_id = str(
            decision["event"]["event_id"]
        )

        claim = self.idempotency_guard.check_and_claim(
            event_id,
            final_action
        )

        if not claim["allowed"]:

            return {
                "event_id":
                    event_id,

                "action":
                    final_action,

                "success":
                    False,

                "recovered_amount":
                    0.0,

                "status":
                    "DUPLICATE_BLOCKED",

                "message":
                    claim["reason"],

                "idempotency_key":
                    claim["key"],

                "duplicate":
                    True,
            }

        # -------------------------------------------------
        # ACTUAL RECOVERY EXECUTION
        # -------------------------------------------------

        result = self.executor.execute(
            decision["event"],
            final_action,
            decision["proposed"]
        )

        result["status"] = (
            "COMPLETED"
            if result["success"]
            else "FAILED"
        )

        result["idempotency_key"] = (
            claim["key"]
        )

        result["duplicate"] = False

        return result

