from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = 'jBVKBekljgbnwLJKNBVKJLBWJKGBWB'  # Replace with a strong, random string
# Configuring the database

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'instance/menu.db')}"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model for the cart
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<CartItem {self.item_name}>"

# define payment database table
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(120), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)


# Define the MenuItem model
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

class CoffeeBlend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

# Initialize the database
with app.app_context():
    db.create_all()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Email configuration
EMAIL_ADDRESS = "Your email address"  # Your email address
EMAIL_PASSWORD = "Your email password"  # Your email password
SMTP_SERVER = "smtp.gmail.com"  # Example for Gmail
SMTP_PORT = 587
TO_EMAIL_ADDRESS="Your email address"

# Route for the contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('Name')
        email = request.form.get('Email')
        phone = request.form.get('Phone')
        message = request.form.get('Message')

        if not name or not email or not message:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('contact'))

        # Compose email
        subject = "New Contact Form Submission"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL_ADDRESS
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Secure the connection
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("There was an error sending your message. Please try again later.", "error")

        return redirect(url_for('contact'))

    return render_template('contact.html')

# Route for the gallery page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the services page
@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/menu', methods=['GET'])
def menu():
    # Get the current category from the query parameters, default to 'flavors'
    category = request.args.get('category', 'flavors')

    # Fetch available items based on the selected category
    if category == 'flavors':
        available_items = MenuItem.query.filter_by(available=True).all()
    elif category == 'coffee blends':
        available_items = CoffeeBlend.query.filter_by(available=True).all()
    else:
        available_items = []  # Return an empty list for invalid categories

    # Fetch cart items and calculate the total price
    cart_items = CartItem.query.all()
    total_price = sum(item.price * item.servings for item in cart_items)

    # Render the menu template with the current category and relevant data
    return render_template(
        'menu.html',
        cart_items=cart_items,
        total_price=total_price,
        items=available_items,
        category=category
    )


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Get item details from the form submission
    item_name = request.form['item_name']
    servings = int(request.form['servings'])
    price = float(request.form['price'])

    # Get the current category from the form
    current_category = request.form.get('current_category', 'flavors')

    # Add the new item to the cart
    new_item = CartItem(item_name=item_name, servings=servings, price=price)
    db.session.add(new_item)
    db.session.commit()

    # Redirect back to the menu with the same category
    return redirect(url_for('menu', category=current_category))


@app.route('/pay', methods=['POST'])
def pay():
    db.session.query(CartItem).delete()  # Clear the cart after payment
    db.session.commit()
    return redirect(url_for('menu'))

if __name__ == '__main__':
    app.run(debug=True)
