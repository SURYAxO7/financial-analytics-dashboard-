-- ============================================================
-- Financial Analytics Dashboard — Core SQL Queries (MySQL version)
-- Database: finance_dashboard
-- Run: USE finance_dashboard; first
-- ============================================================

-- 1. Monthly Revenue, Expense, and Net Profit (company-wide)
SELECT
    DATE_FORMAT(date, '%Y-%m') AS month,
    SUM(CASE WHEN type = 'Revenue' THEN amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expense,
    SUM(CASE WHEN type = 'Revenue' THEN amount ELSE -amount END) AS net_profit
FROM transactions
GROUP BY month
ORDER BY month;


-- 2. Profit Margin Trend (%)
SELECT
    month,
    total_revenue,
    total_expense,
    ROUND((total_revenue - total_expense) * 100.0 / total_revenue, 2) AS profit_margin_pct
FROM (
    SELECT
        DATE_FORMAT(date, '%Y-%m') AS month,
        SUM(CASE WHEN type = 'Revenue' THEN amount ELSE 0 END) AS total_revenue,
        SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expense
    FROM transactions
    GROUP BY month
) AS monthly
ORDER BY month;


-- 3. Expense Breakdown by Category
SELECT
    category,
    ROUND(SUM(amount), 2) AS total_spent,
    ROUND(SUM(amount) * 100.0 / (SELECT SUM(amount) FROM transactions WHERE type = 'Expense'), 2) AS pct_of_total_expense
FROM transactions
WHERE type = 'Expense'
GROUP BY category
ORDER BY total_spent DESC;


-- 4. Revenue by Department
SELECT
    department,
    ROUND(SUM(amount), 2) AS total_revenue
FROM transactions
WHERE type = 'Revenue'
GROUP BY department
ORDER BY total_revenue DESC;


-- 5. Budget vs Actual — Expense Variance by Department (latest month)
SELECT
    t.department,
    ROUND(SUM(t.amount), 2) AS actual_expense,
    ROUND(b.budgeted_amount, 2) AS budgeted_expense,
    ROUND(SUM(t.amount) - b.budgeted_amount, 2) AS variance,
    ROUND((SUM(t.amount) - b.budgeted_amount) * 100.0 / b.budgeted_amount, 2) AS variance_pct
FROM transactions t
JOIN budget b
    ON t.department = b.department
    AND DATE_FORMAT(t.date, '%Y-%m') = DATE_FORMAT(b.date, '%Y-%m')
    AND b.type = 'Expense'
WHERE t.type = 'Expense'
    AND DATE_FORMAT(t.date, '%Y-%m') = (SELECT MAX(DATE_FORMAT(date, '%Y-%m')) FROM transactions)
GROUP BY t.department, b.budgeted_amount
ORDER BY variance_pct DESC;


-- 6. Cash Flow Trend (Net Revenue - Net Expense, cumulative)
SELECT
    month,
    net_profit,
    SUM(net_profit) OVER (ORDER BY month) AS cumulative_cash_flow
FROM (
    SELECT
        DATE_FORMAT(date, '%Y-%m') AS month,
        SUM(CASE WHEN type = 'Revenue' THEN amount ELSE -amount END) AS net_profit
    FROM transactions
    GROUP BY month
) AS monthly
ORDER BY month;


-- 7. Month-over-Month Revenue Growth Rate (%)
SELECT
    month,
    total_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY month))
        * 100.0 / LAG(total_revenue) OVER (ORDER BY month), 2
    ) AS mom_growth_pct
FROM (
    SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) AS total_revenue
    FROM transactions
    WHERE type = 'Revenue'
    GROUP BY month
) AS monthly_rev;


-- 8. Top 5 Highest-Spending Department-Category Combinations
SELECT
    department,
    category,
    ROUND(SUM(amount), 2) AS total_spent
FROM transactions
WHERE type = 'Expense'
GROUP BY department, category
ORDER BY total_spent DESC
LIMIT 5;


-- 9. Departments Consistently Over Budget (count of months where actual > budgeted)
SELECT
    department,
    COUNT(*) AS months_over_budget
FROM (
    SELECT
        t.department,
        DATE_FORMAT(t.date, '%Y-%m') AS month,
        SUM(t.amount) AS actual,
        MAX(b.budgeted_amount) AS budgeted
    FROM transactions t
    JOIN budget b
        ON t.department = b.department
        AND DATE_FORMAT(t.date, '%Y-%m') = DATE_FORMAT(b.date, '%Y-%m')
        AND b.type = 'Expense'
    WHERE t.type = 'Expense'
    GROUP BY t.department, month
    HAVING actual > budgeted
) AS over_budget_months
GROUP BY department
ORDER BY months_over_budget DESC;
