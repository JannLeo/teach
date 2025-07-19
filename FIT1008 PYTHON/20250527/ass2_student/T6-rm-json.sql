/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T6-rm-json.sql

--Student ID: 34550720
--Student Name: Haouxan Zhang


/* Comments for your marker:




*/


-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT FOR THIS PART HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer
select JSON_OBJECT(
         '_id' value t.team_id,
         'carn_name' value c.carn_name,
         'carn_date' value TO_CHAR(ev.carn_date,'DD-Mon-YYYY'),
         'team_leader' value JSON_OBJECT(
                                        'name' value competitorleader.comp_fname || case when competitorleader.comp_fname is NULL then '' else ' ' end || competitorleader.comp_lname,
                                        'phone' value competitorleader.comp_phone,
                                        'email' value TO_CHAR(competitorleader.comp_email)) FORMAT JSON,
         'team_no_of_members' value COUNT(DISTINCT entrymember.comp_no),
         'team_members' value JSON_ARRAYAGG(
                                   JSON_OBJECT(
                                    'competitor_name' value competitormember.comp_fname || case when competitormember.comp_fname is NULL then '' else ' ' end || competitormember.comp_lname,
                                    'competitor_phone' value competitormember.comp_phone,
                                    'entry_no' value entrymember.entry_no,
                                    'starttime' value entrymember.entry_starttime,
                                    'finishtime' value case when entrymember.entry_finishtime is NULL then '-' else entrymember.entry_finishtime end,
                                    'elapsedtime' value case when entrymember.entry_elapsedtime is NULL then '-' else entrymember.entry_elapsedtime end) FORMAT JSON) FORMAT JSON) || ','
from team t
join event ev
on t.event_id = ev.event_id
and t.carn_date = ev.carn_date
join carnival c
on ev.carn_date = c.carn_date
join entry entryleader
on t.event_id = entryleader.event_id
and t.entry_no = entryleader.entry_no
join competitor competitorleader
on entryleader.comp_no = competitorleader.comp_no
left join entry entrymember
on t.team_id = entrymember.team_id
left join competitor competitormember
on entrymember.comp_no = competitormember.comp_no
group by
t.team_id,
c.carn_name,
ev.carn_date,
competitorleader.comp_fname,
competitorleader.comp_lname,
competitorleader.comp_phone,
competitorleader.comp_email;