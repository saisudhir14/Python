# Car Rental Solution

## Overview

This project is a part of my academic curriculum. I have developed this project using Python,tkinter(GUI). It is all about renting cars based on available options. I have provided 2 roles which are Admin and User.

## Requirements

To use this project or if you would like to run this locally in your system, you would need:
- A system with Python 3 installed
- Any IDE which supports python. I used VS Code!

## Installation

Here's how you can get the program running:
1. Download the program files from this repository..
2. Make sure you have Python 3 installed on your computer.
3. Open the program file using Python and run the file based on your IDE settings or options available.

## Database Setup

This project keeps track of users,cars, rental information in a tablular format, I' using SQLite database here in this case.
1. **Users**: Keeps track of who's using the program.
2. **Cars**: Stores information about the cars available for rent.
3. **Rentals**: Records who rented which car and when.

## How you would navigate?

1. Try to run the program.
2. Sign up as a user / create an account if you're new, or log in if you've used it before.
3. Look at the cars available for rent and choose one you like.
4. Pick the dates you want to rent the car.
5. Confirm your rental.

## User Window Class

### Initialization
- The `UserWindow` class creates a window where users can interact with the car rental system.
- It sets up the window size and initializes some variables.

### Buttons
- Several buttons are added to the window for different actions like updating the password, viewing available cars, searching for cars, and making reservations.
- Each button is linked to a specific function that gets called when the button is clicked.

### Making a Reservation
- When the "Make Reservation" button is clicked, a new window pops up where users can enter details like the car ID and rental dates.
- After entering the details, users can confirm the reservation, and the information gets stored in the database.

### Viewing Available Cars
- Clicking the "View Available Cars" button opens a new window displaying a list of cars available for rent.
- The list is fetched from the database and shown in a table format.

### Updating Password
- Clicking the "Update Password" button opens a window where users can change their passwords.
- After entering the new password and confirming it, the password gets updated in the database.

### Viewing Rental History
- Clicking the "View Rental History" button opens a window showing the user's past rental transactions.
- The rental history is retrieved from the database and displayed in a table format.

### Logging Out
- Clicking the "Logout" button closes the user window and brings back the main window of the application.

--------


### AuthenticationApp Class:
