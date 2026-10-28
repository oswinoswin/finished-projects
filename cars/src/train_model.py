import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

df_model = pd.read_csv("../data/all_cars_cleaned.csv")

formulas = ['price ~ Year + Mileage_km + real_power_hp_din',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Bodywork)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Color, levels=all_colors) + C(Gearbox) + C(Bodywork)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Gearbox)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Gearbox) + C(Bodywork)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Type)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Type) + C(Bodywork)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Type) + C(Bodywork) + C(Gearbox)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Fuel) + C(Type) + C(Gearbox)',
            'price ~ Year + Mileage_km + real_power_hp_din + C(Type)',
            'price ~ Year + Mileage_km + real_power_hp_din + Door']


target = ['price']

features = [
    'Bodywork', 'Color', 'Fuel', 'Gearbox', 'Type',
    'Year', 'Mileage_km', 'real_power_hp_din', 'Door'
]
all_colors = df_model['Color'].unique()

# df_model = df[features + [target]].dropna()
best_r2 = 0
best_formula = ""
best_model = None
for f in formulas:
    train, test = train_test_split(df_model, test_size=0.2, random_state=42)
    est = smf.ols(formula=f, data=train).fit()
    y_predict = est.predict(test[features], transform=True)
    mae = mean_absolute_error(test['price'], y_predict)
    r2 = r2_score(test['price'], y_predict)
    print("-----------------------------------------------------------------------------------")
    print(f)
    print(mae, r2)
    print(est.summary())
    if r2 > best_r2:
        best_r2 = r2
        best_formula = f
        best_model = est
print(f"BEST FORMULA: {best_formula}")
joblib.dump(best_model, f"model.pkl")
