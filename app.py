import streamlit as st
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Finance Email Agent",
    page_icon="📧",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #1E3A8A;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 40px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

.green {
    color: green;
    font-weight: bold;
}

.orange {
    color: orange;
    font-weight: bold;
}

.red {
    color: red;
    font-weight: bold;
}

.blue {
    color: #2563EB;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">📧 Finance Credit Follow-Up Email Agent</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">AI Powered Invoice Reminder & Escalation System</div>',
    unsafe_allow_html=True
)

# Read CSV
df = pd.read_csv("data.csv")

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("📄 Total Invoices", len(df))
col2.metric("💰 Total Amount", f"₹{df['amount'].sum()}")
col3.metric("⚠ Overdue Clients", len(df[df['days_overdue'] > 7]))
col4.metric("🚨 Critical Cases", len(df[df['days_overdue'] > 21]))

st.divider()

# Show Table
st.subheader("📋 Pending Invoice Records")
st.dataframe(df, use_container_width=True)

# Tone Logic
def get_tone(days):

    if days <= 7:
        return "Warm and Friendly"

    elif days <= 14:
        return "Polite but Firm"

    elif days <= 21:
        return "Formal and Serious"

    elif days <= 30:
        return "Stern and Urgent"

    else:
        return "Escalate to Legal Team"


# Tone Colors
def tone_color(tone):

    if tone == "Warm and Friendly":
        return "green"

    elif tone == "Polite but Firm":
        return "blue"

    elif tone == "Formal and Serious":
        return "orange"

    else:
        return "red"


# Email Generator
def generate_email(client, invoice, amount, due_date, days, tone):

    if tone == "Warm and Friendly":

        return f"""
Subject: Friendly Reminder – Invoice {invoice}

Hi {client},

I hope you're doing well.

This is a friendly reminder that Invoice {invoice} for ₹{amount} was due on {due_date} and is currently {days} days overdue.

If payment has already been processed, please ignore this message.

Thank you for your cooperation.

Regards,
Finance Team
"""

    elif tone == "Polite but Firm":

        return f"""
Subject: Payment Pending – Invoice {invoice}

Dear {client},

This is a reminder regarding Invoice {invoice} amounting to ₹{amount}, overdue by {days} days.

Please confirm the payment date at the earliest.

Regards,
Finance Team
"""

    elif tone == "Formal and Serious":

        return f"""
Subject: Important: Outstanding Invoice {invoice}

Dear {client},

Despite previous reminders, Invoice {invoice} for ₹{amount} remains unpaid and is now {days} days overdue.

Please respond within 48 hours to avoid escalation.

Regards,
Finance Team
"""

    elif tone == "Stern and Urgent":

        return f"""
Subject: FINAL NOTICE – Invoice {invoice}

Dear {client},

This is the final reminder regarding Invoice {invoice} amounting to ₹{amount}.

The payment is now {days} days overdue. Immediate action is required.

Failure to pay may result in escalation to the legal/recovery team.

Regards,
Finance Team
"""


# Main Cards
for index, row in df.iterrows():

    tone = get_tone(row["days_overdue"])

    color = tone_color(tone)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"## 👤 {row['client_name']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"📄 Invoice Number: {row['invoice_no']}")
        st.write(f"💰 Amount Due: ₹{row['amount']}")
        st.write(f"📅 Due Date: {row['due_date']}")

    with col2:
        st.write(f"⏳ Days Overdue: {row['days_overdue']}")
        st.markdown(
            f'<p class="{color}">⚡ Tone Level: {tone}</p>',
            unsafe_allow_html=True
        )

    # Escalation
    if tone == "Escalate to Legal Team":

        st.error("🚨 Escalation Required - Manual Finance Review Needed")

        with open("logs.txt", "a") as log:
            log.write(
                f"{datetime.now()} | {row['invoice_no']} | ESCALATED\n"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        continue

    # Generate Button
    if st.button(f"📧 Generate Email for {row['invoice_no']}"):

        email = generate_email(
            row["client_name"],
            row["invoice_no"],
            row["amount"],
            row["due_date"],
            row["days_overdue"],
            tone
        )

        st.text_area(
            "Generated Email",
            email,
            height=300
        )

        with open("logs.txt", "a") as log:
            log.write(
                f"{datetime.now()} | {row['invoice_no']} | EMAIL GENERATED\n"
            )

        st.success("✅ Email Generated Successfully")

        # Send Button
        if st.button(f"🚀 Send Email for {row['invoice_no']}"):

            st.balloons()

            st.success("📨 Email Sent Successfully (Simulation Mode)")

            with open("logs.txt", "a") as log:
                log.write(
                    f"{datetime.now()} | {row['invoice_no']} | EMAIL SENT\n"
                )

    st.markdown("</div>", unsafe_allow_html=True)