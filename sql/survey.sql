set @_today=(select curdate());
set @_yesterday=(select date_sub(curdate(), interval 1 DAY));
set @_5days=(select date_sub(curdate(), interval 5 DAY));
set @_10days=(select date_sub(curdate(), interval 10 DAY));
set @_30days=(select date_sub(curdate(), interval 30 DAY));
set @_60days=(select date_sub(curdate(), interval 60 DAY));
set @_90days=(select date_sub(curdate(), interval 90 DAY));
set @_120days=(select date_sub(curdate(), interval 120 DAY));

#set @_startdate='2014-10-31 02:14:09'

drop table if exists zz_survey;

create table zz_survey ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' DEFAULT CHARSET=utf8 select survey_response_id as id,rel_user_id as user_id,msisdn,device,created from p_survey_response where created >'2014-07-31';# 02:14:09';# and created < '2014-05-01';# @_90days;
alter table zz_survey add COLUMN a1 varchar(255), add COLUMN a2 varchar(255), add COLUMN a3 varchar(255), add COLUMN a4 varchar(255), add COLUMN a5 varchar(255);
update zz_survey as s inner join (select rel_survey_response_id as id,answer from p_survey_response_answer where answer_id=1) as aa using (id) SET s.a1=aa.answer;
update zz_survey as s inner join (select rel_survey_response_id as id,answer from p_survey_response_answer where answer_id=2) as aa using (id) SET s.a2=aa.answer;
update zz_survey as s inner join (select rel_survey_response_id as id,answer from p_survey_response_answer where answer_id=3) as aa using (id) SET s.a3=aa.answer;
update zz_survey as s inner join (select rel_survey_response_id as id,answer from p_survey_response_answer where answer_id=4) as aa using (id) SET s.a4=aa.answer;
update zz_survey as s inner join (select rel_survey_response_id as id,answer from p_survey_response_answer where answer_id=5) as aa using (id) SET s.a5=aa.answer;

select count(distinct msisdn,a2) from zz_survey;
#select distinct week(created) date,msisdn,a2 from zz_survey where (a2 like '%lent%' and not a2 like '%exelente%') or a2 like '%demo%' or a2 like '%veloci%' or a2 like '%tard%' or a2 like '%rapid%' or a2 like '% despac%' ;
select week(created)date,count(*) answers_per_week from zz_survey group by date with rollup;

select * from zz_survey order by created desc limit 10;
