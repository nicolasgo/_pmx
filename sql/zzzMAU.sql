set @_now= (select max(last_seen) from smp_user);
set @_now1=@_now - interval 1 day;                                                                                                                                                                
set @_now7=@_now1 - interval 6 day;
set @_now30=@_now1 - interval 29 day;

insert into zzzMAU select now(),rel_operator_id as oid, count(*) as MAU,count(if(last_seen > @_now7,1,null)) as WAU, count(if(last_seen > @_now1,1,null)) as DAU from smp_user where rel_operator_id=10 and state=1 and last_seen > @_now30 group by oid;

