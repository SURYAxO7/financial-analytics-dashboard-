# Setup Guide: MySQL + Tableau on Mac (Step by Step)

Pipeline: **Python (generate data) → MySQL (store + SQL analysis) → Tableau (dashboard)**.
Everything below is written for macOS.

Folder reference (inside the unzipped `finance_project/`):
- `mysql_setup/` SQL scripts for MySQL
- `tableau_setup/` Tableau guide + ready data files
- `dashboard/index.html` instant preview, no install needed

---

## PART 0: Quick preview (30 seconds, no installs)

Double-click `dashboard/index.html`. It opens in Safari/Chrome and shows the finished
dashboard concept. Use it as your visual target while you build the Tableau version.

---

## PART 1: Install MySQL on Mac

Check your chip first: Apple menu → **About This Mac**. "Apple M1/M2/M3/M4" = ARM. "Intel" = x86.

1. Go to https://dev.mysql.com/downloads/mysql/
2. Choose **macOS** and the **DMG Archive** that matches your chip (ARM 64-bit for Apple silicon, x86 64-bit for Intel). Click Download, then "No thanks, just start my download".
3. Open the `.dmg`, run the `.pkg`, and click through the installer.
4. When asked, choose **Use Strong Password Encryption** and set a **root password**. Write it down; you need it for every connection.
5. Start the server: **System Settings → MySQL → Start MySQL Server**. (Tick "Automatically start MySQL Server on startup" if you like.)
6. Install the GUI: go to https://dev.mysql.com/downloads/workbench/ → macOS → download the `.dmg` → drag **MySQL Workbench** into Applications → open it.

*Alternative if you use Homebrew:* `brew install mysql` then `brew services start mysql`, and install Workbench with `brew install --cask mysqlworkbench`. With Homebrew the root user has no password at first; run `mysql_secure_installation` to set one.

---

## PART 2: Create the database and tables

1. Open MySQL Workbench → click the `localhost` connection → enter your root password.
2. **File → New Query Tab**.
3. Open `mysql_setup/01_create_schema.sql` in TextEdit (or any editor), select all, copy, paste into the query tab.
4. Click the lightning bolt icon to run **everything** in the tab.
5. In the left Navigator panel, click the refresh icon next to **SCHEMAS**. You should see `finance_dashboard` with tables `transactions` and `budget`.

---

## PART 3: Load the data

Recent Workbench versions have no Table Data Import Wizard, so this project loads data
with ready-made `INSERT` scripts. No file paths, no permission settings.

1. Open `mysql_setup/03_insert_transactions.sql` → select all → copy → paste into a **new query tab** → lightning bolt. (469 rows.)
2. Open `mysql_setup/04_insert_budget.sql` → copy → new query tab → lightning bolt. (288 rows.)
3. Verify in a new tab:
```sql
USE finance_dashboard;
SELECT COUNT(*) FROM transactions;   -- expect 469
SELECT COUNT(*) FROM budget;         -- expect 288
```
(The `LOAD DATA LOCAL INFILE` method is documented in `ALTERNATIVE_CSV_IMPORT.md`. On Mac use paths like `/Users/yourname/Desktop/finance_project/data/transactions.csv`.)

---

## PART 4: Run the analysis queries

1. Open `mysql_setup/02_analysis_queries_mysql.sql`, copy the whole file into **one** new query tab.
2. Click inside Query 1, then press **Cmd + Return** to run only that query (the lightning bolt runs everything).
3. Look at the result grid at the bottom, screenshot it, move to Query 2, repeat for all 9.
4. Save 2 or 3 screenshots into `screenshots/` for your README.

---

## PART 4B: Run the Python analysis (this is your Pandas / NumPy / Matplotlib / Seaborn skill)

The notebook `notebooks/eda_analysis.ipynb` already contains finished results, so you can read it on GitHub as is. Running it yourself on your Mac is what lets you say you did the analysis, and it takes 5 minutes.

