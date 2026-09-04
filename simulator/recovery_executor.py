import hashlib
from datetime import datetime


class RecoveryExecutor:

    def execute(self, event, action, score):

        event_id = str(event["event_id"])

        # Deterministic value for reproducible demo results
        seed = f"{event_id}_{action}"
        hash_value = hashlib.md5(
            seed.encode()
        ).hexdigest()

        random_value = int(
            hash_value[:8],
            16
        ) / 0xFFFFFFFF

        success_probability = float(
            score["success_probability"]
        )

        success = random_value < success_probability

        recovered_amount = (
            float(event["amount"])
            if success
            else 0.0
        )

        return {
            "event_id": event_id,
            "action": action,
            "success": success,
            "recovered_amount": recovered_amount,
            "success_probability": success_probability,
            "random_value": round(random_value, 4),
            "timestamp": datetime.now().isoformat()
        }