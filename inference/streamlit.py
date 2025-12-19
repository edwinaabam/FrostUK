import streamlit as st
import requests

st.title("Perishable Goods Prediction")

with st.form("form"):
    product_id = st.number_input("Product ID", value=1, min_value=1)
    store_id = st.number_input("Store ID", value=1, min_value=1)
    wastage_unit = st.number_input("Wastage units", value=100, min_value=0)
    product_name = st.text_input("Product Name", value="Whole Wheat Bread 800g")
    product_category = st.selectbox("Product Category", ['Bakery', 'Meat', 'Beverages', 'Dairy'])
    shelf_life = st.number_input("Shelf Life Days", value=3, min_value=1)
    price = st.number_input("Price", value=2.5, min_value=0.0)
    cold_storage = st.number_input("Cold Storage Capacity", value=500)
    store_size = st.number_input("Store Size", value=1500)
    rainfall = st.number_input("Rainfall", value=20.5)
    avg_temp = st.number_input("Average Temperature", value=22.3)
    region = st.selectbox("Region", ['London', 'Midlands', 'North East', 'North West', 'South East', 'South West'])
    supplier_name = st.text_input("Supplier Name", value="Fresh Foods Ltd")
    supply_capacity = st.number_input("Supply Capacity", value=50000)
    marketing_spend = st.number_input("Marketing Spend", value=500.0)
    month = st.number_input("Month", value=1, min_value=1, max_value=12)
    day = st.number_input("Day", value=15, min_value=1, max_value=31)

    submitted = st.form_submit_button("Predict")


if submitted:
    try:
        data = {
            "Product_ID": product_id,
            "Store_ID": store_id,
            "Wastage_Units": wastage_unit,
            "Product_Name": product_name,
            "Product_Category": product_category,
            "Shelf_Life_Days": shelf_life,
            "Price": price,
            "Cold_Storage_Capacity": cold_storage,
            "Store_Size": store_size,
            "Rainfall": rainfall,
            "Avg_Temperature": avg_temp,
            "Region": region,
            "Supplier_Name": supplier_name,
            "Supply_Capacity": supply_capacity,
            "Marketing_Spend": marketing_spend,
            "Month": month,
            "Day": day
        }
        api_url = "https://vfdfwz42-8000.uks1.devtunnels.ms/predict"
        response = requests.post(url = api_url, json = {"records": [data]})

        if response.status_code == 200:
            result = response.json()
            result = result.get("predictions")
            st.write(f"Estimated Unit Sold: {int(result[0])}")
        else:
            st.error(f"API Error: {response.status_code}")

    except Exception as e:
        st.error(str(e))


if __name__ == "__main__":
    pass