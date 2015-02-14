drop table if exists zzuserlog2;

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


#add the number of friends on plugger
drop table if exists zzf;
create temporary table zzf select rel_user_id as user_id,count(if(status=2,1,null)) as friends, count(if(status=0,1,null)) as invites, count(if(status=1,1,null)) as rcvdInv, count(if(status=3,1,null)) as rejectd from smp_contact_friend group by user_id;
update zzuser as u inner join zzf as f using(user_id) SET u.friends = f.friends,u.invites = f.invites,u.rcvdInv = f.rcvdInv,u.rejectd = f.rejectd;
drop table if exists zzf;

create table zzuserlog2 ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select time,user_id,action,device,miscid1,miscid2,miscstr1,miscstr2,miscstr3 from zzuserlog;


select 'creating zzdroid table';
drop table if exists zzdroid;
create table zzdroid ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select device,count(distinct msisdn) as users,count(*) as actions from zzuserlog where time> @_5days and device like '%android%' group by device order by users desc limit 200;


