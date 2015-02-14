set @_startdate=(select date('2013-11-01'));
set @_enddate=@_startdate+interval 2 day;

drop table if exists zzlog311;
create table zzlog311 ENGINE=MyISAM DATA DIRECTORY='/var/mysql-data/smp/' INDEX DIRECTORY='/var/mysql-data/smp/' select * from smp_usage_log where time>= '2013-11-01' and time < '2013-11-02';
#create table zzlog311 select * from smp_usage_log where time>@_startdate and time<@_enddate and action <> 17;

select now(),'start';
select @_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

set @_startdate=@_enddate;
set @_enddate=@_enddate+interval 2 day;
select sleep(9),@_startdate,@_enddate;
insert into zzlog311 select * from smp_usage_log where time >= @_startdate and time < @_enddate;

#insert into zzlog311 select * from smp_usage_log where time >= '2013-10-30 00:00:00' and time < '2013-11-01';

select now(),'done';
create index time on zzlog311(time);
create index msisdn on zzlog311(msisdn);

