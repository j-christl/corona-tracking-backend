CREATE TABLE infected_users (
    user_id BIGINT not null references users,
    firstname text not null,
    lastname text not null,
    phonenumber text not null
);

CREATE FUNCTION update_user_state(user_id BIGINT, status text) RETURNS VOID AS
    $BODY$
        UPDATE users SET state = $2 WHERE user_id = $1;
    $BODY$
LANGUAGE SQL VOLATILE SECURITY DEFINER;

CREATE FUNCTION insert_infected(user_id BIGINT, firstname text, lastname text, phonenumber text) RETURNS VOID AS
    $BODY$
        INSERT INTO infected_users(user_id, firstname, lastname, phonenumber)
        VALUES($1, $2, $3, $4);
    $BODY$
LANGUAGE SQL VOLATILE SECURITY DEFINER;
