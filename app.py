from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------- MODELS ----------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bank_details = db.relationship('BankDetail', backref='user', uselist=False)
    products = db.relationship('Product', backref='farmer', lazy=True)

class BankDetail(db.Model):
    __tablename__ = 'bank_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    account_holder_name = db.Column(db.String(100))
    account_number = db.Column(db.String(50))
    ifsc_code = db.Column(db.String(20))

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(10,2))
    quantity = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- ROUTES ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form.get('phone', '')  # Make phone optional
        email = request.form['email']
        role = request.form['role']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        user = User(name=name, phone=phone, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login to access dashboard.", "warning")
        return redirect(url_for('login'))

    role = session['role']
    if role == 'farmer':
        products = Product.query.filter_by(user_id=session['user_id']).all()
        return render_template('farmer_dashboard.html', user=session['user_name'], products=products)
    else:
        products = Product.query.all()
        return render_template('customer.html', user=session['user_name'], products=products)

@app.route('/product', methods=['GET', 'POST'])
def product_form():
    if 'user_id' not in session:
        flash("Please login to add products.", "warning")
        return redirect(url_for('login'))
    
    # Only farmers can add products
    if session.get('role') != 'farmer':
        flash("Only farmers can add products.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            category = request.form.get('category', '')
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            description = request.form.get('description', '')
            image_url = request.form.get('image_url', '')

            # Validate required fields
            if not name or not price or not quantity:
                flash("Please fill in all required fields!", "danger")
                return render_template('product_form.html')

            product = Product(
                user_id=session['user_id'], 
                name=name, 
                category=category,
                price=float(price), 
                quantity=int(quantity), 
                description=description,
                image_url=image_url
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding product: {str(e)}", "danger")
            return render_template('product_form.html')
    
    return render_template('product_form.html')

@app.route('/bank', methods=['GET', 'POST'])
def bank_details():
    if 'user_id' not in session:
        flash("Please login to access bank details.", "warning")
        return redirect(url_for('login'))

    bank = BankDetail.query.filter_by(user_id=session['user_id']).first()

    if request.method == 'POST':
        name = request.form['account_holder_name']
        number = request.form['account_number']
        ifsc = request.form['ifsc_code']

        if bank:
            bank.account_holder_name = name
            bank.account_number = number
            bank.ifsc_code = ifsc
        else:
            bank = BankDetail(user_id=session['user_id'], account_holder_name=name,
                              account_number=number, ifsc_code=ifsc)
            db.session.add(bank)

        db.session.commit()
        flash("Bank details saved successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('bank_details.html', bank=bank)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

# ---------- MAIN ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if not existing
    app.run(debug=True)