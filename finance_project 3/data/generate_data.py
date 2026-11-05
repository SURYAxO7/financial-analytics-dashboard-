"""
Generates a synthetic 24-month financial dataset for the
Financial Analytics Dashboard project.

Produces:
    - transactions.csv   (monthly revenue & expense line items by department/category)
    - budget.csv          (monthly budget targets by department)
"""

import random
import csv
from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta

BASE = Path(__file__).resolve().parent  # the data/ folder
random.seed(42)

DEPARTMENTS = ["Sales", "Marketing", "Operations", "R&D", "HR", "IT"]

REVENUE_CATEGORIES = ["Product Sales", "Service Revenue", "Licensing", "Subscriptions"]
EXPENSE_CATEGORIES = ["Salaries", "Marketing Spend", "Office Rent", "Software & Tools",
                      "Travel", "Utilities", "Raw Materials", "Logistics"]

START_MONTH = date(2024, 1, 1)
NUM_MONTHS = 24

# Base monthly figures per department (revenue only applies to Sales/Marketing/Ops realistically,
# but we keep it general so the dataset supports company-wide dashboards)
base_revenue = {
    "Sales": 180000,
    "Marketing": 20000,
    "Operations": 60000,
    "R&D": 5000,
    "HR": 0,
    "IT": 8000,
}

base_expense = {
    "Sales": 55000,
    "Marketing": 30000,
    "Operations": 65000,
    "R&D": 35000,
    "HR": 22000,
    "IT": 26000,
}

rows = []
txn_id = 1

for m in range(NUM_MONTHS):
    month_date = START_MONTH + relativedelta(months=m)
    # simple seasonal + growth trend
    growth_factor = 1 + (m * 0.012)                     # ~1.2% growth per month
    seasonal = 1 + 0.15 * random.choice([-1, 1]) * random.random() if month_date.month in (11, 12, 6) else 1

    for dept in DEPARTMENTS:
        # Revenue rows
        rev_base = base_revenue[dept]
        if rev_base > 0:
            noise = random.uniform(0.85, 1.15)
            amount = round(rev_base * growth_factor * seasonal * noise, 2)
            category = random.choice(REVENUE_CATEGORIES)
            rows.append([txn_id, month_date.isoformat(), dept, "Revenue", category, amount])
            txn_id += 1

        # Expense rows (split into 2-3 line items per department per month)
        exp_base = base_expense[dept]
        num_line_items = random.randint(2, 3)
        remaining = exp_base * growth_factor * random.uniform(0.9, 1.1)
        for i in range(num_line_items):
            share = remaining / (num_line_items - i)
            noise = random.uniform(0.8, 1.2)
            amount = round(share * noise, 2)
            remaining -= amount
            category = random.choice(EXPENSE_CATEGORIES)
            rows.append([txn_id, month_date.isoformat(), dept, "Expense", category, round(amount, 2)])
            txn_id += 1

with open(BASE / "transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "date", "department", "type", "category", "amount"])
    writer.writerows(rows)

# ---- Budget data ----
budget_rows = []
bid = 1
for m in range(NUM_MONTHS):
    month_date = START_MONTH + relativedelta(months=m)
    growth_factor = 1 + (m * 0.01)
    for dept in DEPARTMENTS:
        budget_rev = round(base_revenue[dept] * growth_factor, 2)
        budget_exp = round(base_expense[dept] * growth_factor, 2)
        budget_rows.append([bid, month_date.isoformat(), dept, "Revenue", budget_rev])
        bid += 1
        budget_rows.append([bid, month_date.isoformat(), dept, "Expense", budget_exp])
        bid += 1

with open(BASE / "budget.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["budget_id", "date", "department", "type", "budgeted_amount"])
    writer.writerows(budget_rows)

print(f"Generated {len(rows)} transaction rows and {len(budget_rows)} budget rows.")
