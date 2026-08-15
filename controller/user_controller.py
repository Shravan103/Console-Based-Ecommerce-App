from service.user_service import UserService
from controller.product_controller import ProductController
from controller.cart_controller import CartController
from controller.order_controller import OrderController
from model.admin import Admin
from model.regular_user import RegularUser
from utils.backup_service import BackupService
from exceptions.invalid_credentials_exception import InvalidCredentialsException


class UserController:

    def __init__(self):
        self.user_service = UserService()

    def register(self):
        print("\n========== USER REGISTRATION ==========")

        name = input("Enter name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user = self.user_service.register_user(
                name,
                email,
                password
            )

            print("\nRegistration successful!")
            print("User ID:", user.user_id)
            print("Name:", user.name)
            print("Email:", user.email)
            print("Role:", user.get_role())

        except ValueError as e:
            print("\nRegistration failed:", e)

    def login(self):
        print("\n========== LOGIN ==========")

        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user = self.user_service.login_user(
                email,
                password
            )

            print("\nLogin successful!")
            print("Welcome,", user.name)
            print("Role:", user.get_role())

            return user

        except InvalidCredentialsException as e:
            print("\nLogin failed:", e)
            return None

    def admin_menu(self, user):
        product_controller = ProductController()
        backup_service = BackupService()

        while True:
            print("\n================================")
            print("           ADMIN MENU")
            print("================================")
            print("1. View Products")
            print("2. Add Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. Create Backup")
            print("6. Logout")
            print("================================")

            choice = input("Enter choice: ")

            if choice == "1":
                product_controller.view_products()

            elif choice == "2":
                product_controller.add_product()

            elif choice == "3":
                product_controller.update_product()

            elif choice == "4":
                product_controller.delete_product()

            elif choice == "5":
                try:
                    backup_service.backup_all()
                    print("\nBackup created successfully!")
                    print("- backup/users.json")
                    print("- backup/products.json")
                    print("- backup/orders.json")
                except Exception as e:
                    print("\nBackup failed:", e)

            elif choice == "6":
                print("\nLogged out successfully.")
                break

            else:
                print("\nInvalid choice.")

    def regular_user_menu(self, user):
        product_controller = ProductController()
        cart_controller = CartController()
        order_controller = OrderController()

        while True:
            print("\n================================")
            print("       REGULAR USER MENU")
            print("================================")
            print("1. View Products")
            print("2. Add Product to Cart")
            print("3. View Cart")
            print("4. Remove Product from Cart")
            print("5. Place Order")
            print("6. Order History")
            print("7. Logout")
            print("================================")

            choice = input("Enter choice: ")

            if choice == "1":
                product_controller.view_products()

            elif choice == "2":
                cart_controller.add_to_cart(user.user_id)

            elif choice == "3":
                cart_controller.view_cart(user.user_id)

            elif choice == "4":
                cart_controller.remove_from_cart(user.user_id)

            elif choice == "5":
                order_controller.place_order(user.user_id)

            elif choice == "6":
                order_controller.order_history(user.user_id)

            elif choice == "7":
                print("\nLogged out successfully.")
                break

            else:
                print("\nInvalid choice.")

    def route_user(self, user):
        if isinstance(user, Admin):
            self.admin_menu(user)
        elif isinstance(user, RegularUser):
            self.regular_user_menu(user)
        else:
            print("\nUnknown user type.")
