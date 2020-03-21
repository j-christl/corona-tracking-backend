CREATE FUNCTION get_users_by_risk_level(risk_level int) RETURNS SETOF BIGINT AS
$BODY$
SELECT user_id
FROM users
WHERE risk_level = $1;
$BODY$
    LANGUAGE SQL STABLE
                 SECURITY DEFINER;

CREATE FUNCTION get_contacts_after_timestamp(user_id BIGINT, time_thresh timestamp without time zone)
    RETURNS TABLE
            (
                user_id      BIGINT,
                contact_time timestamp without time zone
            )
AS
$BODY$
SELECT contacted_user, contact_time
FROM contact_chains
WHERE reporting_user = $1
  AND contact_time >= $2;
$BODY$
    LANGUAGE SQL STABLE
                 SECURITY DEFINER;
