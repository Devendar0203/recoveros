import random
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)


NUM_EVENTS = 500


EVENT_TYPES = [
    "payment_failure",
    "checkout_abandonment",
    "subscription_failure",
    "overdue_invoice",
]

PAYMENT_METHODS = [
    "upi",
    "card",
    "netbanking",
    "wallet",
]

FAILURE_REASONS = {
    "payment_failure": [
        "insufficient_funds",
        "temporary_bank_failure",
        "technical_error",
        "authentication_failed",
        "payment_timeout",
    ],
    "checkout_abandonment": [
        "high_friction",
        "payment_method_unavailable",
        "price_hesitation",
        "unknown",
    ],
    "subscription_failure": [
        "mandate_failed",
        "insufficient_funds",
        "card_expired",
        "authentication_failed",
    ],
    "overdue_invoice": [
        "customer_delay",
        "invoice_dispute",
        "cash_flow_issue",
        "forgotten_invoice",
    ],
}


def generate_event():
    event_type = random.choice(EVENT_TYPES)

    amount = round(
        random.uniform(500, 100000),
        2
    )

    previous_success_rate = round(
        random.uniform(0.2, 1.0),
        2
    )

    customer_lifetime_value = round(
        random.uniform(1000, 500000),
        2
    )

    retry_count = random.randint(0, 4)

    previous_contact_count = random.randint(0, 5)

    hours_since_event = random.randint(1, 168)

    customer_engagement = round(
        random.uniform(0, 1),
        2
    )

    event_time = (
        datetime.now()
        - timedelta(hours=hours_since_event)
    )

    event = {
        "event_id": str(uuid.uuid4()),

        "customer_id": (
            f"CUST_{random.randint(1000, 9999)}"
        ),

        "event_type": event_type,

        "amount": amount,

        "payment_method": random.choice(
            PAYMENT_METHODS
        ),

        "failure_reason": random.choice(
            FAILURE_REASONS[event_type]
        ),

        "retry_count": retry_count,

        "previous_contact_count":
            previous_contact_count,

        "customer_lifetime_value":
            customer_lifetime_value,

        "previous_success_rate":
            previous_success_rate,

        "customer_engagement":
            customer_engagement,

        "hours_since_event":
            hours_since_event,

        "event_timestamp":
            event_time.isoformat(),
    }

    return event


def generate_dataset(num_events=NUM_EVENTS):

    events = []

    for _ in range(num_events):
        event = generate_event()
        events.append(event)

    df = pd.DataFrame(events)

    return df


if __name__ == "__main__":

    df = generate_dataset()

    output_path = "data/revenue_events.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Generated {len(df)} revenue events"
    )

    print(f"Saved to: {output_path}")

    print("\nSample data:")

    print(df.head())