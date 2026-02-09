# =========================
# BANK APPLICATION (OOP)
# FIXED VERSION
# =========================

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

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.transactions.append(f"Deposited ₹{amount}")
            print(f"₹{amount} deposited successfully.")
        else:
            print("Invalid deposit amount.")

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
            self.transactions.append(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self.transactions.append("Failed withdrawal (Min balance)")
            print("Withdrawal denied! Minimum balance required.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Current Account --------
class CurrentAccount(Account):
    MIN_BALANCE = 5000

    def withdraw(self, amount):
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            self.transactions.append(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self.transactions.append("Failed withdrawal (Insufficient balance)")
            print("Insufficient balance.")


# -------- Privilege Account --------
class PrivilegeAccount(Account):
    MIN_BALANCE = 10000
    INTEREST_RATE = 0.06

    def withdraw(self, amount):
        if self._balance - amount >= self.MIN_BALANCE:
            self._balance -= amount
            self.transactions.append(f"Withdrawn ₹{amount}")
            print(f"₹{amount} withdrawn successfully.")
        else:
            self.transactions.append("Failed withdrawal (Privilege min balance)")
            print("Minimum balance not maintained.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Bank Application --------
class BankApp:
    def __init__(self):
        self.branch = Branch("Zenshastra Main Branch", "ZS001")

        self.customer_db = {
            "101": {"name": "Marushka Dsilva", "password": "maru123"},
            "102": {"name": "Aditi Sharma", "password": "aditi123"},
            "103": {"name": "Rahul Verma", "password": "rahul123"}
        }

        self.accounts = {}  # customer_id -> account
        self.start()

    def start(self):
        print("\n===== Welcome to Bank Application =====")
        self.branch.display_branch()
        self.login()

    def login(self):
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

    def menu(self):
        while True:
            print("\n------ MENU ------")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Balance")
            print("4. Interest")
            print("5. Transactions")
            print("6. Logout")

            option = input("Choose option: ")

            if option == "1":
                self.account.deposit(float(input("Amount: ")))

            elif option == "2":
                self.account.withdraw(float(input("Amount: ")))

            elif option == "3":
                print(f"Balance: ₹{self.account.get_balance()}")

            elif option == "4":
                print(f"Interest: ₹{self.account.calculate_interest()}")

            elif option == "5":
                self.account.show_transactions()

            elif option == "6":
                print("Logged out.")
                self.login()
                break

            else:
                print("Invalid option!")


# -------- Entry Point --------
if __name__ == "__main__":
    BankApp()
