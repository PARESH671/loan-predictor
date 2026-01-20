import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import numpy as np

np.random.seed(42)
num_samples = 1000

data = {
    'income': np.random.randint(15000, 100000, num_samples),
    'age': np.random.randint(18, 65, num_samples),
    'credit_score': np.random.randint(300, 850, num_samples),
    'loan_amount': np.random.randint(5000, 50000, num_samples)
}

df = pd.DataFrame(data)
df['eligible'] = ((df['credit_score'] > 600) & (df['income'] > (df['loan_amount'] * 2)) & (df['age'] > 21)).astype(int)

X = df[['income', 'age', 'credit_score', 'loan_amount']]
y = df['eligible']

model = DecisionTreeClassifier(max_depth=5)
model.fit(X, y)

joblib.dump(model, 'loan_model.pkl')
print(f"Model trained on {num_samples} records.")