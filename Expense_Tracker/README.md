
# 💰 Expense Tracker Web App

A powerful and user-friendly **Flask-based** web application designed to help individuals efficiently manage and track their personal expenses. Log, categorize, filter, visualize, and export your financial data with ease.

## 📊 Technologies Used

- **Python**, **Flask**, **Flask-SQLAlchemy**
- **Chart.js** for data visualization
- **HTML, CSS (Dark Mode)** for frontend
- **xhtml2pdf** for PDF report generation
- **SQLite** as the database

---

## 🚀 Features

### 🔐 User Authentication
- Secure login and registration system to manage personal expense data.

### 💼 Expense Management
- Add new expenses (date, category, amount, description).
- View all expenses in a sortable table.
- Delete specific expenses.

### 🧠 Flexible Filtering
- Filter by month.
- Filter by custom date range (start to end date).

### 📈 Financial Overview
- Real-time total expense calculation.
- Interactive bar chart by category using **Chart.js**.

### 📦 Data Export
- Download expenses as **CSV**.
- Generate and download a printable **PDF** report.

### 🖌️ Modern UI
- Sleek, responsive **dark mode** interface.
- Flash messages for success/error feedback.

---

## 🖼️ User Interface

> The app features a clean and responsive dark-mode UI built with HTML and CSS.

📌 **NOTE**: Replace this section with a screenshot of your dashboard once deployed.

---

## 📂 Project Structure

```
expense_tracker_webapp/
├── app.py                  # Main Flask application logic
├── static/
│   └── css/
│       └── style.css       # Custom dark-mode styling
├── templates/
│   ├── index.html          # Dashboard page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   └── pdf_template.html   # For generating PDF reports
└── expenses.db             # SQLite database file
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd expense_tracker_webapp
```

> Or download and extract the ZIP, then navigate into the project folder.

### 2. Install Dependencies

Make sure Python (3.7+) is installed:

```bash
pip install flask flask_sqlalchemy xhtml2pdf
```

### 3. Initialize the Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...
>>> exit()
```

> This creates the `expenses.db` file. Run this only once unless the DB is deleted.

### 4. Run the App

```bash
python app.py
```

Visit in your browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📸 Sample Outputs

### Login Page
- Simple form with **username/password** and buttons in dark mode.

### Dashboard (Post-login)
- Add Expense form
- Filter options
- Expense table
- Total amount
- Download buttons
- Bar chart

### Add Expense Example

**Input:**
- Date: 2024-06-18  
- Category: Food  
- Amount: 550.00  
- Description: Dinner with friends

**Output:**
- Flash: "Expense successfully added!"
- New row in table.

### Filter by Month: June
**Input:** Month = 6  
**Output:** Only June expenses shown. Total updates.

### Filter by Date Range
**Input:** 2024-06-01 to 2024-06-15  
**Output:** Table and totals filtered accordingly.

---

## 🧑‍💻 Authors

**Lead Developer**: S. Hasika - https://github.com/hasi21-sun

**Team Members**:   P. UdayKiran - https://github.com/Udaykiranpotteppagari , 
                    N. Kalyan reddy - https://github.com/Kalyanreddy0421 ,
                    P N. Uday Kiran - https://github.com/uday777660


---

## 📜 License

This project is licensed under the **MIT License**.  
Free to use, share, and modify with proper attribution.
