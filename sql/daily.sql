# daily requests

delete from smp_usage_log where usage_log_id < 575861319;

#select date(created) d ,count(*),count(distinct rel_user_id) as usr from smp_presence2 where type <> 14 and created >'2014-05-01' group by d with rollup;

set @_FRInterval=now() - interval 4 DAY;
SELECT "**************Friends requests in the last 4 DAY",@_FRInterval;
select date,count(*),count,sum(count) from smp.p_friendship_requests where date > @_FRInterval  group by date,count order by date desc;

select date,count(*),sum(msg) from zzu2u group by date order by date desc limit 10;

# Get how many users subscribe to ixSMS
SELECT "**************ixSMS";
select now(), count(distinct rel_user_id) as people_on_ixSMS ,count(distinct rel_user_id)/count(*) as avgFriends from smp_following;
select count(distinct id) as users,seen, count(*)/count(distinct id) as avg_friends from(select rel_user_id as id,date(last_seen) as seen from smp_following left join smp_user on rel_user_id = user_id) as T group by seen order by seen desc limit 15;

set @_today=(select curdate());
set @_10daysago=(select date_sub(curdate(), interval 10 DAY));
set @_30daysago=(select date_sub(curdate(), interval 30 DAY));
select date(joined) as date,count(if(state=1,1,null)) as newUsers,count(if(state=0,1,null)) as NR from smp_user where joined>@_10daysago and rel_operator_id=10 group by date with rollup;

# this query caused a disk exception!
# SELECT name as op,count(if(state=1,1,NULL)) as users, count(if(state=0,1,NULL)) as NR from smp_user left join smp_operator on rel_operator_id=operator_id where rel_operator_id in (10,14,15,16,19,20,21,24) group by op with rollup;

#
# SELECT "**************Campaigns";
# select rel_campaign_id as id,title,text, count(*) as sms,sent,count(distinct if(last_seen>'2012-07-13',recipient,NULL)) as seen,count(distinct if(state=1 and last_seen>'2012-07-13',recipient,NULL))/count(distinct recipient)*100 as success from smp_campaign_track left join smp_user on recipient=msisdn left join smp_campaign on rel_campaign_id=campaign_id where rel_campaign_id>211 group by rel_campaign_id;

set @_MAU10=(select count(*) from zzuser  where state=1 and last_seen > @_30daysago);
#set @_MAU10=(select count(distinct msisdn) from zzuserlog left join zzuser as u using(msisdn) where u.state=1 and time > @_30daysago and time < @_today);

select date(time) as date, count(distinct msisdn) as DAU, @_MAU10 as MAU, count(distinct msisdn)*100/@_MAU10 as dauMAU, count(distinct if(action=8,msisdn,NULL)) as newUsers, count(distinct if(action=11,msisdn,NULL)) as newSBUsers from zzuserlog left join zzuser as u using(msisdn) where u.state=1 and time>=curdate()-1 and time <@_today;

select 'dauMAU per day for Mexico';
select date(time) as date, count(distinct msisdn) as uniqueU, count(distinct if(action=8,msisdn,NULL)) as newUsers, count(distinct if(action=11,msisdn,NULL)) as newSBUsers,count(distinct msisdn)*100/@_MAU10 as dauMAU from zzuserlog left join zzuser as u using(msisdn) where u.state=1 and time>@_30daysago group by date;

#
SELECT "**************reg rate SMS";

select 
   count(distinct if(u.rel_operator_id=10,msisdn,NULL)) as SMSRegMx, 
   count(distinct if(u.rel_operator_id=15,msisdn,NULL)) as SMSRegCo, 
   count(distinct if(u.rel_operator_id=20,msisdn,NULL)) as SMSRegAr, 
   count(distinct if(u.rel_operator_id=19,msisdn,NULL)) as SMSRegPe, 
   count(distinct if(state=1 and u.rel_operator_id=10, msisdn,NULL))/count(distinct if(u.rel_operator_id=10,msisdn,NULL))*100 as rMx, 
   count(distinct if(state=1 and u.rel_operator_id=15, msisdn,NULL))/count(distinct if(u.rel_operator_id=15,msisdn,NULL))*100 as rCo,
   count(distinct if(state=1 and u.rel_operator_id=20, msisdn,NULL))/count(distinct if(u.rel_operator_id=20,msisdn,NULL))*100 as rAr,
   count(distinct if(state=1 and u.rel_operator_id=19, msisdn,NULL))/count(distinct if(u.rel_operator_id=19,msisdn,NULL))*100 as rPe 
   from smp_usage_log left join smp_user as u using(msisdn) where action=8 and device='sms';

