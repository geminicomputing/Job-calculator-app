import streamlit as st
import pandas as pd
import math
from datetime import datetime
import io
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Gemini Computing - Pro Calculator", layout="wide")

# Logo file path
logo_path = "Gemini computing workwear logo - New.jpeg"

# Sidebar Branding
st.sidebar.title("Gemini Computing")

# Display the logo in the sidebar if it exists
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=200) 
else:
    st.sidebar.warning(f"Logo ({logo_path}) not found.")

st.sidebar.markdown("---")

# 1. Settings Menu
with st.sidebar.expander("⚙️ Settings Menu"):
    st.header("Global Rates")
    labour_rate = st.number_input("Labour rate / hour (£)", value=40.00, format="%.2f")
    overhead_rate = st.number_input("Internal overhead cost / Hour (£)", value=0.00, format="%.2f")
    
    st.header("Markups & Margins")
    parts_markup = st.slider("Parts Markup (%)", 0, 100, 30) / 100
    base_profit_margin = st.slider("Base Profit Margin (%)", 0, 100, 25) / 100
    
    st.header("Rounding Settings")
    # Added 0.5 option here
    rounding_option = st.selectbox("Round Quote To Nearest", [0.5, 1, 5, 10])

# Tiered Pricing
st.sidebar.markdown("---")
st.sidebar.header("Job Tier")
tier = st.sidebar.selectbox("Select Urgency", ["Standard", "Urgent (+10% Margin)", "Warranty (0% Margin)"])
if tier == "Urgent (+10% Margin)":
    profit_margin = base_profit_margin + 0.10
elif tier == "Warranty (0% Margin)":
    profit_margin = 0.0
else:
    profit_margin = base_profit_margin

# 2. Persistent Quote History (File-based)
st.sidebar.markdown("---")
st.sidebar.header("Data Management")
uploaded_file = st.sidebar.file_uploader("Upload existing history (CSV)", type="csv")

if uploaded_file is not None:
    history_df = pd.read_csv(uploaded_file)
else:
    history_df = pd.DataFrame(columns=["Date", "Client", "Quote (£)", "Profit (£)"])

# Main Application Interface
# Display the logo on the main page
if os.path.exists(logo_path):
    st.image(logo_path, width=300)

st.header("Calculate Job Quote")
col_a, col_b = st.columns(2)
job_ref = col_a.text_input("Job Ref / Client")
wholesale_parts = col_b.number_input("Wholesale Parts Cost (£)", min_value=0.00, value=0.00, format="%.2f")
labour_hours = col_a.number_input("Estimated Labour Hours", min_value=0.00, value=0.00, format="%.2f")

if st.button("Calculate and Save"):
    # Perform calculations
    marked_up_parts = wholesale_parts * (1 + parts_markup)
    gross_labour = labour_hours * labour_rate
    allocated_overhead = labour_hours * overhead_rate
    break_even = marked_up_parts + gross_labour + allocated_overhead
    
    if profit_margin < 1:
        raw_quote = break_even / (1 - profit_margin)
    else:
        raw_quote = break_even
    
    # Apply rounding logic
    final_quote = math.ceil(raw_quote / rounding_option) * rounding_option
        
    net_profit = final_quote - break_even

    # Save to history
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
        "Client": job_ref, 
        "Quote (£)": f"{float(final_quote):.2f}", 
        "Profit (£)": f"{float(net_profit):.2f}"
    }
    
    history_df = pd.concat([history_df, pd.DataFrame([new_entry])], ignore_index=True)

    st.success(f"Final Client Quote: £{final_quote:.2f}")
    st.write(f"**Net Profit:** £{net_profit:.2f}")

# Display History Table
if not history_df.empty:
    st.header("Quote History")
    st.table(history_df)
    
    # Export updated history
    csv = history_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Updated History", data=csv, file_name="quote_history.csv")
