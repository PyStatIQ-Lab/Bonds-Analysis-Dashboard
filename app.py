import streamlit as st
import pandas as pd
from datetime import datetime

# Load the bond data
data = [
    ["INE219O07362", "GOSWAMI INFRATECH PRIVATE LIMITED", 0, "30-04-2026", "-", 61643, "1Y,0M,21D", "Secured", "Zero Coupon", 3, 184929, 0.165, "CARE BB-", "Negative", "On Maturity", "2.37% On June 24 & Later 48% Semi Annual"],
    ["INE468N07BJ0", "ECAP EQUITIES LIMITED", 0, "13-08-2026", "-", 100000, "1Y,4M,4D", "Secured", "Zero Coupon", 1, 100000, 0.125, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE07HK07791", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.1095, "23-07-2026", "-", 100000, "1Y,3M,14D", "Secured", "NCD", 7, 700000, 0.124, "CARE A-", "Stable", "Monthly", "50% FV Semi annual from Jan 26"],
    ["INE07HK07783", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.103, "12-06-2026", "-", 100000, "1Y,2M,3D", "Secured", "NCD", 2, 200000, 0.124, "CRISIL A-", "Stable", "Monthly", "33.33% Every Semi- Annual From Jun 25"],
    ["INE07HK07742", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.102, "19-12-2025", "-", 66666.67, "0Y,8M,10D", "Secured", "NCD", 1, 66666.67, 0.124, "CRISIL A-", "Stable", "Monthly", "On Maturity"],
    ["INE090W07675", "LENDINGKART FINANCE LIMITED", 0.107809988, "23-02-2026", "-", 100000, "0Y,10M,14D", "Secured", "NCD", 55, 5500000, 0.1225, "IND BBB+", "Stable", "Monthly", "On Maturity"],
    ["INE01E708024", "ANDHRA PRADESH CAPITAL REGION DEVELOPMENT AUTHORITY", 0.1032, "16-08-2025", "-", 100000, "0Y,4M,7D", "Unsecured", "NCD", 11.25, 1125000, 0.1225, "CRISIL BB+(CE)", "-", "Quarterly", "25% Every Quarter From Nov 24"],
    ["INE090W07683", "LENDINGKART FINANCE LIMITED", 0.1076, "10-05-2026", "-", 100000, "1Y,1M,1D", "Secured", "NCD", 4, 400000, 0.1225, "IND BBB+", "Stable", "Monthly", "On Maturity"],
    ["INE532F07CQ2", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.0915, "28-12-2026", "-", 1000, "1Y,8M,19D", "Secured", "NCD", 3500, 3500000, 0.1215, "CRISIL A+", "-", "Monthly", "On Maturity"],
    ["INE532F07EP0", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.096, "26-10-2026", "-", 1000, "1Y,6M,17D", "Secured", "NCD", 1868, 1868000, 0.1215, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE532F07DL1", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "20-01-2026", "-", 1000, "0Y,9M,11D", "Secured", "Zero Coupon", 1014, 1014000, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DG1", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "20-01-2028", "-", 1000, "2Y,9M,11D", "Secured", "Zero Coupon", 459, 459000, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DK3", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.0967, "20-01-2028", "-", 1000, "2Y,9M,11D", "Secured", "NCD", 378, 378000, 0.1215, "CRISIL A+", "-", "Monthly", "On Maturity"],
    ["INE532F07EV8", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "29-01-2026", "-", 1000, "0Y,9M,20D", "Secured", "Zero Coupon", 3, 3000, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07EX4", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "29-01-2027", "-", 1000, "1Y,9M,20D", "Secured", "Zero Coupon", 225, 225000, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07CS8", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "28-12-2026", "-", 1000, "1Y,8M,19D", "Secured", "Zero Coupon", 365, 365000, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07BO9", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "08-01-2026", "-", 1000, "0Y,8M,30D", "Secured", "Zero Coupon", 194, 194000, 0.1215, "CARE A", "Stable", "On Maturity", "On Maturity"]
]

columns = [
    "ISIN", "Issuer Name", "Coupon", "Redemption Date", "Call/Put Date", 
    "Face Value", "Residual Tenure", "Secured / Unsecured", "Special Feature", 
    "Total Qty", "Total Qty FV", "Offer Yield", "Credit Rating", "Outlook", 
    "Interest Payment Frequency", "Principal Redemption"
]

df = pd.DataFrame(data, columns=columns)

# Convert date strings to datetime objects
df['Redemption Date'] = pd.to_datetime(df['Redemption Date'], dayfirst=True)

# Calculate days to maturity
today = datetime.now()
df['Days to Maturity'] = (df['Redemption Date'] - today).dt.days
df['Years to Maturity'] = df['Days to Maturity'] / 365

# Create a function to categorize bonds as SLIPS or FLIPS
def categorize_bond(row):
    if "CPI" in str(row['Special Feature']) or "inflation" in str(row['Special Feature']):
        return "FLIPS"
    else:
        return "SLIPS"

df['Bond Type'] = df.apply(categorize_bond, axis=1)

# Streamlit app
st.set_page_config(layout="wide", page_title="SLIPS & FLIPS Bonds Dashboard")

st.title("SLIPS & FLIPS Bonds Dashboard")

# Sidebar filters
st.sidebar.header("Filter Bonds")

# Bond type selection
bond_type = st.sidebar.radio("Select Bond Type", ["All", "SLIPS", "FLIPS"])

# Holding time filter
holding_time = st.sidebar.slider(
    "Maximum Years to Maturity", 
    min_value=0.0, 
    max_value=5.0, 
    value=3.0, 
    step=0.25
)

# Risk level filter
risk_levels = sorted(df['Credit Rating'].unique())
selected_risk = st.sidebar.multiselect(
    "Credit Rating", 
    options=risk_levels, 
    default=risk_levels
)

# Coupon rate filter
min_coupon, max_coupon = st.sidebar.slider(
    "Coupon Rate Range (%)",
    min_value=0.0,
    max_value=15.0,
    value=(5.0, 12.0),
    step=0.1
)

# Apply filters
filtered_df = df.copy()

if bond_type != "All":
    filtered_df = filtered_df[filtered_df['Bond Type'] == bond_type]

filtered_df = filtered_df[filtered_df['Years to Maturity'] <= holding_time]
filtered_df = filtered_df[filtered_df['Credit Rating'].isin(selected_risk)]
filtered_df = filtered_df[(filtered_df['Coupon'] >= min_coupon/100) & (filtered_df['Coupon'] <= max_coupon/100)]

# Main display
st.header("Available Bonds")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Bonds", len(filtered_df))
col2.metric("Average Coupon", f"{filtered_df['Coupon'].mean()*100:.2f}%")
col3.metric("Average Yield", f"{filtered_df['Offer Yield'].mean()*100:.2f}%")

# Display the filtered dataframe
st.dataframe(
    filtered_df[[
        'Bond Type', 'Issuer Name', 'Coupon', 'Offer Yield', 'Years to Maturity', 
        'Credit Rating', 'Secured / Unsecured', 'Special Feature', 'Interest Payment Frequency'
    ]].rename(columns={
        'Coupon': 'Coupon Rate',
        'Offer Yield': 'Yield',
        'Years to Maturity': 'Maturity (Years)',
        'Secured / Unsecured': 'Security',
        'Special Feature': 'Features',
        'Interest Payment Frequency': 'Payment Freq.'
    }),
    use_container_width=True,
    height=600
)

# Bond type distribution
st.header("Bond Distribution")
col1, col2 = st.columns(2)

with col1:
    st.subheader("By Bond Type")
    st.bar_chart(filtered_df['Bond Type'].value_counts())

with col2:
    st.subheader("By Credit Rating")
    st.bar_chart(filtered_df['Credit Rating'].value_counts())

# Bond details expander
st.header("Bond Details")
for _, row in filtered_df.iterrows():
    with st.expander(f"{row['Issuer Name']} - {row['ISIN']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Coupon Rate:** {row['Coupon']*100:.2f}%")
            st.write(f"**Yield:** {row['Offer Yield']*100:.2f}%")
            st.write(f"**Maturity Date:** {row['Redemption Date'].strftime('%d-%m-%Y')}")
            st.write(f"**Years to Maturity:** {row['Years to Maturity']:.2f}")
            
        with col2:
            st.write(f"**Credit Rating:** {row['Credit Rating']}")
            st.write(f"**Outlook:** {row['Outlook']}")
            st.write(f"**Payment Frequency:** {row['Interest Payment Frequency']}")
            st.write(f"**Principal Redemption:** {row['Principal Redemption']}")
        
        st.write(f"**Special Features:** {row['Special Feature']}")
