import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="SLIPS & FLIPS Bonds Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load data function with caching
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        
        # Data cleaning and transformations
        df['Redemption Date'] = pd.to_datetime(df['Redemption Date'])
        df['Coupon'] = pd.to_numeric(df['Coupon'], errors='coerce')
        df['Offer Yield'] = pd.to_numeric(df['Offer Yield'], errors='coerce')
        
        # Calculate time to maturity
        today = datetime.now()
        df['Years to Maturity'] = (df['Redemption Date'] - today).dt.days / 365
        
        # Extract credit rating category
        rating_order = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-']
        df['Rating Category'] = df['Credit Rating'].str.extract(r'([A-Za-z]+\+?\-?)')[0]
        df['Rating Category'] = pd.Categorical(
            df['Rating Category'],
            categories=rating_order,
            ordered=True
        )
        
        # Create risk categories
        conditions = [
            df['Rating Category'].isin(['AAA', 'AA+', 'AA']),
            df['Rating Category'].isin(['AA-', 'A+', 'A']),
            df['Rating Category'].isin(['A-', 'BBB+', 'BBB']),
            df['Rating Category'].isin(['BBB-', 'BB+', 'BB']),
            df['Rating Category'].isin(['BB-', 'B+', 'B', 'B-', 'CCC+', 'CCC', 'CCC-', 'CC', 'C', 'D'])
        ]
        choices = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        df['Risk Level'] = np.select(conditions, choices, default='Unknown')
        
        # Create industry/sector categories (simplified for this example)
        df['Industry'] = df['Issuer Name'].apply(lambda x: 'Finance' if 'FINANCE' in x.upper() 
                                               else 'Infrastructure' if 'INFRA' in x.upper()
                                               else 'Banking' if 'BANK' in x.upper()
                                               else 'Government' if 'GOVERNMENT' in x.upper()
                                               else 'Other')
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Main app
def main():
    st.title("📊 SLIPS & FLIPS Bonds Dashboard")
    st.markdown("""
    **SLIPS** (Secured and Liquid Industry Specific Protected Securities) and **FLIPS** (Flexible Liquidity Inflation-Protected Securities) 
    are specialized bond investment strategies designed for different market conditions.
    """)
    
    # File upload
    uploaded_file = st.sidebar.file_uploader("Upload Bonds Data (Excel)", type=['xlsx'])
    if not uploaded_file:
        st.warning("Please upload an Excel file with bonds data")
        return
    
    df = load_data(uploaded_file)
    if df.empty:
        st.error("No data loaded. Please check your file format.")
        return
    
    # Sidebar filters
    st.sidebar.header("Investment Preferences")
    investment_type = st.sidebar.radio("Investment Strategy:", ["SLIPS", "FLIPS"])
    
    if investment_type == "SLIPS":
        show_slips_dashboard(df)
    else:
        show_flips_dashboard(df)

