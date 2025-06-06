--****PLEASE ENTER YOUR DETAILS BELOW****
--T4-rm-mods.sql

--Student ID:
--Student Name:

/* Comments for your marker:




*/

--(a)
ALTER TABLE COMPETITOR ADD comp_completed_events NUMBER(3);

COMMENT ON COLUMN COMPETITOR.comp_completed_events IS
    'Number of events this competitor has finished (entry_finishtime IS NOT NULL)';

update COMPETITOR c
   SET comp_completed_events = (
         select COUNT(*)
           from entry e
          where e.comp_no = c.comp_no
            and e.entry_finishtime IS NOT NULL
        );

DESC COMPETITOR;

select comp_no,
       comp_fname || ' ' || comp_lname as full_name,
       comp_completed_events
from COMPETITOR
order by comp_no;

commit;



--(b)
DROP TABLE ENTRY_CHARITY CASCADE CONSTRAINTS PURGE;

CREATE TABLE ENTRY_CHARITY (
  event_id   NUMERIC(6) NOT NULL,
  entry_no   NUMERIC(5) NOT NULL,
  char_id    NUMERIC(3) NOT NULL,
  percentage NUMERIC(3) NOT NULL
);

ALTER TABLE ENTRY_CHARITY ADD CONSTRAINT entry_char_pk PRIMARY KEY (event_id, entry_no, char_id)

COMMENT ON COLUMN ENTRY_CHARITY.event_id IS
    'FK ENTRY(event_id)';

COMMENT ON COLUMN ENTRY_CHARITY.entry_no IS
    'FK ENTRY(entry_no)';

COMMENT ON COLUMN ENTRY_CHARITY.char_id IS
    'FK CHARITY(char_id)';

COMMENT ON COLUMN ENTRY_CHARITY.percentage IS
    'Percentage of funds for this charity';

ALTER TABLE ENTRY_CHARITY 
    ADD CONSTRAINT entry_char_entry_fk FOREIGN KEY (event_id, entry_no)
        REFERENCES ENTRY (event_id, entry_no);

ALTER TABLE ENTRY_CHARITY
    ADD CONSTRAINT entry_char_char_fk FOREIGN KEY (char_id)
        REFERENCES CHARITY (char_id);

INSERT INTO ENTRY_CHARITY (
    event_id,
    entry_no,
    char_id,
    percentage
) VALUES (
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run')
),
(SELECT e.entry_no 
    FROM ENTRY e
    JOIN COMPETITOR c 
    ON e.comp_no = c.comp_no
    JOIN EVENT ev 
    ON e.event_id = ev.event_id
    JOIN EVENTTYPE et
    ON ev.eventtype_code = et.eventtype_code
    JOIN CARNIVAL ca
    ON ev.carn_date = ca.carn_date
WHERE 
    LOWER(c.comp_fname || ' ' || c.comp_lname) = 'jackson bull'
    AND UPPER(ca.carn_name)             = 'RM WINTER SERIES CAULFIELD 2025'
    AND LOWER(et.eventtype_desc)       = '5 km run'),
(select char_id from CHARITY where char_name = 'RSPCA'),
70
);

INSERT INTO ENTRY_CHARITY (
    event_id,
    entry_no,
    char_id,
    percentage
) VALUES (
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run')
),
(SELECT e.entry_no 
    FROM ENTRY e
    JOIN COMPETITOR c 
    ON e.comp_no = c.comp_no
    JOIN EVENT ev 
    ON e.event_id = ev.event_id
    JOIN EVENTTYPE et
    ON ev.eventtype_code = et.eventtype_code
    JOIN CARNIVAL ca
    ON ev.carn_date = ca.carn_date
WHERE 
    LOWER(c.comp_fname || ' ' || c.comp_lname) = 'jackson bull'
    AND UPPER(ca.carn_name)             = 'RM WINTER SERIES CAULFIELD 2025'
    AND LOWER(et.eventtype_desc)       = '5 km run'),
(select char_id from CHARITY where char_name = 'Beyond Blue'),
30
);


DESC ENTRY_CHARITY;

SELECT event_id,
       entry_no,
       char_id,
       percentage
FROM ENTRY_CHARITY
ORDER BY event_id, entry_no, char_id;
