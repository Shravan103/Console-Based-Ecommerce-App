from config.database import get_connection
from model.admin import Admin
from model.regular_user import RegularUser


class UserDAO:

    def add_user(self, user):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                user.name,
                user.email,
                user.password,
                user.get_role()
            )

            cursor.execute(query, values)
            connection.commit()

            user.user_id = cursor.lastrowid
            return user

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    def get_user_by_email(self, email):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT user_id, name, email, password, role
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._create_user_object(row)

        finally:
            cursor.close()
            connection.close()

    def get_user_by_id(self, user_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT user_id, name, email, password, role
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._create_user_object(row)

        finally:
            cursor.close()
            connection.close()

    def _create_user_object(self, row):
        user_id, name, email, password, role = row

        if role == "ADMIN":
            return Admin(
                user_id=user_id,
                name=name,
                email=email,
                password=password
            )

        return RegularUser(
            user_id=user_id,
            name=name,
            email=email,
            password=password
        )
