import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from PIL import Image
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FrostUK Demand Prediction",
    page_icon="🥦",
    layout="wide"
)

# --- 2. MODEL LOADING ---
@st.cache_resource
def load_model():
    try:
        model_path = Path(__file__).resolve().parent.parent / "model" / "lr_model.pkl"
        if not model_path.exists():
            st.error(f"Model file not found at: {model_path}")
            return None
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

# --- 3. FEATURE SCHEMA ---
EXPECTED_FEATURES = [
    "Marketing_Spend", "Discount_Percent", "Wastage_Units", "Price",
    "Shelf_Life_Days", "Store_Size", "Avg_Temperature", "Rainfall",
    "Holiday_Flag", "Lead_Time_Days", "Supply_Capacity",
    "Product_Category_Beverages", "Product_Category_Dairy", "Product_Category_Meat",
    "Region_Midlands", "Region_North East", "Region_North West",
    "Region_South East", "Region_South West"
]

# --- 4. NAVIGATION SIDEBAR (Option Menu) ---
with st.sidebar:
    # 1. Define Paths & URLs
    # Use the RAW GitHub url, not the blob viewer url
    logo_url = "https://raw.githubusercontent.com/edwinaabam/FrostUK/main/inference/grocerylogo.png"
    
    # Get local path relative to this script
    current_dir = Path(__file__).resolve().parent
    
    # IF your script is in the main FrostUK folder, we need to explicitly look inside "inference"
    # IF your script is already inside the "inference" folder, change this to just: current_dir / "grocerylogo.png"
    local_logo_path = current_dir / "inference" / "grocerylogo.png"

    # 2. Logo Logic (Local first, then Cloud Fallback)
    try:
        left_co, cent_co, last_co = st.columns([0.5, 3, 0.5])
        with cent_co:
            if local_logo_path.exists():
                # Use local file if found
                st.image(Image.open(local_logo_path))
            else:
                # Fallback to the RAW GitHub URL
                st.image(logo_url)

                
    except Exception as e:
        # Don't use 'pass' here, or you will never know why it failed!
        st.error(f"Image error: {e}")

    # 3. The Option Menu
    page = option_menu(
        menu_title="FrostUK Menu",
        options=["Forecast Demand", "About the App"],
        icons=["graph-up-arrow", "info-circle"],
        menu_icon="basket",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "#4A6741", "font-size": "14px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#607D8B", "color": "white"},
        }
    )
    
    st.divider()
    st.caption("FrostUK Supply Chain Management v1.2")

### --- 5. TOP BANNER ---
st.markdown("""
    <div style="
        background-color:#607D8B;
        padding: 10px 0px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 60px;
    ">
    <h2 style="
        color: white; 
        text-align: center; 
        margin: 0; 
        font-family: sans-serif; 
        font-size: 20px; 
        white-space: nowrap;
    ">
         FrostUK Perishable Goods Demand Prediction
    </h2>
    </div>
    """, unsafe_allow_html=True)

# --- 6. PAGE LOGIC ---
if page == "Forecast Demand":
    # Create the Tabs
    tab1, tab2 = st.tabs(["📋 Configuration", "📊 Analysis & Forecast"])

    with tab1:
        st.subheader("Input Transactional Details")
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Product & Pricing")
                product_category = st.selectbox("Category", ['Bakery', 'Meat', 'Beverages', 'Dairy'])
                region = st.selectbox("Region", ['London', 'Midlands', 'North East', 'North West', 'South East', 'South West'])
                price = st.number_input("Price (£)", value=2.50, step=0.1)
                wastage_unit = st.number_input("Wastage units", value=100)
                shelf_life = st.number_input("Shelf Life Days", value=3)

            with col2:
                st.markdown("##### Environmental & Logistics")
                store_size = st.number_input("Store Size (sq ft)", value=1500)
                rainfall = st.number_input("Rainfall (mm)", value=20.5)
                avg_temp = st.number_input("Avg Temp (°C)", value=22.3)
                marketing_spend = st.number_input("Marketing Spend (£)", value=500.0)
                discount_percent = st.slider("Discount Percent", 0, 100, 0)
                # Hidden/Background logistics
                supply_capacity = st.number_input("Supply Capacity", value=50000)
                lead_time = st.number_input("Lead Time (Days)", value=1)
                is_holiday = st.checkbox("Is it a Holiday?")

            submitted = st.form_submit_button("Predict Units Sold")

        # DISPLAY PREDICTED UNITS IMMEDIATELY UNDER THE BUTTON
        if submitted:
            if model:
                try:
                    # Logic to prepare data for the model
                    input_dict = {feat: 0 for feat in EXPECTED_FEATURES}
                    input_dict.update({
                        "Marketing_Spend": marketing_spend, "Discount_Percent": discount_percent,
                        "Wastage_Units": wastage_unit, "Price": price,
                        "Shelf_Life_Days": shelf_life, "Store_Size": store_size,
                        "Avg_Temperature": avg_temp, "Rainfall": rainfall,
                        "Holiday_Flag": 1 if is_holiday else 0, "Lead_Time_Days": lead_time,
                        "Supply_Capacity": supply_capacity,
                        "Month": 12, "Day": 8 # Temporary defaults for the point prediction
                    })
                    
                    cat_col, reg_col = f"Product_Category_{product_category}", f"Region_{region}"
                    if cat_col in input_dict: input_dict[cat_col] = 1
                    if reg_col in input_dict: input_dict[reg_col] = 1

                    input_df = pd.DataFrame([input_dict])[EXPECTED_FEATURES]
                    prediction = model.predict(input_df)
                    final_result = int(max(0, prediction.flatten()[0]))

                    st.success(f"### Estimated Demand: {final_result} Units")
                    st.caption("Check the 'Analysis & Forecast' tab for a detailed 7-day timeline.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with tab2:
        st.subheader("Time-Series Analysis")
        # Move Date Picker here
        forecast_start_date = st.date_input("Select Forecast Start Date", value=pd.to_datetime("2025-12-08"))
        
        if submitted:
            # Generate the chart based on the prediction from Tab 1
            import numpy as np
            dates = pd.date_range(start=forecast_start_date, periods=7)
            forecast_values = [final_result * (1 + np.random.uniform(-0.05, 0.05)) for _ in range(7)]
            
            # --- CRITICAL FIX: Keep Date as a column (don't use set_index) ---
            chart_df = pd.DataFrame({
                "Date": dates, 
                "Demand": forecast_values
            })

            # Charts and Comparisons
            st.divider()
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write(f"### 📈 Projected Horizon ({forecast_start_date.strftime('%B %d')})")
                
                # Explicitly passing Date and Demand columns
                st.line_chart(
                    chart_df, 
                    x="Date", 
                    y="Demand", 
                    color="#607D8B"
                )
                st.caption("Tip: Hover over the dots to see exact daily units.")
                
            with c2:
                st.write("#### Data Summary")
                st.metric("7-Day Total", f"{int(sum(forecast_values))} Units")
                st.metric("Avg Temp", f"{avg_temp}°C")
                st.metric("Peak Demand", f"{int(max(forecast_values))}")
        else:
            st.info("Please fill in the details in the Configuration tab and click Predict to see the analysis.")

elif page == "About the App":
    st.header("🏢 About FrostUK Analytics")
    st.write("""
    This application allows logistics managers to forecast demand for perishable goods by combining
    transactional parameters with real-world environmental data.
    """)
    st.info("💡 Use the sidebar to navigate between forecasting and application details.")