# download_data.py
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status',
           'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss',
           'hours_per_week', 'native_country', 'income']

df = pd.read_csv(url, names=columns, skipinitialspace=True)
df.to_csv("data/adult_income.csv", index=False)
print(f"Dataset saved to data/adult_income.csv, shape: {df.shape}")