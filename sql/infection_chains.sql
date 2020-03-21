CREATE TABLE contact_chains
(
    reporting_user          BIGINT                      not null,
    report_user_curr_level  int                         not null,
    contacted_user          BIGINT                      not null,
    contact_user_curr_level int                         not null,
    contact_time            timestamp without time zone not null,
    relevance_factor        double precision            not null,
    PRIMARY KEY (reporting_user, contacted_user, contact_time)
);

CREATE FUNCTION report_contact(reporting_user BIGINT, contacted_user BIGINT, contact_time timestamp without time zone,
                               relevance_factor double precision)
    RETURNS VOID AS
$BODY$
INSERT INTO contact_chains(reporting_user, report_user_curr_level, contacted_user, contact_user_curr_level,
                           contact_time, relevance_factor)
VALUES ($1, (SELECT risk_level FROM users WHERE user_id = $1), $2, (SELECT risk_level FROM users WHERE user_id = $2),
        $3, $4);
$BODY$
    LANGUAGE SQL VOLATILE
                 SECURITY DEFINER;
