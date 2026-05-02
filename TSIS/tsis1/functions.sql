CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name, -- Теперь база найдет "g", так как мы добавили JOIN ниже
        p.number AS phone,
        p.type AS phone_type
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id -- ЭТОЙ СТРОКИ НЕ ХВАТАЛО
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.number ILIKE '%' || p_query || '%';
END;
$$;