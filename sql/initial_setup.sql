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

CREATE FUNCTION get_users_risk_level(user_id BIGINT) RETURNS int AS
    $BODY$
        SELECT risk_level FROM users WHERE user_id = $1;
    $BODY$
LANGUAGE SQL STABLE SECURITY DEFINER;
