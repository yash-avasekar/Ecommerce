# E-Commerce Business-to-Customer (B2C) Shopping App

This Django project aims to create an e-commerce platform where businesses can showcase their products, and customers can browse, shop, and make secure payments. The app includes several key features:

## Features

1. **Token-Based Authentication and Authorization**:
   - Users can register, log in, and obtain an authentication token.
   - Token-based authentication ensures secure access to protected endpoints.

2. **Payment Integration with Razorpay**:
   - Customers can securely make payments using the Razorpay payment gateway.
   - Integration with Razorpay API ensures smooth transactions.

3. **Temporary Database (SQLite3)**:
   - The project uses SQLite3 as the temporary database for development and testing.
   - You can easily switch to a production database (e.g., PostgreSQL) for deployment.

4. **Image Upload**:
   - Businesses can upload product images.
   - Images are associated with product listings.

5. **Email Notifications**:
   - The app sends email notifications for order confirmations, shipping updates, and other relevant events.
   - Integration with Django's built-in email functionality.

## Getting Started

1. **Installation**:
   - Make sure you have Python and Django installed.
   - Clone this repository: `git clone https://github.com/yourusername/ecommerce-project.git`
   - Move into directory Ecommerce : `cd Ecommerce`
   - Install project dependencies: `pip install -r requirements.txt`

2. **Database Setup**:
   - Run migrations: `python manage.py migrate`
   - Create a superuser: `python manage.py createsuperuser`
   - Load initial data (categories, products, etc.) if needed.

3. **Configuration**:
   - Set up your environment variables (e.g., secret keys, database settings).
   - Configure Razorpay API keys in `settings.py`.

4. **Run the Development Server**:
   - Start the server: `python manage.py runserver`
   - Access the app at `http://localhost:8000/`

5. **Admin Panel**:
   - Log in to the admin panel at `http://localhost:8000/admin/`.
   - Manage products, orders, and users.
   - 

Happy coding! 🚀

