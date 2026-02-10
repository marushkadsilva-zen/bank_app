import threading
import time
from multiprocessing import Process, Value, Lock
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
    def __init__(self, account_number, customer=None, balance=0):
        self.account_number = account_number
        self.customer = customer
        self._balance = balance
        self.transactions = []
        self.lock = threading.Lock()

    def _add_transaction(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"{timestamp} | {message}")

    def deposit(self, amount):
        time.sleep(0.1)  # simulate I/O delay
        with self.lock:
            self._balance += amount
            self._add_transaction(f"Deposited ₹{amount}")
            print(
                f"[{threading.current_thread().name}] "
                f"Deposited ₹{amount} | Balance ₹{self._balance}"
            )

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
        with self.lock:
            if self._balance - amount >= self.MIN_BALANCE:
                self._balance -= amount
                self._add_transaction(f"Withdrawn ₹{amount}")
                print(f"[{threading.current_thread().name}] Withdrawn ₹{amount}")
            else:
                print("Withdrawal denied! Minimum balance required.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Privilege Account --------
class PrivilegeAccount(Account):
    MIN_BALANCE = 10000
    INTEREST_RATE = 0.06

    def withdraw(self, amount):
        with self.lock:
            if self._balance - amount >= self.MIN_BALANCE:
                self._balance -= amount
                self._add_transaction(f"Withdrawn ₹{amount}")
                print(
                    f"[{threading.current_thread().name}] "
                    f"₹{amount} withdrawn successfully."
                )
            else:
                self._add_transaction("Failed withdrawal (Privilege min balance)")
                print("Minimum balance not maintained.")

    def calculate_interest(self):
        return self._balance * self.INTEREST_RATE


# -------- Multiprocessing Helper --------
def process_deposit(balance, lock, amount):
    result = 0
    for i in range(2_000_000):
        result += i * i

    with lock:
        balance.value += amount
        print(f"[Process] Deposited ₹{amount} | Balance ₹{balance.value}")


# -------- Bank Application --------
class BankApp:
    def __init__(self):
        self.branch = Branch("Zenshastra Main Branch", "ZS001")
        self.admin_id = "admin"
        self.admin_password = "admin123"

        self.customer_db = {
            "101": {"name": "Marushka Dsilva", "password": "maru123"},
            "102": {"name": "Aditi Sharma", "password": "aditi123"},
            "103": {"name": "Rahul Verma", "password": "rahul123"},
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
            print("3. Exit")

            choice = input("Choose option: ")

            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.customer_login()
            elif choice == "3":
                print("Thank you for using our banking system!")
                break
            else:
                print("Invalid choice.")

    # -------- Admin Login --------
    def admin_login(self):
        aid = input("Admin ID: ")
        pwd = input("Password: ")

        if aid == self.admin_id and pwd == self.admin_password:
            self.admin_menu()
        else:
            print("Invalid credentials.")

    # -------- Admin Menu --------
    def admin_menu(self):
        while True:
            print("\n--- ADMIN MENU ---")
            print("1. View Accounts")
            print("2. Non-Threaded Demo")
            print("3. Threaded Demo")
            print("4. Non-Multiprocessing Demo")
            print("5. Multiprocessing Demo")
            print("6. Logout")

            option = input("Choose option: ")

            if option == "1":
                self.view_all_accounts()
            elif option == "2":
                self.non_threaded_demo()
            elif option == "3":
                self.threaded_demo_shared_account()
            elif option == "4":
                self.non_multiprocessing_demo()
            elif option == "5":
                self.multiprocessing_demo()
            elif option == "6":
                break

    # -------- Demos --------
    def non_threaded_demo(self):
        acc = Account(1, balance=1000)
        start = time.time()

        for _ in range(5):
            acc.deposit(500)

        print("Final Balance:", acc.get_balance())
        print("Execution Time:", round(time.time() - start, 3), "seconds")

    def threaded_demo_shared_account(self):
        acc = Account(1, balance=1000)
        threads = []
        start = time.time()

        for i in range(5):
            t = threading.Thread(
                target=acc.deposit,
                args=(500,),
                name=f"Thread-{i + 1}",
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("Final Balance:", acc.get_balance())
        print("Execution Time:", round(time.time() - start, 3), "seconds")

    def non_multiprocessing_demo(self):
        balance = Value("i", 1000)
        lock = Lock()
        start = time.time()

        for _ in range(5):
            process_deposit(balance, lock, 500)

        print("Final Balance:", balance.value)
        print("Execution Time:", round(time.time() - start, 3), "seconds")

    def multiprocessing_demo(self):
        balance = Value("i", 1000)
        lock = Lock()
        processes = []
        start = time.time()

        for _ in range(5):
            p = Process(
                target=process_deposit,
                args=(balance, lock, 500),
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print("Final Balance:", balance.value)
        print("Execution Time:", round(time.time() - start, 3), "seconds")

    # -------- View Accounts --------
    def view_all_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for cid, acc in self.accounts.items():
                print(f"{cid} | {acc.customer.name} | ₹{acc.get_balance()}")

    # -------- Customer Login --------
    def customer_login(self):
        cid = input("Customer ID: ")
        pwd = input("Password: ")

        if cid in self.customer_db and self.customer_db[cid]["password"] == pwd:
            customer = Customer(cid, self.customer_db[cid]["name"])
            self.load_account(customer)
        else:
            print("Invalid credentials.")

    # -------- Load Account --------
    def load_account(self, customer):
        if customer.customer_id not in self.accounts:
            print("\nChoose Account Type:")
            print("1. Savings Account")
            print("2. Privilege Account")

            acc_choice = input("Enter choice: ")

            if acc_choice == "2":
                self.accounts[customer.customer_id] = PrivilegeAccount(
                    2001, customer, 20000
                )
                print("Privilege Account created successfully.")
            else:
                self.accounts[customer.customer_id] = SavingsAccount(
                    1001, customer, 5000
                )
                print("Savings Account created successfully.")

        self.account = self.accounts[customer.customer_id]
        self.menu()

    # -------- Customer Menu --------
    def menu(self):
        while True:
            print("\n1.Deposit  2.Withdraw  3.Balance  4.Interest  5.Transactions  6.Logout")
            option = input("Choose: ")

            if option == "1":
                self.account.deposit(float(input("Amount: ")))
            elif option == "2":
                self.account.withdraw(float(input("Amount: ")))
            elif option == "3":
                print("Balance:", self.account.get_balance())
            elif option == "4":
                print("Interest:", self.account.calculate_interest())
            elif option == "5":
                self.account.show_transactions()
            elif option == "6":
                break


# -------- Entry Point --------
if __name__ == "__main__":
    BankApp()
