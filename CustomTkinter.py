import tkinter as tk
from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import sqlite3

# Establish connection to SQLite database
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        confirmed INTEGER DEFAULT 0
    )
''')
conn.commit()


class UserPage(tk.Frame):
    def __init__(self, parent, controller, username):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = username

        label = tk.Label(self, text=f"Welcome, {self.username}!")
        label.pack(padx=10, pady=10)


class AdminPage(tk.Frame):
    def __init__(self, parent, controller, username):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = username

        label = tk.Label(self, text=f"Admin Dashboard\nLogged in as: {self.username}")
        label.pack(padx=10, pady=10)


class AuthenticationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Solution - Sign-In / Sign Up screen")
        self.root.geometry("600x400")

        # Load background image
        background_image = Image.open("C:/Users/sudhi/OneDrive/Desktop/PythonCustomTkinter/7197355.jpg")
        self.background_image = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Center window
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
            if user[4] == 1:  # Check if account is confirmed
                role = user[3]
                messagebox.showinfo("Success", f"Welcome, {username}! Role: {role}")
                # Redirect to user or admin screen based on role
                if role == "User":
                    self.root.destroy()
                    user_screen = tk.Tk()
                    user_page = UserPage(user_screen, self, username)
                    user_page.pack()
                    user_screen.mainloop()
                elif role == "Admin":
                    self.root.destroy()
                    admin_screen = tk.Tk()
                    admin_page = AdminPage(admin_screen, self, username)
                    admin_page.pack()
                    admin_screen.mainloop()
            else:
                messagebox.showerror("Error", "Account not confirmed. Please check your email.")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Error", "Username already taken. Please choose another.")
        else:
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, self.role_var.get()))
            conn.commit()
            messagebox.showinfo("Success", "Sign up successful!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthenticationApp(root)
    root.mainloop()

conn.close()
