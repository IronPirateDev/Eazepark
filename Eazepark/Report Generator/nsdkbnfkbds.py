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
option_select()