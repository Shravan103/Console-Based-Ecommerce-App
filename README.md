# P0 - Console Based Ecommerce App

## Technologies
- Python
- MySQL
- mysql-connector-python
- pytest
- Git

## Features
- Admin and Regular User roles
- User registration and login
- Password hashing using PBKDF2-HMAC-SHA256
- Product management for Admin
- Shopping cart for Regular Users
- Order processing and order history
- JSON backups
- Application logging
- Custom exception handling
- Unit tests with pytest

## Setup
1. Create/activate the Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure MySQL credentials in `config/database.py`.
4. Run `Database_Schema.sql` in MySQL.
5. Start the application:

```bash
python main.py
```
