CREATE FUNCTION get_users_by_risk_level(risk_level int) RETURNS SETOF BIGINT AS
$BODY$
SELECT user_id
FROM users
WHERE risk_level = $1;
$BODY$
    LANGUAGE SQL STABLE
                 SECURITY DEFINER;

CREATE FUNCTION get_contacts_after_timestamp(user_id BIGINT, time_thresh timestamp without time zone)
    RETURNS SETOF contact_chains AS
$BODY$
SELECT *
FROM contact_chains
WHERE reporting_user = $1
  AND contact_time >= $2
ORDER BY contact_time;
$BODY$
    LANGUAGE SQL STABLE
                 SECURITY DEFINER;

CREATE FUNCTION get_users_below_risk_level(risk_level int) RETURNS SETOF users AS
$BODY$
SELECT *
FROM users
WHERE risk_level < $1;
$BODY$
    LANGUAGE SQL
    STABLE
    SECURITY DEFINER;
