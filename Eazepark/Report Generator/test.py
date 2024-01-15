import tkinter as tk
import mysql.connector as ms
from tkcalendar import Calendar
import os
# Global variables
a1y = None
formatted_date = ""
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    # Connect to the database
    db = ms.connect(
        host="localhost",
        user="root",
        password="dpsbn",
        database="cars"
    )
    cursor = db.cursor()

    # Execute a query to check if the username and password match in the 'pswd' table
    query = "SELECT * FROM pswd WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    if result:
        # If the login is successful, close the database connection
        db.close()

        # Close the login window
        root.destroy()

        # Proceed with report generation
        option_select()

    else:
        # If login fails, display an error message
        error_label.config(text="Invalid username or password")


def login_screen():
    global root, username_entry, password_entry, error_label

    # Create the main window
    root = tk.Tk()
    root.title("Login")

    # Create labels and entry fields for username and password
    username_label = tk.Label(root, text="Username:")
    username_entry = tk.Entry(root)
    password_label = tk.Label(root, text="Password:")
    password_entry = tk.Entry(root, show="*")

    # Create a login button that calls the validate_login function
    login_button = tk.Button(root, text="Login", command=validate_login)

    # Create a label to display error messages
    error_label = tk.Label(root, text="", fg="red")

    # Place widgets on the window using grid layout
    username_label.grid(row=0, column=0, padx=10, pady=5)
    username_entry.grid(row=0, column=1, padx=10, pady=5)
    password_label.grid(row=1, column=0, padx=10, pady=5)
    password_entry.grid(row=1, column=1, padx=10, pady=5)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)
    error_label.grid(row=3, column=0, columnspan=2)

    # Start the main event loop
    root.mainloop()

def option_select():
    global a1y
    import tkinter as tk
    a1y = None
    selected_option = None
    def set_option(option_index):
        global a1y, selected_option
        var.set(option_index)
        selected_option = options[option_index]
        if selected_option == "Daily":
            a1y = 1
        elif selected_option == "Monthly":
            a1y = 2
        elif selected_option == "Yearly":
            a1y = 3
        root.quit()  # Close the tkinter window
        root.destroy()  # Release associated resources
    root = tk.Tk()
    root.title("Select Report Generation Mode")
    root.geometry("300x150")  # Set the size to 300x150 pixels
    question_label = tk.Label(root, text="Select your option:")
    question_label.pack()
    options = ["Daily", "Monthly", "Yearly"]
    var = tk.IntVar()
    for i, option in enumerate(options):
        select_button = tk.Button(root, text=f"Generate {option}", command=lambda i=i: set_option(i))
        select_button.pack(anchor='w')
    root.mainloop()
def option_select_disp():
    global a2y, selected_option_disp
    import tkinter as tk
    a2y = None
    selected_option_disp = None
    
    def set_option_disp(option2_index):
        global a2y, selected_option_disp
        var_disp.set(option2_index)
        selected_option_disp = options2_disp[option2_index]
        if selected_option_disp == "Display Here":
            a2y = 1
        elif selected_option_disp == "Save Only":
            a2y = 2
        elif selected_option_disp == "Save And Open":
            a2y = 3
        root_disp.quit()  # Close the tkinter window
        root_disp.destroy()  # Release associated resources

    root_disp = tk.Tk()
    root_disp.title("Select Report Display Mode")
    root_disp.geometry("300x150")  # Set the size to 300x150 pixels
    question_label_disp = tk.Label(root_disp, text="Select your option:")
    question_label_disp.pack()
    options2_disp = ["Display Here", "Save Only", "Save And Open"]
    var_disp = tk.IntVar()
    for i, option in enumerate(options2_disp):
        select_button_disp = tk.Button(root_disp, text=f" {option}", command=lambda i=i: set_option_disp(i))
        select_button_disp.pack(anchor='w')
    root_disp.mainloop()
