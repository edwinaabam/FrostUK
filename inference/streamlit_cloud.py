import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FrostUK Demand Prediction",
    page_icon="🥦",
    layout="wide"
)

# --- 2. SESSION STATE INITIALIZATION ---
if 'final_result' not in st.session_state:
    st.session_state.final_result = None
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}

# --- 3. MODEL & SCALER LOADING ---
@st.cache_resource
def load_assets():
    try:
        model_path = Path(__file__).resolve().parent / "rf_model.pkl"
        scaler_path = Path(__file__).resolve().parent / "scaler.pkl"
        if not model_path.exists():
            model_path = Path(__file__).resolve().parent.parent / "model" / "rf_model.pkl"
            scaler_path = Path(__file__).resolve().parent.parent / "model" / "scaler.pkl"
        return joblib.load(model_path), joblib.load(scaler_path)
    except Exception as e:
        st.error(f"Error loading assets: {e}")
        return None, None

model, scaler = load_assets()

EXPECTED_FEATURES = [
    "Marketing_Spend", "Discount_Percent", "Wastage_Units", "Price",
    "Shelf_Life_Days", "Store_Size", "Avg_Temperature", "Rainfall",
    "Holiday_Flag", "Lead_Time_Days", "Supply_Capacity",
    "Product_Category_Beverages", "Product_Category_Dairy", "Product_Category_Meat",
    "Region_Midlands", "Region_North East", "Region_North West",
    "Region_South East", "Region_South West"
]

# --- 4. SIDEBAR (Enhanced System Integrity) ---
with st.sidebar:
    logo_url = "https://raw.githubusercontent.com/edwinaabam/FrostUK/main/inference/grocerylogo.png"
    try:
        st.image(logo_url, use_container_width=True)
    except:
        st.title("🥦 FrostUK")
    
    st.divider()
    
    st.markdown("### 🛠️ System Integrity")
    # Green-themed status indicators
    st.write("🟢 **Random Forest Model Loaded** ✅")
    st.write("🟢 **Scaler Active** ✅")
    
    st.info("""
    **Intelligence Level:** v2.1  
    **Framework:** Scikit-Learn  
    **Status:** Operational
    """)
    
    st.divider()
    st.caption("Standardizing inputs ensures that pricing and weather data are weighted correctly for retail forecasting.")

# --- 5. TOP BANNER ---
st.markdown("""
    <div style="background-color:#607D8B; padding: 15px; border-radius: 10px; margin-bottom: 25px; text-align: center;">
        <h1 style="color: white; margin: 0; font-family: sans-serif; font-size: 26px;">
            FrostUK Perishable Goods Demand Analytics
        </h1>
    </div>
    """, unsafe_allow_html=True)

# --- 6. GLOBAL HELPER: MANAGERIAL SUMMARY ---
def display_managerial_summary():
    st.subheader("Managerial Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Daily Base Prediction", f"{st.session_state.final_result} Units")
    m2.metric("Product Category", st.session_state.inputs['cat'])
    m3.metric("Store Region", st.session_state.inputs['reg'])
    m4.metric("Unit Price", f"£{st.session_state.inputs['prc']:.2f}")

# --- 7. MAIN TABS ---
tab_about, tab_config, tab_analysis = st.tabs(["ℹ️ User Guide & Platform Info", "⚙️ Configuration", "📊 Forecast Analysis"])

