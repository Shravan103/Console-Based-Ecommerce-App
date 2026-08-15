import hashlib
import os


class PasswordHasher:

    @staticmethod
    def hash_password(password):
        salt = os.urandom(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return (
            salt.hex()
            + "$"
            + password_hash.hex()
        )

    @staticmethod
    def verify_password(password, stored_password):
        try:
            salt_hex, hash_hex = stored_password.split("$")

            salt = bytes.fromhex(salt_hex)

            password_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                100_000
            )

            return password_hash.hex() == hash_hex

        except (ValueError, TypeError):
            return False
