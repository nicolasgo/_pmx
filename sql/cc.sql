drop table if exists zzcontent,zzcontent2;

# Type of content:
#  5 - audio
#  6 - video
#  7 - image
# 54 - unknown
# 55 - avatar (deprecated)
# 56 - profile (deprecated)
# 66 - myprofile (deprecated)

# States:
# 0 - pending
# 1 - published

# process_state = 2 means that this is only about content that is finished
# = 0 means pending
# = 1 started processing
# = 3 is error
# = 4 is processing

create table zzcontent ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select content_id,rel_user_id as user_id,dt_uploaded as time, size, duration, state, no_comments, mime, title from smp_content where dt_uploaded > '2014-01-01' and process_state=2;

#process_state=2 means success (0 is failure, and 4 is ??)

create index user_id on zzcontent(user_id);
create index time on zzcontent(time);
alter table zzcontent add COLUMN oid INT;
update zzcontent as c left join (select user_id,rel_operator_id from smp_user) as u using(user_id) SET c.oid=u.rel_operator_id;

SELECT year(time)as y,month(time)as m,count(*) as upload, count( if(oid=10,1,NULL)) as mx, count( if(oid=18,1,NULL)) as br, count( if(oid=20,1,NULL)) as ar, count( if(oid=19,1,NULL)) as pe, count( if(oid=24,1,NULL)) as cl, count( if(oid=16,1,NULL)) as pa, count( if(oid=14,1,NULL)) as do, count( if(oid=15,1,NULL)) as co, count( if(oid=26,1,NULL)) as gt, count( if(oid=29,1,NULL)) as hn, count( if(oid=27,1,NULL)) as sv, count( if(oid=30,1,NULL)) as ni, count( if(oid=31,1,NULL)) as pr, count( if(oid=33,1,NULL)) as cr, count( if(oid=21,1,NULL)) as ec, count( if(oid=23,1,NULL)) as ur, count( if(oid=22,1,NULL)) as py FROM zzcontent group by y,m;
SELECT year(time)as y,week(time)as w,count(*) as upload, count( if(oid=10,1,NULL)) as mx, count( if(oid=18,1,NULL)) as br, count( if(oid=20,1,NULL)) as ar, count( if(oid=19,1,NULL)) as pe, count( if(oid=24,1,NULL)) as cl, count( if(oid=16,1,NULL)) as pa, count( if(oid=14,1,NULL)) as do, count( if(oid=15,1,NULL)) as co, count( if(oid=26,1,NULL)) as gt, count( if(oid=29,1,NULL)) as hn, count( if(oid=27,1,NULL)) as sv, count( if(oid=30,1,NULL)) as ni, count( if(oid=31,1,NULL)) as pr, count( if(oid=33,1,NULL)) as cr, count( if(oid=21,1,NULL)) as ec, count( if(oid=23,1,NULL)) as ur, count( if(oid=22,1,NULL)) as py FROM zzcontent group by y,w;
