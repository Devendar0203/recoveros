
import streamlit as st
import pandas as pd
import uuid
import os
from datetime import datetime

from simulator.ml_action_scorer import MLActionScorer
from simulator.recovery_executor import RecoveryExecutor
from simulator.recovery_workflow import RecoveryWorkflow
from simulator.audit_logger import AuditLogger
from simulator.batch_recovery import BatchRecoverySimulator
from simulator.policy_engine import RecoveryPolicyEngine


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RecoverOS",
    page_icon="💰",
    layout="wide",
)


# ============================================================
# INITIALIZATION
# ============================================================

@st.cache_resource
def create_workflow():

    scorer = MLActionScorer()
    executor = RecoveryExecutor()

    return RecoveryWorkflow(
        scorer,
        executor
    )


@st.cache_resource
def create_batch_simulator():
    return BatchRecoverySimulator(
        MLActionScorer(),
        RecoveryPolicyEngine(),
        seed=42,
    )


workflow = create_workflow()
batch_simulator = create_batch_simulator()


if "event" not in st.session_state:
    st.session_state.event = None

if "scores" not in st.session_state:
    st.session_state.scores = []

if "recommended_action" not in st.session_state:
    st.session_state.recommended_action = None

if "decision" not in st.session_state:
    st.session_state.decision = None

if "execution_result" not in st.session_state:
    st.session_state.execution_result = None

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if "batch_results" not in st.session_state:
    st.session_state.batch_results = None


audit_logger = AuditLogger()


# ============================================================
# DATA / OPTIONS
# ============================================================

EVENT_TYPES = [
    "payment_failure",
    "checkout_abandonment",
    "subscription_failure",
    "overdue_invoice",
]

FAILURE_REASONS = [
    "insufficient_funds",
    "temporary_bank_failure",
    "technical_error",
    "authentication_failed",
    "payment_timeout",
    "high_friction",
    "payment_method_unavailable",
    "price_hesitation",
    "unknown",
    "mandate_failed",
    "card_expired",
    "customer_delay",
    "invoice_dispute",
    "cash_flow_issue",
    "forgotten_invoice",
]


def get_audit_dataframe():

    if not st.session_state.audit_log:
        return pd.DataFrame()

    return pd.DataFrame(
        st.session_state.audit_log
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("RecoverOS")

st.sidebar.subheader("Recovery Event")

event_type = st.sidebar.selectbox(
    "Event Type",
    EVENT_TYPES,
)

failure_reason = st.sidebar.selectbox(
    "Reported Failure Reason",
    FAILURE_REASONS,
)

gateway_signal = st.sidebar.selectbox(
    "Gateway / Payment Signal",
    [
        "insufficient_funds",
        "card_expired",
        "timeout",
        "network_error",
        "payment_declined",
        "customer_cancelled",
        "fraud_suspected",
    ],
)

simulate_model_failure = st.sidebar.checkbox(
    "Demo: simulate ML model failure",
    help=(
        "Shows RecoverOS selecting a safe deterministic "
        "fallback and recording it in the audit trail."
    ),
)

amount = st.sidebar.number_input(
    "Revenue at Risk (₹)",
    min_value=0.0,
    value=50000.0,
    step=1000.0,
)

retry_count = st.sidebar.number_input(
    "Retry Count",
    min_value=0,
    value=0,
    step=1,
)

customer_lifetime_value = st.sidebar.number_input(
    "Customer Lifetime Value (₹)",
    min_value=0.0,
    value=100000.0,
    step=1000.0,
)

previous_success_rate = st.sidebar.slider(
    "Previous Success Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
)

customer_engagement = st.sidebar.slider(
    "Customer Engagement",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
)

previous_contact_count = st.sidebar.number_input(
    "Previous Contact Count",
    min_value=0,
    value=0,
    step=1,
)

hours_since_event = st.sidebar.number_input(
    "Hours Since Event",
    min_value=0.0,
    value=24.0,
    step=1.0,
)


# ============================================================
# CREATE EVENT
# ============================================================

if st.sidebar.button(
    "🤖 Analyze Event",
    width="stretch",
):

    event = {
        "event_id": str(uuid.uuid4()),

        "event_type": event_type,

        "failure_reason": failure_reason,

        "gateway_signal": gateway_signal,

        "simulate_model_failure": simulate_model_failure,

        "amount": float(amount),

        "retry_count": int(retry_count),

        "customer_lifetime_value": float(
            customer_lifetime_value
        ),

        "previous_success_rate": float(
            previous_success_rate
        ),

        "customer_engagement": float(
            customer_engagement
        ),

        "previous_contact_count": int(
            previous_contact_count
        ),

        "hours_since_event": float(
            hours_since_event
        ),
    }

    decision = workflow.analyze(event)

    st.session_state.event = event

    st.session_state.scores = decision["scores"]

    st.session_state.recommended_action = (
        decision["proposed"]
    )

    st.session_state.decision = decision

    st.session_state.execution_result = None


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🤖 AI Recommendation",
        "⚡ Execute Recovery",
        "📦 Batch Simulation",
        "📊 Analytics",
        "📜 Audit Log",
    ]
)


