CREATE TABLE task_shares (
    task_id INTEGER NOT NULL REFERENCES tasks(id),
    email TEXT NOT NULL,
    PRIMARY KEY (task_id, email)
);
