/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T2-rm-insert.sql

--Student ID: 34550720
--Student Name: Haouxan Zhang

/* Comments for your marker:




*/

-- Task 2 Load the COMPETITOR, ENTRY and TEAM tables with your own
-- test data following the data requirements expressed in the brief

-- =======================================
-- COMPETITOR
-- =======================================
INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    1,
    'Jim',
    'Lu',
    'M',
    TO_DATE('12/SEP/2004','DD/MON/YYYY'),
    'jimlu@gmail.com',
    'Y',
    '0100456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    2,
    'Jack',
    'Hao',
    'M',
    TO_DATE('15/FEB/2004','DD/MON/YYYY'),
    'jackhao@gmail.com',
    'N',
    '0120456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    3,
    'Hollys',
    'Wen',
    'M',
    TO_DATE('26/FEB/2004','DD/MON/YYYY'),
    'hollyswen@gmail.com',
    'N',
    '0130456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    11,
    'Hans',
    'Miao',
    'M',
    TO_DATE('23/JUN/2005','DD/MON/YYYY'),
    'hansmiao@gmail.com',
    'N',
    '0290456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    4,
    'Zonghan',
    'Yang',
    'M',
    TO_DATE('29/MAR/2004','DD/MON/YYYY'),
    'zonghanyang@gmail.com',
    'Y',
    '0140456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    5,
    'Toby',
    'Li',
    'M',
    TO_DATE('04/APR/2004','DD/MON/YYYY'),
    'tobyli@gmail.com',
    'N',
    '0150456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    6,
    'Fred',
    'Cheng',
    'U',
    TO_DATE('07/MAY/2004','DD/MON/YYYY'),
    'fredcheng@gmail.com',
    'Y',
    '0160456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    7,
    'Kaiwei',
    'Sun',
    'U',
    TO_DATE('23/JAN/2004','DD/MON/YYYY'),
    'kaiweisun@gmail.com',
    'N',
    '0170456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    8,
    'Haoxuan',
    'Zhang',
    'M',
    TO_DATE('19/JUL/2005','DD/MON/YYYY'),
    'haoxuanzhang@gmail.com',
    'Y',
    '0180456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    9,
    'Shane',
    'Xu',
    'M',
    TO_DATE('14/NOV/2004','DD/MON/YYYY'),
    'shanexu@gmail.com',
    'N',
    '0190456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    10,
    'Ben',
    'Li',
    'M',
    TO_DATE('26/FEB/2005','DD/MON/YYYY'),
    'benli@gmail.com',
    'Y',
    '0200456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    20,
    'Stella',
    'Lei',
    'F',
    TO_DATE('29/AUG/2004','DD/MON/YYYY'),
    'leizi@gmail.com',
    'Y',
    '0210456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    30,
    'Rose',
    'Li',
    'F',
    TO_DATE('26/DEC/2004','DD/MON/YYYY'),
    'roseli@gmail.com',
    'N',
    '0220456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    40,
    'Della',
    'Tian',
    'F',
    TO_DATE('26/FEB/2004','DD/MON/YYYY'),
    'dellatian@gmail.com',
    'N',
    '0230456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    52,
    'Yiling',
    'Yan',
    'F',
    TO_DATE('13/MAY/2004','DD/MON/YYYY'),
    'yanyiying@gmail.com',
    'Y',
    '0240456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    60,
    'Sylvia',
    'Yu',
    'F',
    TO_DATE('26/MAR/2002','DD/MON/YYYY'),
    'sylviayu@gmail.com',
    'Y',
    '0250456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    70,
    'Tristy',
    'Hong',
    'F',
    TO_DATE('21/JAN/2005','DD/MON/YYYY'),
    'tristyhong@gmail.com',
    'Y',
    '0260456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    80,
    'Harper',
    'wang',
    'F',
    TO_DATE('18/JUN/2006','DD/MON/YYYY'),
    'wangcongwen@gmail.com',
    'N',
    '0270456789' );

INSERT INTO COMPETITOR (
    comp_no,
    comp_fname,
    comp_lname,
    comp_gender,
    comp_dob,
    comp_email,
    comp_unistatus,
    comp_phone
) VALUES (
    90,
    'Cholin',
    'Zhou',
    'U',
    TO_DATE('26/OCT/2004','DD/MON/YYYY'),
    'cholinzhou@gmail.com',
    'Y',
    '0280456789' );

COMMIT;

