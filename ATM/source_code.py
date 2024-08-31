import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY,
            pin INTEGER,
            balance REAL
        )
    ''')
    # Insert a sample account
    c.execute('INSERT OR IGNORE INTO account (id, pin, balance) VALUES (1, 1234, 5000)')
    conn.commit()
    conn.close()

# Function to handle user login
def login():
    pin = int(pin_entry.get())
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('SELECT balance FROM account WHERE pin = ?', (pin,))
    result = c.fetchone()
    conn.close()

    if result:
        global balance  # Declare global here
        balance = result[0]
        show_main_menu()
    else:
        messagebox.showerror("Error", "Wrong PIN, please try again")

# Function to show the main menu
def show_main_menu():
    main_menu_frame.pack()
    login_frame.pack_forget()

# Function to check balance
def check_balance():
    messagebox.showinfo("Balance", f"Your current balance is ${balance}")

# Function to withdraw money
def withdraw():
    global balance  # Declare global here
    amount = float(withdraw_entry.get())
    if amount <= balance:
        balance -= amount
        conn = sqlite3.connect('atm.db')
        c = conn.cursor()
        c.execute('UPDATE account SET balance = ? WHERE pin = ?', (balance, 1234))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"${amount} has been withdrawn. New balance: ${balance}")
    else:
        messagebox.showerror("Error", "Insufficient funds")

# Function to deposit money
def deposit():
    global balance  # Declare global here
    amount = float(deposit_entry.get())
    balance += amount
    conn = sqlite3.connect('atm.db')
    c = conn.cursor()
    c.execute('UPDATE account SET balance = ? WHERE pin = ?', (balance, 1234))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"${amount} has been deposited. New balance: ${balance}")

# Initialize database
init_db()

# Create the main window
root = tk.Tk()
root.title("ATM Simulation")

# Create frames
login_frame = tk.Frame(root)
main_menu_frame = tk.Frame(root)

# Create login frame widgets
tk.Label(login_frame, text="Enter your ATM PIN:").pack(pady=10)
pin_entry = tk.Entry(login_frame)
pin_entry.pack(pady=5)
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
login_frame.pack(pady=20)

# Create main menu frame widgets
tk.Button(main_menu_frame, text="Check Balance", command=check_balance).pack(pady=5)
tk.Label(main_menu_frame, text="Withdraw Amount:").pack(pady=5)
withdraw_entry = tk.Entry(main_menu_frame)
withdraw_entry.pack(pady=5)
tk.Button(main_menu_frame, text="Withdraw", command=withdraw).pack(pady=5)
tk.Label(main_menu_frame, text="Deposit Amount:").pack(pady=5)
deposit_entry = tk.Entry(main_menu_frame)
deposit_entry.pack(pady=5)
tk.Button(main_menu_frame, text="Deposit", command=deposit).pack(pady=5)
tk.Button(main_menu_frame, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
