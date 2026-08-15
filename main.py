from controller.user_controller import UserController


def main():
    user_controller = UserController()

    while True:
        print("\n========================================")
        print("       CONSOLE E-COMMERCE SYSTEM")
        print("========================================")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            user_controller.register()

        elif choice == "2":
            user = user_controller.login()

            if user is not None:
                user_controller.route_user(user)

        elif choice == "3":
            print("\nThank you for using the E-Commerce System!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
