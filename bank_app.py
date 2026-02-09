# =========================
# BANK APPLICATION (OOP)
# WITH ADMIN ROLE + TIMESTAMPS
# =========================

from datetime import datetime


# -------- Branch Class --------
class Branch:
    def __init__(self, branch_name, branch_code):
        self.branch_name = branch_name
        self.branch_code = branch_code

    def display_branch(self):
        print(f"Branch: {self.branch_name} | Code: {self.branch_code}")


# -------- Customer Class --------
class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name


# -------- Base Account Class --------
class Account:
    def __init__(self, account_number, customer, balance):
        self.account_number = account_number
        self.customer = customer
        self._balance = balance
        self.transactions = []

    # ⏱ Timestamped transaction helper
    def _add_transaction(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"{timestamp} | {message}")

    def deposit(self, amount):
        self._balance += amount
        self._add_transaction(f"Deposited ₹{amount}")
        print(f"₹{amount} deposited successfully.")

    def withdraw(self, amount):
        raise NotImplementedError

    def get_balance(self):
        return self._balance

    def calculate_interest(self):
        return 0

    def show_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
        else:
            print("\n--- Transaction History ---")
            for txn in self.transactions:
                print("-", txn)


# -------- Savings Account --------
class SavingsAccount(Account):
    MIN_BALANCE = 1000
    INTEREST_RATE = 0.04

    def withdraw(self, amount):
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            self._add_transaction(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self._add_transaction("Failed withdrawal (Min balance)")
            print("Withdrawal denied! Minimum balance required.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Current Account --------
class CurrentAccount(Account):
    MIN_BALANCE = 5000

    def withdraw(self, amount):
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            self._add_transaction(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self._add_transaction("Failed withdrawal (Insufficient balance)")
            print("Insufficient balance.")


# -------- Privilege Account --------
class PrivilegeAccount(Account):
    MIN_BALANCE = 10000
    INTEREST_RATE = 0.06

    def withdraw(self, amount):
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            self._add_transaction(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self._add_transaction("Failed withdrawal (Privilege min balance)")
            print("Minimum balance not maintained.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Bank Application --------
class BankApp:
    def __init__(self):
        self.branch = Branch("Zenshastra Main Branch", "ZS001")

        # Admin credentials (POC)
        self.admin_id = "admin"
        self.admin_password = "admin123"

        # Customer database
        self.customer_db = {
            "101": {"name": "Marushka Dsilva", "password": "maru123"},
            "102": {"name": "Aditi Sharma", "password": "aditi123"},
            "103": {"name": "Rahul Verma", "password": "rahul123"}
        }

        self.accounts = {}
        self.start()

    # -------- Start Menu --------
    def start(self):
        print("\n===== Welcome to Bank Application =====")
        self.branch.display_branch()

        while True:
            print("\n1. Admin Login")
            print("2. Customer Login")

            choice = input("Choose option: ")

            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.customer_login()
            else:
                print("Invalid choice.")

    # -------- Admin Login --------
    def admin_login(self):
        print("\n--- Admin Login ---")
        aid = input("Admin ID: ")
        pwd = input("Password: ")

        if aid == self.admin_id and pwd == self.admin_password:
            print("Admin login successful.")
            self.admin_menu()
        else:
            print("Invalid admin credentials.")

    # -------- Admin Menu --------
    def admin_menu(self):
        while True:
            print("\n--- ADMIN MENU ---")
            print("1. Create New Customer")
            print("2. Reset Customer Password")
            print("3. View All Accounts")
            print("4. Logout")

            option = input("Choose option: ")

            if option == "1":
                self.create_customer()
            elif option == "2":
                self.reset_customer_password()
            elif option == "3":
                self.view_all_accounts()
            elif option == "4":
                print("Admin logged out.")
                break
            else:
                print("Invalid option.")

    # -------- Admin Functions --------
    def create_customer(self):
        cid = input("Enter new Customer ID: ")

        if cid in self.customer_db:
            print("Customer already exists.")
            return

        name = input("Enter customer name: ")
        password = input("Set password: ")

        self.customer_db[cid] = {
            "name": name,
            "password": password
        }

        print("New customer created successfully.")

    def reset_customer_password(self):
        cid = input("Enter Customer ID: ")

        if cid not in self.customer_db:
            print("Customer not found.")
            return

        new_password = input("Enter new password: ")
        self.customer_db[cid]["password"] = new_password

        print("Password reset successfully.")

    def view_all_accounts(self):
        if not self.accounts:
            print("No accounts available.")
            return

        print("\n--- All Customer Accounts ---")
        for cid, acc in self.accounts.items():
            print(
                f"Customer ID: {cid} | "
                f"Name: {acc.customer.name} | "
                f"Balance: ₹{acc.get_balance()}"
            )

    # -------- Customer Login --------
    def customer_login(self):
        while True:
            print("\n--- Customer Login ---")
            cid = input("Customer ID: ")
            pwd = input("Password: ")

            if cid in self.customer_db and self.customer_db[cid]["password"] == pwd:
                customer = Customer(cid, self.customer_db[cid]["name"])
                print(f"\nLogin successful! Welcome {customer.name}")
                self.load_account(customer)
                break
            else:
                print("Invalid credentials. Try again.")

    # -------- Load Account --------
    def load_account(self, customer):
        if customer.customer_id not in self.accounts:
            print("\nSelect Account Type:")
            print("1. Savings")
            print("2. Current")
            print("3. Privilege")

            choice = input("Enter choice: ")

            if choice == "1":
                self.accounts[customer.customer_id] = SavingsAccount(1001, customer, 5000)
            elif choice == "2":
                self.accounts[customer.customer_id] = CurrentAccount(1002, customer, 10000)
            elif choice == "3":
                self.accounts[customer.customer_id] = PrivilegeAccount(1003, customer, 20000)
            else:
                print("Invalid choice.")
                return

        self.account = self.accounts[customer.customer_id]
        self.menu()

    # -------- Input Validation --------
    def get_valid_amount(self):
        while True:
            try:
                amount = float(input("Amount: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    return amount
            except ValueError:
                print("Please enter a valid numeric amount.")

    # -------- Customer Menu --------
    def menu(self):
        while True:
            print("\n------ MENU ------")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Balance")
            print("4. Interest")
            print("5. Transactions")
            print("6. Logout")

            option = input("Choose option (1-6): ").strip()

            if option not in {"1", "2", "3", "4", "5", "6"}:
                print("Please select a valid option.")
                continue

            if option == "1":
                amount = self.get_valid_amount()
                self.account.deposit(amount)

            elif option == "2":
                amount = self.get_valid_amount()
                self.account.withdraw(amount)

            elif option == "3":
                print(f"Balance: ₹{self.account.get_balance()}")

            elif option == "4":
                print(f"Interest: ₹{self.account.calculate_interest()}")

            elif option == "5":
                self.account.show_transactions()

            elif option == "6":
                print("Logged out.")
                break


# -------- Entry Point --------
if __name__ == "__main__":
    BankApp()
