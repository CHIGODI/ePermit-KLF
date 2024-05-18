# ePermit Web App 

This project is a web application designed for handling user registration, business registration, and role-based access control. The application allows normal users to register and apply for permits, while administrators have the ability to verify business registrations.

The App was contextualised for Kilifi County - Kenya

## Features

- User authentication with JWT
- Email verification for new user registrations
- Role-based access control
- Session management
- Secure password storage
- Email notifications for verification codes
- Expiration of verification codes
- Business Registartion
- Business registration approval
- Business permit download

## Technologies Used

- Jquery
- HTML/CSS
- Jinja
- Flask
- Flask-SQLAlchemy
- Flask-Mail
- Flask-Session
- PyJWT
- MySQL

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/CHIGODI/permit-web-app.git
    cd permit-web-app
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root directory with the following content:

    ```ini
    SECRET_KEY=your_secret_key
    MAIL_SERVER=smtp.your-email-provider.com
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    ```

5. **Configure the database:**

    Update the `config.py` file to include your database connection details:

    ```python
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@hostname/dbname'
    ```

6. **Run database migrations:**

    Ensure you have the flask-migrate tool installed and run the migrations:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

7. **Run the application:**

    ```bash
    flask run
    ```

## Usage

### Registration and Verification

#### Sign Up:

- Navigate to the sign-up page and create a new account by providing your email and password.
- A verification code will be sent to your email.

#### Email Verification:

- Enter the verification code received via email to complete the registration process.

### Login and Role-Based Access

#### Login:

- Navigate to the login page and log in using your email and password.
- Upon successful login, a JWT token will be stored in an HTTP-only cookie.

#### Role-Based Access:

- Normal users can register businesses and apply for permits.
- Admin users can log in and verify business registrations.

### Logout

- Users can log out by navigating to the logout route, which will clear the JWT token from the cookies.

## Project Structure


