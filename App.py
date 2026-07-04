import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gemini Computing - Job Cost Calculator")

st.title("🛠️ Gemini Computing Job Cost Calculator")

# Sidebar for Settings (Pre-populated from "Job cost calculator.xlsx")
st.sidebar.header("Settings")
labour_rate = st.sidebar.number_input("Labour rate / hour (£)", value=40.0)
overhead_rate = st.sidebar.number_input("Internal overhead cost / Hour (£)", value=0.0)
parts_markup = st.sidebar.slider("Parts Markup (%)", 0, 100, 30) / 100
profit_margin = st.sidebar.slider("Profit Margin (%)", 0, 100, 25) / 100

# Input Fields
st.header("Calculate Job Quote")
job_ref = st.text_input("Job Ref / Client")
wholesale_parts = st.number_input("Wholesale Parts Cost (£)", min_value=0.0, value=0.0)
labour_hours = st.number_input("Estimated Labour Hours", min_value=0.0, value=0.0)

if st.button("Calculate"):
    # Calculations
    marked_up_parts = wholesale_parts * (1 + parts_markup)
    gross_labour = labour_hours * labour_rate
    allocated_overhead = labour_hours * overhead_rate
    break_even = marked_up_parts + gross_labour + allocated_overhead
    
    # Avoid division by zero
    if profit_margin < 1:
        final_quote = break_even / (1 - profit_margin)
        net_profit = final_quote - break_even
    else:
        final_quote = 0
        net_profit = 0

    # Display Results
    col1, col2 = st.columns(2)
    col1.metric("Break Even Sub-Total", f"£{break_even:,.2f}")
    col2.metric("Final Client Quote", f"£{final_quote:,.2f}")
    
    st.write(f"**Net Profit Margin Made:** £{net_profit:,.2f}")
