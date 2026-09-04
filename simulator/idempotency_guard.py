
import threading


class IdempotencyGuard:
    """
    RecoverOS Idempotency and Concurrency Guard.

    Prevents the same recovery event/action combination
    from being executed more than once.

    This implementation is intentionally lightweight and
    deterministic for the RecoverOS simulator.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._processed = set()

    def _key(self, event_id, action):
        return f"{event_id}:{action}"

    def check_and_claim(self, event_id, action):
        """
        Atomically check whether an event/action has already
        been claimed.

        Returns:
            {
                "allowed": True/False,
                "duplicate": True/False,
                "key": "...",
                "reason": "..."
            }
        """

        key = self._key(
            event_id,
            action
        )

        with self._lock:

            if key in self._processed:

                return {
                    "allowed": False,
                    "duplicate": True,
                    "key": key,
                    "reason":
                        "Duplicate recovery attempt blocked"
                }

            self._processed.add(key)

            return {
                "allowed": True,
                "duplicate": False,
                "key": key,
                "reason":
                    "Recovery attempt claimed successfully"
            }

    def is_processed(self, event_id, action):
        """
        Check whether an event/action combination has
        already been claimed.
        """

        key = self._key(
            event_id,
            action
        )

        with self._lock:
            return key in self._processed

    def reset(self):
        """
        Clear all claims.

        Useful for isolated simulator tests.
        """

        with self._lock:
            self._processed.clear()

