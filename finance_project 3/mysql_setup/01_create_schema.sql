-- ============================================================
-- Financial Analytics Dashboard — MySQL Schema
-- Run this FIRST in MySQL Workbench (or CLI) before importing data
-- ============================================================

CREATE DATABASE IF NOT EXISTS finance_dashboard;
USE finance_dashboard;

DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    date DATE NOT NULL,
    department VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL
);

DROP TABLE IF EXISTS budget;
CREATE TABLE budget (
    budget_id INT PRIMARY KEY,
    date DATE NOT NULL,
    department VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    budgeted_amount DECIMAL(12,2) NOT NULL
);

-- Helpful indexes for the dashboard queries
CREATE INDEX idx_txn_date ON transactions(date);
CREATE INDEX idx_txn_dept ON transactions(department);
CREATE INDEX idx_txn_type ON transactions(type);
CREATE INDEX idx_budget_date ON budget(date);
CREATE INDEX idx_budget_dept ON budget(department);
