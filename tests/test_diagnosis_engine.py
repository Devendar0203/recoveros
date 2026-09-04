from simulator.diagnosis_engine import DiagnosisEngine


def test_diagnosis_engine():
    engine = DiagnosisEngine()

    test_cases = [
        (
            "insufficient_funds",
            "INSUFFICIENT_FUNDS",
            "CUSTOMER_FUNDS",
            0.96,
        ),
        (
            "payment_timed_out",
            "PAYMENT_TIMED_OUT",
            "TEMPORARY_TECHNICAL",
            0.94,
        ),
        (
            "card_expired",
            "CARD_EXPIRED",
            "PAYMENT_METHOD",
            0.98,
        ),
        (
            "authentication_failed",
            "AUTHENTICATION_FAILED",
            "PAYMENT_AUTHENTICATION",
            0.95,
        ),
        (
            "issuer_down",
            "ISSUER_DOWN",
            "ISSUER_DEGRADATION",
            0.93,
        ),
        (
            "network_error",
            "NETWORK_ERROR",
            "TEMPORARY_TECHNICAL",
            0.90,
        ),
        (
            "unknown_failure",
            "UNKNOWN",
            "UNKNOWN",
            0.40,
        ),
    ]

    for (
        failure_reason,
        expected_root_cause,
        expected_category,
        expected_confidence,
    ) in test_cases:

        result = engine.diagnose({
            "failure_reason": failure_reason
        })

        assert result["root_cause"] == expected_root_cause
        assert result["category"] == expected_category
        assert result["confidence"] == expected_confidence


if __name__ == "__main__":
    test_diagnosis_engine()

    print("=" * 50)
    print("DIAGNOSIS ENGINE TEST")
    print("=" * 50)
    print("All diagnosis cases passed.")
    print("=" * 50)