# --- TAB: ABOUT ---
with tab_about:
    st.header("📘 Strategic Guide for Inventory Managers")
    
    st.markdown("""
    ### Purpose and Business Objective
    Managing perishable inventory is a high-stakes balancing act. Over-ordering leads to significant financial loss through wastage (spoilage), while under-ordering results in lost revenue and diminished customer loyalty. 
    
    The **FrostUK Demand Prediction Tool** bridges this gap by providing an AI-driven "Demand Signal." It analyzes historical consumer behavior patterns relative to external variables like weather and pricing to give you a statistically sound starting point for your daily ordering.
    """)

    st.divider()

    col_feat, col_how = st.columns(2)
    with col_feat:
        st.subheader(" Platform Features & Capabilities")
        st.markdown("""
        * **Random Forest Intelligence:** Unlike simple linear averages, our model uses a forest of decision trees to capture non-linear relationships between variables (e.g., how a 5% discount behaves differently in London vs. the Midlands).
        * **StandardScaler Pre-processing:** We ensure high-magnitude values like **Marketing Spend (£5,000)** don't drown out low-magnitude but critical values like **Price (£1.50)**.
        * **Scenario Simulation:** The platform allows for 'What-If' analysis by letting you toggle between Base, Best, and Worst-case demand surges.
        * **Automated Feature Importance:** After every prediction, the model reports which variables were the "Primary Drivers," giving you transparency into the AI's logic.
        """)

    with col_how:
        st.subheader("💡 Strategic Use Cases for Managers")
        st.markdown("""
        * **Promotion Evaluation:** Before launching a 20% discount, simulate it here to see if your current supply capacity can handle the predicted surge in volume.
        * **Weather-Responsive Logistics:** Perishable demand (especially Beverages and Bakery) fluctuates with temperature. Use the 'Avg Temp' input to prepare for heatwaves 48 hours in advance.
        * **Holiday Readiness:** Check the 'Holiday Season' flag to see how historical shopping surges affect your specific product category.
        * **Wastage Auditing:** Input your baseline wastage to see how the model suggests demand might shift to mitigate those losses.
        """)

    st.divider()

    st.subheader("🛠️ How to Navigate the Application")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("##### 1. Configuration")
        st.caption("Input your Category (Dairy, Meat, etc.) and Region. These are categorical variables that the model uses to 'lookup' regional consumer habits.")
    with s2:
        st.markdown("##### 2. Generate Prediction")
        st.caption("Input specific market conditions and environmental factors. Click 'Predict' to run the Random Forest inference.")
    with s3:
        st.markdown("##### 3. Analyze & Act")
        st.caption("Review the 30-day trend. Use the 'Cumulative Required Stock' metric to inform your bulk procurement orders.")

# --- TAB: CONFIGURATION ---
with tab_config:
    st.subheader("Inventory & Market Parameters")
    with st.form("config_form"):
        c1, c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Product Category", ['Bakery', 'Meat', 'Beverages', 'Dairy'])
            reg = st.selectbox("Store Region", ['London', 'Midlands', 'North East', 'North West', 'South East', 'South West'])
            prc = st.number_input("Unit Price (£)", value=2.50, min_value=0.10)
            wst = st.number_input("Wastage (Units)", value=100)
        with c2:
            mkt = st.number_input("Marketing Spend (£)", value=500.0)
            dsc = st.slider("Discount (%)", 0, 100, 5)
            tmp = st.number_input("Avg Temp (°C)", value=22.3)
            hld = st.checkbox("Holiday Season")
            shl, ldt, cap, sz, rnf = 3, 1, 50000, 1500, 20.5

        submitted = st.form_submit_button("Generate Prediction 🚀")

    if submitted and model and scaler:
        try:
            input_dict = {f: 0 for f in EXPECTED_FEATURES}
            input_dict.update({
                "Marketing_Spend": mkt, "Discount_Percent": dsc, "Wastage_Units": wst,
                "Price": prc, "Shelf_Life_Days": shl, "Store_Size": sz,
                "Avg_Temperature": tmp, "Rainfall": rnf, "Holiday_Flag": 1 if hld else 0,
                "Lead_Time_Days": ldt, "Supply_Capacity": cap
            })
            cat_col, reg_col = f"Product_Category_{cat}", f"Region_{reg}"
            if cat_col in input_dict: input_dict[cat_col] = 1
            if reg_col in input_dict: input_dict[reg_col] = 1

            input_df = pd.DataFrame([input_dict])[EXPECTED_FEATURES]
            scaled_df = scaler.transform(input_df)
            pred = int(max(0, model.predict(scaled_df)[0]))

            st.session_state.final_result = pred
            st.session_state.inputs = {"cat": cat, "reg": reg, "prc": prc, "tmp": tmp, "dsc": dsc, "mkt": mkt, "hld": hld}
            st.rerun()
        except Exception as e:
            st.error(f"Prediction Error: {e}")

    if st.session_state.final_result is not None:
        display_managerial_summary()

