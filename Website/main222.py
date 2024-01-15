from flask import Flask, render_template, request, redirect, send_from_directory
import mysql.connector as ms
from flask import Flask, session, flash
import os
from flask import flash, redirect, url_for
app = Flask(__name__, static_folder='templates/static')
app.secret_key='Eazepark'
from datetime import datetime
from flask import jsonify, request
now = datetime.now() 
current_time = now.strftime("%Y-%m-%d %H:%M:%S")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/')
def mdfycr():
    return render_template('modify_car.html')
@app.route('/process_option1', methods=['POST'])
def process_option1():
    option = request.json.get('option')  # Get the 'option' from the JSON payload
    if option == 'MONTHLY':
        print('mon')
    elif option == 'DAILY':
        print('dail')
    elif option == 'YEARLY':
        print('yearl')
    return jsonify({'message': 'Option received successfully'})
@app.route('/modify_car', methods=['POST', 'GET'])
def modify_car():
    if request.method == 'POST':
        car_number = request.form.get('car_number')
        btnpr = request.form.get('btnpr')
        if btnpr == 'delete_car':
            ab = ms.connect(host='localhost', username='root', password='dpsbn', database='cars')
            cursor = ab.cursor()
            nmm='SELECT * FROM car_no WHERE car_number=%s'
            cursor.execute(nmm,(car_number,))
            car_info = cursor.fetchall()
            if car_info:
                cursor.execute('DELETE FROM car_no WHERE car_number=%s', (car_number,))
                ab.commit()  
                message = f"Deleted car with number: {car_number}"
            else:
                message = f"Car with number {car_number} does not exist"
            cursor.close()
            ab.close()
        elif btnpr == 'add_car':
            ab = ms.connect(host='localhost', username='root', password='dpsbn', database='cars')
            cursor = ab.cursor()
            nmm='SELECT * FROM car_no WHERE car_number=%s'
            cursor.execute(nmm,(car_number,))
            car_info = cursor.fetchall()
            if car_info:
                message = f"Car with the Number {car_number} already Exists"
            else:
                message = f"Car with number {car_number} does not exist"
                cursor.execute('INSERT INTO car_no (car_number,timestamp) values (%s,%s)', (car_number,current_time))
                ab.commit()  
                message = f"Added car with number: {car_number}"
            cursor.close()
            ab.close()
        return render_template('modify_car.html', message=message)  # Pass the message to the template
    return mdfycr()
@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    global message
    message = None  # Initialize message

    added_username = None  # Initialize added_username

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_status = request.form.get('admin_status')
        
        db = ms.connect(host='localhost', user='root', passwd='dpsbn', database='cars')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM pswd')
        existing_users = cursor.fetchall()
        
        for user in existing_users:
            if username == user[1]:
                message = f"User {username} already exists"
                return render_template('add_user.html', added_username=None, message=message)  # Return early

        try:
            cursor.execute('INSERT INTO pswd (username, password, admin) VALUES (%s, %s, %s)',
                        (username, password, admin_status))
            db.commit()
            added_username = username
            message = f"Successfully added user: {username}"
        except ms.IntegrityError as e:
            cursor.execute('SELECT * FROM pswd')
            existing_users = cursor.fetchall()
            for i in existing_users:
                if username in i:
                    message = f"The user {username} already exists in the database."
                else:
                    pass

        cursor.close()
        db.close()
        
    return render_template('add_user.html', added_username=added_username, message=message)
@app.route('/remove_user', methods=['POST', 'GET'])
def remove_user():
    global message
    message = None  # Initialize message

    removed_username = None  # Initialize removed_username

    if request.method == 'POST':
        username = request.form.get('username').strip()  # Remove leading/trailing spaces
        
        db = ms.connect(host='localhost', user='root', passwd='dpsbn', database='cars')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM pswd')
        existing_users = cursor.fetchall()
        
        user_found = False
        for user in existing_users:
            if username == user[0]:  # Case-insensitive comparison
                user_found = True
                cursor.execute('DELETE FROM pswd WHERE username=%s', (user[0],))  # Use the actual username from the database
                db.commit()
                removed_username = user[0]
                message = f"Successfully removed user: {user[0]}"
                break
        
        if not user_found:
            message = f"The user {username} does not exist in the database."

        cursor.close()
        db.close()
        
    return render_template('remove_user.html', removed_username=removed_username, message=message)
