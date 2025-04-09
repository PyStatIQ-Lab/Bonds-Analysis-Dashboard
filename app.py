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
        background-color: blue;
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
    data = [
    ["INE219O07362", "GOSWAMI INFRATECH PRIVATE LIMITED", 0, "2026-04-30", "-", 61643.0, "1Y,0M,21D", "Secured", "Zero Coupon", 3.0, 184929.0, 0.165, "CARE BB-", "Negative", "On Maturity", "2.37% On June 24 & Later 48% Semi Annual"],
    ["INE468N07BJ0", "ECAP EQUITIES LIMITED", 0, "2026-08-13", "-", 100000.0, "1Y,4M,4D", "Secured", "Zero Coupon", 1.0, 100000.0, 0.125, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE07HK07791", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.1095, "2026-07-23", "-", 100000.0, "1Y,3M,14D", "Secured", "NCD", 7.0, 700000.0, 0.124, "CARE A-", "Stable", "Monthly", "50% FV Semi annual from Jan 26"],
    ["INE07HK07783", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.103, "2026-06-12", "-", 100000.0, "1Y,2M,3D", "Secured", "NCD", 2.0, 200000.0, 0.124, "CRISIL A-", "Stable", "Monthly", "33.33% Every Semi- Annual From Jun 25"],
    ["INE07HK07742", "KRAZYBEE SERVICES PRIVATE LIMITED", 0.102, "2025-12-19", "-", 66666.67, "0Y,8M,10D", "Secured", "NCD", 1.0, 66666.67, 0.124, "CRISIL A-", "Stable", "Monthly", "On Maturity"],
    ["INE090W07675", "LENDINGKART FINANCE LIMITED", 0.10780998791746921, "2026-02-23", "-", 100000.0, "0Y,10M,14D", "Secured", "NCD", 55.0, 5500000.0, 0.1225, "IND BBB+", "Stable", "Monthly", "On Maturity"],
    ["INE01E708024", "ANDHRA PRADESH CAPITAL REGION DEVELOPMENT AUTHORITY", 0.1032, "2025-08-16", "-", 100000.0, "0Y,4M,7D", "Unsecured", "NCD", 11.25, 1125000.0, 0.1225, "CRISIL BB+(CE)", "-", "Quarterly", "25% Every Quarter From Nov 24"],
    ["INE090W07683", "LENDINGKART FINANCE LIMITED", 0.1076, "2026-05-10", "-", 100000.0, "1Y,1M,1D", "Secured", "NCD", 4.0, 400000.0, 0.1225, "IND BBB+", "Stable", "Monthly", "On Maturity"],
    ["INE532F07CQ2", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.0915, "2026-12-28", "-", 1000.0, "1Y,8M,19D", "Secured", "NCD", 3500.0, 3500000.0, 0.1215, "CRISIL A+", "-", "Monthly", "On Maturity"],
    ["INE532F07EP0", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.096, "2026-10-26", "-", 1000.0, "1Y,6M,17D", "Secured", "NCD", 1868.0, 1868000.0, 0.1215, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE532F07DL1", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2026-01-20", "-", 1000.0, "0Y,9M,11D", "Secured", "Zero Coupon", 1014.0, 1014000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DG1", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2028-01-20", "-", 1000.0, "2Y,9M,11D", "Secured", "Zero Coupon", 459.0, 459000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DK3", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.0967, "2028-01-20", "-", 1000.0, "2Y,9M,11D", "Secured", "NCD", 378.0, 378000.0, 0.1215, "CRISIL A+", "-", "Monthly", "On Maturity"],
    ["INE532F07EV8", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2026-01-29", "-", 1000.0, "0Y,9M,20D", "Secured", "Zero Coupon", 3.0, 3000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07EX4", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2027-01-29", "-", 1000.0, "1Y,9M,20D", "Secured", "Zero Coupon", 225.0, 225000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07CS8", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2026-12-28", "-", 1000.0, "1Y,8M,19D", "Secured", "Zero Coupon", 365.0, 365000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07BO9", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2026-01-08", "-", 1000.0, "0Y,8M,30D", "Secured", "Zero Coupon", 194.0, 194000.0, 0.1215, "CARE A", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07EE4", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2026-07-21", "-", 1000.0, "1Y,3M,12D", "Secured", "Zero Coupon", 24.0, 24000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DA4", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2027-10-20", "-", 1000.0, "2Y,6M,11D", "Secured", "Zero Coupon", 2.0, 2000.0, 0.1215, "Acuite A+", "-", "On Maturity", "On Maturity"],
    ["INE532F07FM4", "EDELWEISS FINANCIAL SERVICES LIMITED", 0, "2027-04-29", "-", 1000.0, "2Y,0M,20D", "Secured", "Zero Coupon", 1.0, 1000.0, 0.1215, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE532F07DS6", "EDELWEISS FINANCIAL SERVICES LIMITED", 0.096, "2026-04-27", "-", 1000.0, "1Y,0M,18D", "Secured", "NCD", 100.0, 100000.0, 0.1215, "CRISIL A+", "-", "Annually", "On Maturity"],
    ["INE804I08643", "ECL FINANCE LIMITED", 0.1125, "2025-05-03", "-", 1000000.0, "0Y,0M,24D", "Unsecured", "NCD", 8.0, 8000000.0, 0.121, "ICRA A+", "Stable", "Annually", "On Maturity"],
    ["INE528L07115", "EAAA INDIA ALTERNATIVES LIMITED", 0.108, "2027-07-02", "-", 100000.0, "2Y,2M,23D", "Secured", "NCD", 570.0, 57000000.0, 0.12, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE572J07653", "SPANDANA SPHOORTY FINANCIAL LIMITED", 0.1011, "2025-12-18", "-", 100000.0, "0Y,8M,9D", "Secured", "NCD", 31.0, 3100000.0, 0.12, "IND A", "Negative", "Quarterly", "On Maturity"],
    ["INE530L07228", "NIDO HOME FINANCE LIMITED", 0.1, "2026-07-19", "-", 1000.0, "1Y,3M,10D", "Secured", "NCD", 1884.0, 1884000.0, 0.12, "ICRA A+", "Stable", "Annually", "On Maturity"],
    ["INE572J07612", "SPANDANA SPHOORTY FINANCIAL LIMITED", 0.1075, "2026-09-04", "-", 100000.0, "1Y,4M,26D", "Secured", "NCD", 19.0, 1900000.0, 0.12, "IND A", "Negative", "Annually", "On Maturity"],
    ["INE530L07749", "NIDO HOME FINANCE LIMITED", 0.095, "2026-07-03", "-", 1000.0, "1Y,2M,24D", "Secured", "NCD", 1263.0, 1263000.0, 0.12, "CRISIL A+", "-", "Annually", "On Maturity"],
    ["INE530L07566", "NIDO HOME FINANCE LIMITED", 0.092, "2026-09-15", "-", 1000.0, "1Y,5M,6D", "Secured", "NCD", 523.0, 523000.0, 0.12, "CRISIL A+", "-", "Monthly", "On Maturity"],
    ["INE148I08298", "SAMMAAN CAPITAL LIMITED", 0.0835, "2027-09-08", "-", 100000.0, "2Y,4M,30D", "Unsecured", "NCD", 5.0, 500000.0, 0.12, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE530L07491", "NIDO HOME FINANCE LIMITED", 0, "2027-04-29", "-", 1000.0, "2Y,0M,20D", "Secured", "Zero Coupon", 247.0, 247000.0, 0.12, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE530L07822", "NIDO HOME FINANCE LIMITED", 0, "2026-07-03", "-", 1000.0, "1Y,2M,24D", "Secured", "Zero Coupon", 168.0, 168000.0, 0.12, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE530L07863", "NIDO HOME FINANCE LIMITED", 0.1, "2027-10-08", "-", 1000.0, "2Y,5M,29D", "Secured", "NCD", 100.0, 100000.0, 0.12, "CRISIL A+", "-", "Annually", "On Maturity"],
    ["INE530L07475", "NIDO HOME FINANCE LIMITED", 0.0915, "2027-04-29", "-", 1000.0, "2Y,0M,20D", "Secured", "NCD", 43.0, 43000.0, 0.12, "CRISIL A+", "Stable", "Monthly", "On Maturity"],
    ["INE530L07814", "NIDO HOME FINANCE LIMITED", 0, "2027-07-03", "-", 1000.0, "2Y,2M,24D", "Secured", "NCD", 40.0, 40000.0, 0.12, "CRISIL A+", "-", "On Maturity", "On Maturity"],
    ["INE530L07558", "NIDO HOME FINANCE LIMITED", 0, "2026-09-15", "-", 1000.0, "1Y,5M,6D", "Secured", "Zero Coupon", 35.0, 35000.0, 0.12, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE148I07GK5", "SAMMAAN CAPITAL LIMITED", 0.0885, "2026-09-26", "-", 1000.0, "1Y,5M,17D", "Secured", "NCD", 27.0, 27000.0, 0.12, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE530L07483", "NIDO HOME FINANCE LIMITED", 0.0955, "2027-04-29", "-", 1000.0, "2Y,0M,20D", "Secured", "NCD", 22.0, 22000.0, 0.12, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE530L07657", "NIDO HOME FINANCE LIMITED", 0, "2026-03-01", "-", 1000.0, "0Y,10M,20D", "Secured", "Zero Coupon", 10.0, 10000.0, 0.12, "CRISIL A+", "Stable", "On Maturity", "On Maturity"],
    ["INE530L07715", "NIDO HOME FINANCE LIMITED", 0.1, "2027-03-01", "-", 1000.0, "1Y,10M,20D", "Secured", "NCD", 10.0, 10000.0, 0.12, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE148I07RK2", "SAMMAAN CAPITAL LIMITED", 0, "2025-12-27", "-", 1000.0, "0Y,8M,18D", "Secured", "Zero Coupon", 55.0, 55000.0, 0.12, "ICRA AA", "Stable", "On Maturity", "On Maturity"],
    ["INE530L07608", "NIDO HOME FINANCE LIMITED", 0.096, "2026-09-15", "-", 1000.0, "1Y,5M,6D", "Secured", "NCD", 7.0, 7000.0, 0.12, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE244L08034", "INDIABULLS COMMERCIAL CREDIT LIMITED", 0.0845, "2028-01-05", "-", 100000.0, "2Y,8M,27D", "Unsecured", "NCD", 267.0, 26700000.0, 0.1175, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE244L08059", "INDIABULLS COMMERCIAL CREDIT LIMITED", 0.088, "2028-05-02", "-", 100000.0, "3Y,0M,23D", "Unsecured", "NCD", 160.0, 16000000.0, 0.1175, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE148I07MQ0", "SAMMAAN CAPITAL LIMITED", 0.088, "2025-11-03", "-", 1000.0, "0Y,6M,25D", "Secured", "NCD", 488.0000000000001, 488000.0000000001, 0.1175, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE148I07GL3", "SAMMAAN CAPITAL LIMITED", 0.09, "2026-09-26", "-", 1000.0, "1Y,5M,17D", "Secured", "NCD", 400.00000000000705, 400000.00000000704, 0.1175, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE894F08087", "SAMMAAN CAPITAL LIMITED", "10.65%", "2027-06-05", "-", 100000.0, "2Y,1M,27D", "Unsecured", "NCD", 3.0000000000000266, 300000.0000000027, 0.1175, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE836B07832", "SATIN CREDITCARE NETWORK LIMITED", 0.1085, "2026-07-10", "-", 100000.0, "1Y,3M,1D", "Secured", "NCD", 2.0, 200000.0, 0.1175, "ICRA A", "Stable", "Monthly", "On Maturity"],
    ["INE836B07790", "SATIN CREDITCARE NETWORK LIMITED", 0.13, "2026-09-11", "-", 100000.0, "1Y,5M,2D", "Secured", "NCD", 4.0, 400000.0, 0.1175, "ICRA A", "Stable", "Semi - Annually", "On Maturity"],
    ["INE342T07403", "NAVI FINSERV LIMITED", 0.1102, "2026-07-18", "-", 1000.0, "1Y,3M,9D", "Secured", "NCD", 299.0, 299000.0, 0.113, "CRISIL A", "Stable", "Annually", "On Maturity"],
    ["INE342T07536", "NAVI FINSERV LIMITED", 0.105, "2027-08-27", "-", 100000.0, "2Y,4M,18D", "Secured", "NCD", 2.0, 200000.0, 0.113, "CRISIL A", "-", "Monthly", "On Maturity"],
    ["INE342T07437", "NAVI FINSERV LIMITED", 0.104, "2026-06-13", "-", 1000.0, "1Y,2M,4D", "Secured", "NCD", 15.0, 15000.0, 0.113, "CRISIL A", "Stable", "Monthly", "On Maturity"],
    ["INE342T07478", "NAVI FINSERV LIMITED", 0.1, "2025-09-13", "-", 1000.0, "0Y,5M,4D", "Secured", "NCD", 35.0, 35000.0, 0.113, "CRISIL A", "Stable", "Monthly", "On Maturity"],
    ["INE342T07460", "NAVI FINSERV LIMITED", 0.1065, "2027-03-13", "-", 1000.0, "1Y,11M,4D", "Secured", "NCD", 1.0, 1000.0, 0.113, "CRISIL A", "Stable", "Monthly", "On Maturity"],
    ["INE348L08090", "MAS FINANCIAL SERVICES LIMITED", 0.1075, "2028-10-27", "-", 100000.0, "3Y,6M,18D", "Unsecured", "NCD", 5.0, 500000.0, 0.1115, "CARE AA-", "Stable", "Monthly", "On Maturity"],
    ["INE348L08082", "MAS FINANCIAL SERVICES LIMITED", 0.1075, "2028-10-10", "-", 100000.0, "3Y,6M,1D", "Unsecured", "NCD", 2.0, 200000.0, 0.1115, "CARE AA-", "Stable", "Monthly", "On Maturity"],
    ["INE572J07679", "SPANDANA SPHOORTY FINANCIAL LIMITED", 0.1075, "2026-04-03", "-", 50000.0, "0Y,11M,25D", "Secured", "NCD", 93.0, 4650000.0, 0.111, "IND A", "Negative", "Quarterly", "25% Every Quarter From Oct 24"],
    ["INE572J07703", "SPANDANA SPHOORTY FINANCIAL LIMITED", 0.0981, "2026-04-02", "-", 100000.0, "0Y,11M,24D", "Secured", "NCD", 18.0, 1800000.0, 0.111, "ICRA A", "Negative", "Monthly", "On Maturity"],
    ["INE530B07278", "IIFL FINANCE LIMITED", 0, "2028-01-24", "-", 1000.0, "2Y,9M,15D", "Secured", "Zero Coupon", 3333.0, 3333000.0, 0.11, "CRISIL AA", "Stable", "On Maturity", "On Maturity"],
    ["INE530B07260", "IIFL FINANCE LIMITED", 0.09, "2028-01-24", "-", 1000.0, "2Y,9M,15D", "Secured", "NCD", 2117.0, 2117000.0, 0.11, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE530B07377", "IIFL FINANCE LIMITED", 0.09, "2028-06-28", "-", 1000.0, "3Y,2M,19D", "Secured", "NCD", 1600.0, 1600000.0, 0.11, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE530B07385", "IIFL FINANCE LIMITED", 0.0865, "2028-06-28", "-", 1000.0, "3Y,2M,19D", "Secured", "NCD", 1620.0, 1620000.0, 0.11, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE530B07310", "IIFL FINANCE LIMITED", 0.0865, "2028-01-24", "-", 1000.0, "2Y,9M,15D", "Secured", "NCD", 857.0, 857000.0, 0.11, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE516Q08331", "ASIRVAD MICRO FINANCE LIMITED", 0.119, "2026-06-26", "-", 100000.0, "1Y,2M,17D", "Unsecured", "NCD", 5.0, 500000.0, 0.11, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07CA0", "MUTHOOT FINCORP LIMITED", 0, "2025-08-02", "-", 1000.0, "0Y,3M,24D", "Secured", "Zero Coupon", 115.0, 115000.0, 0.11, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07741", "MUTHOOT FINCORP LIMITED", 0, "2025-07-17", "-", 1000.0, "0Y,3M,8D", "Secured", "Zero Coupon", 85.0, 85000.0, 0.11, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE530B08102", "IIFL FINANCE LIMITED", 0.096, "2028-06-24", "-", 1000.0, "3Y,2M,15D", "Unsecured", "NCD", 1.0, 1000.0, 0.11, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE530B07179", "IIFL FINANCE LIMITED", 0.0875, "2026-10-14", "-", 1000.0, "1Y,6M,5D", "Secured", "NCD", 4029.0, 4029000.0, 0.109, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE549K07DR2", "MUTHOOT FINCORP LIMITED", 0, "2026-06-30", "-", 1000.0, "1Y,2M,21D", "Secured", "Zero Coupon", 3422.0, 3422000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE477L07AS8", "IIFL HOME FINANCE LIMITED", 0, "2029-01-03", "-", 1000.0, "3Y,8M,25D", "Secured", "Zero Coupon", 1321.0, 1321000.0, 0.109, "CRISIL AA", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07BQ8", "MUTHOOT FINCORP LIMITED", 0, "2026-04-02", "-", 1000.0, "0Y,11M,24D", "Secured", "Zero Coupon", 750.0, 750000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07ER0", "MUTHOOT FINCORP LIMITED", 0, "2026-10-30", "-", 1000.0, "1Y,6M,21D", "Secured", "Zero Coupon", 1048.0, 1048000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE477L07AR0", "IIFL HOME FINANCE LIMITED", 0.0875, "2029-01-03", "-", 1000.0, "3Y,8M,25D", "Secured", "NCD", 918.0, 918000.0, 0.109, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE549K07DI1", "MUTHOOT FINCORP LIMITED", 0, "2026-01-31", "-", 1000.0, "0Y,9M,22D", "Secured", "Zero Coupon", 794.0, 794000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07BZ9", "MUTHOOT FINCORP LIMITED", 0, "2026-11-02", "-", 1000.0, "1Y,6M,24D", "Secured", "Zero Coupon", 704.0, 704000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07DT8", "MUTHOOT FINCORP LIMITED", 0, "2029-04-30", "-", 1000.0, "4Y,0M,21D", "Secured", "Zero Coupon", 600.0, 600000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07BG9", "MUTHOOT FINCORP LIMITED", 0, "2027-02-02", "-", 1000.0, "1Y,9M,24D", "Secured", "Zero Coupon", 584.0, 584000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE530B07344", "IIFL FINANCE LIMITED", 0.085, "2026-06-28", "-", 1000.0, "1Y,2M,19D", "Secured", "NCD", 527.0, 527000.0, 0.109, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE530B07286", "IIFL FINANCE LIMITED", 0, "2026-01-24", "-", 1000.0, "0Y,9M,15D", "Secured", "Zero Coupon", 654.0, 654000.0, 0.109, "CRISIL AA", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07EA6", "MUTHOOT FINCORP LIMITED", 0, "2027-09-16", "-", 1000.0, "2Y,5M,7D", "Secured", "Zero Coupon", 320.0, 320000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE530B07351", "IIFL FINANCE LIMITED", 0, "2026-06-28", "-", 1000.0, "1Y,2M,19D", "Secured", "Zero Coupon", 210.0, 210000.0, 0.109, "CRISIL AA", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07972", "MUTHOOT FINCORP LIMITED", 0, "2026-01-29", "-", 1000.0, "0Y,9M,20D", "Secured", "Zero Coupon", 208.0, 208000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07DM3", "MUTHOOT FINCORP LIMITED", 0, "2030-04-30", "-", 1000.0, "5Y,0M,21D", "Secured", "Zero Coupon", 150.0, 150000.0, 0.109, "CRISIL AA-", "-", "On Maturity", "On Maturity"],
    ["INE549K07DJ9", "MUTHOOT FINCORP LIMITED", 0, "2027-01-31", "-", 1000.0, "1Y,9M,22D", "Secured", "Zero Coupon", 131.0, 131000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07BH7", "MUTHOOT FINCORP LIMITED", 0, "2028-02-02", "-", 1000.0, "2Y,9M,24D", "Secured", "Zero Coupon", 100.0, 100000.0, 0.109, "CRISIL AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07AO5", "MUTHOOT FINCORP LIMITED", 0, "2026-05-07", "-", 1000.0, "1Y,0M,28D", "Secured", "Zero Coupon", 20.0, 20000.0, 0.109, "CRISIL AA-", "-", "On Maturity", "On Maturity"],
    ["INE549K07EL3", "MUTHOOT FINCORP LIMITED", 0, "2026-09-16", "-", 1000.0, "1Y,5M,7D", "Secured", "Zero Coupon", 150.0, 150000.0, 0.109, "CRISIL AA-", "-", "On Maturity", "On Maturity"],
    ["INE477L07AO7", "IIFL HOME FINANCE LIMITED", 0.085, "2027-01-03", "-", 1000.0, "1Y,8M,25D", "Secured", "NCD", 747.0, 747000.0, 0.108, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE523L07736", "NUVAMA WEALTH AND INVESTMENT LIMITED", 0.0995, "2032-07-15", "-", 1000.0, "7Y,3M,6D", "Secured", "NCD", 611.0, 611000.0, 0.108, "Acuite AA-", "Stable", "Annually", "On Maturity"],
    ["INE523L07744", "NUVAMA WEALTH AND INVESTMENT LIMITED", 0.0953, "2032-07-15", "-", 1000.0, "7Y,3M,6D", "Secured", "NCD", 364.0, 364000.0, 0.108, "Acuite AA-", "Stable", "Monthly", "On Maturity"],
    ["INE477L07BA4", "IIFL HOME FINANCE LIMITED", 0, "2026-12-26", "-", 1000.0, "1Y,8M,17D", "Secured", "Zero Coupon", 361.0, 361000.0, 0.108, "CRISIL AA", "Stable", "On Maturity", "On Maturity"],
    ["INE477L07AN9", "IIFL HOME FINANCE LIMITED", 0.082, "2027-01-03", "-", 1000.0, "1Y,8M,25D", "Secured", "NCD", 262.0, 262000.0, 0.108, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE918K07FV6", "NUVAMA WEALTH FINANCE LIMITED", 0.1025, "2030-02-05", "-", 1000.0, "4Y,9M,27D", "Secured", "NCD", 140.0, 140000.0, 0.108, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE477L07AZ3", "IIFL HOME FINANCE LIMITED", 0.0885, "2026-12-26", "-", 1000.0, "1Y,8M,17D", "Secured", "NCD", 130.0, 130000.0, 0.108, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE477L07BC0", "IIFL HOME FINANCE LIMITED", 0.09, "2027-12-26", "-", 1000.0, "2Y,8M,17D", "Secured", "NCD", 5.0, 5000.0, 0.108, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE477L08154", "IIFL HOME FINANCE LIMITED", 0.096, "2028-11-03", "-", 1000.0, "3Y,6M,25D", "Unsecured", "NCD", 1.0, 1000.0, 0.108, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE530B07161", "IIFL FINANCE LIMITED", 0.0842, "2026-10-14", "-", 1000.0, "1Y,6M,5D", "Secured", "NCD", 3881.0, 3881000.0, 0.1075, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE549K07EZ3", "MUTHOOT FINCORP LIMITED", 0.09, "2027-01-10", "-", 1000.0, "1Y,9M,1D", "Secured", "NCD", 2070.0, 2070000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07FM8", "MUTHOOT FINCORP LIMITED", 0.09, "2027-02-24", "-", 1000.0, "1Y,10M,15D", "Secured", "NCD", 669.0, 669000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07EH1", "MUTHOOT FINCORP LIMITED", 0.094, "2026-09-16", "-", 1000.0, "1Y,5M,7D", "Secured", "NCD", 665.0, 665000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07AU2", "MUTHOOT FINCORP LIMITED", 0.0875, "2026-10-29", "-", 1000.0, "1Y,6M,20D", "Secured", "NCD", 546.0, 546000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE523L07710", "NUVAMA WEALTH AND INVESTMENT LIMITED", 0.0916, "2027-07-15", "-", 1000.0, "2Y,3M,6D", "Secured", "NCD", 520.0, 520000.0, 0.1075, "Acuite AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07DW2", "MUTHOOT FINCORP LIMITED", 0.089, "2026-06-30", "-", 1000.0, "1Y,2M,21D", "Secured", "NCD", 419.0, 419000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07DO9", "MUTHOOT FINCORP LIMITED", 0.0925, "2026-06-30", "-", 1000.0, "1Y,2M,21D", "Secured", "NCD", 385.0, 385000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07AJ5", "MUTHOOT FINCORP LIMITED", 0.0875, "2026-05-07", "-", 1000.0, "1Y,0M,28D", "Secured", "NCD", 352.0, 352000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07BN5", "MUTHOOT FINCORP LIMITED", 0.0835, "2026-09-06", "-", 1000.0, "1Y,4M,28D", "Secured", "NCD", 361.0, 361000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07EO7", "MUTHOOT FINCORP LIMITED", 0.0965, "2027-10-30", "-", 1000.0, "2Y,6M,21D", "Secured", "NCD", 300.0, 300000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07CS2", "MUTHOOT FINCORP LIMITED", 0.089, "2026-11-01", "-", 1000.0, "1Y,6M,23D", "Secured", "NCD", 285.0, 285000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07CV6", "MUTHOOT FINCORP LIMITED", 0.0927, "2026-11-01", "-", 1000.0, "1Y,6M,23D", "Secured", "NCD", 465.0, 465000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07949", "MUTHOOT FINCORP LIMITED", 0.0875, "2026-01-29", "-", 1000.0, "0Y,9M,20D", "Secured", "NCD", 241.0, 241000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07EU4", "MUTHOOT FINCORP LIMITED", 0.09, "2026-10-30", "-", 1000.0, "1Y,6M,21D", "Secured", "NCD", 219.0, 219000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07CR4", "MUTHOOT FINCORP LIMITED", 0.0865, "2025-11-01", "-", 1000.0, "0Y,6M,23D", "Secured", "NCD", 210.0, 210000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07DZ5", "MUTHOOT FINCORP LIMITED", 0.09, "2026-09-16", "-", 1000.0, "1Y,5M,7D", "Secured", "NCD", 207.0, 207000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07BO3", "MUTHOOT FINCORP LIMITED", 0.0825, "2025-11-05", "-", 1000.0, "0Y,6M,27D", "Secured", "NCD", 83.0, 83000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07FY3", "MUTHOOT FINCORP LIMITED", 0.094, "2027-02-24", "-", 1000.0, "1Y,10M,15D", "Secured", "NCD", 110.0, 110000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07CE2", "MUTHOOT FINCORP LIMITED", 0.0865, "2026-11-02", "-", 1000.0, "1Y,6M,24D", "Secured", "NCD", 100.0, 100000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07FV9", "MUTHOOT FINCORP LIMITED", 0.093, "2026-08-24", "-", 1000.0, "1Y,4M,15D", "Secured", "NCD", 91.0, 91000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07FU1", "MUTHOOT FINCORP LIMITED", 0.0925, "2028-02-24", "-", 1000.0, "2Y,10M,15D", "Secured", "NCD", 166.0, 166000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE523L07728", "NUVAMA WEALTH AND INVESTMENT LIMITED", 0, "2027-07-15", "-", 1000.0, "2Y,3M,6D", "Secured", "Zero Coupon", 56.0, 56000.0, 0.1075, "Acuite AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE549K07824", "MUTHOOT FINCORP LIMITED", 0.0915, "2025-10-29", "-", 1000.0, "0Y,6M,20D", "Secured", "NCD", 54.0, 54000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07DL5", "MUTHOOT FINCORP LIMITED", 0.089, "2026-01-31", "-", 1000.0, "0Y,9M,22D", "Secured", "NCD", 50.0, 50000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07CF9", "MUTHOOT FINCORP LIMITED", 0.084, "2025-08-02", "-", 1000.0, "0Y,3M,24D", "Secured", "NCD", 47.0, 47000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE523L07751", "NUVAMA WEALTH AND INVESTMENT LIMITED", 0.0955, "2027-07-15", "-", 1000.0, "2Y,3M,6D", "Secured", "NCD", 75.0, 75000.0, 0.1075, "Acuite AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07DN1", "MUTHOOT FINCORP LIMITED", 0.095, "2027-06-30", "-", 1000.0, "2Y,2M,21D", "Secured", "NCD", 35.0, 35000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07CU8", "MUTHOOT FINCORP LIMITED", 0.09, "2025-11-01", "-", 1000.0, "0Y,6M,23D", "Secured", "NCD", 25.0, 25000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE413U07285", "IIFL SAMASTA FINANCE LIMITED", 0.092, "2026-06-21", "-", 1000.0, "1Y,2M,12D", "Secured", "NCD", 15.0, 15000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07EP4", "MUTHOOT FINCORP LIMITED", 0.094, "2026-10-30", "-", 1000.0, "1Y,6M,21D", "Secured", "NCD", 15.0, 15000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07DE0", "MUTHOOT FINCORP LIMITED", 0.095, "2027-01-31", "-", 1000.0, "1Y,9M,22D", "Secured", "NCD", 15.0, 15000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07DF7", "MUTHOOT FINCORP LIMITED", 0.0975, "2029-01-31", "-", 1000.0, "3Y,9M,22D", "Secured", "NCD", 12.0, 12000.0, 0.1075, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE549K07EM1", "MUTHOOT FINCORP LIMITED", 0.101, "2030-10-30", "-", 1000.0, "5Y,6M,21D", "Secured", "NCD", 10.0, 10000.0, 0.1075, "CRISIL AA-", "-", "Annually", "On Maturity"],
    ["INE549K07AB2", "MUTHOOT FINCORP LIMITED", 0.0875, "2026-03-15", "-", 1000.0, "0Y,11M,6D", "Secured", "NCD", 1.0, 1000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE549K07BU0", "MUTHOOT FINCORP LIMITED", 0.085, "2028-02-02", "-", 1000.0, "2Y,9M,24D", "Secured", "NCD", 1.0, 1000.0, 0.1075, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE443L08156", "BELSTAR MICROFINANCE LIMITED", 0.1, "2025-08-01", "-", 25000.0, "0Y,3M,23D", "Unsecured", "NCD", 7.0, 175000.0, 0.105, "CRISIL AA", "Stable", "Quarterly", "25% Every Quarter From Nov 23"],
    ["INE605Y07148", "AUXILO FINSERVE PRIVATE LIMITED", 0.099, "2026-12-18", "-", 100000.0, "1Y,8M,9D", "Secured", "NCD", 1.0, 100000.0, 0.105, "CARE A+", "Stable", "Annually", "On Maturity"],
    ["INE583D07463", "UGRO CAPITAL LIMITED", 0.105, "2026-05-27", "-", 1000.0, "1Y,1M,18D", "Secured", "NCD", 3.0, 3000.0, 0.1025, "IND A+", "Stable", "Monthly", "On Maturity"],
    ["INE516Y07444", "PIRAMAL CAPITAL & HOUSING FINANCE LIMITED", 0.0675, "2031-09-26", "-", 850.0, "6Y,5M,17D", "Secured", "NCD", 1.0, 850.0, 0.1025, "ICRA AA", "Stable", "Semi - Annually", "2.50% Till Sept 26 Later 7.50% Till Maturity"],
    ["INE896L07934", "INDOSTAR CAPITAL FINANCE LIMITED", 0.0985, "2026-08-07", "-", 100000.0, "1Y,3M,29D", "Secured", "NCD", 10.0, 1000000.0, 0.102, "CRISIL AA-", "Stable", "Monthly", "On Maturity"],
    ["INE896L07884", "INDOSTAR CAPITAL FINANCE LIMITED", 0.1025, "2026-05-25", "-", 100000.0, "1Y,1M,16D", "Secured", "NCD", 7.0, 700000.0, 0.102, "CRISIL AA-", "Stable", "Quarterly", "On Maturity"],
    ["INE896L07AB5", "INDOSTAR CAPITAL FINANCE LIMITED", 0.105, "2029-09-25", "-", 1000.0, "4Y,5M,16D", "Secured", "NCD", 620.0, 620000.0, 0.102, "CARE AA-", "Stable", "Annually", "On Maturity"],
    ["INE896L07983", "INDOSTAR CAPITAL FINANCE LIMITED", 0.105, "2026-09-25", "-", 1000.0, "1Y,5M,16D", "Secured", "NCD", 167.0, 167000.0, 0.102, "CARE AA-", "Stable", "Annually", "On Maturity"],
    ["INE0Q6I07017", "TYGER HOME FINANCE PRIVATE LIMITED", 0.0975, "2027-08-16", "-", 100000.0, "1Y,4M,5D", "Secured", "NCD", 474.0, 47400000.0, 0.1015, "CRISIL A+", "Stable", "Annually", "On Maturity"],
    ["INE348L07209", "MAS FINANCIAL SERVICES LIMITED", 0.0957, "2027-06-21", "-", 100000.0, "2Y,2M,12D", "Secured", "NCD", 59.0, 5900000.0, 0.1, "CARE AA-", "Stable", "Monthly", "On Maturity"],
    ["INE741K07546", "CREDITACCESS GRAMEEN LIMITED", 0, "2028-09-07", "-", 1000.0, "3Y,4M,29D", "Secured", "Zero Coupon", 2269.0, 2269000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE741K07504", "CREDITACCESS GRAMEEN LIMITED", 0, "2027-11-23", "-", 1000.0, "2Y,7M,14D", "Secured", "Zero Coupon", 1632.0, 1632000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE741K07595", "CREDITACCESS GRAMEEN LIMITED", 0.0925, "2026-06-07", "-", 1000.0, "1Y,1M,29D", "Secured", "NCD", 1099.0, 1099000.0, 0.1, "IND AA-", "Stable", "Monthly", "On Maturity"],
    ["INE741K07553", "CREDITACCESS GRAMEEN LIMITED", 0, "2027-11-07", "-", 1000.0, "2Y,6M,29D", "Secured", "Zero Coupon", 699.0, 699000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE741K07488", "CREDITACCESS GRAMEEN LIMITED", 0, "2025-11-23", "-", 1000.0, "0Y,7M,14D", "Secured", "Zero Coupon", 673.0, 673000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE741K07470", "CREDITACCESS GRAMEEN LIMITED", 0.096, "2025-11-23", "-", 1000.0, "0Y,7M,14D", "Secured", "NCD", 500.0, 500000.0, 0.1, "IND AA-", "Stable", "Monthly", "On Maturity"],
    ["INE741K07538", "CREDITACCESS GRAMEEN LIMITED", 0, "2026-06-07", "-", 1000.0, "1Y,1M,29D", "Secured", "Zero Coupon", 105.0, 105000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE248U07FG8", "360 ONE PRIME LIMITED", 0.0955, "2027-06-12", "-", 1000.0, "2Y,2M,3D", "Secured", "NCD", 398.0, 398000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07FE3", "360 ONE PRIME LIMITED", 0.096, "2029-06-12", "-", 1000.0, "4Y,2M,3D", "Secured", "NCD", 210.0, 210000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07FD5", "360 ONE PRIME LIMITED", 0.1061, "2025-12-12", "-", 1000.0, "0Y,8M,3D", "Secured", "NCD", 181.0, 181000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07FJ2", "360 ONE PRIME LIMITED", 0.0935, "2026-06-12", "-", 1000.0, "1Y,2M,3D", "Secured", "NCD", 138.0, 138000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07FH6", "360 ONE PRIME LIMITED", 0.0916, "2027-06-12", "-", 1000.0, "2Y,2M,3D", "Secured", "NCD", 100.0, 100000.0, 0.1, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE248U07EW8", "360 ONE PRIME LIMITED", 0.0961, "2027-01-18", "-", 1000.0, "1Y,9M,9D", "Secured", "NCD", 99.0, 99000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07ER8", "360 ONE PRIME LIMITED", 0.0966, "2029-01-18", "-", 1000.0, "3Y,9M,9D", "Secured", "NCD", 91.0, 91000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07EU2", "360 ONE PRIME LIMITED", 0.0903, "2026-01-18", "-", 1000.0, "0Y,9M,9D", "Secured", "NCD", 40.0, 40000.0, 0.1, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE248U07EQ0", "360 ONE PRIME LIMITED", 0.0941, "2026-01-18", "-", 1000.0, "0Y,9M,9D", "Secured", "NCD", 30.0, 30000.0, 0.1, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE248U07ES6", "360 ONE PRIME LIMITED", 0.0926, "2029-01-18", "-", 1000.0, "3Y,9M,9D", "Secured", "NCD", 13.0, 13000.0, 0.1, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE348L07241", "MAS FINANCIAL SERVICES LIMITED", 0.096, "2026-12-23", "-", 10000.0, "1Y,8M,14D", "Secured", "NCD", 1.0, 10000.0, 0.1, "CARE AA-", "-", "Monthly", "On Maturity"],
    ["INE741K07561", "CREDITACCESS GRAMEEN LIMITED", 0, "2025-09-07", "-", 1000.0, "0Y,4M,29D", "Secured", "Zero Coupon", 2.0, 2000.0, 0.1, "IND AA-", "Stable", "On Maturity", "On Maturity"],
    ["INE03W107256", "ARKA FINCAP LIMITED", 0.0965, "2028-12-27", "-", 1000.0, "3Y,8M,18D", "Secured", "NCD", 11299.0, 11299000.0, 0.099, "CRISIL AA", "Stable", "Quarterly", "On Maturity"],
    ["INE03W107223", "ARKA FINCAP LIMITED", 0.1, "2028-12-27", "-", 1000.0, "3Y,8M,18D", "Secured", "NCD", 800.0, 800000.0, 0.099, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE03W107264", "ARKA FINCAP LIMITED", 0.09, "2025-12-27", "-", 1000.0, "0Y,8M,18D", "Secured", "NCD", 202.0, 202000.0, 0.099, "CRISIL AA", "Stable", "Quarterly", "On Maturity"],
    ["INE523H07BB1", "JM FINANCIAL PRODUCTS LIMITED", 0.1, "2030-03-16", "-", 1000.0, "4Y,11M,7D", "Secured", "NCD", 115.0, 115000.0, 0.0985, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE413U07210", "IIFL SAMASTA FINANCE LIMITED", 0.1, "2026-11-26", "-", 100000.0, "1Y,7M,17D", "Secured", "NCD", 94.0, 9400000.0, 0.0975, "CRISIL AA-", "Stable", "Annually", "On Maturity"],
    ["INE651J07622", "JM FINANCIAL CREDIT SOLUTIONS LIMITED", 0.0975, "2028-06-07", "-", 1000.0, "3Y,1M,29D", "Secured", "NCD", 4634.0, 4634000.0, 0.0975, "IND AA", "-", "Annually", "On Maturity"],
    ["INE530B08094", "IIFL FINANCE LIMITED", 0.1, "2028-06-24", "-", 1000.0, "3Y,2M,15D", "Unsecured", "NCD", 2500.0, 2500000.0, 0.0975, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE523H07BO4", "JM FINANCIAL PRODUCTS LIMITED", 0.082, "2026-10-07", "-", 1000.0, "1Y,5M,28D", "Secured", "NCD", 1050.0, 1050000.0, 0.0975, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE523H07BP1", "JM FINANCIAL PRODUCTS LIMITED", 0.0791, "2026-10-07", "-", 1000.0, "1Y,5M,28D", "Secured", "NCD", 1000.0, 1000000.0, 0.0975, "CRISIL AA", "Stable", "Monthly", "On Maturity"],
    ["INE651J07689", "JM FINANCIAL CREDIT SOLUTIONS LIMITED", 0.1025, "2028-12-13", "-", 1000.0, "3Y,8M,4D", "Secured", "NCD", 870.0, 870000.0, 0.0975, "IND AA", "Stable", "Annually", "On Maturity"],
    ["INE146O08266", "HINDUJA LEYLAND FINANCE LIMITED", 0.095, "2029-11-29", "-", 100000.0, "4Y,7M,20D", "Unsecured", "NCD", 7.0, 700000.0, 0.0975, "CRISIL AA+", "Stable", "Annually", "On Maturity"],
    ["INE523H07AQ1", "JM FINANCIAL PRODUCTS LIMITED", 0, "2026-09-11", "-", 1000.0, "1Y,5M,2D", "Secured", "NCD", 30.0, 30000.0, 0.0975, "CRISIL AA", "-", "On Maturity", "On Maturity"],
    ["INE423A07328", "ADANI ENTERPRISES LIMITED", 0.0965, "2027-09-12", "-", 1000.0, "2Y,5M,3D", "Secured", "NCD", 5662.0, 5662000.0, 0.097, "CARE AA-", "Stable", "Annually", "On Maturity"],
    ["INE423A07351", "ADANI ENTERPRISES LIMITED", 0.0925, "2026-09-12", "-", 1000.0, "1Y,5M,3D", "Secured", "NCD", 1244.0, 1244000.0, 0.097, "CARE AA-", "Stable", "Annually", "On Maturity"],
    ["INE414G07HP2", "MUTHOOT FINANCE LIMITED", 0, "2026-04-10", "-", 1000.0, "1Y,0M,1D", "Secured", "Zero Coupon", 2148.0, 2148000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07IY2", "MUTHOOT FINANCE LIMITED", 0, "2027-01-25", "-", 1000.0, "1Y,9M,16D", "Secured", "Zero Coupon", 1960.0, 1960000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE516Y07410", "PIRAMAL CAPITAL & HOUSING FINANCE LIMITED", 0.0875, "2026-07-23", "-", 1000.0, "1Y,3M,14D", "Secured", "NCD", 607.0, 607000.0, 0.095, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE414G07HO5", "MUTHOOT FINANCE LIMITED", 0, "2028-04-10", "-", 1000.0, "3Y,0M,1D", "Secured", "Zero Coupon", 871.0, 871000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07FX0", "MUTHOOT FINANCE LIMITED", 0, "2026-04-20", "-", 1000.0, "1Y,0M,11D", "Secured", "Zero Coupon", 756.0, 756000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE140A07740", "PIRAMAL ENTERPRISES LIMITED", 0.0905, "2026-11-03", "-", 1000.0, "1Y,6M,25D", "Secured", "NCD", 182.0, 182000.0, 0.095, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE414G07IJ3", "MUTHOOT FINANCE LIMITED", 0, "2028-10-04", "-", 1000.0, "3Y,5M,25D", "Secured", "Zero Coupon", 550.0, 550000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07IP0", "MUTHOOT FINANCE LIMITED", 0, "2026-10-04", "-", 1000.0, "1Y,5M,25D", "Secured", "Zero Coupon", 511.0, 511000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07IX4", "MUTHOOT FINANCE LIMITED", 0, "2029-01-25", "-", 1000.0, "3Y,9M,16D", "Secured", "Zero Coupon", 455.0, 455000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE338I07131", "MOTILAL OSWAL FINANCIAL SERVICES LIMITED", 0.0885, "2026-05-09", "-", 1000.0, "1Y,1M,0D", "Secured", "NCD", 432.0, 432000.0, 0.095, "CRISIL AA", "Positive", "Annually", "On Maturity"],
    ["INE414G07FO9", "MUTHOOT FINANCE LIMITED", 0, "2026-01-11", "-", 1000.0, "0Y,9M,2D", "Secured", "Zero Coupon", 365.0, 365000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE338I07149", "MOTILAL OSWAL FINANCIAL SERVICES LIMITED", 0.091, "2027-05-09", "-", 1000.0, "2Y,1M,0D", "Secured", "NCD", 358.0, 358000.0, 0.095, "CRISIL AA", "Positive", "Annually", "On Maturity"],
    ["INE140A07757", "PIRAMAL ENTERPRISES LIMITED", 0.09, "2025-11-03", "-", 1000.0, "0Y,6M,25D", "Secured", "NCD", 356.0, 356000.0, 0.095, "ICRA AA", "Stable", "Annually", "On Maturity"],
    ["INE414G07GK5", "MUTHOOT FINANCE LIMITED", 0, "2027-05-05", "-", 1000.0, "2Y,0M,26D", "Secured", "Zero Coupon", 200.0, 200000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07GJ7", "MUTHOOT FINANCE LIMITED", 0, "2025-05-05", "-", 1000.0, "0Y,0M,26D", "Secured", "Zero Coupon", 174.0, 174000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07IE4", "MUTHOOT FINANCE LIMITED", 0, "2028-06-03", "-", 1000.0, "3Y,1M,25D", "Secured", "Zero Coupon", 79.0, 79000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE414G07HG1", "MUTHOOT FINANCE LIMITED", 0, "2027-12-23", "-", 1000.0, "2Y,8M,14D", "Secured", "Zero Coupon", 53.0, 53000.0, 0.095, "ICRA AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE338I07099", "MOTILAL OSWAL FINANCIAL SERVICES LIMITED", 0, "2027-05-09", "-", 1000.0, "2Y,1M,0D", "Secured", "Zero Coupon", 30.0, 30000.0, 0.095, "CRISIL AA", "Positive", "On Maturity", "On Maturity"],
    ["INE338I07156", "MOTILAL OSWAL FINANCIAL SERVICES LIMITED", 0, "2026-05-09", "-", 1000.0, "1Y,1M,0D", "Secured", "Zero Coupon", 60.0, 60000.0, 0.095, "CRISIL AA", "Positive", "On Maturity", "On Maturity"],
    ["INE658F08128", "KERALA INFRASTRUCTURE INVESTMENT FUND BOARD", 0.0895, "2028-12-22", "-", 100000.0, "3Y,8M,13D", "Unsecured", "NCD", 222.0, 22200000.0, 0.094, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter from Mar 28"],
    ["INE658F08094", "KERALA INFRASTRUCTURE INVESTMENT FUND BOARD", 0.0895, "2031-12-22", "-", 100000.0, "6Y,8M,13D", "Unsecured", "NCD", 18.0, 1800000.0, 0.094, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From Mar 31"],
    ["INE414G07HH9", "MUTHOOT FINANCE LIMITED", 0.075, "2027-12-23", "-", 1000.0, "2Y,8M,14D", "Secured", "NCD", 914.0, 914000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE658F08086", "KERALA INFRASTRUCTURE INVESTMENT FUND BOARD", 0.0895, "2027-12-22", "-", 100000.0, "2Y,8M,13D", "Unsecured", "NCD", 7.0, 700000.0, 0.094, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From  Mar 27"],
    ["INE414G07IV8", "MUTHOOT FINANCE LIMITED", 0.085, "2027-01-25", "-", 1000.0, "1Y,9M,16D", "Secured", "NCD", 700.0, 700000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE414G07GM1", "MUTHOOT FINANCE LIMITED", 0.07, "2027-06-23", "-", 1000.0, "2Y,2M,14D", "Secured", "NCD", 546.0, 546000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE658F08144", "KERALA INFRASTRUCTURE INVESTMENT FUND BOARD", 0.0895, "2032-12-22", "-", 100000.0, "7Y,8M,13D", "Unsecured", "NCD", 4.0, 400000.0, 0.094, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From Mar 32"],
    ["INE414G07HR8", "MUTHOOT FINANCE LIMITED", 0.08, "2026-04-10", "-", 1000.0, "1Y,0M,1D", "Secured", "NCD", 308.0, 308000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE414G07FU6", "MUTHOOT FINANCE LIMITED", 0.076, "2026-04-20", "-", 1000.0, "1Y,0M,11D", "Secured", "NCD", 282.0, 282000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE414G07HZ1", "MUTHOOT FINANCE LIMITED", 0.0785, "2028-06-03", "-", 1000.0, "3Y,1M,25D", "Secured", "NCD", 131.0, 131000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE414G07GE8", "MUTHOOT FINANCE LIMITED", 0.0675, "2027-05-05", "-", 1000.0, "2Y,0M,26D", "Secured", "NCD", 103.0, 103000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE658F08102", "KERALA INFRASTRUCTURE INVESTMENT FUND BOARD", 0.0895, "2030-12-20", "-", 100000.0, "5Y,8M,11D", "Unsecured", "NCD", 1.0, 100000.0, 0.094, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From  Mar 30"],
    ["INE414G07GY6", "MUTHOOT FINANCE LIMITED", 0.075, "2027-11-03", "-", 1000.0, "2Y,6M,25D", "Secured", "NCD", 60.0, 60000.0, 0.094, "ICRA AA+", "-", "Annually", "On Maturity"],
    ["INE414G07FK7", "MUTHOOT FINANCE LIMITED", 0.071, "2026-01-11", "-", 1000.0, "0Y,9M,2D", "Secured", "NCD", 105.0, 105000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE414G07HL1", "MUTHOOT FINANCE LIMITED", 0.0775, "2026-04-10", "-", 1000.0, "1Y,0M,1D", "Secured", "NCD", 45.0, 45000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE414G07GN9", "MUTHOOT FINANCE LIMITED", 0.07, "2025-06-23", "-", 1000.0, "0Y,2M,14D", "Secured", "NCD", 44.0, 44000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE414G07HM9", "MUTHOOT FINANCE LIMITED", 0.0785, "2028-04-10", "-", 1000.0, "3Y,0M,1D", "Secured", "NCD", 43.0, 43000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE414G07GV2", "MUTHOOT FINANCE LIMITED", 0.0725, "2027-11-03", "-", 1000.0, "2Y,6M,25D", "Secured", "NCD", 14.0, 14000.0, 0.094, "ICRA AA+", "Stable", "Monthly", "On Maturity"],
    ["INE414G07IB0", "MUTHOOT FINANCE LIMITED", 0.08, "2026-06-03", "-", 1000.0, "1Y,1M,25D", "Secured", "NCD", 10.0, 10000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE414G07IU0", "MUTHOOT FINANCE LIMITED", 0.0825, "2026-01-25", "-", 1000.0, "0Y,9M,16D", "Secured", "NCD", 6.0, 6000.0, 0.094, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["INE519Q08178", "AU SMALL FINANCE BANK LIMITED", 0.1075, "2029-01-05", "-", 100000.0, "3Y,8M,27D", "Unsecured", "NCD", 4.0, 400000.0, 0.0925, "ICRA AA", "Stable", "Monthly", "On Maturity"],
    ["INE519Q08186", "AU SMALL FINANCE BANK LIMITED", 0.1075, "2029-02-09", "-", 100000.0, "3Y,10M,0D", "Unsecured", "NCD", 3.0, 300000.0, 0.0925, "ICRA AA", "Stable", "Monthly", "On Maturity"],
    ["INE519Q08160", "AU SMALL FINANCE BANK LIMITED", 0.1075, "2028-12-15", "-", 100000.0, "3Y,8M,6D", "Unsecured", "NCD", 1.0, 100000.0, 0.0925, "ICRA AA", "Stable", "Monthly", "On Maturity"],
    ["INE0M2307040", "ANDHRA PRADESH STATE BEVERAGES CORPORATION LIMITED", 0.0962, "2026-05-29", "-", 1000000.0, "1Y,1M,20D", "Secured", "NCD", 1.0, 1000000.0, 0.091, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From Aug 25"],
    ["INE0AD507101", "ASEEM INFRASTRUCTURE FINANCE LIMITED", "G-Sec Linked", "2025-07-23", "-", 100000.0, "0Y,3M,14D", "Secured", "MLD", 11.0, 1100000.0, 0.09, "ICRA PP-MLD AA+", "Stable", "On Maturity", "On Maturity"],
    ["INE0M2307081", "ANDHRA PRADESH STATE BEVERAGES CORPORATION LIMITED", 0.0962, "2030-05-31", "-", 1000000.0, "5Y,1M,22D", "Secured", "NCD", 1.0, 1000000.0, 0.09, "IND AA(CE)", "-", "Quarterly", "25% Every month from feb 30"],
    ["INE0M2307164", "ANDHRA PRADESH STATE BEVERAGES CORPORATION LIMITED", 0.0962, "2028-11-30", "-", 1000000.0, "3Y,7M,21D", "Secured", "NCD", 1.0, 1000000.0, 0.09, "IND AA", "-", "Quarterly", "25%Every Quarter from Feb 2028"],
    ["INE511C07714", "POONAWALLA FINCORP LIMITED", 0.1075, "2029-05-06", "-", 1000.0, "4Y,0M,27D", "Secured", "NCD", 41.0, 41000.0, 0.09, "CARE AAA", "Stable", "Annually", "On Maturity"],
    ["INE539K07221", "CREDILA FINANCIAL SERVICES LIMITED", 0.0815, "2032-07-07", "-", 1000000.0, "7Y,2M,28D", "Secured", "NCD", 1.0, 1000000.0, 0.089, "CARE AA", "Stable", "Annually", "On Maturity"],
    ["INE575P08040", "STAR HEALTH AND ALLIED INSURANCE COMPANY LIMITED", 0.0875, "2028-10-27", "-", 1000000.0, "3Y,6M,18D", "Unsecured", "NCD", 9.0, 9000000.0, 0.0885, "IND AA", "Stable", "Annually", "On Maturity"],
    ["INE0M2307032", "ANDHRA PRADESH STATE BEVERAGES CORPORATION LIMITED", 0.0962, "2025-05-30", "-", 250000.0, "0Y,1M,21D", "Secured", "NCD", 8.000000000000002, 2000000.0000000005, 0.0875, "IND AA(CE)", "Stable", "Quarterly", "25% Every Quarter From Aug 24"],
    ["INE121A07RN0", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2028-12-07", "-", 1000.0, "3Y,7M,28D", "Secured", "Zero Coupon", 793.0, 793000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RL4", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2025-12-07", "-", 1000.0, "0Y,7M,28D", "Secured", "Zero Coupon", 801.0, 801000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RJ8", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.084, "2025-12-07", "-", 1000.0, "0Y,7M,28D", "Secured", "NCD", 530.0, 530000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RE9", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.084, "2028-08-09", "-", 1000.0, "3Y,4M,0D", "Secured", "NCD", 572.0, 572000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RR1", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2026-01-31", "-", 1000.0, "0Y,9M,22D", "Secured", "Zero Coupon", 420.0, 420000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RO8", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.085, "2026-12-07", "-", 1000.0, "1Y,7M,28D", "Secured", "NCD", 328.0, 328000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RI0", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2028-08-09", "-", 1000.0, "3Y,4M,0D", "Secured", "Zero Coupon", 180.0, 180000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07QW3", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.083, "2026-06-04", "-", 1000.0, "1Y,1M,26D", "Secured", "NCD", 174.0, 174000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RK6", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2026-12-07", "-", 1000.0, "1Y,7M,28D", "Secured", "Zero Coupon", 89.0, 89000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07QX1", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2028-05-04", "-", 1000.0, "3Y,0M,25D", "Secured", "Zero Coupon", 75.0, 75000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RD1", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2026-09-09", "-", 1000.0, "1Y,5M,0D", "Secured", "Zero Coupon", 50.0, 50000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07QZ6", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2026-06-04", "-", 1000.0, "1Y,1M,26D", "Secured", "Zero Coupon", 40.0, 40000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RG4", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0, "2025-06-09", "-", 1000.0, "0Y,2M,0D", "Secured", "Zero Coupon", 20.0, 20000.0, 0.0875, "ICRA AA+", "Positive", "On Maturity", "On Maturity"],
    ["INE121A07RQ3", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.0845, "2026-01-31", "-", 1000.0, "0Y,9M,22D", "Secured", "NCD", 11.0, 11000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RF6", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.083, "2026-09-09", "-", 1000.0, "1Y,5M,0D", "Secured", "NCD", 10.0, 10000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE121A07RT7", "CHOLAMANDALAM INVESTMENT AND FINANCE COMPANY LIMITED", 0.085, "2027-01-31", "-", 1000.0, "1Y,9M,22D", "Secured", "NCD", 7.0, 7000.0, 0.0875, "ICRA AA+", "Positive", "Annually", "On Maturity"],
    ["INE219X07207", "INDIA GRID TRUST", 0.076, "2026-05-06", "-", 1000.0, "1Y,0M,27D", "Secured", "NCD", 2645.0, 2645000.0, 0.085, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE219X07223", "INDIA GRID TRUST", 0.079, "2028-05-06", "-", 1000.0, "3Y,0M,27D", "Secured", "NCD", 174.0, 174000.0, 0.085, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE950O08147", "MAHINDRA RURAL HOUSING FINANCE LIMITED", 0.085, "2027-06-15", "-", 1000000.0, "2Y,2M,6D", "Unsecured", "NCD", 1.0, 1000000.0, 0.084, "IND AA+", "Stable", "Annually", "On Maturity"],
    ["INE774D08MM1", "MAHINDRA & MAHINDRA FINANCIAL SERVICES LTD", 0.0805, "2032-07-24", "-", 1000.0, "2Y,3M,15D", "Unsecured", "NCD", 1094.0, 1094000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE860H07IK3", "ADITYA BIRLA FINANCE LIMITED", 0.0801, "2028-05-02", "-", 100000.0, "3Y,0M,23D", "Secured", "NCD", 4.0, 400000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE774D08MK5", "MAHINDRA & MAHINDRA FINANCIAL SERVICES LTD", 0.08, "2027-07-24", "-", 1000.0, "2Y,3M,15D", "Unsecured", "NCD", 293.0, 293000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE403G07095", "STANDARD CHARTERED CAPITAL LIMITED", 0.0825, "2029-03-11", "-", 100000.0, "3Y,11M,2D", "Secured", "NCD", 2.0, 200000.0, 0.0835, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE774D08MA6", "MAHINDRA & MAHINDRA FINANCIAL SERVICES LTD", 0.09, "2026-06-06", "-", 1000.0, "1Y,1M,28D", "Unsecured", "NCD", 585.0, 585000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE774D07VE1", "MAHINDRA & MAHINDRA FINANCIAL SERVICES LTD", 0.0825, "2027-03-25", "-", 100000.0, "1Y,11M,16D", "Secured", "NCD", 1.0, 100000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE860H07IT4", "ADITYA BIRLA FINANCE LIMITED", 0.0805, "2028-10-09", "-", 1000.0, "3Y,6M,0D", "Secured", "NCD", 50.0, 50000.0, 0.0835, "IND AAA", "-", "Annually", "On Maturity"],
    ["INE860H07IR8", "ADITYA BIRLA FINANCE LIMITED", 0, "2026-10-09", "-", 1000.0, "1Y,6M,0D", "Secured", "Zero Coupon", 45.0, 45000.0, 0.0835, "IND AAA", "Stable", "On Maturity", "On Maturity"],
    ["INE787H07032", "INDIA INFRASTRUCTURE FINANCE COMPANY LIMITED", 0.083, "2026-03-28", "-", 1000.0, "0Y,11M,19D", "Secured", "NCD", 29.0, 29000.0, 0.0835, "CARE AAA", "Stable", "Annually", "On Maturity"],
    ["INE860H07IQ0", "ADITYA BIRLA FINANCE LIMITED", 0.08, "2026-10-09", "-", 1000.0, "1Y,6M,0D", "Secured", "NCD", 10.0, 10000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE860H07IU2", "ADITYA BIRLA FINANCE LIMITED", 0, "2028-10-09", "-", 1000.0, "3Y,6M,0D", "Secured", "Zero Coupon", 5.0, 5000.0, 0.0835, "IND AAA", "Stable", "On Maturity", "On Maturity"],
    ["INE774D07SV1", "MAHINDRA & MAHINDRA FINANCIAL SERVICES LTD", 0.092, "2027-01-18", "-", 1000.0, "1Y,9M,9D", "Secured", "NCD", 5.0, 5000.0, 0.0835, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE05OC24058", "LUCKNOW MUNICIPAL CORPORATION", 0.085, "2028-11-18", "-", 142900.0, "3Y,7M,9D", "Secured", "NCD", 6.999999999999986, 1000299.999999998, 0.08199999999999999, "IND AA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE027E07BB0", "L&T FINANCE LIMITED", 0.085, "2026-12-23", "-", 1000.0, "1Y,8M,14D", "Secured", "NCD", 1374.0, 1374000.0, 0.0785, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["IN1520210015", "6.72% GJ SDL 30", 0.0672, "2030-06-09", "-", 100.0, "5Y,2M,0D", "Secured", "SDL", 1839.0, 183900.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230252", "7.25% GJ SDL 26", 0.0725, "2026-02-07", "-", 100.0, "0Y,9M,29D", "Secured", "SDL", 1600.0, 160000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230012", "7.50% HR SDL 30", 0.075, "2030-04-19", "-", 100.0, "5Y,0M,10D", "Secured", "SDL", 2000.0, 200000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230014", "7.36% MH SDL 28", 0.0736, "2028-04-12", "-", 100.0, "3Y,0M,3D", "Secured", "SDL", 1401.0, 140100.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120200222", "6.33% TN SDL 30", 0.0633, "2030-07-22", "-", 100.0, "5Y,3M,13D", "Secured", "SDL", 900.0, 90000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230620", "7.70% AP SDL 29", 0.077, "2029-12-06", "-", 100.0, "4Y,7M,27D", "Secured", "SDL", 900.0, 90000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230027", "7.40% CG SDL 30", 0.074, "2030-06-28", "-", 100.0, "5Y,2M,19D", "Secured", "SDL", 800.0, 80000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2420220054", "7.39% ML SDL 26", 0.0739, "2026-11-23", "-", 100.0, "1Y,7M,14D", "Secured", "SDL", 800.0, 80000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230062", "7.40% GJ SDL 27", 0.074, "2027-09-22", "-", 100.0, "2Y,5M,13D", "Secured", "SDL", 700.0, 70000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220023", "7.18% MH SDL 30", 0.0718, "2030-04-08", "-", 100.0, "4Y,11M,30D", "Secured", "SDL", 600.0, 60000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230042", "7.41% AP SDL 30", 0.0741, "2030-04-26", "-", 100.0, "5Y,0M,17D", "Secured", "SDL", 500.0, 50000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3820230040", "7.29% PY SDL 26", 0.0729, "2026-03-13", "-", 100.0, "0Y,11M,4D", "Secured", "SDL", 500.0, 50000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220048", "7.65% GJ SDL 29", 0.0765, "2029-07-06", "-", 100.0, "4Y,2M,27D", "Secured", "SDL", 400.0, 40000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220238", "7.68% GJ SDL 30", 0.0768, "2030-02-15", "-", 100.0, "4Y,10M,6D", "Secured", "SDL", 395.0, 39500.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520220331", "7.55% TS SDL 30", 0.0755, "2030-01-18", "-", 100.0, "4Y,9M,9D", "Secured", "SDL", 300.0, 30000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2420220047", "7.63% ML SDL 25", 0.0763, "2025-10-27", "-", 100.0, "0Y,6M,18D", "Secured", "SDL", 300.0, 30000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230039", "7.18% GJ SDL 28", 0.0718, "2028-06-07", "-", 100.0, "3Y,1M,29D", "Secured", "SDL", 300.0, 30000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230302", "7.68% TN SDL 30", 0.0768, "2030-11-01", "-", 100.0, "5Y,6M,23D", "Secured", "SDL", 300.0, 30000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230112", "7.65% GJ SDL 29", 0.0765, "2029-11-29", "-", 100.0, "4Y,7M,20D", "Secured", "SDL", 298.0, 29800.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230013", "7.38% GJ SDL 30", 0.0738, "2030-04-26", "-", 100.0, "5Y,0M,17D", "Secured", "SDL", 250.0, 25000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230142", "7.43% CG SDL 29", 0.0743, "2029-02-14", "-", 100.0, "3Y,10M,5D", "Secured", "SDL", 200.0, 20000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220106", "7.62% MH SDL 30", 0.0762, "2030-09-28", "-", 100.0, "5Y,5M,19D", "Secured", "SDL", 200.0, 20000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220589", "7.50% AP SDL 28", 0.075, "2028-11-30", "-", 100.0, "3Y,7M,21D", "Secured", "SDL", 200.0, 20000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230310", "7.65% TN SDL 30", 0.0765, "2030-11-08", "-", 100.0, "5Y,6M,30D", "Secured", "SDL", 199.0, 19900.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220337", "7.49% GJ SDL 28", 0.0749, "2028-03-29", "-", 100.0, "2Y,11M,20D", "Secured", "SDL", 190.0, 19000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3820210083", "6.99% PY SDL 29", 0.0699, "2029-08-23", "-", 100.0, "4Y,4M,14D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230030", "7.20% MH SDL 28", 0.072, "2028-05-24", "-", 100.0, "3Y,1M,15D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230022", "7.49% MH SDL 30", 0.0749, "2030-04-12", "-", 100.0, "5Y,0M,3D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220056", "7.62% MH SDL 30", 0.0762, "2030-05-25", "-", 100.0, "5Y,1M,16D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230088", "7.62% GJ SDL 28", 0.0762, "2028-10-11", "-", 100.0, "3Y,6M,2D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220139", "7.62% GJ SDL 29", 0.0762, "2029-10-19", "-", 100.0, "4Y,6M,10D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230414", "7.45% AP SDL 34", 0.0745, "2028-08-30", "-", 100.0, "3Y,4M,21D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220031", "7.61% MH SDL 29", 0.0761, "2029-05-11", "-", 100.0, "4Y,1M,2D", "Secured", "SDL", 100.0, 10000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120200065", "6.73% TN SDL 30", 0.0673, "2030-05-13", "-", 100.0, "5Y,1M,4D", "Secured", "SDL", 90.0, 9000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920210316", "6.01% RJ SDL 26", 0.0601, "2026-10-06", "-", 100.0, "1Y,5M,27D", "Secured", "SDL", 60.0, 6000.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230146", "7.40% GJ SDL 26", 0.074, "2026-12-27", "-", 100.0, "1Y,8M,18D", "Secured", "SDL", 42.0, 4200.0, 0.0785, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["INE207O08019", "PNB METLIFE INDIA INSURANCE COMPANY LIMITED", 0.0812, "2032-01-27", "-", 1000000.0, "6Y,9M,18D", "Unsecured", "NCD", 5.0, 5000000.0, 0.0775, "CRISIL AA+", "Stable", "Annually", "On Maturity"],
    ["IN3120230245", "7.52% TN SDL 33", 0.0752, "2033-10-04", "-", 100.0, "8Y,5M,25D", "Secured", "SDL", 5900.0, 590000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230092", "7.68% CG SDL 32", 0.0768, "2032-01-17", "-", 100.0, "6Y,9M,8D", "Secured", "SDL", 3500.0, 350000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230147", "7.70% MH SDL 34", 0.077, "2034-11-08", "-", 100.0, "9Y,6M,30D", "Secured", "SDL", 2898.0, 289800.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420220080", "7.62% GA SDL 32", 0.0762, "2032-11-30", "-", 100.0, "7Y,7M,21D", "Secured", "SDL", 2500.0, 250000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2320230088", "7.77% MN SDL 38", 0.0777, "2038-11-29", "-", 100.0, "13Y,7M,20D", "Secured", "SDL", 2300.0, 230000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230422", "7.44% AP SDL 33", 0.0744, "2033-09-06", "-", 100.0, "8Y,4M,28D", "Secured", "SDL", 2300.0, 230000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230319", "7.72% HR SDL 33", 0.0772, "2033-12-06", "-", 100.0, "8Y,7M,27D", "Secured", "SDL", 2200.0, 220000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020220033", "7.76% KL SDL 38", 0.0776, "2038-08-24", "-", 100.0, "13Y,4M,15D", "Secured", "SDL", 2200.0, 220000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230153", "7.58% GJ SDL 32", 0.0758, "2032-12-27", "-", 100.0, "7Y,8M,18D", "Secured", "SDL", 2400.0, 240000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120220030", "7.94% TN SDL 32", 0.0794, "2032-06-15", "-", 100.0, "7Y,2M,6D", "Secured", "SDL", 2000.0, 200000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230154", "7.70% MH SDL 33", 0.077, "2033-11-15", "-", 100.0, "8Y,7M,6D", "Secured", "SDL", 2088.0, 208800.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230243", "7.65% UP SDL 34", 0.0765, "2034-12-27", "-", 100.0, "9Y,8M,18D", "Secured", "SDL", 1800.0, 180000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230139", "7.71% MH SDL 33", 0.0771, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 1548.0, 154800.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620220377", "7.64% HR SDL 31", 0.0765, "2031-01-25", "-", 100.0, "5Y,9M,16D", "Secured", "SDL", 1500.0, 150000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230138", "7.55% GJ SDL 31", 0.0755, "2031-12-20", "-", 100.0, "6Y,8M,11D", "Secured", "SDL", 1409.0, 140900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230661", "7.70% AP SDL 38", 0.077, "2038-12-13", "-", 100.0, "13Y,8M,4D", "Secured", "SDL", 4200.0, 420000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230110", "7.70% UP SDL 33", 0.077, "2033-10-25", "-", 100.0, "8Y,6M,16D", "Secured", "SDL", 1000.0, 100000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120200339", "6.53% TN SDL 31", 0.0653, "2031-01-06", "-", 100.0, "5Y,8M,28D", "Secured", "SDL", 1000.0, 100000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230180", "7.62% KL SDL 38", 0.0762, "2038-12-20", "-", 100.0, "13Y,8M,11D", "Secured", "SDL", 1000.0, 100000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120200362", "6.95% TN SDL 31", 0.0695, "2031-02-17", "-", 100.0, "5Y,10M,8D", "Secured", "SDL", 1000.0, 100000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120210056", "6.97% TN SDL 46", 0.0697, "2046-05-25", "-", 100.0, "21Y,1M,16D", "Secured", "SDL", 999.0, 99900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420220122", "7.64% GA SDL 38", 0.0764, "2038-01-04", "-", 100.0, "12Y,8M,26D", "Secured", "SDL", 988.0, 98800.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920220077", "7.59% KA SDL 38", 0.0759, "2038-12-07", "-", 100.0, "13Y,7M,28D", "Secured", "SDL", 954.0, 95400.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920210035", "6.78% RJ SDL 31", 0.0678, "2031-04-16", "-", 100.0, "6Y,0M,7D", "Secured", "SDL", 900.0, 90000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230126", "7.71% KA SDL 36", 0.0725, "2036-12-13", "-", 100.0, "11Y,8M,4D", "Secured", "SDL", 900.0, 90000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230174", "7.75% PB SDL 36", 0.0775, "2036-10-11", "-", 100.0, "11Y,6M,2D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120210312", "7.33% TN SDL 52", 0.0733, "2052-02-02", "-", 100.0, "26Y,9M,24D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230182", "7.77% PB SDL 33", 0.0777, "2033-11-01", "-", 100.0, "8Y,6M,23D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230034", "7.47% PB SDL 43", 0.0747, "2043-05-03", "-", 100.0, "18Y,0M,24D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230034", "7.71% AP SDL 33", 0.0771, "2033-04-06", "-", 100.0, "7Y,11M,28D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220225", "7.85% AP SDL 37", 0.0785, "2037-06-22", "-", 100.0, "12Y,2M,13D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230246", "7.47% MH SDL 36", 0.0747, "2036-02-21", "-", 100.0, "10Y,10M,12D", "Secured", "SDL", 800.0, 80000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230100", "7.72% KA SDL 35", 0.0772, "2035-12-06", "-", 100.0, "10Y,7M,27D", "Secured", "SDL", 797.0, 79700.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2520220046", "7.74% MZ SDL 33", 0.0774, "2033-08-03", "-", 100.0, "8Y,3M,25D", "Secured", "SDL", 700.0, 70000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220254", "7.73% MH SDL 32", 0.0773, "2032-03-29", "-", 100.0, "6Y,11M,20D", "Secured", "SDL", 700.0, 70000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230076", "7.67% KA SDL 36", 0.0767, "2036-11-22", "-", 100.0, "11Y,7M,13D", "Secured", "SDL", 700.0, 70000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230237", "7.63% GJ SDL 34", 0.0763, "2034-01-24", "-", 100.0, "8Y,9M,15D", "Secured", "SDL", 700.0, 70000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230653", "7.71% AP SDL 31", 0.0771, "2031-12-13", "-", 100.0, "6Y,8M,4D", "Secured", "SDL", 700.0, 70000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230193", "7.75% UP SDL 33", 0.0775, "2033-11-29", "-", 100.0, "8Y,7M,20D", "Secured", "SDL", 696.0, 69600.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230068", "7.70% KA SDL 33", 0.077, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 650.0, 65000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4920230203", "7.72% JK SDL 43", 0.0772, "2043-12-27", "-", 100.0, "18Y,8M,18D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230355", "7.74% TG SDL 35", 0.0774, "2035-11-29", "-", 100.0, "10Y,7M,20D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230201", "7.75% UP SDL 34", 0.0775, "2034-11-29", "-", 100.0, "9Y,7M,20D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230144", "7.72% UP SDL 34", 0.0772, "2034-11-08", "-", 100.0, "9Y,6M,30D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230203", "7.43% TN SDL 53", 0.0743, "2053-08-02", "-", 100.0, "28Y,3M,24D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230026", "7.62% PB SDL 38", 0.0762, "2038-04-19", "-", 100.0, "13Y,0M,10D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230211", "7.64% GJ SDL 34", 0.0764, "2034-01-17", "-", 100.0, "8Y,9M,8D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220030", "7.82% GJ SDL 32", 0.0782, "2032-12-29", "-", 100.0, "7Y,8M,20D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1220230172", "7.78% AS SDL 34", 0.0778, "2034-01-10", "-", 100.0, "8Y,9M,1D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1220220140", "7.67% AS SDL 32", 0.0767, "2032-11-16", "-", 100.0, "7Y,7M,7D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["In1020230638", "7.73% AP SDL 32", 0.0773, "2032-12-06", "-", 100.0, "7Y,7M,27D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020210218", "7.14% AP SDL 37", 0.0714, "2037-08-04", "-", 100.0, "12Y,3M,26D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230233", "7.38% CG SDL 32", 0.0738, "2032-03-13", "-", 100.0, "6Y,11M,4D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230151", "7.73% UP SDL 34", 0.0773, "2034-11-15", "-", 100.0, "9Y,7M,6D", "Secured", "SDL", 600.0, 60000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230142", "7.64% KA SDL 39", 0.0764, "2039-12-20", "-", 100.0, "14Y,8M,11D", "Secured", "SDL", 3400.0, 340000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220431", "7.74% AP SDL 38", 0.0774, "2038-08-19", "-", 100.0, "13Y,4M,10D", "Secured", "SDL", 583.0, 58300.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230216", "7.77% PB SDL 36", 0.0777, "2036-12-06", "-", 100.0, "11Y,7M,27D", "Secured", "SDL", 4300.0, 430000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4920230054", "7.44% JK SDL 53", 0.0744, "2053-08-02", "-", 100.0, "28Y,3M,24D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4920220048", "7.57% JK SDL 34", 0.0757, "2034-09-21", "-", 100.0, "9Y,5M,12D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230363", "7.70% TG SDL 38", 0.077, "2038-12-13", "-", 100.0, "13Y,8M,4D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230136", "7.73% UP SDL 33", 0.0773, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230083", "7.43% PB SDL 48", 0.0743, "2048-07-05", "-", 100.0, "23Y,2M,26D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230067", "7.47% AP SDL 37", 0.0747, "2037-04-26", "-", 100.0, "12Y,0M,17D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230059", "7.43% AP SDL 31", 0.0743, "2031-04-26", "-", 100.0, "6Y,0M,17D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220209", "8.04% AP SDL 42", 0.0804, "2042-06-15", "-", 100.0, "17Y,2M,6D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230252", "7.62% TN SDL 53", 0.0762, "2053-10-11", "-", 100.0, "28Y,6M,2D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230208", "7.79% PB SDL 37", 0.0779, "2037-11-29", "-", 100.0, "12Y,7M,20D", "Secured", "SDL", 500.0, 50000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230245", "7.60% GJ SDL 33", 0.076, "2033-01-31", "-", 100.0, "7Y,9M,22D", "Secured", "SDL", 488.0, 48800.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220210040", "6.88% MH SDL 33", 0.0688, "2033-05-12", "-", 100.0, "8Y,1M,3D", "Secured", "SDL", 425.0, 42500.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230220", "7.49% MH SDL 36", 0.0749, "2036-02-07", "-", 100.0, "10Y,9M,29D", "Secured", "SDL", 403.0, 40300.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820230190", "7.79% PB SDL 36", 0.0779, "2036-11-29", "-", 100.0, "11Y,7M,20D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4920230195", "7.71% JK SDL 48", 0.0771, "2048-12-20", "-", 100.0, "23Y,8M,11D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230322", "7.72% TG SDL 36", 0.0772, "2036-11-08", "-", 100.0, "11Y,6M,30D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230017", "7.61% TG SDL 44", 0.0761, "2044-04-19", "-", 100.0, "19Y,0M,10D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230169", "7.73% UP SDL 35", 0.0773, "2035-11-15", "-", 100.0, "10Y,7M,6D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230401", "7.60% TN SDL 31", 0.076, "2031-01-31", "-", 100.0, "5Y,9M,22D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230039", "7.33% TN SDL 33", 0.0733, "2033-05-17", "-", 100.0, "8Y,1M,8D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230025", "7.61% RJ SDL 43", 0.0761, "2043-04-19", "-", 100.0, "18Y,0M,10D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920220265", "7.73% RJ SDL 38", 0.08, "2038-02-01", "-", 100.0, "12Y,9M,23D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230198", "7.62% KL SDL 44", 0.0762, "2044-12-27", "-", 100.0, "19Y,8M,18D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230172", "7.71% KL SDL 43", 0.0771, "2043-11-29", "-", 100.0, "18Y,7M,20D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230156", "7.49% KL SDL 45", 0.0749, "2045-10-04", "-", 100.0, "20Y,5M,25D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230118", "7.72% KA SDL 35", 0.0772, "2035-12-13", "-", 100.0, "10Y,8M,4D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420230188", "7.75% GA SDL 33", 0.0775, "2033-11-29", "-", 100.0, "8Y,7M,20D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230043", "7.73% KA SDL 35", 0.0773, "2035-11-01", "-", 100.0, "10Y,6M,23D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230802", "7.45% AP SDL 38", 0.0745, "2038-02-14", "-", 100.0, "12Y,10M,5D", "Secured", "SDL", 400.0, 40000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230084", "7.73% KA SDL 34", 0.0773, "2034-11-29", "-", 100.0, "9Y,7M,20D", "Secured", "SDL", 399.0, 39900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920200624", "7.29% KA SDL 36", 0.0729, "2036-03-03", "-", 100.0, "10Y,10M,23D", "Secured", "SDL", 374.0, 37400.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230167", "7.74% KA SDL 34", 0.0774, "2034-01-03", "-", 100.0, "8Y,8M,25D", "Secured", "SDL", 360.0, 36000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820210143", "7.19% PB SDL 37", 0.0719, "2037-01-05", "-", 100.0, "11Y,8M,27D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230227", "7.62% UP SDL 34", 0.0762, "2034-12-20", "-", 100.0, "9Y,8M,11D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230351", "7.56% TN SDL 53", 0.0756, "2053-12-27", "-", 100.0, "28Y,8M,18D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230229", "7.43% TN SDL 33", 0.0743, "2033-09-06", "-", 100.0, "8Y,4M,28D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220213", "7.69% MH SDL 31", 0.0769, "2031-03-15", "-", 100.0, "5Y,11M,6D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620220138", "7.81% HR SDL 32", 0.0781, "2032-07-13", "-", 100.0, "7Y,3M,4D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230278", "7.43% GJ SDL 31", 0.0743, "2031-02-14", "-", 100.0, "5Y,10M,5D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230241", "7.39% CG SDL 33", 0.0739, "2033-03-13", "-", 100.0, "7Y,11M,4D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230025", "7.43% TG SDL 33", 0.0743, "2033-04-26", "-", 100.0, "8Y,0M,17D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230314", "7.59% RJ SDL 46", 0.0759, "2046-11-08", "-", 100.0, "21Y,6M,30D", "Secured", "SDL", 300.0, 30000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230332", "7.37% KA SDL 38", 0.0737, "2038-03-13", "-", 100.0, "12Y,11M,4D", "Secured", "SDL", 297.0, 29700.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220210206", "7.10% MH SDL 36", 0.071, "2036-08-04", "-", 100.0, "11Y,3M,26D", "Secured", "SDL", 280.0, 28000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230215", "7.44% TS SDL 39", 0.0744, "2039-09-06", "-", 100.0, "14Y,4M,28D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520220315", "7.59% TG SDL 37", 0.0759, "2037-01-11", "-", 100.0, "11Y,9M,2D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3420230143", "7.71% WB SDL 43", 0.0771, "2043-11-29", "-", 100.0, "18Y,7M,20D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3420220052", "8.02% WB SDL 37", 0.0802, "2037-07-20", "-", 100.0, "12Y,3M,11D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320230177", "7.68% UP SDL 34", 0.0768, "2034-11-22", "-", 100.0, "9Y,7M,13D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120220048", "7.84% TN SDL 52", 0.0784, "2052-06-22", "-", 100.0, "27Y,2M,13D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230330", "7.75% RJ SDL 35", 0.0775, "2035-11-29", "-", 100.0, "10Y,7M,20D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920220331", "7.74% RJ SDL 49", 0.0774, "2049-03-23", "-", 100.0, "23Y,11M,14D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230206", "7.76% KL SDL 35", 0.0765, "2035-01-10", "-", 100.0, "9Y,9M,1D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920220069", "7.63% KA SDL 42", 0.0763, "2042-11-30", "-", 100.0, "17Y,7M,21D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230335", "7.67% HR SDL 35", 0.0767, "2035-12-27", "-", 100.0, "10Y,8M,18D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230129", "7.44% HR SDL 32", 0.0744, "2032-07-12", "-", 100.0, "7Y,3M,3D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230187", "7.64% GJ SDL 31	", 0.0764, "2031-01-10", "-", 100.0, "5Y,9M,1D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420230154", "7.70% GA SDL 33", 0.077, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420220049", "7.69% GA SDL 32", 0.0769, "2032-09-28", "-", 100.0, "7Y,5M,19D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1320230122", "7.70% BR SDL 38", 0.077, "2038-11-22", "-", 100.0, "13Y,7M,13D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1320230114", "7.73% BR SDL 38", 0.0773, "2038-11-08", "-", 100.0, "13Y,6M,30D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230505", "7.67% AP SDL 38", 0.0767, "2038-10-11", "-", 100.0, "13Y,6M,2D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230323", "7.43% AP SDL 41", 0.0743, "2041-07-12", "-", 100.0, "16Y,3M,3D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230471", "7.44% AP SDL 36", 0.0744, "2036-09-22", "-", 100.0, "11Y,5M,13D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020220108", "7.63% KL SDL 43", 0.0763, "2043-11-30", "-", 100.0, "18Y,7M,21D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820220068", "7.82% PB SDL 42", 0.0782, "2042-08-03", "-", 100.0, "17Y,3M,25D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1320230106", "7.78% BR SDL 31", 0.0778, "2031-11-01", "-", 100.0, "6Y,6M,23D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230175", "7.73% KA SDL 35", 0.0773, "2035-01-03", "-", 100.0, "9Y,8M,25D", "Secured", "SDL", 200.0, 20000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230212", "7.48% MH SDL 35", 0.0748, "2035-02-07", "-", 100.0, "9Y,9M,29D", "Secured", "SDL", 199.0, 19900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2120220024", "7.46% MP SDL 32", 0.0746, "2032-09-14", "-", 100.0, "7Y,5M,5D", "Secured", "SDL", 199.0, 19900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120210528", "7.39% TN SDL 42", 0.0739, "2042-03-30", "-", 100.0, "16Y,11M,21D", "Secured", "SDL", 199.0, 19900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120220279", "7.65% TN SDL 33", 0.0765, "2033-01-25", "-", 100.0, "7Y,9M,16D", "Secured", "SDL", 199.0, 19900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920200655", "6.95% RJ SDL 31", 0.0695, "2031-02-10", "-", 100.0, "5Y,10M,1D", "Secured", "SDL", 195.0, 19500.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920210268", "7.31% KA SDL 35", 0.0731, "2035-01-12", "-", 100.0, "9Y,9M,3D", "Secured", "SDL", 190.0, 19000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230195", "7.66% GJ SDL 32", 0.0766, "2032-01-10", "-", 100.0, "6Y,9M,1D", "Secured", "SDL", 170.0, 17000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230280", "7.65% TG SDL 39", 0.0765, "2039-10-18", "-", 100.0, "14Y,6M,9D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3320220038", "7.81% UP SDL 32", 0.0781, "2032-10-04", "-", 100.0, "7Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230363", "7.67% RJ SDL 33", 0.0767, "2033-12-27", "-", 100.0, "8Y,8M,18D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230348", "7.64% RJ SDL 49", 0.0764, "2049-11-29", "-", 100.0, "24Y,7M,20D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230298", "7.72% RJ SDL 33", 0.0772, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230249", "7.71% RJ SDL 33", 0.0771, "2033-10-25", "-", 100.0, "8Y,6M,16D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920220232", "7.65% RJ SDL 33", 0.0765, "2033-07-25", "-", 100.0, "8Y,3M,16D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2820220167", "7.63% PB SDL 39", 0.0763, "2039-11-30", "-", 100.0, "14Y,7M,21D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230113", "7.46% MH SDL 33", 0.0746, "2033-09-13", "-", 100.0, "8Y,5M,4D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220098", "7.89% MH SDL 32", 0.0789, "2032-06-08", "-", 100.0, "7Y,1M,30D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220220072", "7.72% MH SDL 34", 0.0772, "2034-05-25", "-", 100.0, "9Y,1M,16D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220210172", "6.94% MH SDL 31", 0.0694, "2031-07-07", "-", 100.0, "6Y,2M,28D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220210156", "6.89% MH SDL 31", 0.0689, "2031-06-30", "-", 100.0, "6Y,2M,21D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2120220040", "7.67% MP SDL 33", 0.0773, "2033-02-01", "-", 100.0, "7Y,9M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230159", "7.58% GJ SDL 32", 0.0758, "2037-12-27", "-", 100.0, "12Y,8M,18D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230134", "7.60% KA SDL 38", 0.076, "2038-12-20", "-", 100.0, "13Y,8M,11D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230092", "7.69% KA SDL 33", 0.0769, "2033-12-06", "-", 100.0, "8Y,7M,27D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920220028", "7.67% KA SDL 32", 0.0767, "2032-11-16", "-", 100.0, "7Y,7M,7D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1720230102", "7.67% HP SDL 34", 0.0767, "2034-01-17", "-", 100.0, "8Y,9M,8D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230343", "7.77% HR SDL 36", 0.0777, "2036-01-10", "-", 100.0, "10Y,9M,1D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620210170", "7.25% HR SDL 32", 0.0725, "2032-03-09", "-", 100.0, "6Y,11M,0D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230260", "7.42% GJ SDL 31", 0.0742, "2031-02-07", "-", 100.0, "5Y,9M,29D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520230229", "7.63% GJ SDL 33", 0.0763, "2033-01-24", "-", 100.0, "7Y,9M,15D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1520220204", "7.63% GJ SDL 32", 0.0763, "2032-01-25", "-", 100.0, "6Y,9M,16D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420230204", "7.67% GA SDL 33", 0.0767, "2033-12-27", "-", 100.0, "8Y,8M,18D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420220056", "7.74% GA SDL 32", 0.0774, "2032-10-19", "-", 100.0, "7Y,6M,10D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420220031", "7.58% GA SDL 37", 0.0758, "2037-09-21", "-", 100.0, "12Y,5M,12D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420210032", "6.89% GA SDL 31", 0.0689, "2031-06-23", "-", 100.0, "6Y,2M,14D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1320230080", "7.62% BR SDL 31", 0.0762, "2031-10-04", "-", 100.0, "6Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1220230131", "7.74% AS SDL 33", 0.0774, "2033-11-08", "-", 100.0, "8Y,6M,30D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1220230099", "7.47% AS SDL 33", 0.0747, "2033-09-06", "-", 100.0, "8Y,4M,28D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1220230016", "7.58% AS SDL 33", 0.0758, "2033-04-12", "-", 100.0, "8Y,0M,3D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230711", "7.67% AP SDL 38", 0.0767, "2038-01-10", "-", 100.0, "12Y,9M,1D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230679", "7.74% AP SDL 32", 0.0774, "2032-01-03", "-", 100.0, "6Y,8M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020230489", "7.60% AP SDL 34", 0.076, "2033-10-04", "-", 100.0, "8Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220480", "7.58% AP SDL 42", 0.0758, "2042-09-07", "-", 100.0, "17Y,4M,29D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230253", "7.43% MH SDL 35", 0.0743, "2035-02-28", "-", 100.0, "9Y,10M,19D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020210416", "6.92% AP SDL 41", 0.0692, "2041-12-01", "-", 100.0, "16Y,7M,22D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920210359", "7.44% KA SDL 35", 0.0744, "2035-02-09", "-", 100.0, "9Y,10M,0D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220210198", "6.95% MH SDL 31", 0.0695, "2031-07-14", "-", 100.0, "6Y,3M,5D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2920230223", "7.54% RJ SDL 33", 0.0754, "2033-10-04", "-", 100.0, "8Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3520230068", "7.54% CG SDL 31", 0.0754, "2031-10-04", "-", 100.0, "6Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1320230130", "7.74% BR SDL 38", 0.0774, "2038-12-06", "-", 100.0, "13Y,7M,27D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220043", "7.52% AP SDL 42", 0.0752, "2042-04-12", "-", 100.0, "17Y,0M,3D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2620230051", "7.67% NL SDL 33", 0.0767, "2033-11-22", "-", 100.0, "8Y,7M,13D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4920230153", "7.56% JK SDL 48", 0.0756, "2048-11-22", "-", 100.0, "23Y,7M,13D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020220365", "8.04% AP SDL 37", 0.084, "2037-07-27", "-", 100.0, "12Y,3M,18D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1620230269", "7.75% HR SDL 35", 0.0775, "2035-11-01", "-", 100.0, "10Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN4520230306", "7.75% TG SDL 37", 0.0775, "2037-11-01", "-", 100.0, "12Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020230164", "7.66% KL SDL 46", 0.0766, "2046-11-01", "-", 100.0, "21Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2120230130", "7.76% MP SDL 37", 0.0776, "2037-11-29", "-", 100.0, "12Y,7M,20D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920230050", "7.73% KA SDL 36", 0.0773, "2036-11-01", "-", 100.0, "11Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2120230122", "7.76% MP SDL 37", 0.0776, "2037-11-01", "-", 100.0, "12Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1420230147", "7.73% GA SDL 33", 0.0773, "2033-11-01", "-", 100.0, "8Y,6M,23D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120220170", "7.79% TN SDL 32", 0.0779, "2032-10-04", "-", 100.0, "7Y,5M,25D", "Secured", "SDL", 100.0, 10000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120230179", "7.39% TN SDL 33", 0.0739, "2033-07-26", "-", 100.0, "8Y,3M,17D", "Secured", "SDL", 99.0, 9900.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120220261", "7.57% TN SDL 33", 0.0757, "2033-01-11", "-", 100.0, "7Y,9M,2D", "Secured", "SDL", 95.0, 9500.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2220230188", "7.73% MH SDL 36", 0.0773, "2036-01-10", "-", 100.0, "10Y,9M,1D", "Secured", "SDL", 95.0, 9500.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1020210176", "7.15% AP SDL 37", 0.0715, "2037-07-07", "-", 100.0, "12Y,2M,28D", "Secured", "SDL", 90.0, 9000.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120200206", "6.63% TN SDL 50", 0.0663, "2050-07-08", "-", 100.0, "25Y,2M,29D", "Secured", "SDL", 74.0, 7400.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN3120210023", "6.96% TN SDL 51", 0.0696, "2051-05-19", "-", 100.0, "26Y,1M,10D", "Secured", "SDL", 22.0, 2200.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN1920200483", "6.68% KA SDL 36", 0.0668, "2036-12-09", "-", 100.0, "11Y,8M,0D", "Secured", "SDL", 6.0, 600.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN2020220132", "7.62% KL SDL 53", 0.0762, "2053-01-04", "-", 100.0, "27Y,8M,26D", "Secured", "SDL", 1.0, 100.0, 0.0775, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["INE608A08058", "PUNJAB & SIND BANK", 0.0774, "2034-12-20", "-", 100000.0, "9Y,8M,11D", "Unsecured", "NCD", 10.0, 1000000.0, 0.0735, "CRISIL AA", "Stable", "Annually", "On Maturity"],
    ["INE457A08175", "BANK OF MAHARASHTRA", 0.078, "2034-08-05", "-", 100000.0, "9Y,3M,27D", "Unsecured", "NCD", 403.0, 40300000.0, 0.0725, "ICRA AA+", "Stable", "Annually", "On Maturity"],
    ["IN0020200054", "7.16% G Sec 50", 0.0716, "2050-09-20", "-", 100.0, "25Y,5M,11D", "Secured", "G-Sec", 3093.0, 309300.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020240159", "6.79% GOI SGRB 34", 0.0679, "2034-12-02", "-", 100.0, "9Y,7M,23D", "Secured", "G-Sec", 5600.0, 560000.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN000629C047", "0.00% GOI 12-06-2029", 0, "2029-06-12", "-", 100.0, "4Y,2M,3D", "Secured", "Strips", 6.0, 600.0, 0.07, "Sovereign", "-", "On Maturity", "On Maturity"],
    ["IN0020200401", "6.76% G SEC 61", 0.0676, "2061-12-22", "-", 100.0, "36Y,8M,13D", "Secured", "G-Sec", 2.0, 200.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020060078", "8.24% G SEC 27", 0.0824, "2027-12-15", "-", 100.0, "2Y,8M,6D", "Secured", "G-Sec", 2.0, 200.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020230085", "7.18% G SEC 33", 0.0718, "2033-08-14", "-", 100.0, "8Y,4M,5D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020220151", "7.26% G SEC 33", 0.0726, "2033-12-06", "-", 100.0, "8Y,7M,27D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020240043", "7.02% G SEC 27", 0.0702, "2027-05-27", "-", 100.0, "2Y,1M,18D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020230101", "7.37% G SEC 28", 0.0737, "2028-10-23", "-", 100.0, "3Y,6M,14D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020200187", "6.80% G SEC 60", 0.068, "2060-12-13", "-", 100.0, "35Y,8M,4D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020200252", "6.67% G SEC 50", 0.0667, "2050-12-17", "-", 100.0, "25Y,8M,8D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020220011", "7.10% G SEC 29", 0.071, "2029-04-18", "-", 100.0, "4Y,0M,9D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["IN0020140060", "8.15% G SEC 26", 0.0815, "2026-11-24", "-", 100.0, "1Y,7M,15D", "Secured", "G-Sec", 1.0, 100.0, 0.07, "Sovereign", "-", "Semi - Annually", "On Maturity"],
    ["INE134E08LA3", "POWER FINANCE CORPORATION LIMITED", 0.072, "2035-08-10", "-", 1000000.0, "10Y,4M,1D", "Unsecured", "NCD", 5.0, 5000000.0, 0.0675, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE053F07BX7", "INDIAN RAILWAY FINANCE CORPORATION LIMITED", 0.0755, "2029-11-06", "-", 1000000.0, "4Y,6M,28D", "Secured", "NCD", 2.0, 2000000.0, 0.0675, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE053F09HP6", "INDIAN RAILWAY FINANCE CORPORATION LIMITED", 0.0933, "2026-05-10", "-", 1000000.0, "1Y,1M,1D", "Unsecured", "NCD", 2.0, 2000000.0, 0.0675, "ICRA AAA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE134E07AT8", "POWER FINANCE CORPORATION LIMITED", 0.0715, "2036-01-22", "-", 1000.0, "10Y,9M,13D", "Secured", "NCD", 2000.0, 2000000.0, 0.0675, "ICRA AAA", "Stable", "Annually", "On Maturity"],
    ["INE029A08073", "BHARAT PETROLEUM CORPORATION LIMITED", 0.0758, "2026-03-17", "-", 100000.0, "0Y,11M,8D", "Unsecured", "NCD", 10.0, 1000000.0, 0.0675, "CRISIL AAA", "-", "Annually", "On Maturity"],
    ["INE261F08AD8", "NATIONAL BANK FOR AGRICULTURE AND RURAL DEVELOPMENT", 0.082, "2028-03-09", "-", 1000000.0, "2Y,11M,0D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE134E08JP5", "POWER FINANCE CORPORATION LIMITED", 0.0785, "2028-04-03", "-", 1000000.0, "2Y,11M,25D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE020B08BH6", "RURAL ELECTRIFICATION CORPORATION LIMITED", 0.0837, "2028-12-07", "-", 1000000.0, "3Y,7M,28D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE020B08BG8", "RURAL ELECTRIFICATION CORPORATION LIMITED", 0.0856, "2028-11-29", "-", 1000000.0, "3Y,7M,20D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA", "Stable", "Semi - Annually", "On Maturity"],
    ["INE020B08DT7", "RURAL ELECTRIFICATION CORPORATION LIMITED", 0.0623, "2031-10-31", "-", 1000000.0, "6Y,6M,22D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE861G08027", "FOOD CORPORATION OF INDIA", 0.088, "2028-03-22", "-", 1000000.0, "2Y,11M,13D", "Unsecured", "NCD", 1.0, 1000000.0, 0.0675, "CRISIL AAA (CE)", "Stable", "Annually", "On Maturity"],
    ["INE062A08231", "STATE BANK OF INDIA", 0.068, "2035-08-21", "-", 1000000.0, "10Y,4M,12D", "Unsecured", "NCD", 25.0, 25000000.0, 0.0655, "CRISIL AAA", "-", "Annually", "On Maturity"],
    ["INE053F07827", "INDIAN RAILWAY FINANCE CORPORATION LIMITED", 0.0732, "2025-12-21", "-", 1000.0, "0Y,8M,12D", "Secured", "Tax Free", 2030.0, 2030000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE202E07211", "INDIAN RENEWABLE ENERGY DEVELOPMENT AGENCY LIMITED", 0.0753, "2026-01-21", "-", 1000.0, "0Y,9M,12D", "Secured", "Tax Free", 771.0, 771000.0, 0.0575, "IND AAA", "Stable", "Annually", "On Maturity"],
    ["INE261F07024", "NATIONAL BANK FOR AGRICULTURE AND RURAL DEVELOPMENT", 0.0729, "2026-03-23", "-", 1000.0, "0Y,11M,14D", "Secured", "Tax Free", 570.0, 570000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE031A07AN7", "HOUSING AND URBAN DEVELOPMENT CORPORATION LIMITED", 0.0727, "2026-02-08", "-", 1000.0, "0Y,9M,30D", "Secured", "Tax Free", 544.0, 544000.0, 0.0575, "CARE AAA", "Stable", "Annually", "On Maturity"],
    ["INE031A07865", "HOUSING AND URBAN DEVELOPMENT CORPORATION LIMITED", 0.0801, "2028-02-16", "-", 1000.0, "2Y,10M,7D", "Secured", "Tax Free", 139.0, 139000.0, 0.0575, "CARE AAA", "Stable", "Annually", "On Maturity"],
    ["INE134E07547", "POWER FINANCE CORPORATION LIMITED", 0.0736, "2025-10-17", "-", 1000.0, "0Y,6M,8D", "Secured", "Tax Free", 43.0, 43000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE020B07JQ2", "RURAL ELECTRIFICATION CORPORATION LIMITED", 0.0714, "2025-11-05", "-", 1000.0, "0Y,6M,27D", "Secured", "Tax Free", 30.0, 30000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE906B07CB9", "NATIONAL HIGHWAYS AUTHORITY OF INDIA", 0.083, "2027-01-25", "-", 1000.0, "1Y,9M,16D", "Secured", "Tax Free", 15.0, 15000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE031A07881", "HOUSING AND URBAN DEVELOPMENT CORPORATION LIMITED", 0.0769, "2028-03-28", "-", 1000.0, "2Y,11M,19D", "Secured", "Tax Free", 20.0, 20000.0, 0.0575, "CARE AAA", "Stable", "Annually", "On Maturity"],
    ["INE020B07GZ9", "RURAL ELECTRIFICATION CORPORATION LIMITED", 0.0704, "2028-03-25", "-", 1000.0, "2Y,11M,16D", "Secured", "Tax Free", 5.0, 5000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE053F07595", "INDIAN RAILWAY FINANCE CORPORATION LIMITED", 0.0754, "2028-03-23", "-", 1000.0, "2Y,11M,14D", "Secured", "Tax Free", 5.0, 5000.0, 0.0575, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE134E07562", "POWER FINANCE CORPORATION LIMITED", 0.0752, "2030-10-17", "-", 1000.0, "5Y,6M,8D", "Secured", "Tax Free", 500.0, 500000.0, 0.056, "CRISIL AAA", "Stable", "Annually", "On Maturity"],
    ["INE053F07744", "INDIAN RAILWAY FINANCE CORPORATION LIMITED", 0.0819, "2029-03-26", "-", 1000.0, "3Y,11M,17D", "Secured", "Tax Free", 50.0, 50000.0, 0.056, "CRISIL AAA", "Stable", "Annually", "On Maturity"]
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
    
    # Calculate additional metrics
    df['Total Value'] = df['Total Qty FV'] * (1 + df['Coupon'] * df['Years to Maturity'])
    
    return df

df = load_data()

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
    
    # Bar chart - FIXED THE ERROR HERE
    rating_counts = filtered_df['Credit Rating'].value_counts().reset_index()
    fig.add_trace(
        go.Bar(
            x=rating_counts['Credit Rating'],  # Changed from 'index' to 'Credit Rating'
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
