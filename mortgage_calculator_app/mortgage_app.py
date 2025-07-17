import streamlit as st
import math
import pandas as pd

st.title('PlanMyMortgage')
st.write('### Your Mortgage Repayment Calculator\n\n')

st.write('### Input Data')
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=500000)
deposit = col1.number_input("Deposit", min_value=0, value=150000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=0, value=30)

#Calculate the repayment
loan_amount = home_value - deposit
monthly_interest = (interest_rate / 100) / 12
total_payments = loan_term * 12


if monthly_interest > 0:
    monthly_payment = (
            (loan_amount * monthly_interest
            * (1 + monthly_interest) ** total_payments)
            / ((1 + monthly_interest) ** total_payments - 1)
    )
else:
    monthly_payment = loan_amount / total_payments  # For 0% interest case


#Display the repayments
full_payment = monthly_payment * total_payments
full_interest = full_payment - loan_amount

st.write('### Repayments')
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${full_payment:,.0f}")
col3.metric(label="Total Interest", value=f"${full_interest:,.0f}")

#Wanna calculate the payment schedule over the loan term

#Create a dataframe with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, total_payments + 1):
    interest_payment = remaining_balance * monthly_interest
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12) #Calculate the year into the rent
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year, #trailing comma is optional
        ]
    )
df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

#display the dataframe as a chart
st.write('### Payment Schedule')
payments_df = df[['Year', 'Remaining Balance']].groupby("Year").min()
st.line_chart(payments_df)