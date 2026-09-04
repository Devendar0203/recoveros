"""Append-only CSV audit trail for RecoverOS decisions."""

import csv
import os
import uuid
from datetime import datetime


class AuditLogger:
    FIELDNAMES = [
        "audit_id", "timestamp", "event_id", "event_type", "gateway_signal",
        "failure_reason", "diagnosis_confidence", "amount", "retry_count",
        "previous_contact_count", "proposed_action", "final_action",
        "decision_source", "fallback_used", "policy_allowed", "policy_reason",
        "execution_status", "success", "recovered_amount", "success_probability",
    ]

    def __init__(self, output_path="data/audit_log.csv"):
        self.output_path = output_path
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self._initialize_file()

    def _initialize_file(self):
        if os.path.exists(self.output_path) and os.path.getsize(self.output_path) > 0:
            return
        with open(self.output_path, "w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=self.FIELDNAMES).writeheader()

    def log_decision(self, decision, execution_result):
        event = decision["event"]
        diagnosis = decision["diagnosis"]
        proposed = decision["proposed"]
        policy = decision["policy"]
        record = {
            "audit_id": f"AUD-{uuid.uuid4()}",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_id": event.get("event_id", ""),
            "event_type": event.get("event_type", ""),
            "gateway_signal": event.get("gateway_signal", ""),
            "failure_reason": diagnosis["root_cause"],
            "diagnosis_confidence": diagnosis["confidence"],
            "amount": event.get("amount", 0.0),
            "retry_count": event.get("retry_count", 0),
            "previous_contact_count": event.get("previous_contact_count", 0),
            "proposed_action": proposed["action"],
            "final_action": policy["final_action"],
            "decision_source": "fallback" if decision["fallback_used"] else "ml",
            "fallback_used": decision["fallback_used"],
            "policy_allowed": policy["allowed"],
            "policy_reason": policy["reason"],
            "execution_status": execution_result.get("status", "UNKNOWN"),
            "success": execution_result.get("success", False),
            "recovered_amount": execution_result.get("recovered_amount", 0.0),
            "success_probability": proposed.get("success_probability", 0.0),
        }
        with open(self.output_path, "a", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=self.FIELDNAMES).writerow(record)
        return record

    # Backward-compatible interface used by existing benchmark scripts.
    def log(self, event, proposed_action, policy_result, execution_result):
        decision = {
            "event": event,
            "diagnosis": {"root_cause": event.get("failure_reason", "unknown"), "confidence": 1.0},
            "proposed": {"action": proposed_action, "success_probability": execution_result.get("success_probability", execution_result.get("probability", 0.0))},
            "policy": policy_result,
            "fallback_used": False,
        }
        return self.log_decision(decision, execution_result)
