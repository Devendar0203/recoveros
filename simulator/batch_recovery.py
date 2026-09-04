"""Reproducible batch measurement for the RecoverOS demo."""

from collections import Counter

import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment


class BatchRecoverySimulator:
    """Evaluate a recovery strategy over the same unseen event cohort."""

    def __init__(self, scorer, policy_engine, seed=42):
        self.scorer = scorer
        self.policy_engine = policy_engine
        self.seed = seed

    def run_ml_policy(self, events):
        """Run the ML proposal and policy gate for every supplied event."""
        return self._run(events, self._ml_policy_action, "ML + Policy")

    def run_baseline(self, events):
        """Run the fixed baseline on the identical cohort for comparison."""
        return self._run(events, self._baseline_action, "Baseline")

    def _ml_policy_action(self, event):
        proposed = self.scorer.choose_best_action(event)
        policy = self.policy_engine.evaluate(event, proposed["action"])
        return proposed, policy["final_action"], policy["reason"]

    @staticmethod
    def _baseline_action(event):
        action = (
            "RETRY_NOW"
            if event["event_type"] == "payment_failure"
            else "SEND_REMINDER"
        )
        return {"action": action}, action, "Fixed baseline action"

    def _run(self, events, action_selector, strategy):
        environment = RecoveryEnvironment(seed=self.seed)
        records = []

        for _, row in events.iterrows():
            event = row.to_dict()
            proposed, final_action, policy_reason = action_selector(event)
            result = environment.execute_action(event, final_action)
            records.append({
                "event_id": event["event_id"],
                "amount_at_risk": float(event["amount"]),
                "proposed_action": proposed["action"],
                "final_action": final_action,
                "policy_reason": policy_reason,
                "success": result["success"],
                "recovered_amount": float(result["recovered_amount"]),
            })

        detail = pd.DataFrame(records)
        recovered = float(detail["recovered_amount"].sum())
        at_risk = float(detail["amount_at_risk"].sum())
        actions = Counter(detail["final_action"])

        return {
            "strategy": strategy,
            "events": len(detail),
            "revenue_at_risk": at_risk,
            "revenue_recovered": recovered,
            "revenue_recovery_rate": (recovered / at_risk * 100) if at_risk else 0.0,
            "successful_recoveries": int(detail["success"].sum()),
            "event_recovery_rate": float(detail["success"].mean() * 100) if len(detail) else 0.0,
            "policy_stops": int(actions["STOP"]),
            "human_escalations": int(actions["ESCALATE_TO_HUMAN"]),
            "action_counts": dict(actions),
            "details": detail,
        }
