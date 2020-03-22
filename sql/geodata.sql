CREATE TABLE geo_data
(
    user_id  BIGINT                      not null,
    lat      double precision            not null,
    lon      double precision            not null,
    gps_time timestamp without time zone not null
);

CREATE FUNCTION insert_geo_data(user_id BIGINT, lat double precision, lon double precision,
                                gps_time timestamp without time zone)
    RETURNS VOID AS
$BODY$ INSERT INTO geo_data(user_id, lat, lon, gps_time)
        VALUES($1, $2, $3, $4);
    $BODY$
    LANGUAGE SQL
    VOLATILE SECURITY DEFINER;

CREATE FUNCTION get_geo_data_after_timestamp(user_id BIGINT, time_thresh timestamp without time zone)
    RETURNS SETOF geo_data AS
$BODY$ SELECT * FROM geo_data WHERE user_id = $1 AND gps_time >= $2;
    $BODY$
    LANGUAGE SQL
    STABLE SECURITY DEFINER;

