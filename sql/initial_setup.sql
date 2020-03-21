CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    state text not null
);

CREATE FUNCTION insert_user() RETURNS BIGINT AS
    $BODY$
        INSERT INTO users(state)
        VALUES('healthy')
        RETURNING user_id;
    $BODY$
LANGUAGE SQL VOLATILE SECURITY DEFINER;