# Modify existing daily(), monthly(), yearly() functions

def daily():
    global formatted_date, nmfl
    formatted_date = ""

    def get_selected_date():
        global formatted_date
        selected_date = cal.get_date()
        formatted_date = format_date(selected_date)
        root.destroy()

        option_select_disp()
        if a2y == 1:
            # Display report in terminal (No CSV file)
            fetch_data_from_database()
        elif a2y == 2:
            # Save report to CSV file
            fetch_data_from_database()
        elif a2y == 3:
            # Save and open CSV file
            fetch_data_from_database()
            os.startfile(nmfl)

    def format_date(date_str):
        formatted_date = date_str.split('/')
        formatted_date = f"20{int(formatted_date[2]):02d}-{int(formatted_date[0]):02d}-{int(formatted_date[1]):02d}"
        return formatted_date

    def fetch_data_from_database():
        global formatted_date,nmfl  # Declare formatted_date as a global variable
        db = ms.connect(
            host="localhost",
            user="root",
            password="dpsbn",
            database="cars"
        )
        cursor = db.cursor()
        q1 = 'select car_number,money_paid from rep where timestamp=%s'
        cursor.execute(q1, (formatted_date,))
        a = cursor.fetchall()
        nmfl = 'F:/Report Generator/'+str(formatted_date) + '.csv'

        import csv
        with open(nmfl, 'w', newline='') as file: 
            wo = csv.writer(file)
            for i in a:
                wo.writerow(list(i))
            
            qqqq = 'SELECT COUNT(*) FROM rep WHERE timestamp=%s'
            cursor.execute(qqqq, (formatted_date,))
            total_count = cursor.fetchone()[0]
            wo.writerow([])  # Add an empty row for spacing
            wo.writerow(["Total Count:", total_count])

            qqqq = 'SELECT SUM(money_paid) FROM rep WHERE timestamp=%s'
            cursor.execute(qqqq, (formatted_date,))
            total_money_paid = cursor.fetchone()[0]
            wo.writerow(["Total Money Paid:", total_money_paid])

        db.close()

    root = tk.Tk()
    root.title("Calendar")
    cal = Calendar(root, selectmode="day")
    cal.pack(padx=20, pady=20)
    btn = tk.Button(root, text="Generate Report", command=get_selected_date)
    btn.pack(pady=10)
    root.mainloop()
    option_select_disp()
    if a2y == 1:
    # Display report in terminal (No CSV file)
        fetch_data_from_database()
    elif a2y == 2:
        # Save report to CSV file
        fetch_data_from_database()
    elif a2y == 3:
        # Save and open CSV file
        fetch_data_from_database()
        os.startfile(nmfl)
