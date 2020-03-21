CREATE TABLE reported_contacts (
    reporting_user BIGINT not null,
    contacted_user BIGINT not null,
    contact_time timestamp without time zone not null,
    PRIMARY KEY (reporting_user, contacted_user, contact_time)
);

CREATE FUNCTION report_contact(reporting_user BIGINT, contacted_user BIGINT, contact_time timestamp without time zone)
RETURNS VOID AS
    $BODY$
        INSERT INTO reported_contacts(reporting_user, contacted_user, contact_time)
        VALUES($1, $2, $3);
    $BODY$
LANGUAGE SQL VOLATILE SECURITY DEFINER;
