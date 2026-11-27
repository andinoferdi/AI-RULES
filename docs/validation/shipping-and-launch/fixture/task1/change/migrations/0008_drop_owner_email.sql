-- The owner's email is now read from users; the copy on tasks is legacy.
ALTER TABLE tasks DROP COLUMN owner_email;