# SLIPS Dashboard
def show_slips_dashboard(df):
    st.header("🔒 SLIPS Bonds Analysis")
    st.markdown("""
    **Secured and Liquid Industry Specific Protected Securities**  
    High-coupon bonds with industry-specific exposure and capital protection features.
    """)
    
    # SLIPS filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_coupon = st.slider(
            "Minimum Coupon Rate (%)",
            min_value=0.0,
            max_value=20.0,
            value=9.5,
            step=0.1,
            key='slips_coupon'
        )
    with col2:
        industries = st.multiselect(
            "Select Industries",
            options=df['Industry'].unique(),
            default=['Finance', 'Infrastructure'],
            key='slips_industries'
        )
    with col3:
        protection_level = st.select_slider(
            "Protection Level",
            options=["Basic", "Moderate", "High", "Very High"],
            value="Moderate",
            key='slips_protection'
        )
    
    # Filter data
    filtered_df = df[
        (df['Coupon'] >= min_coupon/100) &
        (df['Industry'].isin(industries)) &
        (df['Secured / Unsecured'] == 'Secured')
    ].copy()
    
    # Apply protection level filter
    if protection_level == "Basic":
        filtered_df = filtered_df[filtered_df['Risk Level'].isin(['Very Low', 'Low'])]
    elif protection_level == "Moderate":
        filtered_df = filtered_df[filtered_df['Risk Level'].isin(['Very Low', 'Low', 'Medium'])]
    elif protection_level == "High":
        filtered_df = filtered_df[filtered_df['Risk Level'].isin(['Very Low', 'Low', 'Medium', 'High'])]
    
    # Display metrics
    if not filtered_df.empty:
        st.subheader("📊 Portfolio Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Bonds", len(filtered_df))
        m2.metric("Avg Coupon", f"{filtered_df['Coupon'].mean():.2%}")
        m3.metric("Avg Yield", f"{filtered_df['Offer Yield'].mean():.2%}")
        m4.metric("Avg Maturity", f"{filtered_df['Years to Maturity'].mean():.1f} years")
        
        # Interactive data table
        st.subheader("🧾 Available Bonds")
        show_columns = [
            'Issuer Name', 'Industry', 'Coupon', 'Offer Yield', 'Years to Maturity',
            'Credit Rating', 'Risk Level', 'Interest Payment Frequency', 'Principal Redemption'
        ]
        st.dataframe(
            filtered_df[show_columns].sort_values('Offer Yield', ascending=False),
            column_config={
                "Coupon": st.column_config.NumberColumn(format="%.2f%%"),
                "Offer Yield": st.column_config.NumberColumn(format="%.2f%%"),
                "Years to Maturity": st.column_config.NumberColumn(format="%.1f years")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Visualizations
        st.subheader("📈 Market Analysis")
        tab1, tab2, tab3 = st.tabs(["Yield Distribution", "Industry Breakdown", "Maturity Profile"])
        
        with tab1:
            fig = px.histogram(
                filtered_df,
                x='Offer Yield',
                nbins=20,
                title='Distribution of Bond Yields',
                labels={'Offer Yield': 'Yield (%)'},
                color='Risk Level'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            industry_stats = filtered_df.groupby('Industry').agg({
                'Coupon': 'mean',
                'Offer Yield': 'mean',
                'Years to Maturity': 'mean'
            }).reset_index()
            
            fig = px.bar(
                industry_stats,
                x='Industry',
                y='Offer Yield',
                color='Industry',
                title='Average Yield by Industry',
                labels={'Offer Yield': 'Avg Yield (%)'},
                text_auto='.2%'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = px.scatter(
                filtered_df,
                x='Years to Maturity',
                y='Offer Yield',
                color='Risk Level',
                size='Coupon',
                hover_name='Issuer Name',
                title='Yield vs Maturity',
                labels={
                    'Years to Maturity': 'Years to Maturity',
                    'Offer Yield': 'Yield (%)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation engine
        st.subheader("💡 Investment Recommendations")
        holding_period = st.slider(
            "Your planned holding period (years)",
            min_value=1,
            max_value=30,
            value=5,
            key='slips_holding'
        )
        
        risk_tolerance = st.select_slider(
            "Your risk tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate",
            key='slips_risk'
        )
        
        if risk_tolerance == "Conservative":
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period) &
                (filtered_df['Risk Level'].isin(['Very Low', 'Low']))
            ].sort_values(['Rating Category', 'Offer Yield'], ascending=[True, False])
        elif risk_tolerance == "Moderate":
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period + 2) &
                (filtered_df['Risk Level'].isin(['Very Low', 'Low', 'Medium']))
            ].sort_values(['Rating Category', 'Offer Yield'], ascending=[True, False])
        else:  # Aggressive
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period + 5)
            ].sort_values('Offer Yield', ascending=False)
        
        if not rec_df.empty:
            st.success(f"Recommended {len(rec_df)} bonds for your profile:")
            st.dataframe(
                rec_df.head(10)[show_columns],
                column_config={
                    "Coupon": st.column_config.NumberColumn(format="%.2f%%"),
                    "Offer Yield": st.column_config.NumberColumn(format="%.2f%%"),
                    "Years to Maturity": st.column_config.NumberColumn(format="%.1f years")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Generate allocation suggestion
            st.markdown("#### Suggested Allocation Strategy")
            allocation = rec_df.groupby('Industry')['Offer Yield'].mean().sort_values(ascending=False)
            st.write(f"Based on your {risk_tolerance.lower()} risk tolerance and {holding_period}-year horizon:")
            st.write("- Allocate more to industries with higher yields")
            st.write("- Consider laddering maturities for liquidity management")
            
            fig = px.pie(
                allocation,
                names=allocation.index,
                values=allocation.values,
                title='Suggested Industry Allocation',
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No bonds match your criteria. Try adjusting your filters.")
    
    else:
        st.warning("No bonds match your current filters. Try adjusting your criteria.")

# FLIPS Dashboard
def show_flips_dashboard(df):
    st.header("🛡️ FLIPS Bonds Analysis")
    st.markdown("""
    **Flexible Liquidity Inflation-Protected Securities**  
    Bonds designed to protect against inflation while providing liquidity options.
    """)
    
    # FLIPS filters
    col1, col2, col3 = st.columns(3)
    with col1:
        inflation_adjusted = st.checkbox(
            "Show only inflation-linked bonds",
            value=True,
            key='flips_inflation'
        )
    with col2:
        min_real_yield = st.slider(
            "Minimum real yield (%)",
            min_value=-2.0,
            max_value=10.0,
            value=1.0,
            step=0.1,
            key='flips_yield'
        )
    with col3:
        liquidity_pref = st.selectbox(
            "Liquidity preference",
            options=["Daily", "Weekly", "Monthly", "Quarterly"],
            index=1,
            key='flips_liquidity'
        )
    
    # Filter data (simulating inflation-adjusted bonds)
    filtered_df = df[
        (df['Offer Yield'] >= min_real_yield/100)
    ].copy()
    
    # Simulate inflation adjustment (in real app, would use actual CPI data)
    filtered_df['Estimated Real Yield'] = filtered_df['Offer Yield'] - 0.02  # Assuming 2% inflation
    
    # Apply liquidity filter
    if liquidity_pref == "Daily":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'] == 'Monthly']
    elif liquidity_pref == "Weekly":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly'])]
    elif liquidity_pref == "Monthly":
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly', 'Annually'])]
    else:  # Quarterly
        filtered_df = filtered_df[filtered_df['Interest Payment Frequency'].isin(['Quarterly', 'Annually'])]
    
    # Apply inflation-adjusted filter
    if inflation_adjusted:
        # In real app, would filter for actual inflation-linked bonds
        filtered_df = filtered_df[filtered_df['Special Feature'].str.contains('CPI|Inflation', case=False, na=False)]
    
    # Display metrics
    if not filtered_df.empty:
        st.subheader("📊 Portfolio Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Bonds", len(filtered_df))
        m2.metric("Avg Nominal Yield", f"{filtered_df['Offer Yield'].mean():.2%}")
        m3.metric("Avg Real Yield", f"{filtered_df['Estimated Real Yield'].mean():.2%}")
        m4.metric("Avg Payment Freq", filtered_df['Interest Payment Frequency'].mode()[0])
        
        # Interactive data table
        st.subheader("🧾 Available Bonds")
        show_columns = [
            'Issuer Name', 'Industry', 'Coupon', 'Offer Yield', 'Estimated Real Yield',
            'Years to Maturity', 'Credit Rating', 'Risk Level', 'Interest Payment Frequency'
        ]
        st.dataframe(
            filtered_df[show_columns].sort_values('Estimated Real Yield', ascending=False),
            column_config={
                "Coupon": st.column_config.NumberColumn(format="%.2f%%"),
                "Offer Yield": st.column_config.NumberColumn(format="%.2f%%"),
                "Estimated Real Yield": st.column_config.NumberColumn(format="%.2f%%"),
                "Years to Maturity": st.column_config.NumberColumn(format="%.1f years")
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Visualizations
        st.subheader("📈 Inflation Protection Analysis")
        tab1, tab2, tab3 = st.tabs(["Real Yield Distribution", "Maturity vs Yield", "Liquidity Profile"])
        
        with tab1:
            fig = px.histogram(
                filtered_df,
                x='Estimated Real Yield',
                nbins=20,
                title='Distribution of Real Yields',
                labels={'Estimated Real Yield': 'Real Yield (%)'},
                color='Risk Level'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = px.scatter(
                filtered_df,
                x='Years to Maturity',
                y='Estimated Real Yield',
                color='Risk Level',
                size='Coupon',
                hover_name='Issuer Name',
                title='Real Yield vs Maturity',
                labels={
                    'Years to Maturity': 'Years to Maturity',
                    'Estimated Real Yield': 'Real Yield (%)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            freq_counts = filtered_df['Interest Payment Frequency'].value_counts().reset_index()
            fig = px.bar(
                freq_counts,
                x='Interest Payment Frequency',
                y='count',
                color='Interest Payment Frequency',
                title='Payment Frequency Distribution',
                labels={'count': 'Number of Bonds'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendation engine
        st.subheader("💡 Investment Recommendations")
        holding_period = st.slider(
            "Your planned holding period (years)",
            min_value=1,
            max_value=30,
            value=5,
            key='flips_holding'
        )
        
        risk_tolerance = st.select_slider(
            "Your risk tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate",
            key='flips_risk'
        )
        
        if risk_tolerance == "Conservative":
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period) &
                (filtered_df['Risk Level'].isin(['Very Low', 'Low'])) &
                (filtered_df['Interest Payment Frequency'].isin(['Monthly', 'Quarterly']))
            ].sort_values(['Rating Category', 'Estimated Real Yield'], ascending=[True, False])
        elif risk_tolerance == "Moderate":
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period + 3) &
                (filtered_df['Risk Level'].isin(['Very Low', 'Low', 'Medium'])) &
                (filtered_df['Interest Payment Frequency'] != 'On Maturity')
            ].sort_values(['Rating Category', 'Estimated Real Yield'], ascending=[True, False])
        else:  # Aggressive
            rec_df = filtered_df[
                (filtered_df['Years to Maturity'] <= holding_period + 5)
            ].sort_values('Estimated Real Yield', ascending=False)
        
        if not rec_df.empty:
            st.success(f"Recommended {len(rec_df)} bonds for your profile:")
            st.dataframe(
                rec_df.head(10)[show_columns],
                column_config={
                    "Coupon": st.column_config.NumberColumn(format="%.2f%%"),
                    "Offer Yield": st.column_config.NumberColumn(format="%.2f%%"),
                    "Estimated Real Yield": st.column_config.NumberColumn(format="%.2f%%"),
                    "Years to Maturity": st.column_config.NumberColumn(format="%.1f years")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Generate allocation suggestion
            st.markdown("#### Suggested Allocation Strategy")
            st.write(f"Based on your {risk_tolerance.lower()} risk tolerance and {holding_period}-year horizon:")
            
            if inflation_adjusted:
                st.write("- Focus on bonds with highest real yields")
                st.write("- Consider shorter maturities if inflation expectations are volatile")
            else:
                st.write("- Diversify across nominal and inflation-linked bonds")
                st.write("- Balance between yield and inflation protection")
            
            fig = px.scatter(
                rec_df,
                x='Years to Maturity',
                y='Estimated Real Yield',
                color='Industry',
                size='Coupon',
                hover_name='Issuer Name',
                title='Recommended Bonds by Industry',
                labels={
                    'Years to Maturity': 'Years to Maturity',
                    'Estimated Real Yield': 'Real Yield (%)'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No bonds match your criteria. Try adjusting your filters.")
    
    else:
        st.warning("No bonds match your current filters. Try adjusting your criteria.")

if __name__ == "__main__":
    main()
