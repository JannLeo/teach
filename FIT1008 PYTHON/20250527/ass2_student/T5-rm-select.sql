/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T5-rm-select.sql

--Student ID: 34550720
--Student Name: Haouxan Zhang


/* Comments for your marker:




*/


/* (a) */
-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT FOR THIS PART HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer
select t.team_name,
    TO_CHAR(ca.carn_date, 'DD-MON-YYYY') as carn_date,
    c.comp_fname || case when c.comp_fname is null then '' else ' ' || c.comp_lname end as teamleader,
    COUNT(DISTINCT e2.comp_no) as team_no_members
from TEAM t
join CARNIVAL ca
on TO_DATE(t.carn_date, 'DD/MON/YYYY') = TO_DATE(ca.carn_date, 'DD/MON/YYYY')
join ENTRY e1
on e1.event_id = t.event_id and e1.entry_no = t.entry_no
join COMPETITOR c
on e1.comp_no = c.comp_no
left join entry e2
on e2.team_id = t.team_id
where t.team_name in 
(select team_name
from team
group by team_name
having count(*) = (select MAX(team_cnt) as max_cnt from (select team_name,
                                                         COUNT(*) as team_cnt from team group by team_name)))                                                        
group by
t.team_name,
ca.carn_date,
c.comp_fname,
c.comp_lname
order by
t.team_name,
ca.carn_date;





/* (b) */
-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT FOR THIS PART HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer



select et.eventtype_desc as "Event",
    ca.carn_name || ' held ' || TO_CHAR(ca.carn_date, 'DY DD-Mon-YYYY') as "Carnival",
    TO_CHAR(en.entry_elapsedtime, 'HH24:MI:SS') as "Current Record",
    c.comp_no || ' ' || c.comp_fname || CASE WHEN c.comp_fname IS NULL THEN '' ELSE ' ' end|| c.comp_lname as "Competitor No and Name",
    TRUNC((ca.carn_date  - c.comp_dob) / 365) as "Age at Carnival"
from ENTRY en
join EVENT ev
on en.event_id = ev.event_id
join EVENTTYPE et
on ev.eventtype_code = et.eventtype_code
join CARNIVAL ca
on TO_DATE(ev.carn_date, 'DD/MON/YYYY') = TO_DATE(ca.carn_date, 'DD/MON/YYYY')
join COMPETITOR c
on en.comp_no = c.comp_no
where en.entry_elapsedtime IS NOT NULL AND en.entry_elapsedtime = (select MIN(e2.entry_elapsedtime)
                                                                    from ENTRY e2
                                                                    join EVENT ev2
                                                                    on e2.event_id = ev2.event_id
                                                                    where ev2.eventtype_code = et.eventtype_code
                                                                    and e2.entry_elapsedtime IS NOT NULL)
order by
et.eventtype_desc,
c.comp_no;


/* (c) */
-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT FOR THIS PART HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer


select ca.carn_name as "Carnival Name",
    TO_CHAR(ca.carn_date, 'DD Mon YYYY') as "Carnival Date",
    et.eventtype_desc as "Event Description",
    case when NVL(en.entry_count, 0) = 0 then 'Not offered' else TO_CHAR(en.entry_count) end as "Number of Entries",
    case when NVL(en.entry_count,0) = 0 then '' else TO_CHAR(ROUND(en.entry_count / carnival_totals.carn_count * 100)) end as "% of Carnival Entries"
from carnival ca
cross join
eventtype et
left join (select
    	    ev.carn_date,
            ev.eventtype_code,
            COUNT(DISTINCT e.entry_no) as entry_count
            from event ev
            left join entry e
            on ev.event_id = e.event_id
            group by
            ev.carn_date,
            ev.eventtype_code) en
on en.carn_date = ca.carn_date
and en.eventtype_code = et.eventtype_code 
left join (select
            ev.carn_date,
            COUNT(DISTINCT e.entry_no) as carn_count
            from event ev
            left join entry e
            on ev.event_id = e.event_id
            group by
            ev.carn_date) carnival_totals
on carnival_totals.carn_date = ca.carn_date
order by
ca.carn_date,
et.eventtype_desc;
commit;