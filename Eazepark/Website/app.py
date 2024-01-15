from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key_here'

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dpsbn",
    database="cars"
)

cursor = db.cursor()

def logged_in_user_is_admin():
    logged_in_user = session.get('username')
    if logged_in_user and logged_in_user == 'admin':
        return True
    return False

@app.route('/delete_employee_page')
def delete_employee_page():
    return render_template('delete_employee.html')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM pswd WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        if username == "admin" and password == "admin":
            session['username'] = username  # Store username in session
            return "Admin login successful!"
        else:
            session['username'] = username  # Store username in session
            return "Login successful!"
    else:
        return "Invalid credentials. Please try again."

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        username = request.form['username']

        if logged_in_user_is_admin():
            return render_template('confirm_delete.html', employee_name=username)
        else:
            return "You do not have permission to perform this action."

@app.route('/confirm_delete', methods=['POST'])
def confirm_delete():
    username = request.form['employee_name']

    query = "DELETE FROM pswd WHERE username=%s"
    cursor.execute(query, (username,))
    db.commit()

    return f"Employee '{username}' has been deleted successfully."

if __name__ == '__main__':
    app.run(debug=True)
