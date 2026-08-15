CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'REGULAR_USER'
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE IF NOT EXISTS carts (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cart_items (
    cart_item_id INT PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id)
        REFERENCES carts(cart_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,
    UNIQUE (cart_id, product_id)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);

INSERT INTO products (name, description, price, stock)
SELECT 'Laptop', 'Dell Inspiron Laptop', 55000.00, 10
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Laptop'
);

INSERT INTO products (name, description, price, stock)
SELECT 'Mouse', 'Wireless Mouse', 800.00, 25
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Mouse'
);

INSERT INTO products (name, description, price, stock)
SELECT 'Keyboard', 'Mechanical Keyboard', 2500.00, 15
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Keyboard'
);

INSERT INTO products (name, description, price, stock)
SELECT 'Headphones', 'Wireless Bluetooth Headphones', 3000.00, 20
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Headphones'
);

INSERT INTO products (name, description, price, stock)
SELECT 'Monitor', '24 inch Full HD Monitor', 12000.00, 8
WHERE NOT EXISTS (
    SELECT 1 FROM products WHERE name = 'Monitor'
);

INSERT INTO users (name, email, password, role)
SELECT 'Administrator', 'admin@ecommerce.com', '86cba272461aad2880878a1aa00d1236$79e122019b5af985c8ac92b00b49fc42be702d901f6b5f5dab7862398af02792', 'ADMIN'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@ecommerce.com'
);