@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    global message
    message = None  # Initialize message
    message_type = None  # Initialize message_type

    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        
        db = ms.connect(host='localhost', user='root', passwd='dpsbn', database='cars')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM pswd')
        existing_users = cursor.fetchall()
        
        user_found = False
        for user in existing_users:
            if username == user[0]:
                user_found = True
                cursor.execute('UPDATE pswd SET password=%s WHERE username=%s', (new_password, username))
                db.commit()
                message = f"Password reset successful for user: {username}"
                message_type = 'success'
                break
        
        if not user_found:
            message = f"The user {username} does not exist in the database."
            message_type = 'error'

        cursor.close()
        db.close()
        
    return render_template('reset_password.html', message=message, message_type=message_type)
@app.route('/entext')
def entext():
    return render_template('entext.html')
@app.route('/process_entext_option', methods=['POST'])
def process_entext_option():
    option = request.json.get('option')
    textbox_value = request.json.get('textboxValue')  # Get the value of the text box

    # Remove the access code checking from here

    if option == 'Entry':
        os.startfile(r'C:\\Users\\Lenovo\\Desktop\\Reader.lnk')
        message = 'Car Entry Program started successfully.'
    elif option == 'Exit':
        os.startfile(r'C:\\Users\\Lenovo\\Desktop\\Sign_Out.lnk')
        message = 'Car Exit Program started successfully.'
    elif option == 'StpEntry':
        import pygetwindow as gw
        def close_window_by_title(title):
            window = gw.getWindowsWithTitle(title)
            if window:
                window[0].close()
        close_window_by_title("Reader")
        close_window_by_title("Car Number Detection")
        close_window_by_title("Eazepark - Park With Eaze - Google Chrome")
        close_window_by_title("Thank you - Google Chrome")
        message = 'Car Entry Program stopped successfully.'
    elif option == 'StpExit':
        import pygetwindow as gw
        def close_window_by_title(title):
            window = gw.getWindowsWithTitle(title)
            if window:
                window[0].close()
        close_window_by_title("Sign_Out")
        close_window_by_title("Car Number Detection")
        close_window_by_title("Payment Confirmation - Aadithya - Microsoft Edge")
        close_window_by_title("Thank you - Google Chrome")
        message = 'Car Exit Program stopped successfully.'

    return jsonify({'message': message})

@app.route('/rep_home')
def rep_home():
    return render_template('rep_home.html')
def fetch_data_from_database(selected_date):
    result_list = []
    try:
        with ms.connect(
                host="localhost",
                user="root",
                password="dpsbn",
                database="cars"
        ) as db:
            cursor = db.cursor()
            q1 = 'SELECT car_number, money_paid FROM rep WHERE timestamp like %s'
            cursor.execute(q1, (selected_date,))
            data = cursor.fetchall()
            total_count_query = 'SELECT COUNT(*) FROM rep WHERE timestamp like %s'
            cursor.execute(total_count_query, (selected_date,))
            total_count = cursor.fetchone()[0]
            total_money_paid_query = 'SELECT SUM(money_paid) FROM rep WHERE timestamp like %s'
            cursor.execute(total_money_paid_query, (selected_date,))
            total_money_paid = cursor.fetchone()[0]
            result_list.append('<table border="1"><tr><th>Car Number</th><th>Money Paid</th></tr>')
            for row in data:
                result_list.append('<tr><td>{}</td><td>{}</td></tr>'.format(*row))
            result_list.append('<tr><td>Total Money Collected:</td><td>{}</td></tr>'.format(total_money_paid))
            result_list.append('<tr><td>Total Count of Vehicles:</td><td>{}</td></tr>'.format(total_count))
            result_list.append('</table>')
    except ms.Error as e:
        return [f"Error: {e}"]
    return result_list
