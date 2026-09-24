CREATE INDEX idx_tasks_created_by
ON tasks(created_by);

CREATE INDEX idx_tasks_assigned_to
ON tasks(assigned_to);

CREATE INDEX idx_tasks_status
ON tasks(status);

CREATE INDEX idx_tasks_due_date
ON tasks(due_date);