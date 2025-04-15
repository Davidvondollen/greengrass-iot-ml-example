import unittest, tempfile, os
import pandas as pd
from ml_pipeline.train import RandomForestRegressor, joblib

class TestMLPipeline(unittest.TestCase):
    def test_training_pipeline(self):
        df = pd.DataFrame({
            'temperature': [20, 21, 22, 23],
            'humidity': [50, 51, 52, 53],
            'temperature_future': [21, 22, 23, 24],
            'humidity_future': [51, 52, 53, 54]
        })

        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = os.path.join(tmpdir, 'data.csv')
            model_path = os.path.join(tmpdir, 'model.joblib')

            df.to_csv(data_path, index=False)

            # Train model directly
            X = df[['temperature', 'humidity']]
            y = df[['temperature_future', 'humidity_future']]
            model = RandomForestRegressor(n_estimators=10)
            model.fit(X, y)
            joblib.dump(model, model_path)

            self.assertTrue(os.path.exists(model_path))
            
            # Load and predict
            loaded_model = joblib.load(model_path)
            preds = loaded_model.predict([[22, 52]])
            self.assertEqual(len(preds[0]), 2)

if __name__ == '__main__':
    unittest.main()

