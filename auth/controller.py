from dotenv import load_dotenv
import jwt
import json
from datetime import datetime

load_dotenv()


# Convert datetime objects to strings
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def encode_jwt(payload: dict):
    with open(".ssh/private_key.pem", "r") as f:
        private_key = f.read()

    return jwt.encode(
        payload, private_key, algorithm="RS256", json_encoder=CustomJSONEncoder
    )


def decode_jwt(encoded_jwt: str):
    with open(".ssh/public_key.pem", "r") as f:
        public_key = f.read()

    return jwt.decode(encoded_jwt, public_key, algorithms=["RS256"])
