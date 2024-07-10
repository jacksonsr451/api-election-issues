from application.auth.services.access_token_service import AccessTokenService


def get_access_token() -> AccessTokenService:
    return AccessTokenService