# ============================================================
# TAB 1 — AI RECOMMENDATION
# ============================================================

with tab1:

    st.header("AI Recovery Recommendation")

    if st.session_state.event is None:

        st.info(
            "👈 Configure a recovery event from the sidebar "
            "and click **Analyze Event**."
        )

    else:

        event = st.session_state.event

        recommended = (
            st.session_state.recommended_action
        )

        scores = st.session_state.scores

        st.subheader("📌 Event Details")

        event_col1, event_col2, event_col3 = (
            st.columns(3)
        )

        event_col1.metric(
            "Event Type",
            event["event_type"],
        )

        event_col2.metric(
            "Failure Reason",
            event["failure_reason"],
        )

        event_col3.metric(
            "Revenue at Risk",
            f"₹{event['amount']:,.2f}",
        )

        st.divider()

        st.subheader("🆙 Recommended Action")

        rec_col1, rec_col2, rec_col3 = st.columns(3)

        rec_col1.metric(
            "Action",
            recommended["action"],
        )

        rec_col2.metric(
            "Success Probability",
            f"{recommended['success_probability']:.2%}",
        )

        rec_col3.metric(
            "Expected Net Value",
            f"₹{recommended['net_expected_value']:,.2f}",
        )

        st.success(
            f"RecoverOS recommends: "
            f"**{st.session_state.decision['policy']['final_action']}**"
        )

        diagnosis = st.session_state.decision["diagnosis"]
        policy = st.session_state.decision["policy"]

        with st.expander(
            "🔎 Why this decision?",
            expanded=True
        ):

            st.write(
                f"**Root cause:** "
                f"{diagnosis['root_cause']} "
                f"({diagnosis['confidence']:.0%} confidence)"
            )

            for explanation in (
                st.session_state.decision["explanation"]
            ):

                st.write(
                    f"• {explanation}"
                )

            if st.session_state.decision["fallback_used"]:

                st.warning(
                    "ML scorer unavailable: safe fallback "
                    "policy was used. No model-based money "
                    "action is being taken."
                )

        # ====================================================
        # DECISION FLOW VISUALIZATION
        # ====================================================

        st.divider()

        st.subheader("🧠 Decision Flow")

        flow_col1, flow_col2, flow_col3, flow_col4, flow_col5 = (
            st.columns(5)
        )

        with flow_col1:

            st.metric(
                "1. ROOT CAUSE",
                diagnosis["root_cause"]
            )

            st.caption(
                f"{diagnosis['category']} • "
                f"{diagnosis['confidence']:.0%} confidence"
            )

        with flow_col2:

            st.metric(
                "2. ML RECOMMENDS",
                recommended["action"]
            )

            st.caption(
                f"Probability: "
                f"{recommended['success_probability']:.2%}"
            )

        with flow_col3:

            st.metric(
                "3. NET VALUE",
                f"₹{recommended['net_expected_value']:,.2f}"
            )

            st.caption(
                "Probability × amount − action cost"
            )

        with flow_col4:

            st.metric(
                "4. POLICY GATE",
                "APPROVED"
                if policy["allowed"]
                else "BLOCKED"
            )

            st.caption(
                policy["reason"]
            )

        with flow_col5:

            st.metric(
                "5. FINAL ACTION",
                policy["final_action"]
            )

            st.caption(
                "Execution follows policy"
            )

        st.info(
            "ML recommends → Policy controls → Execution records"
        )

        st.divider()

        st.subheader("📊 Action Comparison")

        display_scores = pd.DataFrame(scores)

        display_scores = display_scores[
            [
                "action",
                "success_probability",
                "gross_expected_value",
                "action_cost",
                "net_expected_value",
            ]
        ]

        display_scores.columns = [
            "Action",
            "Success Probability",
            "Gross Expected Recovery",
            "Action Cost",
            "Net Expected Value",
        ]

        st.dataframe(
            display_scores,
            width="stretch",
        )

        st.subheader("Expected Net Value by Action")

        chart_data = pd.DataFrame(scores)

        chart_data = chart_data.set_index(
            "action"
        )

        st.bar_chart(
            chart_data["net_expected_value"]
        )


