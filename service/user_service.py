import re

from dao.user_dao import UserDAO
from model.regular_user import RegularUser
from utils.logger import AppLogger
from utils.password_hasher import PasswordHasher
from exceptions.invalid_credentials_exception import InvalidCredentialsException


class UserService:

    def __init__(self):
        self.user_dao = UserDAO()
        self.logger = AppLogger.get_logger()

    def register_user(self, name, email, password):
        name = name.strip()
        email = email.strip().lower()

        if not name:
            raise ValueError("Name cannot be empty.")

        if not email:
            raise ValueError("Email cannot be empty.")

        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.fullmatch(email_pattern, email):
            raise ValueError(
                "Invalid email format. Please enter a valid email address."
            )

        if not password:
            raise ValueError("Password cannot be empty.")

        if len(password) < 6:
            raise ValueError(
                "Password must contain at least 6 characters."
            )

        existing_user = self.user_dao.get_user_by_email(email)

        if existing_user is not None:
            self.logger.warning(
                f"Registration failed - email already registered: {email}"
            )
            raise ValueError("Email already registered.")

        hashed_password = PasswordHasher.hash_password(password)

        user = RegularUser(
            name=name,
            email=email,
            password=hashed_password
        )

        user = self.user_dao.add_user(user)

        self.logger.info(
            f"User registered successfully: "
            f"user_id={user.user_id}, email={user.email}"
        )

        return user

    def login_user(self, email, password):
        email = email.strip().lower()

        if not email or not password:
            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        user = self.user_dao.get_user_by_email(email)

        if (
            user is None
            or not PasswordHasher.verify_password(
                password,
                user.password
            )
        ):
            self.logger.warning(
                f"Login failed: {email}"
            )
            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        self.logger.info(
            f"User login successful: "
            f"user_id={user.user_id}, "
            f"email={user.email}, "
            f"role={user.get_role()}"
        )

        return user

    def get_user_by_id(self, user_id):
        return self.user_dao.get_user_by_id(user_id)