def fetch_data_from_database1(formatted_date):
    import mysql.connector as ms
    db = ms.connect(
        host="localhost",
        user="root",
        password="dpsbn",
        database="cars"
    )
    cursor = db.cursor()
    q1 = 'select car_number,money_paid from rep where timestamp like %s'
    formatted_date1 = formatted_date
    cursor.execute(q1, (formatted_date1,))
    a = cursor.fetchall()
    if formatted_date1[(len(formatted_date1)-1)] == '%':
        date_for_file=formatted_date[:len(formatted_date)-1]
    else:
        date_for_file=formatted_date1
    print(date_for_file)
    nmfl = 'F:/Report Generator/' + str(date_for_file) + '.csv'
    import csv
    data_to_write = []
    for i in a:
        data_to_write.append(list(i))
    qqqq1 = 'SELECT COUNT(*) FROM rep WHERE timestamp like %s'
    cursor.execute(qqqq1, (formatted_date1,))
    total_count = cursor.fetchone()[0]
    data_to_write.extend([[], ["Total Count:", total_count]])
    qqqq2 = 'SELECT SUM(money_paid) FROM rep WHERE timestamp like %s'
    cursor.execute(qqqq2, (formatted_date1,))
    total_money_paid = cursor.fetchone()[0]
    data_to_write.append(["Total Money Paid:", total_money_paid])

    with open(nmfl, 'w', newline='') as file:
        wo = csv.writer(file)
        wo.writerows(data_to_write)

    db.close()
    return data_to_write
@app.route('/monthly/<selected_month>/<selected_year>')
def monthly(selected_month, selected_year):
    print(selected_month)
    print(selected_year)
    result = fetch_data_from_database(f'{selected_year}-{selected_month}%')
    print(result)
    return '\n'.join(result)
@app.route('/genmonthly/<selected_month>/<selected_year>')
def genmonthly(selected_month, selected_year):
    print(selected_month)
    print(selected_year)
    fetch_data_from_database1(f'{selected_year}-{selected_month}%')
    return 'Process Successful'
@app.route('/gendaily/<selected_date>')
def gendaily(selected_date):
    l1=''
    sl=selected_date
    l1=l1+(sl[6:])
    l1=l1+'-'
    l1=l1+(sl[3:5])
    l1=l1+'-'
    l1=l1+(sl[0:2])
    print(l1)
    fetch_data_from_database1(l1)
    return 'Process Successful'
@app.route('/genyearly/<selected_year_yearly>')
def genyearly(selected_year_yearly):
    print(selected_year_yearly)
    fetch_data_from_database1(f'{selected_year_yearly}%')
    return 'Process Successful'
@app.route('/daily/<selected_date>')
def daily(selected_date):
    l1=''
    sl=selected_date
    l1=l1+(sl[6:])
    l1=l1+'-'
    l1=l1+(sl[3:5])
    l1=l1+'-'
    l1=l1+(sl[0:2])
    print(l1)
    result = fetch_data_from_database(l1)
    print(result)
    return '\n'.join(result)
@app.route('/yearly/<selected_year_yearly>')
def yearly(selected_year_yearly):
    print(selected_year_yearly)
    result = fetch_data_from_database(f'{selected_year_yearly}%')
    print(result)
    return '\n'.join(result)
def fetch_data_from_database2():
    result_list = []
    try:
        with ms.connect(
            host="localhost",
            user="root",
            password="dpsbn",
            database="cars"
        ) as db:
            cursor = db.cursor()
            q1 = 'SELECT car_number FROM car_no'
            cursor.execute(q1)
            data = cursor.fetchall()
            total_count_query = 'SELECT COUNT(*) FROM car_no'
            cursor.execute(total_count_query)
            total_count = cursor.fetchone()[0]
            result_list.append('<table border="1"><tr><th>Car Number</th>')
            
            for row in data:
                if len(row) >= 1:  # Check if there is at least one element in the row
                    result_list.append('<tr><td>{}</td></tr>'.format(row[0]))
                else:
                    result_list.append('<tr><td>Invalid Data</td></tr>')
            
            result_list.append('<tr><td>Total Count of Vehicles:</td><td>{}</td></tr>'.format(total_count))
            result_list.append('</table>')
    except ms.Error as e:
        return [f"Error: {e}"]
    return result_list
