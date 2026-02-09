# 🏦 Bank Application – OOP in Python

## 📌 Project Overview
This project is a console-based Bank Application implemented using Object-Oriented Programming (OOP) principles in Python.  
It simulates real-world banking operations such as account creation, deposits, withdrawals, interest calculation, and transaction tracking.

---

## 🧠 OOP Concepts Used
- Classes and Objects
- Inheritance
- Encapsulation
- Polymorphism
- Role-Based Access Control (Admin / Customer)

---

## 🧩 Class Diagram

+----------------+
|     Branch     |
+----------------+
| branch_name    |
| branch_code    |
+----------------+
| display_branch |
+----------------+


+----------------+
|    Customer    |
+----------------+
| customer_id    |
| name           |
+----------------+


+---------------------+
|      Account        |
+---------------------+
| account_number      |
| customer            |
| _balance            |
| transactions        |
+---------------------+
| deposit()           |
| withdraw()          |
| get_balance()       |
| calculate_interest()|
| show_transactions() |
+---------------------+
          ^
          |
          |  Inheritance
          |
+---------------------+   +---------------------+   +----------------------+
|   SavingsAccount    |   |   CurrentAccount    |   |  PrivilegeAccount    |
+---------------------+   +---------------------+   +----------------------+
| MIN_BALANCE         |   | MIN_BALANCE         |   | MIN_BALANCE          |
| INTEREST_RATE       |   |                     |   | INTEREST_RATE        |
+---------------------+   +---------------------+   +----------------------+
| withdraw()          |   | withdraw()          |   | withdraw()           |
| calculate_interest()|   |                     |   | calculate_interest() |
+---------------------+   +---------------------+   +----------------------+

### Diagram Explanation
- `Account` is the base class that defines common banking operations.
- `SavingsAccount`, `CurrentAccount`, and `PrivilegeAccount` inherit from `Account` and override specific behaviors.
- `Customer` represents a bank user associated with an account.
- `Branch` represents the bank branch details.

---

## ⚙️ Features
- Multiple account types (Savings, Current, Privilege)
- Minimum balance enforcement
- Interest calculation for applicable accounts
- Deposit and withdrawal operations with validation
- Timestamped transaction history
- Admin role for customer management
- Secure role-based access (Admin vs Customer)
- Console-based menu-driven interaction

---

## ▶️ How to Run the Application

1. Ensure Python is installed (Python 3.x)
2. Open a terminal in the project directory
3. Run the application:

```bash
python bank_app.py
