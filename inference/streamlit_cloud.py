import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from PIL import Image
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FrostUK Demand Prediction",
    page_icon="🥕",
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
    logo_filename = "foodlogo.png"
    logo_url = "https://github.com/edwinaabam/FrostUK/blob/main/inference/foodlogo.png?raw=true"
    
    # Get local path relative to this script
    current_dir = Path(__file__).resolve().parent
    local_logo_path = current_dir / logo_filename

    # 2. Logo Logic (Local first, then Cloud Fallback)
    try:
        left_co, cent_co, last_co = st.columns([0.5, 3, 0.5])
        with cent_co:
            if local_logo_path.exists():
                # Use local file if found
                st.image(Image.open(local_logo_path), use_container_width=True)
            else:
                # Fallback to GitHub URL if local file is missing (e.g., on Cloud)
                st.image(logo_url, use_container_width=True)
    except Exception as e:
        # If both fail, show nothing or a small error
        pass

    # 3. The Option Menu (The rest remains the same)
    page = option_menu(
        menu_title="FrostUK Menu",
        options=["Forecast Demand", "About the App"],
        icons=["graph-up-arrow", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "#444", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff8d27", "color": "white"},
        }
    )
    
    st.divider()
    st.caption("FrostUK Supply Chain Management v1.2")

### --- 5. TOP BANNER ---
st.markdown("""
    <div style="
        background-color:#5e81d1;
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
        🥦 FrostUK Perishable Goods Demand Prediction
    </h2>
    </div>
    """, unsafe_allow_html=True)

# --- 6. PAGE LOGIC ---
if page == "Forecast Demand":
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
            marketing_spend = st.number_input("Marketing Spend (£)", value=500.0)
            discount_percent = st.slider("Discount Percent", 0, 100, 0)

        with col2:
            st.markdown("##### Environmental & Logistics")
            store_size = st.number_input("Store Size (sq ft)", value=1500)
            rainfall = st.number_input("Rainfall (mm)", value=20.5)
            avg_temp = st.number_input("Avg Temp (°C)", value=22.3)
            supply_capacity = st.number_input("Supply Capacity", value=50000)
            lead_time = st.number_input("Lead Time (Days)", value=1)
            is_holiday = st.checkbox("Is it a Holiday?")

        submitted = st.form_submit_button("Predict Units Sold")

    if submitted:
        if model:
            try:
                # Prepare data
                input_dict = {feat: 0 for feat in EXPECTED_FEATURES}
                input_dict.update({
                    "Marketing_Spend": marketing_spend, "Discount_Percent": discount_percent,
                    "Wastage_Units": wastage_unit, "Price": price,
                    "Shelf_Life_Days": shelf_life, "Store_Size": store_size,
                    "Avg_Temperature": avg_temp, "Rainfall": rainfall,
                    "Holiday_Flag": 1 if is_holiday else 0, "Lead_Time_Days": lead_time,
                    "Supply_Capacity": supply_capacity
                })

                # One-Hot Encoding
                cat_col, reg_col = f"Product_Category_{product_category}", f"Region_{region}"
                if cat_col in input_dict: input_dict[cat_col] = 1
                if reg_col in input_dict: input_dict[reg_col] = 1

                # Inference
                input_df = pd.DataFrame([input_dict])[EXPECTED_FEATURES]
                prediction = model.predict(input_df)
                final_result = int(prediction.flatten()[0])
                
                st.divider()
                r_col, c_col = st.columns([1, 1])
                
                with r_col:
                    st.metric(label="Estimated Demand", value=f"{final_result} Units")
                    temp_diff = avg_temp - 15.0
                    rain_diff = rainfall - 10.0
                    st.metric("Temperature Variation", f"{avg_temp}°C", f"{temp_diff:.1f}°C vs Avg")
                    st.metric("Rainfall Variation", f"{rainfall}mm", f"{rain_diff:.1f}mm vs Avg")

                with c_col:
                    st.write("### Environmental Factor Comparison")
                    chart_data = pd.DataFrame({
                        "Metric": ["Temperature", "Rainfall"],
                        "Current Input": [avg_temp, rainfall],
                        "Baseline Avg": [15.0, 10.0]
                    }).set_index("Metric")
                    
                    # Colors list must match column length
                    st.bar_chart(chart_data, color=["#ff8d27", "#d3d3d3"])

            except Exception as e:
                st.error(f"Prediction Error: {e}")

elif page == "About the App":
    st.header("🏢 About FrostUK Analytics")
    st.write("""
    This application allows logistics managers to forecast demand for perishable goods by combining
    transactional parameters with real-world environmental data.
    """)
    st.info("💡 Use the sidebar to navigate between forecasting and application details.")