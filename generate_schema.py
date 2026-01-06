import pickle
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "lr_model.pkl"
SCHEMA_PATH = BASE_DIR / "model" / "schema.json"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

schema = {
    "features": model.feature_names_in_.tolist()
}

with open(SCHEMA_PATH, "w") as f:
    json.dump(schema, f, indent=2)

print("schema.json created")
print("Number of features:", len(schema["features"]))