import ast

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer

df = pd.read_csv("../data/all_cars.csv", index_col='vehicle reference')
print(df.head())
print(f"Duplikaty: {df.duplicated()}")
df.drop_duplicates(inplace=True)
print(f"Ilość rekordów po usunięciu duplikatów: {len(df)}")
df = df.replace('Data not available', None)
df = df.replace('Other', None)
df = df.replace('Not defined', None)
print("Braki danych w %")
print((df.isnull().sum()  / len(df)) * 100)
df.drop(columns=['CO2', 'CO2 WLTP'], inplace=True) # kolumny z dużymi brakami danych

print(df.nunique() < 2)
df.drop(columns=['Mixed consumption', 'Availability date'], inplace=True) # Kolumny z jedną wartością
print((df.isnull().sum()  / len(df)) * 100)
df.dropna(subset=['Fuel', 'Bodywork', 'Color'], inplace=True)
print((df.isnull().sum()  / len(df)) * 100)
print(df.shape)


# equipments
equipments_df = df[["equipments"]]
equipments_df.dropna(inplace=True)
equipments_df['equipments'] = equipments_df['equipments'].apply(ast.literal_eval)
mlb = MultiLabelBinarizer()
equipments_df = pd.DataFrame(mlb.fit_transform(equipments_df['equipments']),
                              columns=mlb.classes_,
                              index=equipments_df.index)
print(equipments_df.head())
equipments_df.to_csv("../data/equipments_binarized.csv")

#    rekodowanie zmiennych
df.loc[:,"price"] = df["Price all taxes included"].apply(lambda x: int(x[:-2].replace(" ","")))
df["Door"] = df["Door"].apply(lambda x: int(x[0]))
df["Mileage_km"] = df["Mileage"].apply(lambda x: int(x[:-2].replace(" ","")))
df["Release"] = pd.to_datetime(df["Release"], dayfirst=True)
df["fiscal_power_hp"] = df["Fiscal power"].apply(lambda x: int(x.replace(" HP", "")))
df["real_power_hp_din"] = df["Real power"].apply(lambda x: int(x.replace(" Hp din", "")))
df = df.drop(columns=["Fiscal power", "Real power", "Mileage", "Price all taxes included", "equipments"]) #delete old columns

## delete
df.to_csv("../data/all_cars_cleaned.csv")


# wybieranie zmiennych do analizy
features = [
    'Bodywork', 'Color', 'Fuel', 'Gearbox', 'Type',
    'Year', 'Mileage_km', 'real_power_hp_din', 'Door'
]
df = df[features + ['price']]
df.to_csv("../data/all_cars_cleaned.csv")

## plot histograms
df.hist(bins=20, figsize=(15, 15), edgecolor='black')
plt.title("Histogramy zmiennych numerycznych")
plt.tight_layout()
plt.savefig("../plots/histogramy_zmiennych_numerycznych.png")
plt.show()
# plot categorical features
categorical_features = ['Bodywork', 'Color', 'Fuel', 'Gearbox', 'Type']
for col in categorical_features:
    df[col].value_counts().plot(kind='bar')
    plt.ylabel("Count")
    plt.xlabel("")
    plt.title(col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"../plots/{col}_values.png",  bbox_inches='tight')
    plt.show()


