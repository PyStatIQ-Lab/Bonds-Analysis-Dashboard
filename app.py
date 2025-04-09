import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
@st.cache_data
def load_data():
    # Read the Excel file (in a real app, you would use pd.read_excel('Bonds Data 2025.xlsx'))
    # For this example, I'll create a sample DataFrame based on the provided data structure
    data = {
        'ISIN': ['INE219O07362', 'INE468N07BJ0', 'INE07HK07791', 'INE07HK07783', 'INE07HK07742'],
        'Issuer Name': ['GOSWAMI INFRATECH PRIVATE LIMITED', 'ECAP EQUITIES LIMITED', 
                       'KRAZYBEE SERVICES PRIVATE LIMITED', 'KRAZYBEE SERVICES PRIVATE LIMITED',
                       'KRAZYBEE SERVICES PRIVATE LIMITED'],
        'Coupon': [0, 0, 0.1095, 0.103, 0.102],
        'Redemption Date': ['2026-04-30', '2026-08-13', '2026-07-23', '2026-06-12', '2025-12-19'],
        'Face Value': [61643, 100000, 100000, 100000, 66666.67],
        'Residual Tenure': ['1Y,0M,21D', '1Y,4M,4D', '1Y,3M,14D', '1Y,2M,3D', '0Y,8M,10D'],
        'Secured / Unsecured': ['Secured', 'Secured', 'Secured', 'Secured', 'Secured'],
        'Special Feature': ['Zero Coupon', 'Zero Coupon', 'NCD', 'NCD', 'NCD'],
        'Offer Yield': [0.165, 0.125, 0.124, 0.124, 0.124],
        'Credit Rating': ['CARE BB-', 'CRISIL A+', 'CARE A-', 'CRISIL A-', 'CRISIL A-'],
        'Outlook': ['Negative', 'Stable', 'Stable', 'Stable', 'Stable'],
        'Interest Payment Frequency': ['On Maturity', 'On Maturity', 'Monthly', 'Monthly', 'Monthly'],
        'Principal Redemption': ['2.37% On June 24 & Later 48% Semi Annual', 'On Maturity', 
                                '50% FV Semi annual from Jan 26', '33.33% Every Semi- Annual From Jun 25',
                                'On Maturity']
    }
    df = pd.DataFrame(data)
    
    # Convert dates to datetime
    df['Redemption Date'] = pd.to_datetime(df['Redemption Date'])
    
    # Calculate maturity in years
    today = datetime.now()
    df['Years to Maturity'] = (df['Redemption Date'] - today).dt.days / 365
    
    # Create risk categories based on credit rating
    rating_order = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-']
    df['Risk Category'] = pd.Categorical(
        df['Credit Rating'].str.extract(r'(\w+\+?\-?)')[0],
        categories=rating_order,
        ordered=True
    )
    
    return df

df = load_data()

# Dashboard Title
st.title("SLIPS and FLIPS Bonds Dashboard")

# Sidebar filters
st.sidebar.header("Investment Preferences")

# Investment type selection
investment_type = st.sidebar.radio("Select Investment Type:", ["SLIPS", "FLIPS"])

