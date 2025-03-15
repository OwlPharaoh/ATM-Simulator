
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, Listbox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# FilePaths
USER_DATA_FILE = "user data file.txt"
ADMIN_DATA_FILE = "sysadmin data.txt"

# Load user data
def load_user_data():
    users = {}
    try:
        with open(USER_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                username, password, balance = row
                users[username] = {'password': password, 'balance': float(balance)}
    except FileNotFoundError:
        pass
    return users

# Save user data
def save_user_data(users):
    with open(USER_DATA_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for username, data in users.items():
            writer.writerow([username, data['password'], data['balance']])

# Load admin data
def load_admin_data():
    admins = {}
    try:
        with open(ADMIN_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                username, password = row
                admins[username] = password
    except FileNotFoundError:
        pass
    return admins

class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('ATM Simulator')
        self.geometry('400x500')
        self.users = load_user_data()
        self.admins = load_admin_data()
        self.current_user = None
        self.attempts = 0
        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frame()
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(pady=15)

        ctk.CTkLabel(self.login_frame, text='Username:').grid(row=0, column=0, pady=10)
        self.username_entry = ctk.CTkEntry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=10)

        ctk.CTkLabel(self.login_frame, text='Password:').grid(row=1, column=0, pady=10)
        self.password_entry = ctk.CTkEntry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text='Login', command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.admin_button = ctk.CTkButton(self.login_frame, text='Admin Login', command=self.admin_login)
        self.admin_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.admin_button = ctk.CTkButton(self.login_frame, text='Exit Application', command=self.exit_app)
        self.admin_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username]['password'] == password:
            self.current_user = username
            self.create_user_frame()
        else:
            self.attempts += 1
            if self.attempts >= 3:
                messagebox.showerror('Error', 'Too many failed attempts. Exiting.')
                self.quit()
            else:
                messagebox.showerror('Error', 'Invalid credentials. Try again')

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.admins and self.admins[username] == password:
            self.create_admin_frame()
        else:
            messagebox.showerror('Error', 'Invalid Admin credentials.')

    def create_user_frame(self):
        self.clear_frame()
        self.user_frame = ctk.CTkFrame(self)
        self.user_frame.pack(pady=20)

        ctk.CTkLabel(self.user_frame, text=f'Welcome, {self.current_user}').pack(pady=10)
        ctk.CTkButton(self.user_frame, text='Balance Inquiry', command=self.balance_inquiry).pack(pady=5)
        ctk.CTkButton(self.user_frame, text='Deposit Funds', command=self.deposit_funds).pack(pady=5)
        ctk.CTkButton(self.user_frame, text='Change PIN', command=self.change_pin).pack(pady=5)
        ctk.CTkButton(self.user_frame, text='Exit to Main Menu', command=self.create_login_frame).pack(pady=5)

    def create_admin_frame(self):
        self.clear_frame()
        self.admin_frame = ctk.CTkFrame(self)
        self.admin_frame.pack(pady=20)

        ctk.CTkLabel(self.admin_frame, text='Admin Panel').pack(pady=10)
        ctk.CTkButton(self.admin_frame, text='Add User', command=self.add_user).pack(pady=5)
        ctk.CTkButton(self.admin_frame, text='Delete User', command=self.delete_user).pack(pady=5)
        ctk.CTkButton(self.admin_frame, text='Plot Account Balances', command=self.plot_account_balances).pack(pady=5)
        ctk.CTkButton(self.admin_frame, text='Exit to Main Menu', command=self.create_login_frame).pack(pady=5)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def balance_inquiry(self):
        balance = self.users[self.current_user]['balance']
        messagebox.showinfo('Balance Inquiry', f'Your current balance is ${balance:.2f}')

    def deposit_funds(self):
        def process_deposit():
            try:
                amount = float(deposit_entry.get())
                if amount > 0:
                    self.users[self.current_user]['balance'] += amount
                    save_user_data(self.users)
                    messagebox.showinfo('Deposit Successful', f'${amount:.2f} deposited successfully.')
                    deposit_window.destroy()
                else:
                    messagebox.showerror('Error', 'Enter a positive amount.')
            except ValueError:
                messagebox.showerror('Error', 'Invalid amount entered.')

        deposit_window = ctk.CTkToplevel(self)
        deposit_window.title('Deposit Funds')
        deposit_window.geometry('300x300')

        ctk.CTkLabel(deposit_window, text='Enter amount to deposit($): ').pack(pady=10)
        deposit_entry = ctk.CTkEntry(deposit_window)
        deposit_entry.pack(pady=5)

        ctk.CTkButton(deposit_window, text='Deposit', command=process_deposit).pack(pady=10)

    def change_pin(self):
        def process_pin_change():
            current_pin = current_pin_entry.get()
            new_pin = new_pin_entry.get()
            if current_pin == self.users[self.current_user]['password']:
                if new_pin:
                    self.users[self.current_user]['password'] = new_pin
                    save_user_data(self.users)
                    messagebox.showinfo('Success', 'PIN changed successfully.')
                    pin_change_window.destroy()
                else:
                    messagebox.showerror('Error', 'New PIN cannot be empty')
            else:
                messagebox.showerror('Error', 'Current PIN is incorrect.')
        
        pin_change_window = ctk.CTkToplevel(self)
        pin_change_window.title('Change PIN')
        pin_change_window.geometry('400x400')

        ctk.CTkLabel(pin_change_window, text='Change PIN:').pack(pady=10)
        current_pin_entry = ctk.CTkEntry(pin_change_window, show='*')
        current_pin_entry.pack(pady=5)

        ctk.CTkLabel(pin_change_window, text='New PIN:').pack(pady=10)
        new_pin_entry = ctk.CTkEntry(pin_change_window, show='*')
        new_pin_entry.pack(pady=5)

        ctk.CTkButton(pin_change_window, text='Change PIN', command=process_pin_change).pack(pady=20)

    def add_user(self):
        def process_add_user():
            username = username_entry.get()
            password = password_entry.get()
            try:
                initial_balance = float(balance_entry.get())
                if username and password:
                    if username not in self.users:
                        self.users[username] = {'password': password, 'balance': initial_balance}
                        save_user_data(self.users)
                        messagebox.showinfo('Success', f"User '{username}' added successfully.")
                        add_user_window.destroy()
                    else:
                        messagebox.showerror("Error", 'Username already exists.')
                else:
                    messagebox.showerror("Error", 'Username and password cannot be empty.')
            except ValueError:
                messagebox.showerror('Error', 'Invalid balance amount.')

        add_user_window = ctk.CTkToplevel(self)
        add_user_window.title('Add new user')
        add_user_window.geometry('400x400')

        ctk.CTkLabel(add_user_window, text='Username:').pack(pady=10)
        username_entry = ctk.CTkEntry(add_user_window)
        username_entry.pack(pady=5)

        ctk.CTkLabel(add_user_window, text='Password:').pack(pady=10)
        password_entry = ctk.CTkEntry(add_user_window, show='*')
        password_entry.pack(pady=5)

        ctk.CTkLabel(add_user_window, text='Initial Balance:').pack(pady=10)
        balance_entry = ctk.CTkEntry(add_user_window)
        balance_entry.pack(pady=5)

        ctk.CTkButton(add_user_window, text='Add User', command=process_add_user).pack(pady=20)

    def delete_user(self):
        def process_delete_user():
            selected_user = user_Listbox.get(user_Listbox.curselection())
            if selected_user:
                if messagebox.askyesno('Confirm Deletion', f"Are you sure you want to delete user '{selected_user}'?"):
                    del self.users[selected_user]
                    save_user_data(self.users)
                    messagebox.showinfo("Success", f"User '{selected_user}' deleted successfully")
                    refresh_user_list()  # Refresh the list after deletion

        def refresh_user_list():
            user_Listbox.delete(0, ctk.END)  # Clear the listbox
            for user in self.users.keys():  # Re-populate the listbox
                user_Listbox.insert(ctk.END, user)

        delete_user_window = ctk.CTkToplevel(self)
        delete_user_window.title('Delete User')
        delete_user_window.geometry('400x400')

        ctk.CTkLabel(delete_user_window, text='Select a user to delete: ').pack(pady=10)
        user_Listbox = Listbox(delete_user_window)
        user_Listbox.pack(pady=5)

        refresh_user_list()  # Initially populate the listbox

        ctk.CTkButton(delete_user_window, text='Delete User', command=process_delete_user).pack(pady=10)



    def plot_account_balances(self):
        balances = {user: data['balance'] for user, data in self.users.items()}
        if not balances:
            messagebox.showinfo('No Data', 'No user data available to plot.')
            return
        
        plot_window = ctk.CTkToplevel(self)
        plot_window.title('Account Balances')
        plot_window.geometry('600x600')

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(balances.keys(), balances.values(), color='skyblue')
        ax.set_xlabel('Users')
        ax.set_ylabel('Balance ($)')
        ax.set_title('Account Balances')
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        toolbar_frame = ctk.CTkFrame(plot_window)
        toolbar_frame.pack()
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

    def exit_app(self):
        self.quit()  # Properly exits the application

if __name__ == "__main__":
    root = ATMApp()
    root.mainloop()
    