def monthly():
    global g,k, options1,nmfl
    import tkinter as tk
    def get_selected_values():
        global g, k, options1
        g = var1.get()
        k = var2.get()
        root.destroy()  # Close the window after getting the values
    
        g1=options1.index(g)+1
        g0='0'+str(g1)
        g1=g0
        fetch_data_from_database1()
        option_select_disp()
        if a2y == 1:
            # Display report in terminal (No CSV file)
            fetch_data_from_database1()
        elif a2y == 2:
            # Save report to CSV file
            fetch_data_from_database1()
        elif a2y == 3:
            # Save and open CSV file
            fetch_data_from_database1()
            os.startfile(nmfl)
    # Create main window
    root = tk.Tk()
    root.title("Monthly Report")
    # Set window size
    root.geometry("300x150")
    # Create variables to hold selected values
    g = None
    k = None
    # Create labels
    label1 = tk.Label(root, text="Select Month:")
    label2 = tk.Label(root, text="Enter Year:")
    # Create dropdown menu for month
    options1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    var1 = tk.StringVar(root)
    var1.set(options1[0])  # Set default value for dropdown 1
    dropdown1 = tk.OptionMenu(root, var1, *options1)
    # Create entry for year
    var2 = tk.StringVar(root)
    entry2 = tk.Entry(root, textvariable=var2)
    # Create button to get selected values
    button = tk.Button(root, text="Get Values", command=get_selected_values)
    # Pack widgets
    label1.pack()
    dropdown1.pack()
    label2.pack()
    entry2.pack()
    button.pack()
    # Start the main event loop
    root.mainloop()
    g1=options1.index(g)+1
    g0='0'+str(g1)
    g1=g0
    def fetch_data_from_database1():
        import mysql.connector as ms
        global formatted_date,nmfl  # Declare formatted_date as a global variable
        formatted_date = ''
        db = ms.connect(
            host="localhost",
            user="root",
            password="dpsbn",
            database="cars"
        )
        cursor = db.cursor()
        q1 = 'select car_number,money_paid from rep where timestamp like %s'
        formatted_date = str(k) + '-' + str(g1)
        formatted_date1 = formatted_date + '%'
        cursor.execute(q1, (formatted_date1,))
        a = cursor.fetchall()
        nmfl = 'F:/Report Generator/' + str(formatted_date) + '.csv'
        import csv
        with open(nmfl, 'w', newline='') as file:
            wo = csv.writer(file)
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
    fetch_data_from_database1()
    option_select_disp()
    if a2y == 1:
    # Display report in terminal (No CSV file)
        fetch_data_from_database1()
    elif a2y == 2:
        # Save report to CSV file
        fetch_data_from_database1()
    elif a2y == 3:
        # Save and open CSV file
        fetch_data_from_database1()
        os.startfile(nmfl)
def yearly():
    global k, options1,nmfl
    import tkinter as tk
    def get_selected_values():
        global k, options1
        k = var2.get()
        root.destroy()  # Close the window after getting the values

        fetch_data_from_database2()
        option_select_disp()
        if a2y == 1:
            # Display report in terminal (No CSV file)
            fetch_data_from_database2()
        elif a2y == 2:
            # Save report to CSV file
            fetch_data_from_database2()
        elif a2y == 3:
            # Save and open CSV file
            fetch_data_from_database2()
            os.startfile(nmfl)
    # Create main window
    root = tk.Tk()
    root.title("Yearly Report")
    # Set window size
    root.geometry("300x150")
    # Create variables to hold selected values
    k = None
    # Create labels
    label2 = tk.Label(root, text="Enter Year:")
    # Create dropdown menu for month
    var2 = tk.StringVar(root)
    entry2 = tk.Entry(root, textvariable=var2)
    # Create button to get selected values
    button = tk.Button(root, text="Get Values", command=get_selected_values)
    # Pack widgets
    label2.pack()
    entry2.pack()
    button.pack()
    # Start the main event loop
    root.mainloop()
    def fetch_data_from_database2():
        import mysql.connector as ms
        global formatted_date,nmfl  # Declare formatted_date as a global variable
        formatted_date = ''
        db = ms.connect(
            host="localhost",
            user="root",
            password="dpsbn",
            database="cars"
        )
        cursor = db.cursor()
        q1 = 'select car_number,money_paid from rep where timestamp like %s'
        formatted_date = str(k)
        formatted_date1 = formatted_date + '%'
        cursor.execute(q1, (formatted_date1,))
        a = cursor.fetchall()
        nmfl = 'F:/Report Generator/' + str(formatted_date) + '.csv'
        import csv
        with open(nmfl, 'w', newline='') as file:
            wo = csv.writer(file)
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
    option_select_disp()
    if a2y == 1:
    # Display report in terminal (No CSV file)
        fetch_data_from_database2()
    elif a2y == 2:
        # Save report to CSV file
        fetch_data_from_database2()
    elif a2y == 3:
        # Save and open CSV file
        fetch_data_from_database2()
        os.startfile(nmfl)
login_screen()
if a1y==1:
    daily()
elif a1y==2:
    monthly()
elif a1y==3:
    yearly()