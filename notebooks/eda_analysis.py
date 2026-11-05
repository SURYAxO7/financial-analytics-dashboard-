"""
Financial Analytics Dashboard — Exploratory Data Analysis
Reads transactions.csv and budget.csv, analyzes trends, and generates chart images
used in the dashboard preview and the README.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

ROOT = Path(__file__).resolve().parent.parent          # project folder
df = pd.read_csv(ROOT / "data" / "transactions.csv", parse_dates=["date"])
budget_df = pd.read_csv(ROOT / "data" / "budget.csv", parse_dates=["date"])

OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# 1. Monthly Revenue vs Expense vs Net Profit
# ------------------------------------------------------------------
monthly = df.groupby([df["date"].dt.to_period("M"), "type"])["amount"].sum().unstack().fillna(0)
monthly.index = monthly.index.to_timestamp()
monthly["Net Profit"] = monthly["Revenue"] - monthly["Expense"]

fig, ax = plt.subplots()
ax.plot(monthly.index, monthly["Revenue"], marker="o", label="Revenue", linewidth=2)
ax.plot(monthly.index, monthly["Expense"], marker="o", label="Expense", linewidth=2)
ax.plot(monthly.index, monthly["Net Profit"], marker="o", label="Net Profit", linewidth=2, linestyle="--")
ax.set_title("Monthly Revenue, Expense & Net Profit Trend")
ax.set_ylabel("Amount (₹)")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/01_revenue_expense_trend.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 2. Profit Margin % Trend
# ------------------------------------------------------------------
monthly["Profit Margin %"] = (monthly["Net Profit"] / monthly["Revenue"]) * 100

fig, ax = plt.subplots()
ax.plot(monthly.index, monthly["Profit Margin %"], color="green", marker="o", linewidth=2)
ax.axhline(monthly["Profit Margin %"].mean(), color="gray", linestyle=":", label="Average")
ax.set_title("Profit Margin % Over Time")
ax.set_ylabel("Profit Margin (%)")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/02_profit_margin_trend.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 3. Expense Breakdown by Category
# ------------------------------------------------------------------
expense_by_cat = df[df["type"] == "Expense"].groupby("category")["amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
sns.barplot(x=expense_by_cat.values, y=expense_by_cat.index, hue=expense_by_cat.index,
            palette="viridis", legend=False, ax=ax)
ax.set_title("Total Expense by Category")
ax.set_xlabel("Total Spent (₹)")
plt.tight_layout()
plt.savefig(f"{OUT}/03_expense_by_category.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 4. Revenue by Department
# ------------------------------------------------------------------
rev_by_dept = df[df["type"] == "Revenue"].groupby("department")["amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
sns.barplot(x=rev_by_dept.index, y=rev_by_dept.values, hue=rev_by_dept.index,
            palette="mako", legend=False, ax=ax)
ax.set_title("Total Revenue by Department")
ax.set_ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(f"{OUT}/04_revenue_by_department.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 5. Budget vs Actual (latest month)
# ------------------------------------------------------------------
latest_month = df["date"].max().to_period("M")
actual_latest = (
    df[(df["type"] == "Expense") & (df["date"].dt.to_period("M") == latest_month)]
    .groupby("department")["amount"].sum()
)
budget_latest = (
    budget_df[(budget_df["type"] == "Expense") & (budget_df["date"].dt.to_period("M") == latest_month)]
    .groupby("department")["budgeted_amount"].sum()
)
compare = pd.DataFrame({"Actual": actual_latest, "Budgeted": budget_latest}).fillna(0)

fig, ax = plt.subplots()
compare.plot(kind="bar", ax=ax, color=["#e74c3c", "#3498db"])
ax.set_title(f"Budget vs Actual Expense — {latest_month}")
ax.set_ylabel("Amount (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUT}/05_budget_vs_actual.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 6. Cumulative Cash Flow
# ------------------------------------------------------------------
monthly["Cumulative Cash Flow"] = monthly["Net Profit"].cumsum()

fig, ax = plt.subplots()
ax.fill_between(monthly.index, monthly["Cumulative Cash Flow"], color="skyblue", alpha=0.4)
ax.plot(monthly.index, monthly["Cumulative Cash Flow"], color="steelblue", linewidth=2)
ax.set_title("Cumulative Cash Flow Over Time")
ax.set_ylabel("Cumulative Cash Flow (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUT}/06_cumulative_cash_flow.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# Key insights summary (printed + saved to text file for README)
# ------------------------------------------------------------------
total_revenue = monthly["Revenue"].sum()
total_expense = monthly["Expense"].sum()
avg_margin = monthly["Profit Margin %"].mean()
top_expense_cat = expense_by_cat.idxmax()
top_expense_pct = expense_by_cat.max() / total_expense * 100
over_budget_depts = compare[compare["Actual"] > compare["Budgeted"]].index.tolist()

insights = f"""
KEY INSIGHTS — Financial Analytics Dashboard
=============================================
- Total Revenue (24 months): ₹{total_revenue:,.0f}
- Total Expense (24 months): ₹{total_expense:,.0f}
- Overall Net Profit: ₹{(total_revenue - total_expense):,.0f}
- Average Profit Margin: {avg_margin:.1f}%
- Highest expense category: {top_expense_cat} ({top_expense_pct:.1f}% of total expenses)
- Departments over budget in {latest_month}: {', '.join(over_budget_depts) if over_budget_depts else 'None'}
- Revenue growth trend: {'Positive' if monthly['Revenue'].iloc[-1] > monthly['Revenue'].iloc[0] else 'Negative'} over the period
  ({monthly['Revenue'].iloc[0]:,.0f} -> {monthly['Revenue'].iloc[-1]:,.0f})
"""

with open(OUT / "key_insights.txt", "w") as f:
    f.write(insights)

print(insights)
print("All charts saved to:", OUT)

# Save processed monthly summary for dashboard use
monthly.to_csv(ROOT / "data" / "monthly_summary.csv")
