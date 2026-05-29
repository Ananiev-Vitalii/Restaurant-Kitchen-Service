# Restaurant Kitchen Service

A Django-based web application for managing restaurant kitchen orders, cooks, and order statuses.

## Live Demo

🔗 [View Deployed Application](https://restaurant-kitchen-service-g7sl.onrender.com)

### Test Account

- **Username:** `Cook2`
- **Password:** `Test12345678`

## Project Description

Restaurant Kitchen Service is a web application developed using Django to manage orders and cooks in a restaurant
kitchen. The application allows customers to place orders and administrators to efficiently manage kitchen resources,
track order status, and assign chefs.

## Features

- **User Authentication**
    - User registration and login.
    - Admin authentication with enhanced management capabilities.
    - Updating user data.
    - Password recovery via email.

- **Order Management**
    - Create, edit, and delete orders.
    - View order history and statuses.

- **Cook Assignment**
    - Automatically assign chefs based on dish requirements.
    - Manual assignment of chefs if needed.
    - Registered cooks can update their details if necessary.
    - In their personal account, cooks can view the list of orders created by buyers, and cancel or complete orders.

- **Cook Management**
    - Add, edit, and remove chef profiles.
    - Track chef availability and workload.

## Technologies

- **Programming Language:** Python 3.12.2
- **Framework:** Django 5.1
- **Database:** SQLite(default for base), PostgreSQL(default for development and production)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Additional Libraries:** Django Crispy Forms and Crispy Bootstrap5 for enhanced form styling

## Installation

### Prerequisites

- Python 3.12.2
- Git

### Steps to Install

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Ananiev-Vitalii/Restaurant-Kitchen-Service.git
    cd RestaurantKitchenService
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    ```

    - **For Windows:**

      ```bash
      venv\Scripts\activate
      ```

    - **For macOS/Linux:**

      ```bash
      source venv/bin/activate
      ```

3. **Create a `.env` File**

   ### Setting Environment Variables

   Create a `.env` file in the root directory of your project and add the necessary environment variables to allow users
   to recover their passwords via email:

    ```env
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_app_password
    ```

   To ensure the project works correctly, you need to assign your secret key to the `DJANGO_SECRET_KEY` environment
   variable in your `.env` file, and specify which settings module you want to use by setting `DJANGO_SETTINGS_MODULE`.
   By default, the deployment environment settings are used:

    - **DJANGO_SECRET_KEY**: The secret key for your Django application. This key is used for security purposes.
    - **DJANGO_SETTINGS_MODULE**: Specifies which settings module to use (e.g., `restaurant.settings.dev` for
      production).

   Example `.env` file content:

    ```env
    DJANGO_SECRET_KEY=your_secret_key
    DJANGO_SETTINGS_MODULE=restaurant.settings.dev

    # Database (only required if using PostgreSQL)
    POSTGRES_DB=your_db_name
    POSTGRES_DB_PORT=5432
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_HOST=your_db_host
   
    # media / cloudinary for development or production 
    CLOUDINARY_CLOUD_NAME=your_cloud_name
    CLOUDINARY_API_KEY=your_api_key
    CLOUDINARY_API_SECRET=your_api_secret

    # domain for production (optional)
    RENDER_EXTERNAL_HOSTNAME=<domain>
    ```

   **Note:** Please ensure that in production mode, if you are using a PostgreSQL database, you have added the necessary
   environment variables in the `.env` file as shown above.

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply Migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

8. **Access the Application**

   Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the application.

## Usage

1. **Registration and Login**

    - Users can register via the registration page.
    - Administrators can log in via the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

2. **Placing an Order**

    - Customers can select dishes from the menu, specify the number of dishes, choose a cook, and place an order
      at [http://127.0.0.1:8000/menu/](http://127.0.0.1:8000/menu/).
    - Orders are displayed in the cook's personal account for order management
      at [http://127.0.0.1:8000/cook/orders/](http://127.0.0.1:8000/cook/orders/). Additionally, the history of all
      orders created by clients can be viewed at [http://127.0.0.1:8000/orders/](http://127.0.0.1:8000/orders/).

      
## Contact

- **Developer:** Vitalii Ananiev
- **Email:** ananievvitalii10@gmail.com
- **GitHub:** [Ananiev-Vitalii](https://github.com/Ananiev-Vitalii/Restaurant-Kitchen-Service)
