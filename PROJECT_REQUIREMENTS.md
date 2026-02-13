# 📋 Project Brief: Core Banking System

**Role:** Backend Engineer

**Client:** FinTech Startup "SecureBank" (Mock Project)

**Objective:** Build the core transaction engine for a new banking platform (Personal Project for Learning Backend).

**Context:**
This is a personal project designed to simulate a real-world banking environment for learning backend development. We are building a banking system from scratch. We do not have a frontend (website/app) yet. Your job is to build the **backend logic** that will eventually power the API. Even though this is a simulation, the system must be reliable and secure. Treat it as if real money disappears if your code fails.

---

### 🚀 Phase 1: Core Requirements

Your system must support the following operations via Python code (no user interface required):

1.  **Customer Onboarding:**
    *   Register a new customer with a Name and Email.
    *   Assign a unique ID to every customer.

2.  **Account Management:**
    *   Allow customers to open multiple accounts.
    *   Support two distinct types of accounts: **Savings** and **Checking**.

3.  **The Transaction Engine:**
    *   Support **Deposits** (add money).
    *   Support **Withdrawals** (remove money).
    *   Support **Transfers** (move money from Account A to Account B).

4.  **Audit Trail:**
    *   Every time a balance changes, a `Transaction` record must be created (Date, Type, Amount).
    *   Users should be able to request a "Bank Statement" showing their history.

---

### ⚠️ The Business Rules (Constraints)

You must enforce these rules strictly in your code. If a rule is violated, your program should raise an error.

#### 1. The "Golden Rule" of Integrity
*   **Private Balance:** The balance attribute of an account must never be accessible directly (e.g., `account.balance = 1000` is forbidden).
*   **Transaction Only:** The only way to change a balance is through a method (e.g., `.deposit()`, `.withdraw()`).

#### 2. Savings Account Logic
*   **Strict Limits:** A Savings Account can **never** have a negative balance. If a user tries to withdraw $100 but only has $50, the transaction must fail.
*   **Interest:** Implement a method to apply an interest rate (e.g., 1.5%) to the current balance.

#### 3. Checking Account Logic
*   **Overdraft Protection:** A Checking Account **can** go negative, but only up to a specific limit (e.g., -$500).
*   **The Penalty:** If a withdrawal causes the balance to drop below $0, automatically deduct an extra **$35 overdraft fee**.

#### 4. Transfer Logic (Atomicity)
*   **All or Nothing:** A transfer is two steps: Withdraw from A, Deposit to B.
*   If the Withdrawal fails (e.g., insufficient funds), the Deposit **must not happen**. Money cannot vanish or appear out of thin air.

---

### 🏁 Definition of Done

You have completed this project when:
1.  You have a clean project structure (`src/`, `tests/`).
2.  You can run a script that simulates a user opening an account, depositing money, and transferring it.
3.  You have tests proving that a Savings Account rejects withdrawals that would make it negative.

---

### 🗄️ Phase 2: Database Integration (MySQL)

**Objective:** Replace in-memory lists with a persistent MySQL database to support scalability and authentication.

#### Core Requirements
1.  **Database Setup:**
    *   Install **MySQL Community Server** and **MySQL Workbench**.
    *   Design the schema: `Users`, `Accounts`, `Transactions`.
2.  **Python Integration:**
    *   Install `mysql-connector-python`.
    *   Create a `database.py` module to handle connections.
3.  **Refactoring:**
    *   Update `Customer` and `Account` classes to fetch/save data to SQL.

#### The Business Rules (Constraints)
1.  **Data Persistence:**
    *   Data must survive if the Python script is stopped and restarted.
2.  **Referential Integrity:**
    *   A Transaction cannot exist without an Account.
    *   An Account cannot exist without a User.
3.  **Atomic Transactions:**
    *   Use `commit()` only when the full operation succeeds.
    *   Use `rollback()` if any part fails.

#### Definition of Done
1.  You can restart the application and previous users/accounts still exist.
2.  The `src/` code no longer uses global lists (e.g., `customers = []`).

---

### 🖥️ Phase 3: The Graphical User Interface (GUI)

**Objective:** Transform the CLI script into a secure desktop application with login capabilities.

#### Core Requirements
1.  **Authentication System:**
    *   **Login Screen:** Email/Password input.
    *   **Sign Up Screen:** Create new Customer profiles.
2.  **Customer Dashboard:**
    *   View Account Balances (Savings/Checking).
    *   Perform Transfers/Deposits via buttons/inputs.
    *   View Personal Transaction History.
3.  **Admin Dashboard:**
    *   View all Customers and total Bank Reserves.
    *   View Master Transaction Log.

#### The Business Rules (Constraints)
1.  **Access Control:**
    *   Customers can **only** see their own accounts.
    *   Admins can see everything but cannot move customer money without permission (simulation).
2.  **State Management:**
    *   The app must track the "Current User" session after login.
3.  **Input Validation:**
    *   Prevent empty fields or invalid numbers in the UI.

#### Definition of Done
1.  You can log in as a Customer and see your specific balance.
2.  You can log in as Admin and see a list of all users.

---

### 🌐 Phase 4: REST API (Future Roadmap)

**Objective:** Decouple the GUI from the Database by introducing a REST API. This moves the "Backend Logic" from the user's computer to a dedicated server.

#### Core Requirements
1.  **API Endpoints:**
    *   `POST /login`: Authenticate user.
    *   `GET /accounts`: Fetch balances.
    *   `POST /transfer`: Execute money movement.
2.  **GUI Refactoring:**
    *   Remove direct MySQL connection from the GUI.
    *   Use HTTP requests to communicate with the backend.

#### The Business Rules (Constraints)
1.  **Security:**
    *   The Database credentials must **only** exist in the API, never in the GUI client.
2.  **Statelessness:**
    *   The API should not hold session state in memory (use tokens if applicable).

#### Definition of Done
1.  The GUI works exactly as before, but connects to `localhost:5000` instead of MySQL directly.
