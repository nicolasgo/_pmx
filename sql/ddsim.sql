set @_from=concat(year(now()),'-',month(now())-1,'-01');
set @_date=concat(year(now()),'-',month(now()),'-01');

select @_from as fromDate, @_date as toDate;

SELECT count(*) as TotalAPIAccess  FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id = 10 AND action IN (9, 10, 11, 12) AND miscstr3 = 'sb';
SELECT count(*) as sbRegistration FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id= 10  AND action= 11 AND miscstr3= 'sb' ;
SELECT count(*) as setStatus FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id= 10  AND action= 10 AND miscstr3= 'sb' ;
SELECT Count(distinct msisdn) as UniqueUsers  FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id= 10  AND action IN (9, 10, 11, 12) AND miscstr3= 'sb' ;
SELECT count(*) as getStatus FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id= 10  AND action= 9 AND miscstr3= 'sb' ;
SELECT count(*) as sbConnectSNSMsg FROM zzlog405 where time>@_from AND time<@_date AND rel_operator_id= 10  AND action= 12 AND miscstr3= 'sb' ;