1. Check Python: open **Terminal** (Cmd + Space, type Terminal) and run `python3 --version`. If it isn't installed, get it from python.org.
2. In Terminal, go into the project folder, for example:
```bash
cd ~/Desktop/finance_project
```
3. Install the libraries:
```bash
pip3 install pandas numpy matplotlib seaborn jupyter
```
4. Open the notebook:
```bash
jupyter notebook notebooks/eda_analysis.ipynb
```
It opens in your browser. Click **Run → Run All Cells** (or Kernel → Restart & Run All) and read the charts and findings as they appear.
5. Optional: regenerate the chart images with `python3 notebooks/eda_analysis.py`.

If `pip3` isn't found, use `python3 -m pip install pandas numpy matplotlib seaborn jupyter`. If you use VS Code, you can open the `.ipynb` file there instead of Jupyter.

The data files are identical to the ones loaded into MySQL, so the notebook and the Tableau dashboard show the same numbers (revenue 7,365,086 and expense 6,337,730).

---

## PART 5: Create the views Tableau will use

1. Open `mysql_setup/05_tableau_views.sql` → copy all → new query tab → lightning bolt.
2. The last two lines return row counts. Expect **469** and **288**.

These views give Tableau two clean tables:
- `vw_transactions` (every transaction, with a month label)
- `vw_budget_vs_actual` (actual vs budget per month, department and type, already summed so budgets are never double counted)

---

## PART 6: Install Tableau on Mac

**Recommended: Tableau Desktop Public Edition (free, no expiry)**
1. Go to the Tableau for Students page (tableau.com/blog/tableau-students-free-access-tableau-desktop) and click **Get Tableau for Free**.
2. Create a free Tableau Public account when asked.
3. Download the macOS installer, open the `.dmg`, install, then open Tableau and sign in.
4. Check the app name says **Tableau Public** / **Public Edition**. Do not use Tableau Cloud, Tableau Next or Prep for this project.

Public Edition cannot connect to MySQL. It reads files, so you will use the CSVs in
`tableau_setup/data/` (they match the MySQL views exactly).

**Optional: full Tableau Desktop 14-day trial** (only if you want a live MySQL connection screenshot)
Download from tableau.com/products/trial, and connect to MySQL as described in Path A of `TABLEAU_GUIDE.md`.

---

## PART 7: Connect Tableau to the data and build the dashboard

Open **`tableau_setup/TABLEAU_GUIDE.md`** and follow it in order. It covers:

1. Connecting (CSV files with Public Edition; MySQL live only with the trial)
2. Setting up the relationship on **Date + Department + Type**
3. Calculated fields (copy-paste formulas)
4. Eight sheets (4 KPI cards, trend, margin, category, department, budget vs actual, cash flow, variance heatmap)
5. Parameters (metric selector, Top N)
6. Filters, dashboard layout, and click-to-filter actions
7. Saving as `.twbx` / publishing to Tableau Public

---

## PART 8: Package for GitHub

1. Put your finished `Financial_Analytics_Dashboard.twbx` (or the Tableau Public link) and 3 screenshots into the repo.
2. Keep the README's "Key Insight" section; update it with the numbers you see in your own dashboard.
3. Upload the whole folder to a new GitHub repo.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Workbench "Can't connect to MySQL server" | System Settings → MySQL → **Start MySQL Server** |
| `Table doesn't exist` when running inserts | Run Part 2 first, and make sure `USE finance_dashboard;` is at the top |
| `Duplicate entry for key PRIMARY` | The insert script ran twice. Run `TRUNCATE TABLE transactions;` (or `budget`) and run it once |
| Views error "Unknown database" | Part 2 not done, or typed the database name differently |
| Tableau won't show MySQL | You are on Public Edition, which does not support MySQL. Use the CSV files (or the 14-day full Desktop trial) |
| Tableau asks for a driver | Use the download link in the connection dialog, install it, restart Tableau |
| Mac says the installer can't be opened | System Settings → Privacy & Security → **Open Anyway** |

You end up with the real stack: **MySQL** (database) → **SQL** (analysis) → **Tableau** (dashboard).
