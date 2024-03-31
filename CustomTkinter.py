import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

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
        year INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'available'  -- Add the status column with a default value
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
    def __init__(self, root, username, user_id):
        self.root = root
        self.username = username
        self.user_id = user_id  
        self.root.geometry("400x300")
        
        # User details label
        user_details_label = tk.Label(
            self.root, text=f"Welcome, {self.username}!", font=("Arial", 16)
        )
        user_details_label.pack(pady=20)

        # Logout button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

        # Buttons for user functionalities
        view_available_cars_button = tk.Button(self.root, text="View Available Cars", command=self.view_available_cars)
        view_available_cars_button.pack(pady=10)

        
        #Redirecting this reservation to view_rentals function -
        
        #make_reservation_button = tk.Button(self.root, text="Make Reservation", command=self.make_reservation)
        #make_reservation_button.pack(pady=10)

        view_my_rentals_button = tk.Button(self.root, text="View My Rentals", command=self.view_my_rentals)
        view_my_rentals_button.pack(pady=10)

        cancel_reservation_button = tk.Button(self.root, text="Cancel Reservation", command=self.cancel_reservation)
        cancel_reservation_button.pack(pady=10)

        update_profile_button = tk.Button(self.root, text="Update Profile", command=self.update_profile)
        update_profile_button.pack(pady=10)

        view_rental_history_button = tk.Button(self.root, text="View Rental History", command=self.view_rental_history)
        view_rental_history_button.pack(pady=10)

        search_cars_button = tk.Button(self.root, text="Search Cars", command=self.search_cars)
        search_cars_button.pack(pady=10)

        filter_cars_button = tk.Button(self.root, text="Filter Cars", command=self.filter_cars)
        filter_cars_button.pack(pady=10)

    def logout(self):
        self.root.destroy()  # Close user window
        app.root.deiconify()  # Unhide main window (assuming 'app' is an instance)

    def open_make_reservation_window(self, parent, tree, selected_car_id):
        # Close the parent window
        parent.destroy()

        # Open a new window to make a reservation
        make_reservation_window = tk.Toplevel(self.root)
        make_reservation_window.title("Make Reservation")
        make_reservation_window.geometry("400x400")

        # Add labels and entry fields for reservation details
        rental_date_label = tk.Label(make_reservation_window, text="Rental Date (YYYY-MM-DD):")
        rental_date_label.pack(pady=5)
        rental_date_entry = tk.Entry(make_reservation_window)
        rental_date_entry.pack(pady=5)

        return_date_label = tk.Label(make_reservation_window, text="Return Date (YYYY-MM-DD):")
        return_date_label.pack(pady=5)
        return_date_entry = tk.Entry(make_reservation_window)
        return_date_entry.pack(pady=5)

        # Button to confirm reservation
        confirm_button = tk.Button(make_reservation_window, text="Confirm Reservation",
                                    command=lambda: self.make_reservation(selected_car_id, rental_date_entry.get(), return_date_entry.get()))
        confirm_button.pack(pady=10)



    def view_available_cars(self):
        # Open a new window to display available cars
        available_cars_window = tk.Toplevel(self.root)
        available_cars_window.title("Available Cars")
        available_cars_window.geometry("600x400")

        # Add a Treeview widget to display available cars
        tree = ttk.Treeview(available_cars_window)
        tree["columns"] = ("make", "model", "year", "status")
        tree.heading("#0", text="ID")
        tree.heading("make", text="Make")
        tree.heading("model", text="Model")
        tree.heading("year", text="Year")
        tree.heading("status", text="Status")

        # Fetch available car data from the database
        cursor.execute("SELECT * FROM cars WHERE status='available'")
        available_cars = cursor.fetchall()

        # Insert available car data into the Treeview
        for car in available_cars:
            tree.insert("", tk.END, text=car[0], values=(car[1], car[2], car[3], car[4]))

        tree.pack(expand=True, fill=tk.BOTH)

        # Button to make reservation for selected car
        make_reservation_button = tk.Button(available_cars_window, text="Make Reservation",
                                            command=lambda: self.open_make_reservation_window(available_cars_window, tree, car[0]))
        make_reservation_button.pack(pady=10)

    def make_reservation(self, car_id, rental_date, return_date):
        # Insert reservation into the database
        cursor.execute("INSERT INTO rentals (car_id, user_id, rental_date, return_date) VALUES (?, ?, ?, ?)",
                       (car_id, self.user_id, rental_date, return_date))
        conn.commit()
        messagebox.showinfo("Success", "Reservation made successfully!")


    def confirm_reservation(self, car_id, rental_date, return_date):
        # Validate input
        if not rental_date or not return_date:
            messagebox.showerror("Error", "Please enter both rental date and return date")
            return

        # Check if return date is after rental date
        if rental_date >= return_date:
            messagebox.showerror("Error", "Return date must be after rental date")
            return

        # Make reservation in the database
        self.make_reservation_in_database(car_id, rental_date, return_date)


    def view_my_rentals(self):
        # Open a new window to display user's rentals
        my_rentals_window = tk.Toplevel(self.root)
        my_rentals_window.title("My Rentals")
        my_rentals_window.geometry("600x400")

        # Add a Treeview widget to display user's rentals
        tree = ttk.Treeview(my_rentals_window)
        tree["columns"] = ("car_id", "rental_date", "return_date")
        tree.heading("#0", text="ID")
        tree.heading("car_id", text="Car ID")
        tree.heading("rental_date", text="Rental Date")
        tree.heading("return_date", text="Return Date")

        # Fetch user's rental data from the database
        cursor.execute("SELECT * FROM rentals WHERE user_id=?", (self.user_id,))
        user_rentals = cursor.fetchall()

        # Insert user's rental data into the Treeview
        for rental in user_rentals:
            tree.insert("", tk.END, text=rental[0], values=(rental[1], rental[3], rental[4]))

        tree.pack(expand=True, fill=tk.BOTH)
    
    def cancel_reservation(self):
        # Functionality to cancel a reservation
        pass

    def cancel_selected_reservation(self, tree):
        # Get the selected item from the Treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a reservation to cancel")
            return

        # Get the reservation ID from the selected item
        reservation_id = tree.item(selected_item, "text")

        # Confirm cancellation
        confirm_cancel = messagebox.askyesno("Confirmation", "Are you sure you want to cancel this reservation?")
        if confirm_cancel:
            # Remove the reservation from the database
            cursor.execute("DELETE FROM rentals WHERE id=?", (reservation_id,))
            conn.commit()
            messagebox.showinfo("Success", "Reservation canceled successfully")
            # Remove the selected item from the Treeview
            tree.delete(selected_item)


    def update_profile(self):
        # Open a new window to update user's profile
        update_profile_window = tk.Toplevel(self.root)
        update_profile_window.title("Update Profile")
        update_profile_window.geometry("400x300")

        # Add labels and entry fields for updating profile
        username_label = tk.Label(update_profile_window, text="New Username:")
        username_label.pack(pady=5)
        new_username_entry = tk.Entry(update_profile_window)
        new_username_entry.pack(pady=5)

        password_label = tk.Label(update_profile_window, text="New Password:")
        password_label.pack(pady=5)
        new_password_entry = tk.Entry(update_profile_window, show="*")
        new_password_entry.pack(pady=5)

        # Button to update the profile in the database
        update_button = tk.Button(update_profile_window, text="Update Profile", 
                                  command=lambda: self.update_profile_in_database(new_username_entry.get(), new_password_entry.get()))
        update_button.pack(pady=10)

    def update_profile_in_database(self, new_username, new_password):
        # Update the user's profile in the database
        if new_username or new_password:
            cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (new_username, new_password, self.user_id))
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully")
        else:
            messagebox.showerror("Error", "Please enter new username or password")

    def view_rental_history(self):
        # Open a new window to view user's rental history
        rental_history_window = tk.Toplevel(self.root)
        rental_history_window.title("Rental History")
        rental_history_window.geometry("600x400")

        # Add a Treeview widget to display rental history
        tree = ttk.Treeview(rental_history_window)
        tree["columns"] = ("car_id", "rental_date", "return_date")
        tree.heading("#0", text="ID")
        tree.heading("car_id", text="Car ID")
        tree.heading("rental_date", text="Rental Date")
        tree.heading("return_date", text="Return Date")

        # Fetch user's rental history from the database
        cursor.execute("SELECT * FROM rentals WHERE user_id=?", (self.user_id,))
        rental_history = cursor.fetchall()

        # Insert user's rental history into the Treeview
        for rental in rental_history:
            tree.insert("", tk.END, text=rental[0], values=(rental[1], rental[3], rental[4]))

        tree.pack(expand=True, fill=tk.BOTH)


    def search_cars(self):
        # Open a new window to search for cars
        search_cars_window = tk.Toplevel(self.root)
        search_cars_window.title("Search Cars")
        search_cars_window.geometry("400x200")

        # Add label and entry field for search query
        search_label = tk.Label(search_cars_window, text="Search:")
        search_label.pack(pady=5)
        search_entry = tk.Entry(search_cars_window)
        search_entry.pack(pady=5)

        # Button to perform search
        search_button = tk.Button(search_cars_window, text="Search", command=lambda: self.perform_car_search(search_entry.get()))
        search_button.pack(pady=10)

    def perform_car_search(self, search_query):
        # Implement functionality to search for cars based on the query
        cursor.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ? OR year LIKE ?", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        search_results = cursor.fetchall()

        # Display search results in a new window
        self.display_search_results(search_results)

    def display_search_results(self, search_results):
        # Open a new window to display search results
        search_results_window = tk.Toplevel(self.root)
        search_results_window.title("Search Results")
        search_results_window.geometry("600x400")

        # Add a Treeview widget to display search results
        tree = ttk.Treeview(search_results_window)
        tree["columns"] = ("make", "model", "year")
        tree.heading("#0", text="ID")
        tree.heading("make", text="Make")
        tree.heading("model", text="Model")
        tree.heading("year", text="Year")

        # Insert search results into the Treeview
        for car in search_results:
            tree.insert("", tk.END, text=car[0], values=(car[1], car[2], car[3]))

        tree.pack(expand=True, fill=tk.BOTH)


    def filter_cars(self):
        # Open a new window to filter cars
        filter_cars_window = tk.Toplevel(self.root)
        filter_cars_window.title("Filter Cars")
        filter_cars_window.geometry("400x400")

        # Add labels and entry fields for filter criteria
        make_label = tk.Label(filter_cars_window, text="Make:")
        make_label.pack(pady=5)
        make_entry = tk.Entry(filter_cars_window)
        make_entry.pack(pady=5)

        model_label = tk.Label(filter_cars_window, text="Model:")
        model_label.pack(pady=5)
        model_entry = tk.Entry(filter_cars_window)
        model_entry.pack(pady=5)

        year_label = tk.Label(filter_cars_window, text="Year:")
        year_label.pack(pady=5)
        year_entry = tk.Entry(filter_cars_window)
        year_entry.pack(pady=5)

        # Button to apply the filter
        apply_filter_button = tk.Button(filter_cars_window, text="Apply Filter", 
                                        command=lambda: self.apply_filter(make_entry.get(), model_entry.get(), year_entry.get()))
        apply_filter_button.pack(pady=10)

    def apply_filter(self, make, model, year):
        # Implement functionality to apply filter to cars
        cursor.execute("SELECT * FROM cars WHERE make=? AND model=? AND year=?", (make, model, year))
        filtered_cars = cursor.fetchall()

        # Display filtered cars in a new window
        self.display_filtered_cars(filtered_cars)

    def display_filtered_cars(self, filtered_cars):
        # Open a new window to display filtered cars
        filtered_cars_window = tk.Toplevel(self.root)
        filtered_cars_window.title("Filtered Cars")
        filtered_cars_window.geometry("600x400")

        # Add a Treeview widget to display filtered cars
        tree = ttk.Treeview(filtered_cars_window)
        tree["columns"] = ("make", "model", "year")
        tree.heading("#0", text="ID")
        tree.heading("make", text="Make")
        tree.heading("model", text="Model")
        tree.heading("year", text="Year")

        # Insert filtered cars into the Treeview
        for car in filtered_cars:
            tree.insert("", tk.END, text=car[0], values=(car[1], car[2], car[3]))

        tree.pack(expand=True, fill=tk.BOTH)

    # Insert filtered car data into the Treeview
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
                self.root.withdraw()
                admin_window = tk.Toplevel()
                admin_app = AdminWindow(admin_window, username)
            else:
                self.root.withdraw()
                user_window = tk.Toplevel()
                user_app = UserWindow(user_window, username, user[0])  # Pass user_id here
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
