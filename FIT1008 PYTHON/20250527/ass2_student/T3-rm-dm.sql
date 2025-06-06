--****PLEASE ENTER YOUR DETAILS BELOW****
--T3-rm-dm.sql

--Student ID: 
--Student Name:

/* Comments for your marker:




*/

--(a)
DROP SEQUENCE competitor_seq;
DROP SEQUENCE team_seq;

CREATE SEQUENCE competitor_seq START with 100 increment by 5;
CREATE SEQUENCE team_seq START with 100 increment by 5;

commit;
--(b)
--Keith Rose
insert into COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    competitor_seq.NEXTVAL,
    'Keith',
    'Rose',
    'F',
    TO_DATE('31/JAN/2005','DD/MON/YYYY'),
    'keithrose@gmail.com',
    'Y',
    '0422141112'
);

insert into ENTRY (
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    (select event_id from EVENT
        where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
        and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run')
    ),
    99,
    TO_DATE('08:00:00','hh24:mi:ss'),
    NULL,
    NULL,
    competitor_seq.CURRVAL,
    NULL,
    (Select char_id from CHARITY where char_name = 'Salvation Army')
);

INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
) VALUES (
    team_seq.NEXTVAL,
    'Super Runners',
    (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025'),
    (select event_id from EVENT
        where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
        and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run')
    ),
    99
);

update ENTRY
set team_id = team_seq.CURRVAL
where event_id = 
(select event_id from EVENT
        where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
        and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run')
    )
and entry_no = 99;

--Jackson Bull
insert into COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    competitor_seq.NEXTVAL,
    'Jackson',
    'Bull',
    'M',
    TO_DATE('15/MAR/2004','DD/MON/YYYY'),
    'jacksonbull@gmail.com',
    'Y',
    '0422412524'
);

insert into ENTRY (
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    (select event_id from EVENT
        where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
        and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run')
    ),
    77,
    TO_DATE('08:00:00','hh24:mi:ss'),
    NULL,
    NULL,
    competitor_seq.CURRVAL,
    team_seq.CURRVAL,
    (Select char_id from CHARITY where char_name = 'RSPCA')
);
--(c)
update ENTRY
set event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run')
)
, entry_no = 
(select NVL(MAX(entry_no),0) + 1 from ENTRY
    where event_id = 
    (select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run')
))
, char_id = (Select char_id from CHARITY where char_name = 'Beyond Blue')
where --comp_no = (select comp_no from COMPETITOR where comp_phone = '0422412524')
event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run'))
and entry_no = 77;

commit;
--(d)
update ENTRY
set team_id = NULL
where
event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run'))
and entry_no = (select entry_no from ENTRY where
comp_no = (select comp_no from COMPETITOR where comp_phone = '0422412524')
and event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '5 km run')));
commit;

update ENTRY
set team_id = NULL
where
event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run'))
and entry_no = 99;
commit;


delete from TEAM
where team_name = 'Super Runners'
and carn_date = (select carn_date from CARNIVAL where UPPER(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
and event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run'));

commit;



delete from ENTRY
where --comp_no = (select comp_no from COMPETITOR where comp_phone = '0422141112')
event_id = 
(select event_id from EVENT
    where carn_date = (select carn_date from CARNIVAL where upper(carn_name) = 'RM WINTER SERIES CAULFIELD 2025')
    and eventtype_code = (select eventtype_code from EVENTTYPE where LOWER(eventtype_desc) = '10 km run'))
and entry_no = 99;
commit;