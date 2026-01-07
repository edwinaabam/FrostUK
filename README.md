# FrostUK
## Project Overview

FrostMart is a large UK grocery retailer with over 800 stores nationwide, offering fresh produce, dairy, baked goods, and seasonal products such as Christmas and Easter specials. While these seasonal and perishable products are a major driver of customer loyalty and revenue, they also introduce significant operational challenges due to short shelf life, weather sensitivity, and unpredictable demand.

This project focuses on building a data-driven demand forecasting solution to help FrostMart better predict weekly demand for perishable products, reduce food waste, and avoid lost sales caused by under- or over-stocking. The work combines historical sales data, product information, store characteristics, weather conditions, and supplier constraints to support smarter inventory and procurement decisions.

A simple interactive demo is included to show how demand predictions can be generated for different product and store scenarios.

## Business Problem

Seasonal and perishable products account for approximately **35% of FrostMart’s annual revenue**, but they also represent one of the highest sources of operational risk.

Key challenges include:

- **Over-stocking**: which leads to food waste, markdown losses, and unnecessary storage costs

- **Under-stocking**: which results in missed sales opportunities, customer dissatisfaction, and reputational damage

- **Weather-driven demand spikes**: where sudden temperature changes can cause rapid increases in demand for chilled or seasonal items

- **Complex supply chain constraints**: including limited supplier capacity, cold-storage requirements, and long lead times for certain products

Together, these factors contribute to an estimated **£12.2 million annual impact**, split between excess inventory waste and lost revenue.

Traditional inventory planning methods struggle to handle this level of variability, particularly when weather, promotions, holidays, and regional differences interact.

## Project Objective

The primary goal of this project is to:

**Use predictive modelling to forecast weekly demand for perishable seasonal products, enabling data-driven inventory and procurement decisions across FrostMart’s store network.**

More specifically, the project aims to:

- Improve demand forecasting accuracy at both store and regional levels

- Reduce perishable food waste by aligning stock levels with expected demand

- Prevent stock-outs during peak seasonal periods

- Support evidence-based decision-making for procurement and supply chain planning

## Expected Impact

If applied in a real operational setting, the approach demonstrated in this project could support:

- 30–40% reduction in perishable food waste

- 10–20% increase in seasonal revenue capture through improved availability

- A shift from intuition-based planning to fully data-driven decision making

These improvements also align with sustainability goals and UK regulatory expectations around food waste reduction.


## Data Used

This project brings together multiple data sources to reflect the real-world complexity of managing perishable products in a national retail chain. Each dataset captures a different aspect of demand, supply, or operational constraints.

Core Data Sources

- **Product Details**

    - Product name and category (e.g. bakery, meat, dairy, beverages)

    - Shelf-life in days, which is critical for waste and expiry risk

    - Supplier identifiers to reflect sourcing constraints

- **Weekly Sales Data**

    - Units sold per product, per store, per week (target variable)

    - Marketing spend and promotional activity

    - Wastage units to track losses from unsold stock

- **Store Information**

    - Store location and region

    - Store size (floor area)

    - Cold storage capacity, which limits how much perishable stock can be held

- **Weather Data**

    - Average temperature

    - Rainfall levels

    - Holiday indicators
      
These variables help capture weather-driven and seasonal demand fluctuations.

- **Supplier Information**

    - Supplier lead times

    - Supply capacity constraints

This reflects the fact that stock availability is not unlimited or instant.

## Why Multiple Data Sources Matter

Demand for perishable goods is rarely driven by a single factor. Instead, it is influenced by a combination of:

- Seasonality (e.g. Christmas, Easter, summer periods)

- Weather conditions (temperature and rainfall)

- Store characteristics (size, location, storage capacity)

- Promotions and pricing

- Supply-side limitations

By integrating these datasets into a unified analytical view, the model is better able to reflect how demand behaves in practice, rather than relying on sales history alone.

## Target Variable

- **Units_Sold**

The model predicts the number of units expected to be sold for a given product, store, and time period.
This prediction can then be used to guide inventory, procurement, and replenishment decisions.


## How the Model Works 

The model is designed to estimate how many units of a perishable product are likely to be sold in a given week, based on patterns observed in historical data.

Rather than relying on intuition or fixed rules, the model learns from past behaviour to understand how different factors influence demand.

### What the model looks at:

For each product and store, the model considers information such as:

- Product characteristics

  - Product category (e.g. bakery, meat, dairy)

  - Shelf-life, which affects urgency of purchase and waste risk

- Store characteristics

     - Store size

     - Cold storage capacity

     - Geographic region

- Time-related factors

    - Week and month

    - Seasonal effects such as holidays or festive periods

- Weather conditions

    - Average temperature

    - Rainfall levels
      
These help capture sudden changes in demand, especially for chilled or seasonal items.

- Commercial factors

    - Marketing spend and promotional activity

    - Supplier capacity constraints
 

### What the Model Produces

The output of the model is:

A weekly forecast of units sold for a specific product at a specific store.

This forecast can then be used to:

- guide how much stock should be ordered

- adjust inventory levels ahead of seasonal peaks

- reduce waste caused by excess stock

- avoid lost sales due to stock-outs


### Why a Regression-Based Approach Was Used

Regression models are well suited to this problem because they:

- handle multiple influencing factors at once

- are transparent and easy to interpret

- perform well for continuous outcomes like units sold

- allow comparison between simple baseline models and more advanced approaches

The project begins with a **Linear Regression baseline** and explores more advanced models where needed to capture non-linear demand patterns. This ensures a balance between accuracy, interpretability, and practical usability.



## How the Model Is Deployed

The model is deployed as a lightweight, interactive demo to illustrate how demand predictions can be generated and explored in practice.

The deployment consists of two main components:

- **Prediction API (FastAPI)**  
  The trained Linear Regression model is exposed via a REST API that accepts product, store, and contextual information and returns a demand forecast.  
  A feature schema is used to ensure that incoming data is aligned consistently with how the model was trained.

- **Interactive Interface (Streamlit)**  
  A simple web interface allows users to adjust input variables (e.g. product details, store characteristics, weather conditions) and view predicted weekly demand.  
  This interface is intended for demonstration and discussion purposes rather than direct operational use.

This setup separates the modelling logic from the user interface, making the system easier to test, extend, and explain to non-technical stakeholders.


## Results and Impact

### Model Performance

The project successfully delivers a working demand forecasting model capable of predicting weekly units sold for perishable seasonal products.

Model evaluation focused on forecast accuracy using standard regression metrics (e.g. MAE and RMSE) and comparison against simple baseline approaches. Results show that the model captures key demand drivers such as seasonality, weather conditions, and store characteristics more effectively than naïve forecasting methods.

While exact performance varies by product and context, the results demonstrate that a data-driven approach provides more reliable demand estimates than manual or rule-based planning alone.

---

### Potential Business Impact

Although the model has not been deployed in live operations, the results suggest clear potential benefits if integrated into FrostMart’s planning workflows:

- **Reduced over-stocking risk**, by aligning orders more closely with expected demand  
- **Lower food waste**, particularly for short shelf-life products  
- **Improved availability during peak seasonal periods**, reducing lost sales  
- **More consistent planning decisions**, supported by data rather than intuition alone  

The model is intended as a decision-support tool rather than a replacement for operational expertise. Further impact assessment would require live deployment and controlled testing within the supply chain.



