/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T6-rm-json.sql

--Student ID:
--Student Name:


/* Comments for your marker:




*/


-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT FOR THIS PART HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer

-- 生成每个参赛队伍的完整 JSON 数据
SELECT JSON_OBJECT(
  -- 队伍ID作为JSON的"_id"字段
  '_id' VALUE t.team_id,

  -- 嘉年华名称
  'carn_name' VALUE c.carn_name,

  -- 嘉年华日期，格式为"01-Jun-2025"
  'carn_date' VALUE TO_CHAR(c.carn_date, 'DD-Mon-YYYY'),

  -- 队伍名称
  'team_name' VALUE t.team_name,

  -- 队伍领队信息，作为嵌套的JSON对象
  'team_leader' VALUE JSON_OBJECT(
      -- 领队姓名（姓+名）
      'name' VALUE TRIM(LEADING ' ' FROM tm.comp_fname || ' ' || tm.comp_lname),
      -- 领队电话
      'phone' VALUE tm.comp_phone,
      -- 领队邮箱
      'email' VALUE tm.comp_email
  ),

  -- 队员人数：统计成员comp_no的数量
  'team_no_of_members' VALUE COUNT(members.comp_no),

  -- 队员详细信息数组，每个成员是一个JSON对象
  'team_members' VALUE JSON_ARRAYAGG(
      JSON_OBJECT(
        -- 队员姓名（姓+名），若为NULL则显示"-"
        'competitor_name' VALUE COALESCE(TRIM(members.comp_fname || ' ' || members.comp_lname), '-'),
        -- 队员电话，若为NULL则显示"-"
        'competitor_phone' VALUE COALESCE(members.comp_phone, '-'),
        -- 队员所参与的项目名称，若无则显示"-"
        'event_type' VALUE COALESCE(e.eventtype_desc, '-'),
        -- 报名编号，若无则显示"-"
        'entry_no' VALUE COALESCE(en.entry_no, '-'),
        -- 比赛开始时间，格式为"HH24:MI:SS"
        'starttime' VALUE TO_CHAR(en.entry_starttime, 'HH24:MI:SS'),
        -- 比赛结束时间，格式为"HH24:MI:SS"
        'finishtime' VALUE TO_CHAR(en.entry_finishtime, 'HH24:MI:SS'),
        -- 比赛耗时，格式为"HH24:MI:SS"
        'elapsedtime' VALUE TO_CHAR(en.entry_elapsedtime, 'HH24:MI:SS')
      )
  )
) AS team_json -- 整个JSON结果命名为 team_json

FROM team t
-- 将队伍表与领队信息表连接（通过队伍中的team_leader字段）
JOIN competitor tm ON t.team_leader = tm.comp_no

-- 连接嘉年华表，获取该队伍所属嘉年华的信息
JOIN carnival c ON t.carn_date = c.carn_date

-- 左连接队伍成员表，获取所有属于该队伍的成员
LEFT JOIN team_members tmembers ON t.team_id = tmembers.team_id

-- 左连接成员信息表，获取每位队员的详细资料
LEFT JOIN competitor members ON tmembers.comp_no = members.comp_no

-- 左连接报名信息表，获取成员在该队伍所属项目中的报名信息
LEFT JOIN entry en ON members.comp_no = en.comp_no AND en.event_id = t.event_id

-- 左连接比赛项目信息表，获取比赛项目名称
LEFT JOIN event e ON en.event_id = e.event_id

GROUP BY 
  t.team_id,        -- 按队伍ID分组
  c.carn_name,      -- 嘉年华名称
  c.carn_date,      -- 嘉年华日期
  t.team_name,      -- 队伍名称
  tm.comp_fname,    -- 领队名
  tm.comp_lname,    -- 领队姓
  tm.comp_phone,    -- 领队电话
  tm.comp_email     -- 领队邮箱




