import streamlit as st
import pandas as pd
import math
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Gemini Computing - Pro Calculator", layout="wide")

# Branding
st.sidebar.title("Gemini Computing")
st.sidebar.markdown("---")

# 1. Settings Menu (Refined)
with st.sidebar.expander("⚙️ Settings Menu"):
    st.header("Global Rates")
    labour_rate = st.number_input("Labour rate / hour (£)", value=40.0)
    overhead_rate = st.number_input("Internal overhead cost / Hour (£)", value=0.0)
    st.header("Markups & Margins")
    parts_markup = st.slider("Parts Markup (%)", 0, 100, 30) / 100
    base_profit_margin = st.slider("Base Profit Margin (%)", 0, 100, 25) / 100

# 3. Tiered Pricing Logic (Remains in Sidebar)
st.sidebar.markdown("---")
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

# Main Application Interface
st.header("Calculate Job Quote")
col_a, col_b = st.columns(2)
job_ref = col_a.text_input("Job Ref / Client")
wholesale_parts = col_b.number_input("Wholesale Parts Cost (£)", min_value=0.0, value=0.0)
labour_hours = col_a.number_input("Estimated Labour Hours", min_value=0.0, value=0.0)

# Calculate Button Logic
if st.button("Calculate and Save"):
    # Perform calculations
    marked_up_parts = wholesale_parts * (1 + parts_markup)
    gross_labour = labour_hours * labour_rate
    allocated_overhead = labour_hours * overhead_rate
    break_even = marked_up_parts + gross_labour + allocated_overhead
    
    # Calculate Final Quote (Rounded up)
    if profit_margin < 1:
        raw_quote = break_even / (1 - profit_margin)
        final_quote = math.ceil(raw_quote)
    else:
        final_quote = math.ceil(break_even)
        
    net_profit = final_quote - break_even

    # Save to history session
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "Client": job_ref, 
        "Quote (£)": float(final_quote), 
        "Profit (£)": round(net_profit, 2)
    }
    
    # Use pd.concat properly
    new_row = pd.DataFrame([new_entry])
    st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

    # Display Results
    st.success(f"Final Client Quote: £{final_quote:,.2f}")
    st.write(f"**Net Profit:** £{net_profit:,.2f}")

# Display History Table
if not st.session_state.history.empty:
    st.header("Quote History")
    st.table(st.session_state.history)
    
    # Export button
    csv = st.session_state.history.to_csv(index=False).encode('utf-8')
    st.download_button("Download History as CSV", data=csv, file_name="quote_history.csv")