if investment_type == "SLIPS":
    st.sidebar.subheader("SLIPS Preferences")
    
    # SLIPS specific filters
    min_coupon = st.sidebar.slider(
        "Minimum Coupon Rate (%):",
        min_value=0.0,
        max_value=20.0,
        value=9.5,
        step=0.1
    )
    
    industries = df['Issuer Name'].unique()
    selected_industries = st.sidebar.multiselect(
        "Select Industries:",
        options=industries,
        default=industries[:3]
    )
    
    protection_level = st.sidebar.select_slider(
        "Protection Level:",
        options=["Basic", "Moderate", "High", "Very High"],
        value="Moderate"
    )
    
    liquidity = st.sidebar.selectbox(
        "Liquidity Preference:",
        options=["High", "Medium", "Low"],
        index=0
    )
    
    # Filter data for SLIPS
    filtered_df = df[
        (df['Coupon'] >= min_coupon/100) &
        (df['Issuer Name'].isin(selected_industries)) &
        (df['Secured / Unsecured'] == 'Secured')
    ]
    
    # Sort by protection level (simplified for demo)
    if protection_level == "Basic":
        filtered_df = filtered_df.sort_values('Credit Rating', ascending=False)
    elif protection_level == "Moderate":
        filtered_df = filtered_df.sort_values(['Credit Rating', 'Offer Yield'], ascending=[False, False])
    elif protection_level == "High":
        filtered_df = filtered_df.sort_values(['Credit Rating', 'Years to Maturity'], ascending=[False, True])
    else:  # Very High
        filtered_df = filtered_df.sort_values(['Credit Rating', 'Years to Maturity', 'Offer Yield'], 
                                            ascending=[False, True, False])
    
    # Display results
    st.header("SLIPS Bonds Recommendations")
    st.write("""
    **SLIPS** (Secured and Liquid Industry Specific Protected Securities) are bonds with:
    - High coupon rates (typically 9.5%+)
    - Industry-specific or diversified exposure
    - Secured protection
    - Flexible adjustment frequencies
    """)
    
    if filtered_df.empty:
        st.warning("No bonds match your criteria. Try adjusting your filters.")
    else:
        st.dataframe(filtered_df[[
            'Issuer Name', 'Coupon', 'Years to Maturity', 'Credit Rating', 
            'Offer Yield', 'Interest Payment Frequency', 'Principal Redemption'
        ]].style.format({
            'Coupon': '{:.2%}',
            'Offer Yield': '{:.2%}',
            'Years to Maturity': '{:.1f} years'
        }))
        
        # Industry analysis
        st.subheader("Industry Analysis")
        industry_stats = filtered_df.groupby('Issuer Name').agg({
            'Coupon': 'mean',
            'Offer Yield': 'mean',
            'Years to Maturity': 'mean'
        }).sort_values('Offer Yield', ascending=False)
        
        st.bar_chart(industry_stats['Offer Yield'])
        
        # Recommendation
        st.subheader("Investment Recommendation")
        if len(selected_industries) > 1:
            st.write("Based on your diversified industry selection, we recommend:")
            st.write("- Allocating more to industries with higher yields (right side of chart)")
            st.write("- Considering staggered maturities for liquidity management")
        else:
            st.write(f"Focusing on {selected_industries[0]}, we recommend:")
            st.write("- Selecting bonds with the highest credit ratings")
            st.write("- Balancing between yield and maturity based on your protection needs")

else:  # FLIPS
    st.sidebar.subheader("FLIPS Preferences")
    
    # FLIPS specific filters
    inflation_adjustment = st.sidebar.checkbox(
        "Inflation-Adjusted Bonds Only",
        value=True
    )
    
    min_real_yield = st.sidebar.slider(
        "Minimum Real Yield (%):",
        min_value=-2.0,
        max_value=10.0,
        value=1.0,
        step=0.1
    )
    
    liquidity_pref = st.sidebar.selectbox(
        "Liquidity Preference:",
        options=["Daily", "Weekly", "Monthly", "Quarterly"],
        index=1
    )
    
    # Filter data for FLIPS (simulated - real app would have CPI-linked bonds)
    filtered_df = df[
        (df['Offer Yield'] >= min_real_yield/100) &
        (df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly', 'Annually']))
    ]
    
    # Sort by liquidity preference
    if liquidity_pref == "Daily":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'] == 'Monthly']
    elif liquidity_pref == "Weekly":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly'])]
    elif liquidity_pref == "Monthly":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly', 'Annually'])]
    else:  # Quarterly
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Quarterly', 'Annually'])]
    
    # Display results
    st.header("FLIPS Bonds Recommendations")
    st.write("""
    **FLIPS** (Flexible Liquidity Inflation-Protected Securities) are bonds with:
    - Inflation protection (CPI-linked)
    - Preservation of purchasing power
    - Higher interest rates than traditional bonds
    - Risk mitigation features
    """)
    
    if filtered_df.empty:
        st.warning("No bonds match your criteria. Try adjusting your filters.")
    else:
        st.dataframe(filtered_df[[
            'Issuer Name', 'Coupon', 'Years to Maturity', 'Credit Rating', 
            'Offer Yield', 'Interest Payment Frequency', 'Principal Redemption'
        ]].style.format({
            'Coupon': '{:.2%}',
            'Offer Yield': '{:.2%}',
            'Years to Maturity': '{:.1f} years'
        }))
        
        # Inflation protection analysis
        st.subheader("Inflation Protection Analysis")
        st.write("""
        The following bonds offer the best inflation protection based on:
        - Real yield above inflation expectations
        - Frequent interest payments for liquidity
        - Principal protection features
        """)
        
        # Simulated inflation-adjusted yields
        filtered_df['Estimated Real Yield'] = filtered_df['Offer Yield'] - 0.02  # Assuming 2% inflation
        top_inflation_bonds = filtered_df.nlargest(5, 'Estimated Real Yield')
        
        st.bar_chart(top_inflation_bonds.set_index('Issuer Name')['Estimated Real Yield'])
        
        # Recommendation
        st.subheader("Investment Recommendation")
        st.write("For optimal inflation protection:")
        st.write("- Focus on bonds with the highest real yields (above chart)")
        st.write("- Consider shorter maturities if inflation expectations are volatile")
        st.write("- Diversify across issuers to mitigate specific risks")

# Common analytics section
st.sidebar.markdown("---")
st.sidebar.subheader("Portfolio Analytics")
holding_period = st.sidebar.slider(
    "Expected Holding Period (years):",
    min_value=1,
    max_value=30,
    value=5
)

risk_tolerance = st.sidebar.select_slider(
    "Risk Tolerance:",
    options=["Conservative", "Moderate", "Aggressive"],
    value="Moderate"
)

# Display portfolio suggestions based on common filters
st.markdown("---")
st.header("Portfolio Suggestions Based on Your Preferences")

if investment_type == "SLIPS":
    st.write(f"Based on a {holding_period}-year holding period and {risk_tolerance.lower()} risk tolerance:")
    
    if risk_tolerance == "Conservative":
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period) &
            (filtered_df['Risk Category'] >= 'AA')
        ].sort_values('Credit Rating', ascending=False)
    elif risk_tolerance == "Moderate":
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period + 2) &
            (filtered_df['Risk Category'] >= 'A')
        ].sort_values('Offer Yield', ascending=False)
    else:  # Aggressive
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period + 5)
        ].sort_values('Offer Yield', ascending=False)
    
    if not rec_df.empty:
        st.write("Recommended allocation:")
        cols = st.columns(3)
        cols[0].metric("High Quality", f"{len(rec_df[rec_df['Risk Category'] >= 'AA'])} bonds")
        cols[1].metric("Yield Range", 
                      f"{rec_df['Offer Yield'].min():.2%} - {rec_df['Offer Yield'].max():.2%}")
        cols[2].metric("Avg Maturity", 
                      f"{rec_df['Years to Maturity'].mean():.1f} years")
        
        st.write("Top recommendations:")
        st.dataframe(rec_df.head(5)[[
            'Issuer Name', 'Coupon', 'Years to Maturity', 'Credit Rating', 'Offer Yield'
        ]].style.format({
            'Coupon': '{:.2%}',
            'Offer Yield': '{:.2%}',
            'Years to Maturity': '{:.1f} years'
        }))
    else:
        st.warning("No bonds match your combined criteria. Consider adjusting risk tolerance or holding period.")

