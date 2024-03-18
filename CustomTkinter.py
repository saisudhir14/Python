import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
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

        # Adding widgets for managing cars (e.g., add, edit, delete buttons)
        add_car_button = tk.Button(manage_cars_window, text="Add Car", command=self.add_car)
        add_car_button.pack(pady=10)

        edit_car_button = tk.Button(manage_cars_window, text="Edit Car", command=self.edit_car)
        edit_car_button.pack(pady=10)

        delete_car_button = tk.Button(manage_cars_window, text="Delete Car", command=self.delete_car)
        delete_car_button.pack(pady=10)

    def add_car(self):
        # Implement functionality to add a new car
        pass

    def edit_car(self):
        # Implement functionality to edit an existing car
        pass

    def delete_car(self):
        # Implement functionality to delete a car
        pass

    def view_rentals(self):
        # Open a new window to view rentals
        view_rentals_window = tk.Toplevel(self.root)
        view_rentals_window.title("View Rentals")
        view_rentals_window.geometry("600x400")

        # Add widgets to display rental information (e.g., table or listbox)
        rentals_label = tk.Label(view_rentals_window, text="List of Rentals", font=("Arial", 14))
        rentals_label.pack(pady=10)

        # Retrieve rental information from the database and display it
        # Example: You can fetch rental data from the database and display it in a table or listbox
        # Example:
        # rentals_listbox = tk.Listbox(view_rentals_window)
        # rentals_listbox.pack(fill=tk.BOTH, expand=True)
        # for rental in rental_data:
        #     rentals_listbox.insert(tk.END, rental)

    def logout(self):
        self.root.destroy()  # Close admin window
        app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)


# class AdminWindow:
#     def __init__(self, root, admin_username):
#         self.root = root
#         self.root.title(f"Car Rental System - Admin: {admin_username}")
#         self.root.geometry("600x400")

#         # Admin functionalities (e.g., manage cars, view rentals)
#         self.manage_cars_button = tk.Button(self.root, text="Manage Cars", command=self.manage_cars)
#         self.manage_cars_button.pack(pady=20)

#         self.view_rentals_button = tk.Button(self.root, text="View Rentals", command=self.view_rentals)
#         self.view_rentals_button.pack(pady=20)

#         # Logout button
#         logout_button = tk.Button(self.root, text="Logout", command=self.logout)
#         logout_button.pack(pady=20)

#     def manage_cars(self):
#         # I need to Implement manage cars functionality
#         pass

#     def view_rentals(self):
#         # I need to implement view rentals functionality
#         pass

#     def logout(self):
#         self.root.destroy()  # Close admin window
#         app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)

#     def logout(self):
#         self.root.destroy()  # Close admin window
#         app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)


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
        self.password_entry.place(x=x_center + 50, y=y_center)

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
            if role == 'admin':
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
