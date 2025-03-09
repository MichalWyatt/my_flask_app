# my_flask_app
Updated Flask website with password update form, NIST password validation, and logging.

Collecting workspace information# FlaskLogin Application

## Overview

This is a simple Flask web application that demonstrates user registration, login, and password update functionalities. The application includes password validation adhering to NIST SP 800-63B guidelines and logs failed login attempts.

## Features

- User Registration
- User Login
- Password Update
- Password Validation
- Logging of Failed Login Attempts
- Dynamic Content Rendering
- Responsive Design

## Project Structure

```
.idea/
    .gitignore
    FlaskLogin.iml
    inspectionProfiles/
        profiles_settings.xml
    misc.xml
    modules.xml
    vcs.xml
    workspace.xml
failed_logins.log
Final-FlaskApp.docx
my_flask_app.py
static/
    paving1.jpeg
    paving2.jpeg
    paving3.jpg
    paving4.jpeg
    styles.css
templates/
    about.html
    contact.html
    home.html
    login.html
    register.html
    update_password.html
```

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```sh
    cd FlaskLogin
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Run the Flask application:
    ```sh
    python my_flask_app.py
    ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Routes

- `/` - Home page (requires login)
- `/about` - About page (requires login)
- `/contact` - Contact page (requires login)
- `/register` - User registration page
- `/login` - User login page
- `/logout` - User logout
- `/update_password` - Password update page (requires login)

## Password Validation

The application validates passwords based on the following criteria:
- At least 12 characters long
- Contains at least 1 uppercase letter
- Contains at least 1 lowercase letter
- Contains at least 1 number
- Contains at least 1 special character
- Not a common password

## Logging

Failed login attempts are logged to failed_logins.log with the timestamp, email, and IP address.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
