ALTER TABLE users
    ALTER COLUMN id DROP DEFAULT;

ALTER TABLE users
    ADD CONSTRAINT users_id_auth_fk
    FOREIGN KEY (id)
    REFERENCES auth.users(id)
    ON DELETE CASCADE;