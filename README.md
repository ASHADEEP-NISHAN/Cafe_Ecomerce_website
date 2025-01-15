Flask Coffee Shop Website

Overview

This project is a Flask-based web application for a coffee shop. It integrates a SQL database for managing coffee shop data and allows sending emails via SMTP for customer communication or notifications. The application provides a user-friendly interface for showcasing coffee products and managing orders.

Features

Web framework: Flask

Database integration: Flask-SQLAlchemy

Email sending capability using SMTP

Routes for displaying coffee products and handling customer interactions

Prerequisites

Ensure you have the following installed on your machine:

Python 3.7 or later

Pip (Python package installer)

Installation

Clone the repository:

git clone <repository-url>
cd <repository-folder>

Install dependencies:

pip install -r requirements.txt

Set up the environment:

Create a .env file to store sensitive information like email credentials and database connection details.

Example .env format:

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-password
DATABASE_URL=sqlite:///coffee_shop.db

Initialize the database:

flask db init
flask db migrate
flask db upgrade

Run the application:

flask run

Configuration

Email Configuration

Update the email server details in your .env file or directly in the application code under the SMTP setup section.

Database Configuration

The application uses Flask-SQLAlchemy. By default, the database is set to use SQLite. You can change the database URI in the .env file.

Usage

Navigate to the running application in your browser.

Browse coffee products, place orders, and interact with the available features.

Use admin routes (if implemented) to manage the product catalog and orders.

Dependencies

Flask

Flask-SQLAlchemy

smtplib (Standard Library)

email (Standard Library)

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Contribution

Feel free to fork the repository and submit pull requests for improvements or additional features.

Support

For any issues, please create a GitHub issue or contact the maintainer directly.

Acknowledgments

Flask Documentation

SQLAlchemy Documentation
