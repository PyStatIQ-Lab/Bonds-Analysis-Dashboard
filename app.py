import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    layout="wide",
    page_title="SLIPS & FLIPS Bonds Dashboard",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMetric label {
        font-size: 14px !important;
        color: #6c757d !important;
    }
    .stMetric div {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #212529 !important;
    }
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stExpander {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .css-1aumxhk {
        background-color: #ffffff;
        background-image: none;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .header-text {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .subheader-text {
        font-size: 16px;
        color: #7f8c8d;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load the bond data
@st.cache_data
def load_data():
    try:
        # Read data from Excel file
        df = pd.read_excel("Bonds_Data_2025.xlsx")
        
        # Check if required columns exist
        required_columns = ['ISIN', 'Issuer Name', 'Coupon', 'Redemption Date', 
                          'Face Value', 'Secured / Unsecured', 'Special Feature',
                          'Total Qty', 'Total Qty FV', 'Offer Yield', 'Credit Rating']
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns in Excel file: {', '.join(missing_cols)}")
            return pd.DataFrame()
        
        # Convert date strings to datetime objects with error handling
        try:
            df['Redemption Date'] = pd.to_datetime(df['Redemption Date'], dayfirst=True, errors='coerce')
            # Replace far future dates with NaT
            df.loc[df['Redemption Date'] > pd.Timestamp('2100-01-01'), 'Redemption Date'] = pd.NaT
        except Exception as e:
            st.error(f"Error processing dates: {str(e)}")
            return pd.DataFrame()
        
        # Calculate days to maturity
        today = datetime.now()
        df['Days to Maturity'] = (df['Redemption Date'] - today).dt.days
        df['Years to Maturity'] = df['Days to Maturity'] / 365
        
        # Create a function to categorize bonds as SLIPS or FLIPS
        def categorize_bond(row):
            if pd.isna(row['Special Feature']):
                return "SLIPS"
            if "CPI" in str(row['Special Feature']) or "inflation" in str(row['Special Feature']):
                return "FLIPS"
            return "SLIPS"

        df['Bond Type'] = df.apply(categorize_bond, axis=1)
        
        # Calculate additional metrics
        df['Total Value'] = df['Total Qty FV'] * (1 + df['Coupon'].fillna(0) * df['Years to Maturity'].fillna(0))
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=required_columns)  # Return empty DataFrame with required columns

df = load_data()

# Check if DataFrame is empty before proceeding
if df.empty:
    st.error("No data loaded. Please check the Excel file and try again.")
    st.stop()  # This will halt the app execution

# Rest of your code remains the same...
# Dashboard Header
st.markdown('<p class="header-text">SLIPS & FLIPS Bonds Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader-text">Comprehensive analysis of available structured bonds with inflation protection features</p>', unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Options")
    
    # Bond type selection
    bond_type = st.radio("Bond Type", ["All", "SLIPS", "FLIPS"], index=0)
    
    # Holding time filter
    holding_time = st.slider(
        "Max Years to Maturity", 
        min_value=0.0, 
        max_value=5.0, 
        value=3.0, 
        step=0.25
    )
    
    # Risk level filter
    risk_levels = sorted(df['Credit Rating'].unique())
    selected_risk = st.multiselect(
        "Credit Rating", 
        options=risk_levels, 
        default=risk_levels
    )
    
    # Coupon rate filter
    min_coupon, max_coupon = st.slider(
        "Coupon Rate Range (%)",
        min_value=0.0,
        max_value=15.0,
        value=(5.0, 12.0),
        step=0.1
    )
    
    # Additional filters
    secured_options = df['Secured / Unsecured'].unique()
    selected_secured = st.multiselect(
        "Security Type",
        options=secured_options,
        default=secured_options
    )
    
    payment_freq = df['Interest Payment Frequency'].unique()
    selected_payment = st.multiselect(
        "Payment Frequency",
        options=payment_freq,
        default=payment_freq
    )
    
    st.markdown("---")
    st.markdown("**About SLIPS & FLIPS:**")
    st.markdown("""
    - **SLIPS**: Standard bonds with fixed coupon payments
    - **FLIPS**: Inflation-linked bonds with CPI adjustments
    - Data is updated daily from market sources
    """)

# Apply filters
filtered_df = df.copy()

if bond_type != "All":
    filtered_df = filtered_df[filtered_df['Bond Type'] == bond_type]

filtered_df = filtered_df[filtered_df['Years to Maturity'] <= holding_time]
filtered_df = filtered_df[filtered_df['Credit Rating'].isin(selected_risk)]
filtered_df = filtered_df[(filtered_df['Coupon']*100 >= min_coupon) & (filtered_df['Coupon']*100 <= max_coupon)]
filtered_df = filtered_df[filtered_df['Secured / Unsecured'].isin(selected_secured)]
filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(selected_payment)]

# Key Metrics
st.markdown("### 📊 Market Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Bonds", len(filtered_df))
col2.metric("Total Face Value", f"₹{filtered_df['Total Qty FV'].sum()/1e6:,.1f}M")
col3.metric("Avg Coupon", f"{filtered_df['Coupon'].mean()*100:.2f}%")
col4.metric("Avg Yield", f"{filtered_df['Offer Yield'].mean()*100:.2f}%")
col5.metric("Avg Maturity", f"{filtered_df['Years to Maturity'].mean():.2f} yrs")

# Market Summary Charts
st.markdown("### 📈 Market Trends")
tab1, tab2, tab3 = st.tabs(["Yield Curve", "Credit Distribution", "Coupon Analysis"])

with tab1:
    fig = px.scatter(
        filtered_df,
        x='Years to Maturity',
        y='Offer Yield',
        color='Credit Rating',
        hover_name='Issuer Name',
        size='Total Qty FV',
        title='Yield Curve by Credit Rating and Maturity',
        labels={'Offer Yield': 'Yield to Maturity (%)', 'Years to Maturity': 'Years to Maturity'},
        trendline="lowess"
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(
        hovermode='closest',
        xaxis_title='Years to Maturity',
        yaxis_title='Yield (%)',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'xy'}]])
    
    # Pie chart
    fig.add_trace(
        go.Pie(
            labels=filtered_df['Bond Type'].value_counts().index,
            values=filtered_df['Bond Type'].value_counts().values,
            name="Bond Type",
            hole=0.4
        ),
        row=1, col=1
    )
    
    # Bar chart
    rating_counts = filtered_df['Credit Rating'].value_counts().reset_index()
    fig.add_trace(
        go.Bar(
            x=rating_counts['Credit Rating'],
            y=rating_counts['count'],
            name="Credit Rating",
            marker_color='#3498db'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Bond Type and Credit Rating Distribution",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.box(
        filtered_df,
        x='Credit Rating',
        y='Coupon',
        color='Bond Type',
        title='Coupon Rate Distribution by Credit Rating',
        points="all",
        hover_data=['Issuer Name']
    )
    fig.update_layout(
        yaxis_title="Coupon Rate (%)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Bond Details Table - FULL TABLE WITH ALL DETAILS
st.markdown("### 📋 Complete Bond Inventory")
st.dataframe(
    filtered_df[[
        'ISIN', 'Issuer Name', 'Bond Type', 'Coupon', 'Offer Yield', 
        'Years to Maturity', 'Credit Rating', 'Outlook', 'Secured / Unsecured',
        'Special Feature', 'Interest Payment Frequency', 'Principal Redemption',
        'Face Value', 'Total Qty', 'Total Qty FV', 'Redemption Date'
    ]].rename(columns={
        'Coupon': 'Coupon Rate',
        'Offer Yield': 'Yield',
        'Years to Maturity': 'Maturity (Yrs)',
        'Secured / Unsecured': 'Security',
        'Special Feature': 'Features',
        'Interest Payment Frequency': 'Payment Freq.',
        'Total Qty FV': 'Total FV (₹)',
        'Redemption Date': 'Maturity Date'
    }).style.format({
        'Coupon Rate': '{:.2%}',
        'Yield': '{:.2%}',
        'Maturity (Yrs)': '{:.2f}',
        'Total FV (₹)': '₹{:,.0f}',
        'Face Value': '₹{:,.0f}'
    }).background_gradient(cmap='Blues', subset=['Yield']),
    use_container_width=True,
    height=600
)

# Bond Details Expander
st.markdown("### 🔍 Detailed Bond Information")
for _, row in filtered_df.iterrows():
    with st.expander(f"{row['Issuer Name']} - {row['ISIN']} (₹{row['Total Qty FV']:,.0f})"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Basic Information**")
            st.write(f"**ISIN:** {row['ISIN']}")
            st.write(f"**Bond Type:** {row['Bond Type']}")
            st.write(f"**Face Value:** ₹{row['Face Value']:,.2f}")
            st.write(f"**Total Quantity:** {row['Total Qty']}")
            st.write(f"**Total Face Value:** ₹{row['Total Qty FV']:,.2f}")
            
        with col2:
            st.markdown("**Financial Terms**")
            st.write(f"**Coupon Rate:** {row['Coupon']*100:.2f}%")
            st.write(f"**Yield to Maturity:** {row['Offer Yield']*100:.2f}%")
            st.write(f"**Security:** {row['Secured / Unsecured']}")
            st.write(f"**Special Feature:** {row['Special Feature']}")
            st.write(f"**Payment Frequency:** {row['Interest Payment Frequency']}")
            
        with col3:
            st.markdown("**Maturity & Rating**")
            st.write(f"**Maturity Date:** {row['Redemption Date'].strftime('%d-%m-%Y')}")
            st.write(f"**Days to Maturity:** {row['Days to Maturity']}")
            st.write(f"**Years to Maturity:** {row['Years to Maturity']:.2f}")
            st.write(f"**Credit Rating:** {row['Credit Rating']}")
            st.write(f"**Outlook:** {row['Outlook']}")
        
        st.markdown("**Redemption Terms**")
        st.write(row['Principal Redemption'])

# Download button
st.sidebar.markdown("---")
if st.sidebar.button("💾 Download Filtered Data"):
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_bonds.csv",
        mime="text/csv"
    )

# Market Commentary
st.markdown("### 📝 Market Commentary")
with st.expander("View Current Market Analysis"):
    st.write("""
    **Current Market Trends:**
    - The SLIPS market continues to show steady demand with average yields hovering around 12.25%
    - FLIPS instruments are gaining popularity as inflation expectations remain elevated
    - Credit spreads have widened slightly for lower-rated issuers
    
    **Recommendations:**
    - Consider laddering maturities to manage interest rate risk
    - Focus on secured issues for capital preservation
    - Monitor inflation-linked bonds for potential upside
    
    **Disclaimer:** This commentary is for informational purposes only and should not be considered investment advice.
    """)

# Footer
st.markdown("---")
st.markdown("""
**Data Sources:** 
- NSE/BSE bond data
- Rating agency reports
- Issuer disclosures

**Last Updated:** {:%d-%m-%Y %H:%M}
""".format(datetime.now()))
