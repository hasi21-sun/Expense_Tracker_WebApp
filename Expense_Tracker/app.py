from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date # Import date
from functools import wraps
import csv
from io import BytesIO
from xhtml2pdf import pisa

app = Flask(__name__)
app.secret_key = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error') # Added category
            return redirect('/register')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully.', 'success') # Added category
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user_id'] = user.id
            return redirect('/')
        flash('Invalid credentials.', 'error') # Added category
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    categories = ['Food', 'Rent', 'Travel', 'Utilities', 'Others']
    
    expenses_query = Expense.query.filter_by(user_id=session['user_id'])

    start_date_str = None
    end_date_str = None
    
    if request.method == 'POST' and 'month' in request.form and request.form['month']:
        month = request.form['month']
        expenses_query = expenses_query.filter(db.extract('month', Expense.date) == int(month))
    else: # Handle GET request for date range filters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                expenses_query = expenses_query.filter(Expense.date >= start_date)
            except ValueError:
                flash('Invalid start date format.', 'error')
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                expenses_query = expenses_query.filter(Expense.date <= end_date)
            except ValueError:
                flash('Invalid end date format.', 'error')

    expenses = expenses_query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    chart_data = {cat: sum(e.amount for e in expenses if e.category == cat) for cat in categories}
    
    return render_template('index.html', expenses=expenses, categories=categories, total=total, chart_data=chart_data,
                           start_date=start_date_str, end_date=end_date_str)


@app.route('/add', methods=['POST'])
@login_required
def add_expense():
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']
    new_expense = Expense(date=date, category=category, amount=amount, description=description, user_id=session['user_id'])
    db.session.add(new_expense)
    db.session.commit()
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense and expense.user_id == session['user_id']:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    else:
        flash('Expense not found or unauthorized.', 'error')
    return redirect(url_for('index'))

@app.route('/download_csv')
@login_required
def download_csv():
    expenses = Expense.query.filter_by(user_id=session['user_id']).order_by(Expense.date.desc()).all()
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    for e in expenses:
        writer.writerow([e.date, e.category, e.amount, e.description])
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='expenses.csv')

@app.route('/download_pdf')
@login_required
def download_pdf():
    expenses = Expense.query.filter_by(user_id=session['user_id']).order_by(Expense.date.desc()).all()
    rendered = render_template('pdf_template.html', expenses=expenses)
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)
    return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name='expenses.pdf')

if __name__ == '__main__':
    app.run(debug=True)