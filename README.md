# Restaurant Kitchen Service

## Project Description:

Restaurant Kitchen Service is a web application developed using Django to manage orders and cooks in a restaurant
kitchen. The application allows customers to place orders and administrators to efficiently manage kitchen resources,
track order status, and assign chefs.

## Features:

- **User Authentication**
    - User registration and login.
    - Admin authentication with enhanced management capabilities.
    - Updating user data.
    - Password recovery by email.

- **Order Management**
    - Create, edit, and delete orders.
    - View order history and statuses.

- **Cook Assignment**
    - Automatically assign chefs based on dish requirements.
    - Manual assignment of chefs if needed.
    - Registered cooks can update their details if necessary.
    - In their personal account, cooks can view the list of orders created by buyers, and cancel or complete orders.

- **Chef Management**
    - Add, edit, and remove chef profiles.
    - Track chef availability and workload.

## Technologies

- **Programming Language:** Python 3.12.2
- **Framework:** Django 5.1
- **Database:** SQLite (default), can be switched to PostgreSQL or other DBMS
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Additional Libraries:** Django Crispy Forms for enhanced form styling

## Installation

### Prerequisites

- Python 3.12.2
- Git

### Steps to Install

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Ananiev-Vitalii/Restaurant-Kitchen-Service.git
    cd RestaurantKitchenService
    ```

2. **Create and Activate a Virtual Environment:**

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

3. **Create a .env File:**

   ### Setting Environment Variables

   Create a `.env` file in the root directory of your project and add the necessary environment variables to allow users
   to recover their password via email:

    ```bash
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_app_password
    ```

   To ensure the project runs correctly, add the following variables to your `.env` file:

    - **DJANGO_SECRET_KEY**: The secret key for your Django application. This key is used for security purposes.
    - **DJANGO_DEBUG**: Set this variable to `True` to enable debug mode during development or to `False` for
      production.

   Example `.env` file content:

    ```bash
    DJANGO_SECRET_KEY=your_secret_key
    DJANGO_DEBUG=True  # Set to False for production
    ```

   **Note**: If these variables are not set, the application will use default values.

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the Application:**

   Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the application.

## Usage

1. **Registration and Login:**

    - Users can register via the registration page.
    - Administrators can log in via the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

2. **Placing an Order:**

    - Customers can select dishes from the menu, specify the number of dishes, choose a cook, and place an order
      at [http://127.0.0.1:8000/menu/](http://127.0.0.1:8000/menu/).
    - Orders are displayed in the cook's personal account for order management
      at [http://127.0.0.1:8000/cook/orders/](http://127.0.0.1:8000/cook/orders/). Additionally, the history of all
      orders created by clients can be viewed at [http://127.0.0.1:8000/orders/](http://127.0.0.1:8000/orders/).

## Contact

- **Developer:** Vitalii Ananiev
- **Email:** ananievvitalii10@gmail.com
- **GitHub:** [Ananiev-Vitalii](https://github.com/Ananiev-Vitalii/Restaurant-Kitchen-Service.git)
