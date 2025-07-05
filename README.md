# ConCost: ***proof of concept*** - Construction Company Double-Entry Bookkeeping System ( under development with github copilot GPT-4.1 and Gemini 2.5 Pro)

This Django project provides a double-entry bookkeeping system for construction companies. It supports:

- Multiple construction sites
- Company-wide and site-specific transactions
- Double-entry accounting (accounts, transactions, entries)
- Capital contributions by shareholders

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Main App
- `accounting`: Contains all bookkeeping models and logic.

## Customization
- Extend models and views in `accounting` as needed for your workflow.

---