select 
   count(distinct if(u.rel_operator_id=10,msisdn,NULL)) as SMSRegMx, 
   count(distinct if(u.rel_operator_id=15,msisdn,NULL)) as SMSRegCo, 
   count(distinct if(u.rel_operator_id=20,msisdn,NULL)) as SMSRegAr, 
   count(distinct if(u.rel_operator_id=19,msisdn,NULL)) as SMSRegPe, 
   count(distinct if(state=1 and u.rel_operator_id=10, msisdn,NULL))/count(distinct if(u.rel_operator_id=10,msisdn,NULL))*100 as rMx3Days, 
   count(distinct if(state=1 and u.rel_operator_id=15, msisdn,NULL))/count(distinct if(u.rel_operator_id=15,msisdn,NULL))*100 as rCo3Days,
   count(distinct if(state=1 and u.rel_operator_id=20, msisdn,NULL))/count(distinct if(u.rel_operator_id=20,msisdn,NULL))*100 as rAr3Days,
   count(distinct if(state=1 and u.rel_operator_id=19, msisdn,NULL))/count(distinct if(u.rel_operator_id=19,msisdn,NULL))*100 as rPe3Days 
   from smp_usage_log left join smp_user as u using(msisdn) where action=8 and device='sms' and time > (CURDATE() - INTERVAL 4 DAY) and time < (CURDATE() - INTERVAL 1 DAY);

SELECT "**************reg rate MMS";
select 
   count(distinct if(u.rel_operator_id=10,msisdn,NULL)) as MMSRegMx, 
   count(distinct if(u.rel_operator_id=15,msisdn,NULL)) as MMSRegCo, 
   count(distinct if(u.rel_operator_id=20,msisdn,NULL)) as MMSRegAr, 
   count(distinct if(u.rel_operator_id=19,msisdn,NULL)) as MMSRegPe, 
   count(distinct if(state=1 and u.rel_operator_id=10, msisdn,NULL))/count(distinct if(u.rel_operator_id=10,msisdn,NULL))*100 as rMx, 
   count(distinct if(state=1 and u.rel_operator_id=15, msisdn,NULL))/count(distinct if(u.rel_operator_id=15,msisdn,NULL))*100 as rCo,
   count(distinct if(state=1 and u.rel_operator_id=20, msisdn,NULL))/count(distinct if(u.rel_operator_id=20,msisdn,NULL))*100 as rAr,
   count(distinct if(state=1 and u.rel_operator_id=19, msisdn,NULL))/count(distinct if(u.rel_operator_id=19,msisdn,NULL))*100 as rPe 
   from smp_usage_log left join smp_user as u using(msisdn) where action=8 and device='mms';

select 
   count(distinct if(u.rel_operator_id=10,msisdn,NULL)) as MMSRegMx, 
   count(distinct if(u.rel_operator_id=15,msisdn,NULL)) as MMSRegCo, 
   count(distinct if(u.rel_operator_id=20,msisdn,NULL)) as MMSRegAr, 
   count(distinct if(u.rel_operator_id=19,msisdn,NULL)) as MMSRegPe, 
   count(distinct if(state=1 and u.rel_operator_id=10, msisdn,NULL))/count(distinct if(u.rel_operator_id=10,msisdn,NULL))*100 as rMx3Days, 
   count(distinct if(state=1 and u.rel_operator_id=15, msisdn,NULL))/count(distinct if(u.rel_operator_id=15,msisdn,NULL))*100 as rCo3Days,
   count(distinct if(state=1 and u.rel_operator_id=20, msisdn,NULL))/count(distinct if(u.rel_operator_id=20,msisdn,NULL))*100 as rAr3Days,
   count(distinct if(state=1 and u.rel_operator_id=19, msisdn,NULL))/count(distinct if(u.rel_operator_id=19,msisdn,NULL))*100 as rPe3Days 
   from smp_usage_log left join smp_user as u using(msisdn) where action=8 and device='mms' and time > (CURDATE() - INTERVAL 4 DAY) and time < (CURDATE() - INTERVAL 1 DAY);


