CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    risk_level int not null
);

CREATE FUNCTION insert_user() RETURNS BIGINT AS
    $BODY$
        INSERT INTO users(risk_level)
        VALUES(0)
        RETURNING user_id;
    $BODY$
LANGUAGE SQL VOLATILE SECURITY DEFINER;
