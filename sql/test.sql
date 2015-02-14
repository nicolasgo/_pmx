set @_today=(select curdate());
set @_yesterday=(select date_sub(curdate(), interval 1 DAY));
set @_5days=(select date_sub(curdate(), interval 5 DAY));
set @_10days=(select date_sub(curdate(), interval 10 DAY));
set @_30days=(select date_sub(curdate(), interval 30 DAY));
set @_60days=(select date_sub(curdate(), interval 60 DAY));
set @_90days=(select date_sub(curdate(), interval 90 DAY));
set @_120days=(select date_sub(curdate(), interval 120 DAY));

drop table if exists zzuser;
create table zzuser ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select user_id,msisdn,rel_operator_id as oid,joined,last_seen,disk_usage,state from smp_user where rel_operator_id=10 and joined > @_90days and joined < @_60days;

create index user_id on zzuser(user_id);
create index msisdn on zzuser(msisdn);

alter table zzuser add COLUMN content INT, add COLUMN friends INT,add COLUMN invites INT, add COLUMN rcvdInv INT, add COLUMN rejectd INT, add COLUMN sms INT,
        add COLUMN mms INT, add COLUMN sim int, add COLUMN login INT, add COLUMN web int,
        add COLUMN twFrs INT, add COLUMN tw_url varchar(128), add COLUMN fbFrs INT, add COLUMN fb_url varchar(128), add COLUMN yt BOOL, add COLUMN pi BOOL, add COLUMN fk BOOL,
        add COLUMN area INT;
								
update zzuser as u set u.area=substring(u.msisdn,1,4);

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

#add the number of friends on plugger
drop table if exists zzf;
create temporary table zzf select rel_user_id as user_id,count(if(status=2,1,null)) as friends, count(if(status=0,1,null)) as invites, count(if(status=1,1,null)) as rcvdInv, count(if(status=3,1,null)) as rejectd from smp_contact_friend group by user_id;
update zzuser as u inner join zzf as f using(user_id) SET u.friends = f.friends,u.invites = f.invites,u.rcvdInv = f.rcvdInv,u.rejectd = f.rejectd;
drop table if exists zzf;

drop table if exists zzc2;
create temporary table zzc2 select user_id,count(*) as content from zzcontent group by user_id;
update zzuser as u inner join zzc2 as c using(user_id) SET u.content = c.content;
drop table if exists zzc2;