-- =======================================
-- ENTRY
-- =======================================
INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    1,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:45:00','hh24:mi:ss'),
    TO_DATE('01:00:00','hh24:mi:ss'),
    1,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    2,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:44:00','hh24:mi:ss'),
    TO_DATE('00:59:00','hh24:mi:ss'),
    2,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    3,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:43:00','hh24:mi:ss'),
    TO_DATE('00:58:00','hh24:mi:ss'),
    3,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    4,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:42:00','hh24:mi:ss'),
    TO_DATE('00:57:00','hh24:mi:ss'),
    4,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    5,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:44:00','hh24:mi:ss'),
    TO_DATE('00:59:00','hh24:mi:ss'),
    5,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    6,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:40:00','hh24:mi:ss'),
    TO_DATE('00:55:00','hh24:mi:ss'),
    6,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    7,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:35:00','hh24:mi:ss'),
    TO_DATE('00:50:00','hh24:mi:ss'),
    7,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    8,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:50:00','hh24:mi:ss'),
    TO_DATE('01:05:00','hh24:mi:ss'),
    8,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    9,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:55:00','hh24:mi:ss'),
    TO_DATE('01:10:00','hh24:mi:ss'),
    9,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    10,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:39:00','hh24:mi:ss'),
    TO_DATE('00:54:00','hh24:mi:ss'),
    10,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    11,
    TO_DATE('09:45:00','hh24:mi:ss'),
    TO_DATE('10:50:00','hh24:mi:ss'),
    TO_DATE('01:05:00','hh24:mi:ss'),
    20,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    1,
    12,
    TO_DATE('09:45:00','hh24:mi:ss'),
    NULL,
    NULL,
    30,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    1,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:50:00','hh24:mi:ss'),
    TO_DATE('02:20:00','hh24:mi:ss'),
    1,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    2,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:45:00','hh24:mi:ss'),
    TO_DATE('02:15:00','hh24:mi:ss'),
    2,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    3,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:40:00','hh24:mi:ss'),
    TO_DATE('02:10:00','hh24:mi:ss'),
    3,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    4,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:50:00','hh24:mi:ss'),
    TO_DATE('02:20:00','hh24:mi:ss'),
    4,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    5,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:20:00','hh24:mi:ss'),
    TO_DATE('01:50:00','hh24:mi:ss'),
    5,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    4,
    6,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:49:00','hh24:mi:ss'),
    TO_DATE('02:19:00','hh24:mi:ss'),
    10,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    1,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('12:20:00','hh24:mi:ss'),
    TO_DATE('04:20:00','hh24:mi:ss'),
    1,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    2,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('12:00:00','hh24:mi:ss'),
    TO_DATE('04:00:00','hh24:mi:ss'),
    2,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    3,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('12:30:00','hh24:mi:ss'),
    TO_DATE('04:30:00','hh24:mi:ss'),
    3,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    4,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('11:40:00','hh24:mi:ss'),
    TO_DATE('03:40:00','hh24:mi:ss'),
    6,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    5,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('12:01:00','hh24:mi:ss'),
    TO_DATE('04:01:00','hh24:mi:ss'),
    5,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    9,
    6,
    TO_DATE('08:00:00','hh24:mi:ss'),
    NULL,
    NULL,
    20,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    2,
    1,
    TO_DATE('08:30:00','hh24:mi:ss'),
    TO_DATE('10:11:00','hh24:mi:ss'),
    TO_DATE('01:41:00','hh24:mi:ss'),
    60,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    7,
    5,
    TO_DATE('08:40:00','hh24:mi:ss'),
    TO_DATE('09:59:00','hh24:mi:ss'),
    TO_DATE('01:19:00','hh24:mi:ss'),
    7,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    8,
    5,
    TO_DATE('08:00:00','hh24:mi:ss'),
    TO_DATE('10:01:00','hh24:mi:ss'),
    TO_DATE('02:01:00','hh24:mi:ss'),
    5,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    8,
    8,
    TO_DATE('08:00:00','hh24:mi:ss'),
    NULL,
    NULL,
    40,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    11,
    6,
    TO_DATE('07:45:00','hh24:mi:ss'),
    TO_DATE('19:45:00','hh24:mi:ss'),
    TO_DATE('12:00:00','hh24:mi:ss'),
    70,
    NULL,
    4 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    11,
    1,
    TO_DATE('07:45:00','hh24:mi:ss'),
    TO_DATE('15:45:00','hh24:mi:ss'),
    TO_DATE('08:00:00','hh24:mi:ss'),
    1,
    NULL,
    3 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    11,
    89,
    TO_DATE('07:45:00','hh24:mi:ss'),
    TO_DATE('14:45:00','hh24:mi:ss'),
    TO_DATE('7:00:00','hh24:mi:ss'),
    2,
    NULL,
    2 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    11,
    34,
    TO_DATE('07:45:00','hh24:mi:ss'),
    NULL,
    NULL,
    3,
    NULL,
    1 );

INSERT INTO ENTRY(
    event_id,
    entry_no,
    entry_starttime,
    entry_finishtime,
    entry_elapsedtime,
    comp_no,
    team_id,
    char_id
) VALUES (
    11,
    44,
    TO_DATE('07:45:00','hh24:mi:ss'),
    TO_DATE('13:45:00','hh24:mi:ss'),
    TO_DATE('06:00:00','hh24:mi:ss'),
    4,
    NULL,
    4 );

COMMIT;


-- =======================================
-- TEAM
-- =======================================
INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
)
VALUES (
    1,
    'LZTXDY',
    TO_DATE('22/SEP/2024','DD/MON/YYYY'),
    1,
    1
);

INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
)
VALUES (
    2,
    'Red',
    TO_DATE('22/SEP/2024','DD/MON/YYYY'),
    1,
    2
);

INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
)
VALUES (
    3,
    'Orange',
    TO_DATE('05/OCT/2024','DD/MON/YYYY'),
    4,
    1
);

INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
)
VALUES (
    4,
    'LZTXDY',
    TO_DATE('15/MAR/2025','DD/MON/YYYY'),
    11,
    1
);

INSERT INTO TEAM (
    team_id,
    team_name,
    carn_date,
    event_id,
    entry_no
)
VALUES (
    5,
    'Yellow',
    TO_DATE('15/MAR/2025','DD/MON/YYYY'),
    11,
    6
);

UPDATE ENTRY
SET team_id = 1
WHERE event_id = 1 AND entry_no IN (1, 3, 6, 9);

UPDATE ENTRY
SET team_id = 2
WHERE event_id = 1 AND entry_no IN (2, 4);

UPDATE ENTRY
SET team_id = 3
WHERE event_id = 4 AND entry_no IN (1, 2, 3);

UPDATE ENTRY
SET team_id = 4
WHERE event_id = 11 AND entry_no IN (1, 6, 34);

UPDATE ENTRY
SET team_id = 5
WHERE event_id = 11 AND entry_no IN (44, 89);

COMMIT;
