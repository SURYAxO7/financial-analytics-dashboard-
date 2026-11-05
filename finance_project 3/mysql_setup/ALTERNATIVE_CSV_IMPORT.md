# Alternative: Importing via LOAD DATA LOCAL INFILE

The primary method in this project uses `03_insert_transactions.sql` and
`04_insert_budget.sql` (pre-built INSERT statements — just paste and run, no setup).

This file is a reference for the CSV-based method, useful to know for interviews
since it's a common real-world skill, but it requires a couple of settings enabled
first and can behave differently across MySQL versions.

## 1. Enable local file loading

In a Workbench query tab:
```sql
SHOW VARIABLES LIKE 'local_infile';
```
If it shows `OFF`:
```sql
SET GLOBAL local_infile = 1;
```

## 2. Enable it on the connection itself

**Database → Manage Connections** → select your connection → **Advanced** tab →
in the "Others" box add:
```
OPT_LOCAL_INFILE=1
```
Close Workbench completely and reopen it, then reconnect.

## 3. Run the load (edit the path to match your system)

```sql
USE finance_dashboard;

LOAD DATA LOCAL INFILE 'C:/Users/YourName/Desktop/finance_project/data/transactions.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(transaction_id, date, department, type, category, amount);

LOAD DATA LOCAL INFILE 'C:/Users/YourName/Desktop/finance_project/data/budget.csv'
INTO TABLE budget
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(budget_id, date, department, type, budgeted_amount);
```

Use forward slashes `/` in the path even on Windows — MySQL expects that format.

## Common errors

- **"Loading local data is disabled"** → you missed step 2 (connection-level setting)
- **"Access denied" / "secure_file_priv" error** → your MySQL server restricts file
  loading to a specific folder; check with `SHOW VARIABLES LIKE 'secure_file_priv';`
  and move your CSVs there, or just use the INSERT script method instead
