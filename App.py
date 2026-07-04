import streamlit as st
import pandas as pd
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Gemini Computing - Pro Calculator", layout="wide")

# Branding
st.sidebar.title("Gemini Computing")
st.sidebar.markdown("---")

# 1. Persistent/Adjustable Settings
st.sidebar.header("Settings")
labour_rate = st.sidebar.number_input("Labour rate / hour (£)", value=40.0)
overhead_rate = st.sidebar.number_input("Internal overhead cost / Hour (£)", value=0.0)
parts_markup = st.sidebar.slider("Parts Markup (%)", 0, 100, 30) / 100
base_profit_margin = st.sidebar.slider("Base Profit Margin (%)", 0, 100, 25) / 100

# 3. Tiered Pricing Logic
st.sidebar.header("Job Tier")
tier = st.sidebar.selectbox("Select Urgency", ["Standard", "Urgent (+10% Margin)", "Warranty (0% Margin)"])
if tier == "Urgent (+10% Margin)":
    profit_margin = base_profit_margin + 0.10
elif tier == "Warranty (0% Margin)":
    profit_margin = 0.0
else:
    profit_margin = base_profit_margin

# 2. Session State for Quote History
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Date", "Client", "Quote (£)", "Profit (£)"])

# Input Fields
st.header("Calculate Job Quote")
col_a, col_b = st.columns(2)
job_ref = col_a.text_input("Job Ref / Client")
wholesale_parts = col_b.number_input("Wholesale Parts Cost (£)", min_value=0.0, value=0.0)
labour_hours = col_a.number_input("Estimated Labour Hours", min_value=0.0, value=0.0)

if st.button("Calculate and Save"):
    # Calculations
    marked_up_parts = wholesale_parts * (1 + parts_markup)
    gross_labour = labour_hours * labour_rate
    allocated_overhead = labour_hours * overhead_rate
    break_even = marked_up_parts + gross_labour + allocated_overhead
    
    if profit_margin < 1:
        final_quote = break_even / (1 - profit_margin)
    else:
        final_quote = break_even
        
    net_profit = final_quote - break_even

    # Save to history
    new_entry = {"Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 "Client": job_ref, 
                 "Quote (£)": round(final_quote, 2), 
                 "Profit (£)": round(net_profit, 2)}
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_entry])], ignore_index=True)

    # Display Results
    st.success(f"Final Client Quote: £{final_quote:,.2f}")
    st.write(f"**Net Profit:** £{net_profit:,.2f}")

# Display History
if not st.session_state.history.empty:
    st.header("Quote History")
    st.table(st.session_state.history)
    
    # Export button
    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button("Download History as CSV", data=csv, file_name="quote_history.csv")
