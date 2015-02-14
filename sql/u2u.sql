set @_today=(select curdate());
set @_yesterday=(select date_sub(@_today, interval 1 DAY));
set @_10daysago=(select date_sub(@_today, interval 10 DAY));
set @_30daysago=(select date_sub(@_today, interval 30 DAY));
set @_60daysago=(select date_sub(@_today, interval 60 DAY));
set @_90daysago=(select date_sub(@_today, interval 90 DAY));
set @_180daysago=(select date_sub(@_today, interval 180 DAY));
#set @_startdate=(@_180daysago);
#set @_enddate=@_90daysago;
set @_startdate=(@_10daysago);
set @_enddate=@_today;

select 'U2U interval:',@_startdate,@_enddate;

drop table if exists zzu2u;
create table zzu2u (`user_id` bigint(20) unsigned NOT NULL,`date` datetime, msg int NOT NULL DEFAULT '0', pics int NOT NULL DEFAULT '0', convos int NOT NULL DEFAULT '0', UNIQUE KEY `user_id` (`user_id`,date)) ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' ;

insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_0 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_1 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_2 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_3 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_4 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_5 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_6 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_7 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_8 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_9 where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_a where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_b where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_c where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_d where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_e where created >= @_startdate and created < @_enddate;
select sleep(9); 
insert ignore into zzu2u (user_id,date) select distinct user_id,date(created) from plg.p_chat_message_f where created >= @_startdate and created < @_enddate;
select sleep(9); 

update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_0 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_1 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_2 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_3 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_4 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_5 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_6 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_7 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_8 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_9 where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_a where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_b where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_c where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_d where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_e where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 
update zzu2u as u inner join (select user_id, date(created) as date, count(*) as msg,count(distinct chat_id) as convos,count(if(image_id<>'',1,null)) as pics from plg.p_chat_message_f where created >= @_startdate and created < @_enddate group by user_id,date) as uu on u.user_id=uu.user_id and u.date=uu.date SET u.msg=uu.msg+u.msg,u.pics=uu.pics+u.pics,u.convos=uu.convos+u.convos;
select sleep(9); 


select * from zzu2u where date >= @_yesterday order by msg desc limit 20;
select * from zzu2u order by msg desc limit 20;

select date(date) as date, count(*) as users,sum(msg),sum(msg)/count(*) as ratioM2U from zzu2u group by date with rollup;

# Peak hours
select date(created)as dd,hour(created)as hh,count(*)*16 as msg,count(if(image_id <>'',1,null))*16 as img,count(if(image_id <>'',1,null))/count(*)*100 as ratio from  plg.p_chat_message_7 where created >= '2013-11-21' group by dd,hh order by msg desc limit 20;