# ============================================================
# TAB 2 — EXECUTE RECOVERY
# ============================================================

with tab2:

    st.header("Recovery Execution")

    if st.session_state.event is None:

        st.info(
            "Analyze an event first before executing "
            "a recovery action."
        )

    else:

        event = st.session_state.event

        recommended = (
            st.session_state.recommended_action
        )

        decision = st.session_state.decision

        st.subheader("Final Recovery Strategy")

        st.write(
            f"### 🤖 {decision['policy']['final_action']}"
        )

        st.write(
            "Success Probability: "
            f"**{recommended['success_probability']:.2%}**"
        )

        st.write(
            "Expected Net Value: "
            f"**₹{recommended['net_expected_value']:,.2f}**"
        )

        st.divider()

        can_execute = (
            st.session_state.execution_result is None
        )

        if st.button(
            "⚡ Execute Recovery",
            width="stretch",
            disabled=not can_execute,
        ):

            try:

                result = workflow.execute(
                    decision
                )

                st.session_state.execution_result = (
                    result
                )

                audit_entry = audit_logger.log_decision(
                    decision,
                    result
                )

                st.session_state.audit_log.append(
                    audit_entry
                )

                st.success(
                    f"Execution status: {result['status']}"
                )

            except Exception as e:

                st.error(
                    f"Recovery execution error: {e}"
                )


# ============================================================
# TAB 3 — BATCH SIMULATION
# ============================================================

