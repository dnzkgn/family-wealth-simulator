
# Family Wealth Simulator App (Streamlit Version)
import streamlit as st

# Inputs
st.title("🏡 Family Wealth Simulator: Buy vs Rent vs Invest")
st.write("Adjust the sliders and inputs to simulate your future wealth in different scenarios!")

home_price = st.number_input('Home Price ($)', value=950000)
down_payment_percent = st.slider('Down Payment (%)', 5, 30, 10)
mortgage_rate = st.slider('Initial Mortgage Rate (%)', 3.0, 8.0, 6.75)
refinance_rate = st.slider('Refinance Rate After 2 Years (%)', 3.0, 6.0, 5.0)
years_projection = st.slider('Years to Project', 5, 30, 10)
home_appreciation_rate = st.slider('Home Appreciation Rate (%)', 0.0, 6.0, 3.0)
rent = st.number_input('Monthly Rent ($)', value=3500)
rent_control = st.checkbox('Apply Rent Control (lower rent increase)?', value=True)
monthly_rent_increase = 3 if rent_control else 5
investment_return = st.slider('Investment Return if Renting (%)', 0.0, 10.0, 7.0)
monthly_saving = st.number_input('Monthly Savings (Rent cheaper than Buy)', value=2800)

# Calculations
loan_amount = home_price * (1 - down_payment_percent/100)
monthly_interest_rate = mortgage_rate / 100 / 12
num_payments = 30 * 12

monthly_mortgage = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / ((1 + monthly_interest_rate)**num_payments - 1)

remaining_loan_balance = loan_amount
principal_paid = []
home_values = []
loan_balances = []
equity_list = []

investment_value = 0
cumulative_rent_paid = 0
rent_costs = []

for year in range(1, years_projection + 1):
    # Home Value Appreciation
    new_home_value = home_price * ((1 + home_appreciation_rate/100) ** year)
    home_values.append(new_home_value)
    
    # Mortgage
    if year <=2:
        monthly_payment_now = monthly_mortgage
    else:
        if year == 3:
            refinance_closing_cost = 0.02 * remaining_loan_balance
            loan_amount += refinance_closing_cost
            monthly_interest_rate = refinance_rate / 100 / 12
            num_payments = 30 * 12
            monthly_mortgage = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) / ((1 + monthly_interest_rate)**num_payments - 1)
            monthly_payment_now = monthly_mortgage
        else:
            monthly_payment_now = monthly_mortgage

    principal_payment = (monthly_payment_now * 0.2) * 12
    remaining_loan_balance -= principal_payment
    loan_balances.append(remaining_loan_balance)

    net_equity = new_home_value - remaining_loan_balance
    equity_list.append(net_equity)

    # Rent & Invest
    investment_value = (investment_value + monthly_saving * 12) * (1 + investment_return/100)
    cumulative_rent_paid += rent * 12
    rent_costs.append(cumulative_rent_paid)
    rent *= (1 + monthly_rent_increase/100)

# Outputs
st.header("📈 Results After {} Years:".format(years_projection))
st.success(f"Estimated Home Value: ${home_values[-1]:,.0f}")
st.success(f"Estimated Home Equity if Buying: ${equity_list[-1]:,.0f}")
st.info(f"Total Cumulative Rent Paid: ${rent_costs[-1]:,.0f}")
st.warning(f"Estimated Wealth if Rent + Invest: ${investment_value:,.0f}")

# Charts
import matplotlib.pyplot as plt

years = list(range(1, years_projection+1))
plt.figure(figsize=(10,6))
plt.plot(years, equity_list, label="🏠 Home Equity Built", marker='o')
plt.plot(years, rent_costs, label="💸 Rent Paid", marker='x')
plt.plot(years, [(monthly_saving*12*(1+investment_return/100)**(y)) for y in years], label="📈 Rent + Invest Wealth", marker='^')
plt.title("Wealth Growth Over Time")
plt.xlabel("Years")
plt.ylabel("Amount ($)")
plt.grid(True)
plt.legend()
st.pyplot(plt)

import pandas as pd

# Build a simple DataFrame
results_df = pd.DataFrame({
    "Year": years,
    "Home Value": home_values,
    "Home Equity": equity_list,
    "Rent Paid (Cumulative)": rent_costs,
    "Rent + Invest Wealth": [(monthly_saving*12*(1+investment_return/100)**(y)) for y in years]
})

# Download CSV
st.download_button(
    label="📥 Download Simulation Data as CSV",
    data=results_df.to_csv(index=False),
    file_name='family_wealth_simulation.csv',
    mime='text/csv'
)

# Smart Recommendation
st.header("🤔 Final Recommendation:")

if equity_list[-1] > investment_value and equity_list[-1] > rent_costs[-1]:
    st.success("🏡 Buying looks financially stronger for you over the next {} years!".format(years_projection))
    st.balloons()  # Celebrate!
elif investment_value > equity_list[-1]:
    st.warning("📈 Renting + Investing could create more wealth, but requires discipline to save & invest monthly.")
else:
    st.info("🤷 It's pretty close! Your decision should focus on lifestyle, emotional goals, and cash flow comfort.")


st.sidebar.header("🔧 Adjust Assumptions")
st.sidebar.write("Move the sliders to change assumptions and project different futures!")

# Move your input sliders inside the sidebar for cleaner main page

