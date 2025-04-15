import argparse
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def parse_args():
    parser = argparse.ArgumentParser()

    # Hyperparameters
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--max-depth', type=int, default=None)

    # SageMaker environment variables
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))

    return parser.parse_args()

def load_and_prepare_data(train_path):
    df = pd.read_csv(os.path.join(train_path, 'data.csv'))

    # Create future values as labels if not already present
    if 'temperature_future' not in df.columns or 'humidity_future' not in df.columns:
        df['temperature_future'] = df['temperature'].shift(-1)
        df['humidity_future'] = df['humidity'].shift(-1)
        df.dropna(inplace=True)

    X = df[['temperature', 'humidity']]
    y = df[['temperature_future', 'humidity_future']]

    return X, y

def train_and_save_model(X, y, model_dir, n_estimators, max_depth):
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X, y)

    output_path = os.path.join(model_dir, 'model.joblib')
    joblib.dump(model, output_path)
    print(f"✅ Model saved to: {output_path}")

def main():
    args = parse_args()

    print("📥 Loading data...")
    X, y = load_and_prepare_data(args.train)

    print("🔧 Training model...")
    train_and_save_model(X, y, args.model_dir, args.n_estimators, args.max_depth)

if __name__ == "__main__":
    main()