select date(time) as date,count(distinct msisdn) as MMSsubs, count(distinct if(state=1, msisdn,NULL))/count(distinct msisdn)*100 as rate from zzuserlog left join smp_user as u using(msisdn) where action=8 and u.rel_operator_id=10 and device='mms' group by date(time);
select date(time) as date,count(distinct msisdn) as SMSsubs, count(distinct if(state=1, msisdn,NULL))/count(distinct msisdn)*100 as rate from zzuserlog left join smp_user as u using(msisdn) where action=8 and u.rel_operator_id=10 and device='sms' group by date(time);
select date(time) as date,count(distinct msisdn) as MMSsubsPe, count(distinct if(state=1, msisdn,NULL))/count(distinct msisdn)*100 as rate from zzuserlog left join smp_user as u using(msisdn) where action=8 and u.rel_operator_id=19 and device='mms' group by date(time);
#select count(distinct msisdn) as SMSsubsPe, count(distinct if(state=1, msisdn,NULL))/count(distinct msisdn)*100 as rate from smp_usage_log left join smp_user as u using(msisdn) where action=8 and u.rel_operator_id=19 and device='sms';

SELECT "**************RETENTION";

select
count(*) as newUsers,
count(if(last_seen>CURDATE() - INTERVAL 7 WEEK,msisdn,NULL))/count(*)*100 as 1week,
count(if(last_seen>CURDATE() - INTERVAL 6 WEEK,msisdn,NULL))/count(*)*100 as 2weeks,
count(if(last_seen>CURDATE() - INTERVAL 5 WEEK,msisdn,NULL))/count(*)*100 as 3weeks,
count(if(last_seen>CURDATE() - INTERVAL 4 WEEK,msisdn,NULL))/count(*)*100 as 4weeks,
count(if(last_seen>CURDATE() - INTERVAL 3 WEEK,msisdn,NULL))/count(*)*100 as 5weeks,
count(if(last_seen>CURDATE() - INTERVAL 2 WEEK,msisdn,NULL))/count(*)*100 as 6weeks
from smp_user where state=1 and last_seen > 0 and date(joined)=date(CURDATE() - INTERVAL 8 WEEK) and rel_operator_id=10;select

count(*) as newUsersPe,
count(if(last_seen>CURDATE() - INTERVAL 7 WEEK,msisdn,NULL))/count(*)*100 as 1week,
count(if(last_seen>CURDATE() - INTERVAL 6 WEEK,msisdn,NULL))/count(*)*100 as 2weeks,
count(if(last_seen>CURDATE() - INTERVAL 5 WEEK,msisdn,NULL))/count(*)*100 as 3weeks,
count(if(last_seen>CURDATE() - INTERVAL 4 WEEK,msisdn,NULL))/count(*)*100 as 4weeks,
count(if(last_seen>CURDATE() - INTERVAL 3 WEEK,msisdn,NULL))/count(*)*100 as 5weeks,
count(if(last_seen>CURDATE() - INTERVAL 2 WEEK,msisdn,NULL))/count(*)*100 as 6weeks
from smp_user where state=1 and last_seen > 0 and date(joined)=date(CURDATE() - INTERVAL 8 WEEK) and rel_operator_id=19;

# select * from smp_instrumentation.counter where (counter_name like '%Failed' and (counter_name like 'telcel%' or counter_name like '%peru%' or counter_name like '%colom')) and counter_value >1000;

select action,count(if(date(time)=(CURDATE() - INTERVAL 1 DAY),1,NULL))/count(if(date(time)=(CURDATE() - INTERVAL 2 DAY),1,NULL))*100-100 as variation,count(if(date(time)=(CURDATE() - INTERVAL 1 DAY),1,NULL)) as ayer,count(*) as todate from smp_usage_log group by action order by action;

# select date(time) as date, count(if(action=1, 1,NULL)) as page1, count(if(action=2, 1,NULL)) as presence2, count(if(action=3, 1,NULL)) as upload3, count(if(action=4, 1,NULL)) as like4, count(if(action=5, 1,NULL)) as comment5, count(if(action=6, 1,NULL)) as u2u6, count(if(action=7, 1,NULL)) as activation7, count(if(action=8, 1,NULL)) as registr8, count(if(action=9, 1,NULL)) as SBGetStat9, count(if(action=10, 1,NULL)) as sbSet10, count(if(action=11, 1,NULL)) as sbReg11, count(if(action=12, 1,NULL)) as sbSNS12, count(if(action=13, 1,NULL)) as uDel13, count(if(action=14, 1,NULL)) as Hook14, count(if(action=15, 1,NULL)) as login15, count(if(action=16 and device='sms', 1,NULL)) as MO_SMS, count(if(action=16 and device='mms', 1,NULL)) as MO_MMS, count(if(action=17, 1,NULL)) as MT17 FROM smp_usage_log group by date with rollup;



