from pwdlib import PasswordHash


class PasswordEncryptionService:
    @staticmethod
    def encrypt_password(password: str) -> str:
        return PasswordHash.recommended().hash(password=password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordHash.recommended().verify(plain_password, hashed_password)
