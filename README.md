# ConCost: Construction Company Double-Entry Bookkeeping System

*This project is under active development as a proof-of-concept, built with the assistance of AI models.*


This is a comprehensive, GAAP-compliant double-entry bookkeeping system built with Django, designed specifically for the construction industry. It facilitates a robust workflow from on-site expense submission to final accounting and reporting.

## Key Features

- **GAAP-Compliant Double-Entry Accounting**: Core of the system, with Journals, Debits, and Credits.
- **Hierarchical Chart of Accounts**: Supports complex account structures with parent-child relationships.
- **Multi-Site Management**: Track finances for individual construction sites as well as the entire company.
- **Site Expense Workflow**: A simple interface for site staff to submit expenses with receipts for approval.
- **Purchase Management**: A workflow for accountants to create multi-line purchases, convert site expenses into formal purchases, and manage approvals.
- **Item Catalog**: A centralized catalog of materials and services, each linked to a default expense account, ensuring consistent and accurate expense tracking.
- **Role-Based Permissions**: Secure workflows for different user roles (Admin, Accountant, Site Staff).
- **Financial Reporting**: Includes Trial Balance, Income Statement, General Ledger, Balance Sheet, and more.

## Core Applications

- `accounting`: Contains the core bookkeeping models (`Account`, `Journal`, `JournalEntry`), reporting views, and capital contribution tracking.
- `SiteExpense`: Provides the interface for site personnel to submit expense requests.
- `purchase`: Manages the item catalog, purchase orders, and the approval process that generates journal entries.

## User Roles & Workflow

The system is designed around a typical workflow involving different user roles:

1.  **Site Staff**: Submits a `SiteExpense` with a description, amount, date, and an optional receipt image.
2.  **Accountant**: 
    - Reviews pending site expenses.
    - Creates a formal `Purchase` from a site expense, adding line items by selecting from the `Item` catalog.
    - Manages the `Item` catalog, defining default expense accounts for each item.
    - Approves `Purchase` orders, which automatically generates the correct double-entry `Journal` records.
3.  **Admin**: Has full access to the system, including user and group management.

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
    - Create three user groups: `Admin`, `Accountant`, and `Site Staff`.
    - Create user accounts for your team and assign them to the appropriate groups.
    - Populate the Chart of Accounts, or ensure the initial migrations have created the necessary default accounts (e.g., Accounts Payable, expense accounts).
    - Populate the Item Catalog via the UI (`/purchases/items/`).

---
*This project is under active development as a proof-of-concept, built with the assistance of AI models.*
