# bias_monitor.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from fairlearn.metrics import demographic_parity_difference
import os

class BiasMonitor:
    def __init__(self, dataset_path="data/adult_income.csv"):
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")
        self.df = pd.read_csv(dataset_path)
        self.threshold = 0.8
        self._prepare_data()
        self._train_model()

    def _prepare_data(self):
        # Encode categoricals
        le = LabelEncoder()
        for col in self.df.select_dtypes(include=['object', 'string']).columns:
            self.df[col] = le.fit_transform(self.df[col].astype(str))
        # Target: income (already encoded, but ensure binary)
        self.y_true = self.df['income']
        # Protected attribute: sex (0=Male, 1=Female after encoding)
        self.protected = self.df['sex']
        # Features: drop target
        self.X = self.df.drop(['income'], axis=1)

    def _train_model(self):
        X_train, _, y_train, _ = train_test_split(self.X, self.y_true, test_size=0.3, random_state=42)
        self.model = RandomForestClassifier(n_estimators=30, random_state=42)
        self.model.fit(X_train, y_train)
        self.y_pred = self.model.predict(self.X)

    def compute_demographic_parity(self):
        dp = demographic_parity_difference(self.y_true, self.y_pred, sensitive_features=self.protected)
        return abs(dp)

    def is_compliant(self):
        dp = self.compute_demographic_parity()
        print(f"📊 Demographic parity difference: {dp:.4f}")
        print(f"📏 Compliance threshold: {self.threshold}")
        return bool(dp < self.threshold)




if __name__ == "__main__":
    monitor = BiasMonitor()
    compliant = monitor.is_compliant()
    print(f"✅ Compliant? {compliant}")