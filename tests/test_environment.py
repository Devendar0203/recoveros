import unittest
import pandas as pd

from simulator.recovery_environment import RecoveryEnvironment


class TestRecoveryEnvironment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(
            "data/revenue_events.csv"
        )
        cls.environment = RecoveryEnvironment()
        cls.event = cls.df.iloc[0].to_dict()

    def test_all_actions_return_valid_results(self):

        actions = [
            "RETRY_NOW",
            "RETRY_LATER",
            "SEND_REMINDER",
            "SUGGEST_ALTERNATIVE_PAYMENT",
            "OFFER_INCENTIVE",
            "ESCALATE_TO_HUMAN",
            "STOP",
        ]

        for action in actions:

            with self.subTest(action=action):

                result = self.environment.execute_action(
                    self.event,
                    action
                )

                self.assertIn(
                    "success",
                    result
                )

                self.assertIn(
                    "recovered_amount",
                    result
                )

                self.assertIn(
                    "success_probability",
                    result
                )

                self.assertIn(
                    "probability",
                    result
                )

                self.assertIn(
                    "random_value",
                    result
                )

    def test_probability_alias_matches_success_probability(self):

        result = self.environment.execute_action(
            self.event,
            "RETRY_LATER"
        )

        self.assertEqual(
            result["probability"],
            result["success_probability"]
        )

    def test_stop_action(self):

        result = self.environment.execute_action(
            self.event,
            "STOP"
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["recovered_amount"],
            0.0
        )

        self.assertEqual(
            result["probability"],
            0.0
        )

    def test_deterministic_results(self):

        first = self.environment.execute_action(
            self.event,
            "RETRY_LATER"
        )

        second = self.environment.execute_action(
            self.event,
            "RETRY_LATER"
        )

        self.assertEqual(
            first,
            second
        )


if __name__ == "__main__":
    unittest.main()