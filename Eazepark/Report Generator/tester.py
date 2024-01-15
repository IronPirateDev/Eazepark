import tkinter as tk
from tkinter import ttk,messagebox
def login():
    def submit():
        global a, b
        a = entry1.get()
        b = entry2.get()
        root.quit() 
    root = tk.Tk()
    root.title("UserName")
    root.configure(bg='#333333')
    style = ttk.Style()
    style.configure('TLabel', foreground='white', background='#333333')
    style.configure('TButton', foreground='black', background='#555555')
    style.configure('TEntry', foreground='black', background='#555555')
    label1 = ttk.Label(root, text="Enter 'a':", font=("Helvetica", 12))
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = ttk.Entry(root, font=("Helvetica", 12))
    entry1.grid(row=0, column=1, padx=10, pady=10)
    label2 = ttk.Label(root, text="Enter 'b':", font=("Helvetica", 12))
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = ttk.Entry(root, font=("Helvetica", 12))
    entry2.grid(row=1, column=1, padx=10, pady=10)
    button = ttk.Button(root, text="Submit", command=submit)
    button.grid(row=2, column=0, columnspan=2, pady=10)
    style.configure('TButton', foreground='black', background='#555555')
    result_label = ttk.Label(root, text="", font=("Helvetica", 12))
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    root.mainloop()
login()
def mode_select():
    global a1y
    import tkinter as tk
    from tkinter import ttk

    a1y = None
    selected_option = None

    def set_option(option_index):
        global a1y, selected_option
        var.set(option_index)
        selected_option = options[option_index]
        if selected_option == "Delete A User":
            a1y = 1
        elif selected_option == "View Current Users":
            a1y = 2
        elif selected_option == "Add a user":
            a1y = 3
        elif selected_option == "Delete a Car":
            a1y = 4
        elif selected_option == "Add a car":
            a1y = 5        
        root.quit()  # Close the tkinter window
        root.destroy()  # Release associated resources

    root = tk.Tk()
    root.title("Select Admin Access Mode")
    root.geometry("300x500")  # Set the size to 300x150 pixels

    # Set dark mode
    root.configure(bg='#333333')
    style = ttk.Style()
    style.configure('TLabel', foreground='white', background='#333333')
    style.configure('TButton', foreground='black', background='black')  # Make buttons black
    style.configure('TButton', font=('Arial', 14))  # Increase font size

    question_label = ttk.Label(root, text='''Select your Task''', font=('Arial', 25))  # Increase font size
    question_label.pack(pady=10)  # Added padding

    options = ["Delete A User", "View Current Users", "Add a user", "Delete a Car", 'Add a car']
    var = tk.IntVar()
    for i, option in enumerate(options):
        select_button = ttk.Button(root, text=f"{option}", command=lambda i=i: set_option(i), width=50)
        select_button.pack(anchor='w')
    root.mainloop()
#mode_select()
#print(a1y)
import tkinter as tk
from tkinter import ttk
import mysql.connector as ms
def auth():
    def submit():
        global a, b
        a = entry1.get()
        root.quit()  # Quit the main loop

    top = tk.Toplevel()
    top.title("User Delete")
    top.configure(bg='#333333')
    style = ttk.Style()
    style.configure('TLabel', foreground='white', background='#333333')
    style.configure('TButton', foreground='black', background='#555555')
    style.configure('TEntry', foreground='black', background='#555555')
    label1 = ttk.Label(top, text="Enter User To Be Deleted:", font=("Helvetica", 12))
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = ttk.Entry(top, font=("Helvetica", 12))
    entry1.grid(row=0, column=1, padx=10, pady=10)
    button = ttk.Button(top, text="Submit", command=submit)
    button.grid(row=2, column=0, columnspan=2, pady=10)
    style.configure('TButton', foreground='black', background='#555555')
    result_label = ttk.Label(top, text="", font=("Helvetica", 12))
    result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    top.mainloop()  # Start the main loop

def conf():
    global con
    result = messagebox.askokcancel("Warning", f"Are you sure you want to delete the user {a}?")
    con = 1 if result else 0

con = None

root = tk.Tk()
root.title("Warning Box Example")

def delusr():
    db = ms.connect(
        host="localhost",
        user="root",
        password="dpsbn",
        database="cars"
    )
    cursor = db.cursor()
    auth()
    conf()
    db.close()

delete_button = tk.Button(root, text="Delete User", command=delusr)
delete_button.pack(pady=20)

root.mainloop()

# Check the value of 'con' after the main loop
print("Value of 'con':", con)
