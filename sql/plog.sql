set @_startdate=(select (min(time) + interval 24 hour) from smp_usage_log where time >0);
select  @_startdate;
delete from smp_usage_log where time >0 and time < @_startdate;
