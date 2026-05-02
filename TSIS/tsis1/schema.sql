CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(150),
    birthday DATE,
    group_id INT REFERENCES groups(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INT NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    number     VARCHAR(20) NOT NULL,
    type       VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, number)
);