@app.route('/vpp')
def live():
    result = fetch_data_from_database2()
    print(result)
    return '\n'.join(result)

def generate_report():
    global report_type, selected_date, selected_month, selected_year, selected_year_yearly
    import mysql.connector as ms
    db = ms.connect(host='localhost', user='root', password='dpsbn', database='cars')
    cursor = db.cursor()
    report_type = request.json.get('reportType')
    selected_date = request.json.get('selectedDate')
    selected_month = request.json.get('selectedMonth')
    selected_year = request.json.get('selectedYear')
    selected_year_yearly = request.json.get('selectedYearYearly')

    print(report_type, selected_date, selected_month, selected_year, selected_year_yearly)

    if report_type == 'view-mon':
        return monthly(selected_month, selected_year)
    elif report_type == 'view-dai':
        return daily(selected_date)
    elif report_type == 'view-yea':
        return yearly(selected_year_yearly)
    elif report_type == 'daily':
        return gendaily(selected_date)
    elif report_type == 'monthly':
        return genmonthly(selected_month,selected_year)
    elif report_type == 'yearly':
        return genyearly(selected_year_yearly)
    # Close the database connection
    cursor.close()
    db.close()

    return jsonify({'message': 'Report generation completed'})

@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/process_option', methods=['POST'])
@app.route('/mdfy')
def mdfy_mode():
    return redirect('/modify_car')
@app.route('/user_mod_page')
def user_mod_page():
    return render_template('user_mod.html')
@app.route('/add_user_page')
def add_user_page():
    return render_template('add_user.html')
@app.route('/process_option', methods=['POST'])
@app.route('/process_option', methods=['POST'])
def process_option():
    option = request.json.get('option')  # Get the 'option' from the JSON payload
    if option == 'MDFY':
        return redirect('/modify_car_page')
    elif option == 'ARU':
        return 'Hello World'
    return render_template('admin_home.html')  # Return the template with no specific option
# Inside the login() function
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    db = ms.connect(host='localhost', user='root', passwd='dpsbn', database='cars')
    cursor = db.cursor()
    cursor.execute('select * from pswd')
    a = cursor.fetchall()
    for i in a:
        if username == i[0] and password == i[1]:
            if i[2] == 'Yes':
                return render_template('admin_home.html', username=username)  # Pass the username to the template
            elif i[2] == 'No':
                return render_template('user_home.html', username=username)  # Pass the username to the template
    message = 'Invalid credentials. Please try again'
    return render_template('login.html', message=message)
@app.route('/reset_password_page/<username>', methods=['GET'])
def reset_password_page(username):
    return render_template('rese_pswd.html', username=username)
@app.route('/user_pswd_reset', methods=['POST'])
def user_pswd_reset():
    username = request.form.get('username')
    new_password = request.form.get('newPassword')
    confirm_password = request.form.get('confirmPassword')

    # Validate passwords
    if new_password != confirm_password:
        flash("Passwords do not match. Please try again.", 'error')
        return redirect(url_for('reset_password_page', username=username))

    # Update the password in the database
    db = ms.connect(host='localhost', user='root', passwd='dpsbn', database='cars')
    cursor = db.cursor()
    cursor.execute('UPDATE pswd SET password=%s WHERE username=%s', (new_password, username))
    db.commit()
    cursor.close()
    db.close()

    # Flash a success message
    flash(f"Password reset successful for user: {username}", 'success')

    # Redirect to the login page after a successful password reset
    return redirect('/login')
@app.route('/static/')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True,host='0.0.0.0')