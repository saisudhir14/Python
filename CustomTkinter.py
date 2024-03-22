import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        rental_date TEXT NOT NULL,
        return_date TEXT
    )
''')

conn.commit()

class UserWindow:
    def __init__(self, root, username):
        self.root = root
        self.root.title(f"Car Rental System - User: {username}")
        self.root.geometry("400x300")

        # User details label
        user_details_label = tk.Label(
            self.root, text=f"Welcome, {username}!", font=("Arial", 16)
        )
        user_details_label.pack(pady=20)

        # Logout button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def logout(self):
        self.root.destroy()  # Close user window
        app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)

class AdminWindow:
    def __init__(self, root, admin_username):
        self.root = root
        self.root.title(f"Car Rental System - Admin: {admin_username}")
        self.root.geometry("600x400")

        # Admin functionalities (e.g., manage cars, view rentals)
        self.manage_cars_button = tk.Button(self.root, text="Manage Cars", command=self.manage_cars)
        self.manage_cars_button.pack(pady=20)

        self.view_rentals_button = tk.Button(self.root, text="View Rentals", command=self.view_rentals)
        self.view_rentals_button.pack(pady=20)

        # Logout button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def manage_cars(self):
        # Open a new window for managing cars
        manage_cars_window = tk.Toplevel(self.root)
        manage_cars_window.title("Manage Cars")
        manage_cars_window.geometry("400x300")

        # Add widgets for managing cars (e.g., add, edit, delete buttons)
        add_car_button = tk.Button(manage_cars_window, text="Add Car", command=self.add_car)
        add_car_button.pack(pady=10)

        edit_car_button = tk.Button(manage_cars_window, text="Edit Car", command=self.edit_car)
        edit_car_button.pack(pady=10)

        delete_car_button = tk.Button(manage_cars_window, text="Delete Car", command=self.delete_car)
        delete_car_button.pack(pady=10)

        display_car_button = tk.Button(manage_cars_window, text="Display Cars", command=self.display_cars)
        display_car_button.pack(pady=10)

    def add_car(self):
        # Open a new window to add a car
        add_car_window = tk.Toplevel(self.root)
        add_car_window.title("Add Car")
        add_car_window.geometry("400x300")

        # Add labels and entry fields for car details
        make_label = tk.Label(add_car_window, text="Make:")
        make_label.pack(pady=5)
        make_entry = tk.Entry(add_car_window)
        make_entry.pack(pady=5)

        model_label = tk.Label(add_car_window, text="Model:")
        model_label.pack(pady=5)
        model_entry = tk.Entry(add_car_window)
        model_entry.pack(pady=5)

        year_label = tk.Label(add_car_window, text="Year:")
        year_label.pack(pady=5)
        year_entry = tk.Entry(add_car_window)
        year_entry.pack(pady=5)

        # Button to add the car to the database
        add_button = tk.Button(add_car_window, text="Add", command=lambda: self.add_car_to_database(make_entry.get(), model_entry.get(), year_entry.get()))
        add_button.pack(pady=10)


    def add_car_to_database(self, make, model, year):
        # Implement functionality to add a car to the database
        if make and model and year:
            cursor.execute("INSERT INTO cars (make, model, year) VALUES (?, ?, ?)", (make, model, year))
            conn.commit()
            messagebox.showinfo("Success", "Car added successfully")
        else:
            messagebox.showerror("Error", "Please fill in all the fields")

    def edit_car(self):
        # Open a new window to edit a car
        edit_car_window = tk.Toplevel(self.root)
        edit_car_window.title("Edit Car")
        edit_car_window.geometry("400x300")

        # Add labels and entry fields for car details
        car_id_label = tk.Label(edit_car_window, text="Car ID:")
        car_id_label.pack(pady=5)
        car_id_entry = tk.Entry(edit_car_window)
        car_id_entry.pack(pady=5)

        make_label = tk.Label(edit_car_window, text="Make:")
        make_label.pack(pady=5)
        make_entry = tk.Entry(edit_car_window)
        make_entry.pack(pady=5)

        model_label = tk.Label(edit_car_window, text="Model:")
        model_label.pack(pady=5)
        model_entry = tk.Entry(edit_car_window)
        model_entry.pack(pady=5)

        year_label = tk.Label(edit_car_window, text="Year:")
        year_label.pack(pady=5)
        year_entry = tk.Entry(edit_car_window)
        year_entry.pack(pady=5)

        # Button to save the changes to the database
        save_button = tk.Button(edit_car_window, text="Save Changes", command=lambda: self.save_car_changes(car_id_entry.get(), make_entry.get(), model_entry.get(), year_entry.get()))
        save_button.pack(pady=10)

    def save_car_changes(self, car_id, make, model, year):
        # Implement functionality to save the edited car details to the database
        if car_id and make and model and year:
            cursor.execute("UPDATE cars SET make=?, model=?, year=? WHERE id=?", (make, model, year, car_id))
            conn.commit()
            messagebox.showinfo("Success", "Car details updated successfully")
        else:
            messagebox.showerror("Error", "Please fill in all the fields")

    def delete_car(self):
        # Open a new window to delete a car
        delete_car_window = tk.Toplevel(self.root)
        delete_car_window.title("Delete Car")
        delete_car_window.geometry("300x150")

        # Add label and entry field for car ID
        id_label = tk.Label(delete_car_window, text="Car ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(delete_car_window)
        id_entry.pack(pady=5)

        # Button to delete the car from the database
        delete_button = tk.Button(delete_car_window, text="Delete", command=lambda: self.delete_car_from_database(id_entry.get()))
        delete_button.pack(pady=10)

    def delete_car_from_database(self, car_id):
        # Implement functionality to delete a car from the database
        if car_id:
            cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
            conn.commit()
            messagebox.showinfo("Success", "Car deleted successfully")
        else:
            messagebox.showerror("Error", "Please enter a car ID")

    def display_cars(self):
        # Open a new window to display cars
        display_cars_window = tk.Toplevel(self.root)
        display_cars_window.title("Display Cars")
        display_cars_window.geometry("600x600")

        # Add a Treeview widget to display car information
        tree = ttk.Treeview(display_cars_window)
        tree["columns"] = ("make", "model", "year")
        tree.heading("#0", text="ID")
        tree.heading("make", text="Make")
        tree.heading("model", text="Model")
        tree.heading("year", text="Year")

        # Fetch car data from the database
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()

        # Insert car data into the Treeview
        for car in cars:
            tree.insert("", tk.END, text=car[0], values=(car[1], car[2], car[3]))

        tree.pack(expand=True, fill=tk.BOTH)

    def view_rentals(self):
        # Open a new window to view rentals
        view_rentals_window = tk.Toplevel(self.root)
        view_rentals_window.title("View Rentals")
        view_rentals_window.geometry("600x400")

        # Add a Treeview widget to display rental information
        tree = ttk.Treeview(view_rentals_window)
        tree["columns"] = ("car_id", "user_id", "rental_date", "return_date")
        tree.heading("#0", text="ID")
        tree.heading("car_id", text="Car ID")
        tree.heading("user_id", text="User ID")
        tree.heading("rental_date", text="Rental Date")
        tree.heading("return_date", text="Return Date")

        # Fetch rental data from the database
        cursor.execute("SELECT * FROM rentals")
        rentals = cursor.fetchall()

        # Insert rental data into the Treeview
        for rental in rentals:
            tree.insert("", tk.END, text=rental[0], values=(rental[1], rental[2], rental[3], rental[4]))

        tree.pack(expand=True, fill=tk.BOTH)

    def logout(self):
        self.root.destroy()  # Close admin window
        app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)

class AuthenticationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Solution - Sign-In / Sign Up screen")
        self.root.geometry("600x400")

        # Load the image using Pillow
        background_image = Image.open("C:/Users/sudhi/OneDrive/Desktop/PythonCustomTkinter/7197355.jpg")
        self.background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Calculate the center of the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_center = (screen_width - 600) / 2
        y_center = (screen_height - 400) / 2

        # Create labels and entry fields
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.place(x=x_center - 100, y=y_center - 50)

        self.username_entry = tk.Entry(root)
        self.username_entry.place(x=x_center + 50, y=y_center - 50)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.place(x=x_center - 100, y=y_center)

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.place(x=x_center  + 50, y=y_center)

        self.role_label = tk.Label(root, text="Role:")
        self.role_label.place(x=x_center - 100, y=y_center + 50)

        self.role_var = tk.StringVar()
        self.role_var.set("User")
        self.role_combobox = tk.OptionMenu(root, self.role_var, "User", "Admin")
        self.role_combobox.place(x=x_center + 50, y=y_center + 50)

        # Create buttons
        self.signin_button = tk.Button(root, text="Sign In", command=self.signin)
        self.signin_button.place(x=x_center, y=y_center + 100)

        self.signup_button = tk.Button(root, text="Sign Up", command=self.signup)
        self.signup_button.place(x=x_center + 100, y=y_center + 100)

    def signin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Check if the user exists in the database
        cursor.execute('SELECT * FROM users WHERE username=? AND password=? AND role=?', (username, password, self.role_var.get()))
        user = cursor.fetchone()

        if user:
            role = user[3]
            if role == 'Admin':
                self.root.withdraw()  # Hide the authentication window
                admin_window = tk.Toplevel()  # Create a new window for admin
                admin_app = AdminWindow(admin_window, username)
            else:
                self.root.withdraw()  # Hide the authentication window
                user_window = tk.Toplevel()  # Create a new window for user
                user_app = UserWindow(user_window, username)
        else:
            messagebox.showerror("Error", "Invalid username, password, or role")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Check if username already exists
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            # Insert new user into the database
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User created successfully. You can now sign in.")

# Create the main application window
root = tk.Tk()
app = AuthenticationApp(root)
root.mainloop()
