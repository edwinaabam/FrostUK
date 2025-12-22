import pandas as pd
import numpy as np


def clean_data(data: pd.DataFrame) -> pd.DataFrame:

        data = data.sort_values(['Product_ID', 'Store_ID'])
        
        data['Wastage_Rate_trend'] = (
            data.groupby(['Product_ID', 'Store_ID'])['Wastage_Units']
            .rolling(4)
            .mean()
            .reset_index(level=[0,1], drop=True)
        )
        
        data.drop('Wastage_Units', axis=1, inplace=True)

        norminal_columns = ['Product_Category', 'Region']
        high_cardinality_columns = ['Product_Name', 'Supplier_Name']

        for col in norminal_columns:
            dummies = pd.get_dummies(data[col], prefix=col)
            dummies = dummies.astype(int)
            data = pd.concat([data, dummies], axis=1)
            data.drop(columns=[col], inplace=True)

        for col in high_cardinality_columns:
            target_mean = data.groupby(col)['Price'].mean()
            data[col] = data[col].map(target_mean)
        
        return data



