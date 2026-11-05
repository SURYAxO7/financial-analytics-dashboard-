-- ============================================================
-- Financial Analytics Dashboard — Views for Tableau
-- Run AFTER 01, 03 and 04 (tables must exist and contain data).
-- Tableau Desktop connects to these two views (or the raw tables).
-- ============================================================

USE finance_dashboard;

-- View 1: transaction-level detail (used for revenue, expense, category, department visuals)
CREATE OR REPLACE VIEW vw_transactions AS
SELECT
    transaction_id,
    `date`,
    DATE_FORMAT(`date`, '%Y-%m') AS month_label,
    department,
    `type`,
    category,
    amount
FROM transactions;

-- View 2: budget vs actual at month x department x type grain.
-- Actuals are summed FIRST, then joined to budget, so budget numbers are never
-- double-counted (joining raw transactions to budget would multiply budget rows).
CREATE OR REPLACE VIEW vw_budget_vs_actual AS
SELECT
    b.`date`,
    b.department,
    b.`type`,
    COALESCE(a.actual_amount, 0)                      AS actual_amount,
    b.budgeted_amount,
    COALESCE(a.actual_amount, 0) - b.budgeted_amount  AS variance
FROM budget b
LEFT JOIN (
    SELECT `date`, department, `type`, SUM(amount) AS actual_amount
    FROM transactions
    GROUP BY `date`, department, `type`
) a
    ON  a.`date`     = b.`date`
    AND a.department = b.department
    AND a.`type`     = b.`type`;

-- Quick checks (run these after creating the views)
SELECT COUNT(*) AS rows_in_vw_transactions FROM vw_transactions;     -- expect 469
SELECT COUNT(*) AS rows_in_vw_budget_vs_actual FROM vw_budget_vs_actual;  -- expect 288
