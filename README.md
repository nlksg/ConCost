# ConCost: Construction Company Double-Entry Bookkeeping System

*This project is under active development as a proof-of-concept, built with the assistance of AI models.*

This is a comprehensive, GAAP-compliant double-entry bookkeeping system built with Django, designed specifically for the construction industry. It facilitates a robust workflow from on-site expense submission to final accounting and reporting.

## Key Features

- **GAAP-Compliant Double-Entry Accounting**: Core of the system, with Journals, Debits, and Credits.
- **Hierarchical Chart of Accounts**: Supports complex account structures with parent-child relationships.
- **Multi-Site Management**: Track finances for individual construction sites as well as the entire company.
- **Site Expense Workflow**: A simple interface for site staff to submit expenses with receipts for approval.
- **Purchase Management**: Accountants can create multi-line purchases, convert site expenses into formal purchases, and manage approvals.
- **Item Catalog**: Centralized catalog of materials/services, each linked to a default expense account for accurate tracking.
- **Role-Based Permissions**: Secure workflows for Admin, Accountant, and Site Staff roles.
- **Financial Reporting**: Trial Balance, Income Statement, General Ledger, Balance Sheet, and more.
- **Admin Tools**: Management commands to purge data, initialize default chart of accounts, and create default user groups.
- **Mobile-Friendly UI**: Responsive design for use on phones and tablets.

## Core Applications

- `accounting`: Core bookkeeping models (`Account`, `Journal`, `JournalEntry`), reporting, and capital contributions.
- `SiteExpense`: Interface for site personnel to submit expense requests with receipts.
- `purchase`: Manages the item catalog, purchase orders, and approval workflow that generates journal entries.

## User Roles & Workflow

- **Site Staff**: Submits a `SiteExpense` with a description, amount, date, and optional receipt image.
- **Accountant**: 
    - Reviews pending site expenses.
    - Creates a formal `Purchase` from a site expense, adding line items from the `Item` catalog.
    - Manages the `Item` catalog and default expense accounts.
    - Approves `Purchase` orders, which automatically generate double-entry `Journal` records.
- **Admin**: Full access, including user/group management and admin tools for data reset and initialization.

## Getting Started

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run database migrations**:
    ```bash
    python manage.py migrate
    ```
3.  **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```
4.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```
5.  **Initial Setup (Required)**:
    - Log in to the admin panel (`/admin`).
    - Run management commands to create default groups and chart of accounts:
      ```bash
      python manage.py init_default_groups
      python manage.py init_chart_of_accounts
      ```
    - Create user accounts and assign them to the appropriate groups.
    - Populate the Item Catalog via the UI (`/purchases/items/`).

---
*This project is under active development as a proof-of-concept, built with the assistance of AI models.*