with tab3:

    st.header("Live Batch Recovery Simulation")

    st.write(
        "Run RecoverOS across the same 100 unseen payment events used for "
        "evaluation. The dashboard calculates recovered revenue live and "
        "compares it with a fixed baseline on the identical cohort."
    )

    if st.button("▶ Run 100-Event Recovery Batch", width="stretch"):
        try:
            evaluation_events = pd.read_csv("data/evaluation_events.csv")
            st.session_state.batch_results = {
                "baseline": batch_simulator.run_baseline(evaluation_events),
                "ml_policy": batch_simulator.run_ml_policy(evaluation_events),
            }
        except Exception as error:
            st.error(f"Batch simulation failed: {error}")

    if st.session_state.batch_results is None:
        st.info("Run the batch to display live recovery and policy metrics.")
    else:
        baseline = st.session_state.batch_results["baseline"]
        ml_policy = st.session_state.batch_results["ml_policy"]
        additional_revenue = (
            ml_policy["revenue_recovered"]
            - baseline["revenue_recovered"]
        )
        improvement = (
            additional_revenue / baseline["revenue_recovered"] * 100
            if baseline["revenue_recovered"]
            else 0.0
        )

        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("Events Evaluated", ml_policy["events"])
        metric2.metric(
            "ML + Policy Revenue Recovered",
            f"₹{ml_policy['revenue_recovered']:,.2f}",
        )
        metric3.metric(
            "Additional vs Baseline",
            f"₹{additional_revenue:,.2f}",
            f"{improvement:+.2f}%",
        )
        metric4.metric(
            "Revenue Recovery Rate",
            f"{ml_policy['revenue_recovery_rate']:.2f}%",
        )

        st.caption(
            "Counterfactual simulation: each strategy is evaluated with the "
            "same deterministic environment, unseen event cohort, and seed."
        )

        comparison = pd.DataFrame([
            {
                "Strategy": baseline["strategy"],
                "Recovered Revenue": baseline["revenue_recovered"],
                "Revenue Recovery Rate": baseline["revenue_recovery_rate"] / 100,
                "Event Success Rate": baseline["event_recovery_rate"] / 100,
            },
            {
                "Strategy": ml_policy["strategy"],
                "Recovered Revenue": ml_policy["revenue_recovered"],
                "Revenue Recovery Rate": ml_policy["revenue_recovery_rate"] / 100,
                "Event Success Rate": ml_policy["event_recovery_rate"] / 100,
            },
        ])
        st.subheader("Strategy Comparison")
        st.dataframe(comparison, width="stretch", hide_index=True)

        policy1, policy2, policy3 = st.columns(3)
        policy1.metric("Successful Recoveries", ml_policy["successful_recoveries"])
        policy2.metric("Policy Stops", ml_policy["policy_stops"])
        policy3.metric("Human Escalations", ml_policy["human_escalations"])

        st.subheader("Final Action Distribution")
        st.bar_chart(pd.Series(ml_policy["action_counts"], name="Events"))

        st.subheader("Batch Decision Records")
        st.dataframe(ml_policy["details"], width="stretch", hide_index=True)
        st.download_button(
            "⬇️ Download Batch Decision Records",
            ml_policy["details"].to_csv(index=False).encode("utf-8"),
            file_name="recoveros_batch_results.csv",
            mime="text/csv",
            width="stretch",
        )


# ============================================================
# TAB 4 — ANALYTICS
# ============================================================

with tab4:

    st.header("RecoverOS Analytics")

    audit_df = get_audit_dataframe()

    if audit_df.empty:

        st.info(
            "No recovery executions yet. "
            "Execute a recovery to see analytics."
        )

    else:

        total_events = len(audit_df)

        successful_events = int(
            audit_df["success"].sum()
        )

        total_recovered = float(
            audit_df["recovered_amount"].sum()
        )

        success_rate = (
            successful_events / total_events
        ) * 100

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Events Processed",
            total_events,
        )

        col2.metric(
            "Successful Recoveries",
            successful_events,
        )

        col3.metric(
            "Success Rate",
            f"{success_rate:.2f}%",
        )

        col4.metric(
            "Revenue Recovered",
            f"₹{total_recovered:,.2f}",
        )

        st.divider()

        st.subheader("Recovery Action Distribution")

        action_counts = (
            audit_df["proposed_action"]
            .value_counts()
        )

        st.bar_chart(action_counts)

        st.subheader("Recovered Revenue per Event")

        recovery_chart = audit_df[
            [
                "event_id",
                "recovered_amount",
            ]
        ]

        recovery_chart = (
            recovery_chart.set_index(
                "event_id"
            )
        )

        st.bar_chart(
            recovery_chart
        )


# ============================================================
# TAB 5 — AUDIT LOG
# ============================================================

with tab5:

    st.header("Recovery Audit Log")

    audit_df = get_audit_dataframe()

    if audit_df.empty:

        st.info(
            "The audit log is currently empty."
        )

    else:

        st.dataframe(
            audit_df,
            width="stretch",
        )

        csv = audit_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Audit Log",
            data=csv,
            file_name="recoveros_audit_log.csv",
            mime="text/csv",
            width="stretch",
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RecoverOS • AI-Powered Revenue Recovery "
    "Decision System • ML + Policy Engine"
)

