from jwt import encode, decode, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from jwcrypto import jwk


class AccessToken:
    @staticmethod
    def load_rsa_keys():
        with open('./private_key.pem', 'rb') as f:
            priv_pem = f.read()
            priv_key = jwk.JWK.from_pem(priv_pem).export_to_pem(private_key=True, password=None).decode('utf-8')

        with open('./public_key.pem', 'rb') as f:
            pub_pem = f.read()
            pub_key = jwk.JWK.from_pem(pub_pem).export_to_pem().decode('utf-8')

        return priv_key, pub_key

    priv_key, pub_key = load_rsa_keys()

    @staticmethod
    def get_algorithm() -> str:
        return 'RS256'

    @staticmethod
    def get_exp() -> datetime:
        return datetime.now(timezone.utc) + timedelta(hours=1)

    @staticmethod
    def create_access_token(user_id) -> tuple[int, str]:
        _priv_key, _pub_key = AccessToken.load_rsa_keys()

        algorithm = AccessToken.get_algorithm()

        exp = AccessToken.get_exp()

        claims = {'sub': user_id, 'exp': exp.timestamp()}

        return exp.timestamp(), encode(
            claims, _priv_key, algorithm=algorithm)

    @staticmethod
    def verify_token(token: str) -> dict:
        _priv_key, _pub_key = AccessToken.load_rsa_keys()

        algorithm = AccessToken.get_algorithm()

        try:
            return decode(token, _pub_key, algorithms=[algorithm])
        except ExpiredSignatureError as e:
            raise ValueError("Token expired") from e
        except Exception as e:
            raise ValueError(f"Invalid token: {e}") from e
