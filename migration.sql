ALTER TABLE t_budgets
ADD COLUMN a_notify_status BOOLEAN NOT NULL DEFAULT 0 AFTER a_amount_spent;
