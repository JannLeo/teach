/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T1-rm-schema.sql

--Student ID: 34550720
--Student Name: Haouxan Zhang

/* Comments for your marker:




*/

/* drop table statements - do not remove*/

DROP TABLE competitor CASCADE CONSTRAINTS PURGE;

DROP TABLE entry CASCADE CONSTRAINTS PURGE;

DROP TABLE team CASCADE CONSTRAINTS PURGE;

/* end of drop table statements*/

-- Task 1 Add Create table statements for the Missing TABLES below.
-- Ensure all column comments, and constraints (other than FK's)are included.
-- FK constraints are to be added at the end of this script

-- COMPETITOR
CREATE TABLE COMPETITOR (
    comp_no        NUMERIC(5) NOT NULL,
    comp_fname     VARCHAR2(30),
    comp_lname     VARCHAR2(30),
    comp_gender    CHAR(1) NOT NULL,
    comp_dob       DATE NOT NULL,
    comp_email     VARCHAR2(50) NOT NULL,
    comp_unistatus CHAR(1) NOT NULL,
    comp_phone     CHAR(10) NOT NULL
);

COMMENT ON COLUMN COMPETITOR.comp_no IS
    'Unique identifier for a competitor';

COMMENT ON COLUMN COMPETITOR.comp_fname IS
    'Competitor''s first name';

COMMENT ON COLUMN COMPETITOR.comp_lname IS
    'Competitor''s last name';

COMMENT ON COLUMN COMPETITOR.comp_gender IS
    'Competitor''s gender (''M'' for male, ''F'' for female, or ''U'' for ''Undisclosed'')';

COMMENT ON COLUMN COMPETITOR.comp_dob IS
    'Competitor''s date of birth';

COMMENT ON COLUMN COMPETITOR.comp_email IS
    'Competitor''s email - unique for each competitor';

COMMENT ON COLUMN COMPETITOR.comp_unistatus IS
    'Competitor is a university student or staff (''Y'' for Yes or ''N'' for No)';

COMMENT ON COLUMN COMPETITOR.comp_phone IS
    'Competitor''s phone number - unique for each competitor';

ALTER TABLE COMPETITOR ADD CONSTRAINT competitor_pk PRIMARY KEY (comp_no);

ALTER TABLE COMPETITOR ADD CONSTRAINT competitor_ck_gender CHECK (comp_gender IN ('M','F','U'));

ALTER TABLE COMPETITOR ADD CONSTRAINT competitor_ck_unistatus CHECK (comp_unistatus IN ('Y','N'));

ALTER TABLE COMPETITOR ADD CONSTRAINT competitor_nk_email UNIQUE (comp_email);

ALTER TABLE COMPETITOR ADD CONSTRAINT competitor_nk_phone UNIQUE (comp_phone);

COMMIT;

--ENTRY
CREATE TABLE ENTRY (
    event_id           NUMERIC(6) NOT NULL,
    entry_no           NUMERIC(5) NOT NULL,
    entry_starttime    DATE,
    entry_finishtime   DATE,
    entry_elapsedtime  DATE,
    comp_no            NUMERIC(5) NOT NULL,
    team_id            NUMERIC(3),
    char_id            NUMERIC(3)
);

COMMENT ON COLUMN ENTRY.event_id IS
    'Event id (foreign key)';

COMMENT ON COLUMN ENTRY.entry_no IS
    'Entry number (unique only within an event)';

COMMENT ON COLUMN ENTRY.entry_starttime IS
    'The entrant''s start time (time only), stored using the format of hh24:mi:ss';

COMMENT ON COLUMN ENTRY.entry_finishtime IS
    'The entrant''s finish time (time only), stored using the format of hh24:mi:ss';

COMMENT ON COLUMN ENTRY.entry_elapsedtime IS
    'The time the entrant took to complete the event, stored using the format of hh24:mi:ss
     (e.g. 01:25:30 for 1 hour 25 minutes and 30 seconds)';

COMMENT ON COLUMN ENTRY.comp_no IS
    'identifier for a competitor (foreign key)';

COMMENT ON COLUMN ENTRY.team_id IS
    'Team identifier (foreign key)';

COMMENT ON COLUMN ENTRY.char_id IS
    'Charity identifier (foreign key)';

ALTER TABLE ENTRY ADD CONSTRAINT entry_pk PRIMARY KEY (event_id, entry_no);

COMMIT;

--TEAM
CREATE TABLE TEAM (
    team_id    NUMERIC(3) NOT NULL,
    team_name  VARCHAR2(30) NOT NULL,
    carn_date  DATE NOT NULL,
    event_id   NUMERIC(6) NOT NULL,
    entry_no   NUMERIC(5) NOT NULL
);

COMMENT ON COLUMN TEAM.team_id IS
    'Team identifier (unique)';

COMMENT ON COLUMN TEAM.team_name IS
    'Team name';

COMMENT ON COLUMN TEAM.carn_date IS
    'Date of carnival (foreign key)';

COMMENT ON COLUMN TEAM.event_id IS
    'Event id (foreign key)';

COMMENT ON COLUMN TEAM.entry_no IS
    'Entry number (foreign key)';

ALTER TABLE TEAM ADD CONSTRAINT team_pk PRIMARY KEY (team_id);

ALTER TABLE TEAM ADD CONSTRAINT team_nk UNIQUE (team_name, carn_date);

COMMIT;

-- Add all missing FK Constraints below here

ALTER TABLE ENTRY
    ADD CONSTRAINT entry_comp_fk FOREIGN KEY (comp_no)
        REFERENCES COMPETITOR (comp_no);

ALTER TABLE ENTRY
    ADD CONSTRAINT entry_team_fk FOREIGN KEY (team_id)
    REFERENCES TEAM (team_id);

ALTER TABLE ENTRY
    ADD CONSTRAINT entry_char_fk FOREIGN KEY (char_id)
        REFERENCES CHARITY (char_id);

ALTER TABLE ENTRY
    ADD CONSTRAINT entry_event_fk FOREIGN KEY (event_id)
        REFERENCES EVENT (event_id);

ALTER TABLE TEAM
    ADD CONSTRAINT team_carn_fk FOREIGN KEY (carn_date)
        REFERENCES CARNIVAL (carn_date);

ALTER TABLE TEAM
    ADD CONSTRAINT team_entry_fk FOREIGN KEY (event_id, entry_no)
        REFERENCES ENTRY (event_id, entry_no);

COMMIT;