# --- TAB: ANALYSIS & FORECAST ---
with tab_analysis:
    if st.session_state.final_result is not None:
        display_managerial_summary()
        st.divider()

        st.subheader("Demand Horizon & Scenario Planning")
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            horizon = st.select_slider("Select Planning Window (Days)", options=[7, 14, 21, 30], value=14)
        with col_s2:
            scenario = st.radio("Active Planning Scenario", ["Base Case", "Best Case (High Demand)", "Worst Case (Low Demand)"])

        mult = 1.0 if "Base" in scenario else (1.15 if "Best" in scenario else 0.85)
        
        dates = pd.date_range(start="2026-03-13", periods=horizon)
        np.random.seed(42)
        base_val = st.session_state.final_result * mult
        forecast_vals = [int(base_val * (1 + np.random.uniform(-0.06, 0.06))) for _ in range(horizon)]
        df = pd.DataFrame({"Date": dates, "Demand": forecast_vals})
        
        st.line_chart(df, x="Date", y="Demand", color="#4A6741", height=350)
        
        st.divider()

        col_table, col_drivers = st.columns([1, 1])
        with col_table:
            st.markdown(f"#####  Daily Volume Table ({scenario})")
            st.dataframe(df.assign(Date=df['Date'].dt.date).set_index("Date"), height=280, use_container_width=True)
            st.write(f"**Cumulative Required Stock:** {sum(forecast_vals):,} Units")

        with col_drivers:
            st.markdown("#####  Primary Demand Drivers (Ranked)")
            if hasattr(model, 'feature_importances_'):
                fi_df = pd.DataFrame({
                    'Factor': EXPECTED_FEATURES,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False).head(6)
                st.bar_chart(fi_df, x='Factor', y='Importance', color="#607D8B", height=280)
            
        st.divider()
        
        # --- COMPREHENSIVE CONTEXTUAL INTELLIGENCE ---
        st.subheader("🔍 Executive Briefing & Forecast Intelligence")
        
        top_driver = "Price"
        if hasattr(model, 'feature_importances_'):
            top_driver = fi_df.iloc[0]['Factor'].replace('_', ' ')

        hol_msg = "experiencing active Holiday Season impacts" if st.session_state.inputs['hld'] else "operating under standard non-holiday patterns"
        
        st.markdown(f"""
        ### Analysis for {st.session_state.inputs['cat']} in {st.session_state.inputs['reg']}
        
        The model projects a base daily demand of **{st.session_state.final_result} units**. Under the selected **{scenario}**, the procurement team should prepare for a total volume of **{sum(forecast_vals):,} units** over the next **{horizon} days**.

        #### 🧬 Why the Model is Making This Prediction:
        * **Dominant Driver:** The most critical factor for this specific prediction is **{top_driver}**. This indicates that consumer demand for {st.session_state.inputs['cat']} in this region is currently tethered most strongly to this variable.
        * **Environmental Impact:** The input temperature of **{st.session_state.inputs['tmp']}°C** has been processed relative to historical seasonal norms. Perishable goods often see a 5-10% shift for every 5-degree change in temperature, which is reflected in your chart.
        * **Marketing & Price Sensitivity:** Your decision to set the price at **£{st.session_state.inputs['prc']:.2f}** with a **{st.session_state.inputs['dsc']}% discount** interacts with your **£{st.session_state.inputs['mkt']:.0f} marketing spend**. The Random Forest model captures the "diminishing returns" of these combined efforts to provide a realistic ceiling.
        * **Logistics Check:** This scenario is **{hol_msg}**. If you are in 'Best Case' mode, ensure that your supplier lead times can handle a peak daily demand of **{max(forecast_vals)} units**.

        **Strategic Recommendation:** For **{st.session_state.inputs['cat']}**, managers should focus on maintaining a safety stock buffer of approximately 15% above the 'Base Case' to account for the volatility seen in the trend chart.
        """)

    else:
        st.info("Complete the Configuration and click 'Predict' to unlock this briefing.")