# ePermit Web App

This project is a web application designed for handling user registration, business registration, and role-based access control. The application allows normal users to register and apply for permits, while administrators have the ability to verify business registrations.

The App was contextualized for Kilifi County - Kenya

## Features

- User authentication with JWT
- Email verification for new user registrations
- Role-based access control
- Session management
- Secure password storage
- Email notifications for verification codes
- Expiration of verification codes
- Business Registration
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
- reportLab

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/CHIGODI/ePermit-KLF.git
    cd ePermit-KLF
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
    SECRET_KEY=''
    SESSION_TYPE=''
    SESSION_FILE_DIR=''
    SESSION_FILE_THRESHOLD=
    MAIL_SERVER=''
    MAIL_PORT=
    MAIL_USE_TLS=
    MAIL_USERNAME=''
    MAIL_PASSWORD=''
    MAPS_API_KEY=''
    CONSUMER_KEY=''
    CONSUMER_SECRET=''
    SHORT_CODE=''
    PASS_KEY=''
    EPERMIT_ENV=production
    EPERMIT_MYSQL_USER=epermit_dev
    EPERMIT_MYSQL_PWD=epermit_pwd
    EPERMIT_MYSQL_HOST=localhost
    EPERMIT_MYSQL_DB=epermit_dev_db
    ```

5. **Create the database:**

    ```bash
    cat setup_es_db.sql | mysql -uroot -p
    ```

6. **Set Up Admin User:**

    The admin user is set up with the `setup_es_db.sql` file. You can modify the admin email and password in this file, which you will use to log in as admin. The admin has different roles, such as rejecting and approving businesses.

7. **Run the application:**

    ```bash
    python3 -m web_flask.app
    ```

8. **Run the API service:**

    ```bash
    python3 -m api.v1.app
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

## Dashboard

The dashboard serves as a centralized hub for users to manage their ePermit-related activities. Here are the key functionalities available on the dashboard:

### Service Selection

Upon logging in, users are presented with a panel where they can select a service. At present, only two services are available:

- **Business Registration**: Users can register a new business by filling out a registration form and submitting it for approval.
- **Renew Business**: Users can renew an existing business registration by submitting a renewal request.

### Business Registration

When users select the "Business Registration" service, they are directed to a registration form where they can provide details about the new business.

After filling out the form, users can submit it for review. The submission triggers an approval process by the admin.

### Admin Approval

Admin users have the authority to approve or reject business registration requests. They can access the pending requests from their admin dashboard.

Once the admin approves a registration request, the status of the business registration is updated, and users can view it in the "My Business" section of the side navigation.

### Payment and Permit Issuance

After the business registration request is approved, users have the option to proceed with payment for the permit.

Upon successful payment, a system-generated permit is issued to the user. The permit is valid for one year from the date of issuance.

### My Business

In the "My Business" section of the side navigation, users can view the status of their business registrations. This includes pending, approved, and rejected registrations.

### My Permits

Users can access their active permits under the "My Permits" section of the side navigation.

Downloading of active permits is available for one month from the date of issuance. After this period, users will not be able to download the permit.

### Logout

- Users can log out by navigating to the logout route, which will clear the JWT token from the cookies.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.

## Project Updates

This project is under constant development and will be regularly updated to add new features, improve existing functionalities, and ensure security.
