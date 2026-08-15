from service.product_service import ProductService


class ProductController:

    def __init__(self):
        self.product_service = ProductService()

    def view_products(self):
        print("\n========== AVAILABLE PRODUCTS ==========")

        products = self.product_service.get_all_products()

        if not products:
            print("No products available.")
            return

        print(
            f"{'ID':<5}"
            f"{'Name':<20}"
            f"{'Price':<15}"
            f"{'Stock':<10}"
        )
        print("-" * 50)

        for product in products:
            print(
                f"{product.product_id:<5}"
                f"{product.name:<20}"
                f"₹{product.price:<14.2f}"
                f"{product.stock:<10}"
            )

    def add_product(self):
        print("\n========== ADD PRODUCT ==========")

        name = input("Enter product name: ")
        description = input("Enter description: ")

        try:
            price = float(input("Enter price: "))
            stock = int(input("Enter stock: "))

            product = self.product_service.add_product(
                name,
                description,
                price,
                stock
            )

            print("\nProduct added successfully!")
            print("Product ID:", product.product_id)

        except ValueError as e:
            print("\nFailed to add product:", e)

    def update_product(self):
        print("\n========== UPDATE PRODUCT ==========")

        try:
            product_id = int(input("Enter product ID: "))
            name = input("Enter new product name: ")
            description = input("Enter new description: ")
            price = float(input("Enter new price: "))
            stock = int(input("Enter new stock: "))

            product = self.product_service.update_product(
                product_id,
                name,
                description,
                price,
                stock
            )

            print("\nProduct updated successfully!")
            print("Product:", product.name)

        except ValueError as e:
            print("\nFailed to update product:", e)

    def delete_product(self):
        print("\n========== DELETE PRODUCT ==========")

        try:
            product_id = int(input("Enter product ID: "))

            product = self.product_service.delete_product(
                product_id
            )

            print(
                f"\nProduct '{product.name}' deleted successfully!"
            )

        except ValueError as e:
            print("\nFailed to delete product:", e)
