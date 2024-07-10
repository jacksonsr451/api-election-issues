from jwt import encode, decode, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from jwcrypto import jwk


class AccessTokenService:
    @staticmethod
    def load_rsa_keys():
        with open('./private_key.pem', 'rb') as f:
            priv_pem = f.read()
            priv_key = jwk.JWK.from_pem(priv_pem)

        with open('./public_key.pem', 'rb') as f:
            pub_pem = f.read()
            pub_key = jwk.JWK.from_pem(pub_pem)

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
        _priv_key, _pub_key = AccessTokenService.load_rsa_keys()

        algorithm = AccessTokenService.get_algorithm()

        exp = AccessTokenService.get_exp()

        claims = {'sub': user_id, 'exp': exp.timestamp()}

        return exp.timestamp(), encode(
            claims, _priv_key.export_to_pem(private_key=True, password=None).decode('utf-8'), algorithm=algorithm)

    @staticmethod
    def verify_token(token: str, token_type: str = 'access') -> dict:
        _priv_key, _pub_key = AccessTokenService.load_rsa_keys()

        algorithm = AccessTokenService.get_algorithm()

        try:
            claims = decode(token, _pub_key.export_to_pem(), algorithms=[algorithm])
            if claims.get('type') != token_type:
                raise ValueError("Invalid token type")
            return claims
        except ExpiredSignatureError as e:
            raise ValueError("Token expired") from e
        except Exception as e:
            raise ValueError(f"Invalid token: {e}") from e
