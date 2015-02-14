update zzu as z inner join (select user_id,msisdn,rel_operator_id as oid,joined,last_seen,disk_usage,state from smp_user where rel_operator_id=10 ) as u using(msisdn) SET z.user_id=u.user_id, z.joined=u.joined,z.last_seen=u.last_seen, z.oid=u.oid,z.disk_usage=u.disk_usage, z.state=u.state;

create index user_id on zzu(user_id);

alter table zzul add COLUMN user_id bigint(20) unsigned;
update zzul as l inner join zzu as u using(msisdn) SET l.user_id=u.user_id;
create index user_id on zzul(user_id);

#
drop table if exists zzfriends;
create table zzfriends select rel_user_id as user_id,rel_friend_id from smp_contact_friend where rel_user_id in (select user_id from zzu);

alter table zzu add COLUMN friends INT,add COLUMN invites INT, add COLUMN rcvdInv INT, add COLUMN rejectd INT, add COLUMN sms INT,
        add COLUMN mms INT, add COLUMN sim int, add COLUMN login INT, add COLUMN web int,
        add COLUMN twFrs INT, add COLUMN tw_url varchar(128), add COLUMN fbFrs INT, add COLUMN fb_url varchar(128), add COLUMN yt BOOL, add COLUMN pi BOOL, add COLUMN fk BOOL,
        add COLUMN device varchar(255), add COLUMN area INT;

