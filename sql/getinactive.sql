

#create index msisdn on zzlog306(msisdn);
#

drop table if exists zzu306;

create table zzu306 ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select user_id,msisdn,rel_operator_id as oid,joined,last_seen,disk_usage,state from smp_user where rel_operator_id=10 and last_seen < '2013-07-01' and last_seen > '2013-06-01';

create index user_id on zzu306(user_id);
create index msisdn on zzu306(msisdn);

alter table zzlog306 add COLUMN user_id bigint(20) unsigned;
update zzlog306 as l inner join zzuser as u using(msisdn) SET l.user_id=u.user_id where l.time > '2013-06-01';

#
drop table if exists zzfriends;
create table zzfriends ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select rel_user_id as user_id,rel_friend_id,status from smp_contact_friend where rel_user_id in (select user_id from zzu306);

alter table zzu306 add COLUMN friends INT,add COLUMN invites INT, add COLUMN rcvdInv INT, add COLUMN rejectd INT, add COLUMN sms INT, 
	add COLUMN mms INT, add COLUMN sim int, add COLUMN login INT, add COLUMN web int, 
	add COLUMN twFrs INT, add COLUMN tw_url varchar(128), add COLUMN fbFrs INT, add COLUMN fb_url varchar(128), add COLUMN yt BOOL, add COLUMN pi BOOL, add COLUMN fk BOOL,
	add COLUMN area INT;

#
#  Connection to SNS
#
#
update zzu306 as u inner join (select rel_user_id as user_id,num_friends from smp_sns where type=29) as tmp using (user_id) SET u.fbFrs =tmp.num_friends;
update zzu306 as u inner join (select rel_user_id as user_id,num_friends from smp_sns where type=47) as tmp using (user_id) SET u.twFrs =tmp.num_friends;
update zzu306 as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=27 and connect_state=1) as tmp using (user_id) SET u.yt =1;
update zzu306 as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=58 and connect_state=1) as tmp using (user_id) SET u.pi =1;
update zzu306 as u inner join (select rel_user_id as user_id,connect_state from smp_sns where type=28 and connect_state=1) as tmp using (user_id) SET u.fk =1;
update zzu306 as u inner join (select rel_user_id as user_id,profile_url from smp_sns where type=29) as tmp using (user_id) SET u.fb_url =tmp.profile_url;
update zzu306 as u inner join (select rel_user_id as user_id,profile_url from smp_sns where type=47) as tmp using (user_id) SET u.tw_url =tmp.profile_url;



update zzu306 as u inner join (select user_id, count(if(miscstr3='sms',1,NULL)) as sms,count(if(miscstr3='mms',1,NULL)) as mms from zzlog306 where action=16 group by user_id) as ll using (user_id) SET u.sms=ll.sms,u.mms=ll.mms ;
update zzu306 as u inner join (select user_id, count(if(action=10,1,NULL)) as sim from zzlog306 where action in (9,10,11,12) group by user_id) as ll using (user_id) SET u.sim=ll.sim;
update zzu306 as u inner join (select msisdn, count(*) as login from zzlog306 where action=15 and miscstr3='mobile' group by msisdn) as ll using (msisdn) SET u.login=ll.login;
update zzu306 as u inner join (select msisdn, count(*) as web from zzlog306 where action=15 and miscstr3='web' group by msisdn) as ll using (msisdn) SET u.web=ll.web;


#add the number of friends on plugger
drop table if exists zzf;
create temporary table zzf select rel_user_id as user_id,count(if(status=2,1,null)) as friends, count(if(status=0,1,null)) as invites, count(if(status=1,1,null)) as rcvdInv, count(if(status=3,1,null)) as rejectd from smp_contact_friend group by user_id;
update zzu306 as u inner join zzf as f using(user_id) SET u.friends = f.friends,u.invites = f.invites,u.rcvdInv = f.rcvdInv,u.rejectd = f.rejectd;
drop table if exists zzf;

update zzu306 as u set u.area=substring(u.msisdn,1,5);

