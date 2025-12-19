from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from DataCleaning.preprocess import clean_data
import pandas as pd
import pickle
from typing import List, Dict, Any
import os
import uvicorn
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(title = 'Perishable Goods Prediction API', version = '1.0')

class Item(BaseModel):
    records: List[Dict[str, Any]] = Field(..., example = [
            {   
                "Product_ID": 1,
                "Store_ID": 1,
                "Wastage_Units": 100,
                "Product_Name": "Whole Wheat Bread 800g",
                "Product_Category": "Bakery",
                "Shelf_Life_Days": 3,
                "Price": 2.5,
                "Cold_Storage_Capacity": 500,
                "Store_Size": 1500,
                "Rainfall": 20.5,
                "Avg_Temperature": 22.3,
                "Region": "North",
                "Supplier_Name": "Fresh Foods Ltd",
                "Supply_Capacity": 50000,
                "Marketing_Spend": 500.0,
                "Month": 1,
                "Day": 15,
            }
        ]
    )

@app.post("/predict")
def predict(req: Item):
    try:
        data = pd.DataFrame(req.records)
        cleaned_data = clean_data(data)

        model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'rf_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        schema_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'schema.json')
        with open(schema_path, 'r') as f:
            feature = json.load(f)
            main_features = feature['features']

        cleaned_data = cleaned_data.reindex(columns = main_features, fill_value=0)
        
        pred = model.predict(cleaned_data)

        return {"predictions": pred.tolist()}

    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Data cleaning error: {str(e)}")
    
if __name__ == "__main__":
    print(f"Server is on port {os.getenv('port', 3000)}")
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv('port', 3000)))
