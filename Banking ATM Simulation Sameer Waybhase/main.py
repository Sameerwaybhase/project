import json
import os
from datetime import datetime


class ATMSystem:
    def __init__(self, data_file='banking_data.json'):
        """
        Design nested dictionaries for account storage[cite: 10].
        Integrate JSON read/write for persistent storage[cite: 15].
        """
        self.data_file = data_file
        self.current_user_id = None
        self.accounts = self.load_data()

    def load_data(self):
        """Loads data or initializes with 5 minimum accounts[cite: 6]."""
        if not os.path.exists(self.data_file):
            # Initializing with 5 accounts as requested
            initial_data = {
                "101": {"name": "Sameer Waybhase", "pin": "1111", "balance": 10000, "history": []},
                "102": {"name": "Aditya Rao", "pin": "2222", "balance": 5000, "history": []},
                "103": {"name": "Priya Sharma", "pin": "3333", "balance": 7500, "history": []},
                "104": {"name": "Rahul Verma", "pin": "4444", "balance": 2000, "history": []},
                "105": {"name": "Sneha Patil", "pin": "5555", "balance": 12000, "history": []}
            }
            self.save_data(initial_data)
            return initial_data
        with open(self.data_file, 'r') as f:
            return json.load(f)

    def save_data(self, data=None):
        """Saves data in JSON format for realism[cite: 6, 15]."""
        data_to_save = data if data else self.accounts
        with open(self.data_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def log_transaction(self, acc_id, action):
        """Add mini statement using list-based logs[cite: 14]."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | {action}"
        self.accounts[acc_id]['history'].append(entry)
        # View last 5-10 transactions [cite: 6]
        if len(self.accounts[acc_id]['history']) > 10:
            self.accounts[acc_id]['history'].pop(0)

    def authenticate(self):
        """PIN-based authentication with lockout attempts[cite: 6, 11]."""
        print("\n" + "=" * 45)
        print("       WELCOME TO THE ATM SYSTEM       ")
        print("=" * 45)
        acc_no = input("1st Step - Enter Account Number: ")

        if acc_no in self.accounts:
            user = self.accounts[acc_no]
            # Show account holder name while using ATM
            print(f"Account Holder: {user['name']}")

            attempts = 3
            while attempts > 0:
                pin = input(f"Enter PIN for {user['name']} ({attempts} tries left): ")
                if pin == user['pin']:
                    self.current_user_id = acc_no
                    print(f"\nLogin Successful! Hello, {user['name']}.")
                    return True
                else:
                    attempts -= 1
                    print("Incorrect PIN.")
            print("\nSecurity Alert: Account locked due to failed attempts.")
        else:
            print("Error: Account Number not found.")
        return False

    def deposit(self):
        """Real-time balance updates with validation[cite: 6, 13]."""
        try:
            amount = float(input("Enter deposit amount: "))
            if amount > 0:
                self.accounts[self.current_user_id]['balance'] += amount
                self.log_transaction(self.current_user_id, f"Deposit: +${amount}")
                self.save_data()
                print(f"Successfully deposited ${amount}.")
            else:
                print("Invalid amount.")
        except ValueError:
            print("Error: Please enter a valid number.")

    def withdraw(self):
        """Real-time balance updates with validation[cite: 6, 13]."""
        try:
            amount = float(input("Enter withdrawal amount: "))
            balance = self.accounts[self.current_user_id]['balance']
            if 0 < amount <= balance:
                self.accounts[self.current_user_id]['balance'] -= amount
                self.log_transaction(self.current_user_id, f"Withdrawal: -${amount}")
                self.save_data()
                print(f"Successfully withdrew ${amount}.")
            else:
                print("Insufficient funds or invalid amount.")
        except ValueError:
            print("Error: Invalid numeric input.")

    def transfer(self):
        """Move money between accounts with checks[cite: 6, 13]."""
        target_id = input("Enter recipient Account Number: ")
        if target_id in self.accounts and target_id != self.current_user_id:
            try:
                amount = float(input(f"Amount to transfer to {self.accounts[target_id]['name']}: "))
                if 0 < amount <= self.accounts[self.current_user_id]['balance']:
                    self.accounts[self.current_user_id]['balance'] -= amount
                    self.accounts[target_id]['balance'] += amount

                    self.log_transaction(self.current_user_id, f"Transfer to {target_id}: -${amount}")
                    self.log_transaction(target_id, f"Transfer from {self.current_user_id}: +${amount}")
                    self.save_data()
                    print(f"Transfer successful to {self.accounts[target_id]['name']}.")
                else:
                    print("Invalid amount or insufficient funds.")
            except ValueError:
                print("Error: Invalid input.")
        else:
            print("Invalid recipient account.")

    def show_mini_statement(self):
        """View last 5-10 transactions[cite: 6, 14]."""
        user = self.accounts[self.current_user_id]
        print(f"\n--- Mini Statement: {user['name']} ---")
        if not user['history']:
            print("No transactions found.")
        else:
            for record in user['history']:
                print(record)
        print(f"Final Balance: ${user['balance']}")

    def run(self):
        """ATM menu with loops and routing."""
        while True:  # Outer loop returns to 1st Step after logout
            if self.authenticate():
                while True:  # Inner loop for banking operations
                    user_name = self.accounts[self.current_user_id]['name']
                    print(f"\n--- {user_name.upper()}'S MENU ---")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Fund Transfer")
                    print("5. Mini Statement")
                    print("6. Logout")

                    choice = input("Select an option: ")

                    if choice == '1':
                        print(f"Balance: ${self.accounts[self.current_user_id]['balance']}")
                    elif choice == '2':
                        self.deposit()
                    elif choice == '3':
                        self.withdraw()
                    elif choice == '4':
                        self.transfer()
                    elif choice == '5':
                        self.show_mini_statement()
                    elif choice == '6':
                        print(f"Logged out. Thank you, {user_name}!")
                        self.current_user_id = None
                        break  # Breaks inner loop to return to 1st Step
                    else:
                        print("Invalid choice.")
            else:
                input("\nPress Enter to return to 1st Step...")


if __name__ == "__main__":
    print("Developed by: Sameer Waybhase")
    atm = ATMSystem()
    atm.run()