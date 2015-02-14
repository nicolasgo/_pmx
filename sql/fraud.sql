# daily requests

set @_today=(select curdate());
set @_yesterday=(select date_sub(curdate(), interval 1 DAY));
set @_5days=(select date_sub(curdate(), interval 5 DAY));
set @_10days=(select date_sub(curdate(), interval 10 DAY));
set @_30days=(select date_sub(curdate(), interval 30 DAY));
set @_60days=(select date_sub(curdate(), interval 60 DAY));
set @_90days=(select date_sub(curdate(), interval 90 DAY));
set @_120days=(select date_sub(curdate(), interval 120 DAY));


drop table if exists zzuserlog;

create table zzuserlog ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select * from smp_usage_log where msisdn in ( 526643020140, 527711016015, 524651189877, 522221090951, 527222504055, 522941263261, 523313587557, 528991042539, 523141258978, 525532598478, 525535011253, 526142492278, 525547852891, 522831127773, 527121009486, 528112790213, 529512826795, 528777922350, 524811128356, 528771121087, 527848888533, 527721017627, 527671086185, 528721175029, 529671264748, 527471633021, 526241130244, 524431158606, 527131056218, 524561007389, 526161013647, 528411092642, 527721251939, 526449976736, 523318310098, 526241454254, 526771026134, 529373787522, 529676801690);

#OPTIMIZE table zzuserlog;
/****/
select '++creating zzuser table';

drop table if exists zzuser;

create table zzuser ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select user_id,msisdn,rel_operator_id as oid,joined,last_seen,disk_usage,state from smp_user where msisdn in ( select distinct msisdn from zzuserlog);


create index user_id on zzuser(user_id);
create index msisdn on zzuser(msisdn);

alter table zzuserlog add COLUMN user_id bigint(20) unsigned;
update zzuserlog as l inner join zzuser as u using(msisdn) SET l.user_id=u.user_id;

/****/

alter table zzuser add COLUMN friends INT,add COLUMN invites INT, add COLUMN rcvdInv INT, add COLUMN rejectd INT, add COLUMN sms INT, 
	add COLUMN mms INT, add COLUMN sim int, add COLUMN login INT, add COLUMN web int, 
	add COLUMN twFrs INT, add COLUMN tw_url varchar(128), add COLUMN fbFrs INT, add COLUMN fb_url varchar(128), add COLUMN yt BOOL, add COLUMN pi BOOL, add COLUMN fk BOOL,
	add COLUMN area INT;
update zzuser as u inner join (select msisdn,user_id from smp_user) as uu using (user_id) SET u.msisdn=uu.msisdn;

#
#  Connection to SNS
#
#
update zzuser as u inner join (select rel_user_id as user_id,num_friends from smp_sns where type=29) as tmp using (user_id) SET u.fbFrs =tmp.num_friends;
update zzuser as u inner join (select rel_user_id as user_id,num_friends from smp_sns where type=47) as tmp using (user_id) SET u.twFrs =tmp.num_friends;
update zzuser as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=27 and connect_state=1) as tmp using (user_id) SET u.yt =1;
update zzuser as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=58 and connect_state=1) as tmp using (user_id) SET u.pi =1;
update zzuser as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=28 and connect_state=1) as tmp using (user_id) SET u.fk =1;
update zzuser as u inner join (select rel_user_id as user_id,profile_url from smp_sns where type=29) as tmp using (user_id) SET u.fb_url =tmp.profile_url;
update zzuser as u inner join (select rel_user_id as user_id,profile_url from smp_sns where type=47) as tmp using (user_id) SET u.tw_url =tmp.profile_url;



update zzuser as u inner join (select user_id, count(if(miscstr3='sms',1,NULL)) as sms,count(if(miscstr3='mms',1,NULL)) as mms from zzuserlog where action=16 group by user_id) as ll using (user_id) SET u.sms=ll.sms,u.mms=ll.mms ;
update zzuser as u inner join (select user_id, count(if(action=10,1,NULL)) as sim from zzuserlog where action in (9,10,11,12) group by user_id) as ll using (user_id) SET u.sim=ll.sim;
update zzuser as u inner join (select msisdn, count(*) as login from zzuserlog where action=15 and miscstr3='mobile' group by msisdn) as ll using (msisdn) SET u.login=ll.login;
update zzuser as u inner join (select msisdn, count(*) as web from zzuserlog where action=15 and miscstr3='web' group by msisdn) as ll using (msisdn) SET u.web=ll.web;

select '--creating zzuser table';


#add the number of friends on plugger
drop table if exists zzf;
create temporary table zzf select rel_user_id as user_id,count(if(status=2,1,null)) as friends, count(if(status=0,1,null)) as invites, count(if(status=1,1,null)) as rcvdInv, count(if(status=3,1,null)) as rejectd from smp_contact_friend group by user_id;
update zzuser as u inner join zzf as f using(user_id) SET u.friends = f.friends,u.invites = f.invites,u.rcvdInv = f.rcvdInv,u.rejectd = f.rejectd;
drop table if exists zzf;

