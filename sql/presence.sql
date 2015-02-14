drop table if exists zzpresence;

create table zzpresence ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select rel_user_id user_id,year(created)*100+(lpad(month(created),2,0)) m, type, count(*) c from smp_presence group by user_id,m,type;

create index usr on zzpresence(user_id);
create index ti  on zzpresence(m);