else:  # FLIPS
    st.write(f"Based on a {holding_period}-year holding period and {risk_tolerance.lower()} risk tolerance:")
    
    if risk_tolerance == "Conservative":
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period) &
            (filtered_df['Risk Category'] >= 'AA') &
            (filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly']))
        ].sort_values('Credit Rating', ascending=False)
    elif risk_tolerance == "Moderate":
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period + 3) &
            (filtered_df['Risk Category'] >= 'A') &
            (filtered_df['Interest Payment Frequency'] != 'On Maturity')
        ].sort_values('Offer Yield', ascending=False)
    else:  # Aggressive
        rec_df = filtered_df[
            (filtered_df['Years to Maturity'] <= holding_period + 5)
        ].sort_values('Offer Yield', ascending=False)
    
    if not rec_df.empty:
        st.write("Recommended allocation:")
        cols = st.columns(3)
        cols[0].metric("Inflation Protection", 
                      f"{len(rec_df[rec_df['Estimated Real Yield'] > 0.01])} bonds")
        cols[1].metric("Yield Range", 
                      f"{rec_df['Offer Yield'].min():.2%} - {rec_df['Offer Yield'].max():.2%}")
        cols[2].metric("Avg Payment Freq", 
                      rec_df['Interest Payment Frequency'].mode()[0])
        
        st.write("Top recommendations for inflation protection:")
        st.dataframe(rec_df.head(5)[[
            'Issuer Name', 'Coupon', 'Years to Maturity', 'Credit Rating', 
            'Offer Yield', 'Estimated Real Yield'
        ]].style.format({
            'Coupon': '{:.2%}',
            'Offer Yield': '{:.2%}',
            'Estimated Real Yield': '{:.2%}',
            'Years to Maturity': '{:.1f} years'
        }))
    else:
        st.warning("No bonds match your combined criteria. Consider adjusting risk tolerance or holding period.")

# Footer
st.markdown("---")
st.markdown("""
**Definitions:**
- **SLIPS**: Secured and Liquid Industry Specific Protected Securities
- **FLIPS**: Flexible Liquidity Inflation-Protected Securities
- **Real Yield**: Nominal yield minus expected inflation
""")
