import json
import os
from app import app  # import your Flask app and Api instance

# Access the Api instance via app.extensions for flask-smorest
api = app.extensions.get("flask-smorest")

with app.app_context():
    # flask-smorest stores the spec in api.spec
    openapi_spec = api.spec.to_dict()

    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_spec, f, indent=2)
