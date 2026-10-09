# Personal Expense Tracker — Django

This Django web project follows the Personal Expense Tracker described in the uploaded SEPM lab manual. It includes login/registration, add/edit/delete transactions, categories, budgets, budget warnings, dashboard summaries, and monthly reporting.

## Requirements
- Python 3.10 or newer
- VS Code
- Internet is only needed to install Django the first time.

## Run on Windows (VS Code)

1. Extract `Personal_Expense_Tracker_Django.zip`.
2. Open VS Code → **File → Open Folder** → select `Personal_Expense_Tracker_Django`.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
5. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
6. Install Django:
   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Create database tables:
   ```powershell
   python manage.py migrate
   ```
8. Create an admin account (optional):
   ```powershell
   python manage.py createsuperuser
   ```
9. Start the server:
   ```powershell
   python manage.py runserver
   ```
10. Open `http://127.0.0.1:8000/` in your browser.
11. Admin site: `http://127.0.0.1:8000/admin/`

## Features
- Django authentication: register, log in, log out.
- Each user sees only their own transactions and budgets.
- Create, update, and delete income/expense records.
- Categories and category budgets.
- Budget warning when spending reaches 80% or more of a category budget.
- Dashboard totals and current-month summary.
- Filter transactions by keyword and type.
- SQLite database, created locally by Django migrations.

## Notes
- This is an academic starter project. It is not financial advice and does not connect to bank accounts.
- Django's built-in authentication is used; passwords are hashed by Django.
- Keep `SECRET_KEY` private before deploying publicly. `DEBUG=True` is for local development only.
