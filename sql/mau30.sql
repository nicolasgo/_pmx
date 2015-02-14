set @_now=(select max(last_seen) from smp_user);
set @_now30=@_now - interval 30 day;


SELECT count(*) as MAU30days, count(distinct if(rel_operator_id=10,msisdn,NULL)) as mx, count(distinct if(rel_operator_id=18,msisdn,NULL)) as br, count(distinct if(rel_operator_id=20,msisdn,NULL)) as ar, count(distinct if(rel_operator_id=19,msisdn,NULL)) as pe, count(distinct if(rel_operator_id=24,msisdn,NULL)) as cl, count(distinct if(rel_operator_id=16,msisdn,NULL)) as pa, count(distinct if(rel_operator_id=14,msisdn,NULL)) as do, count(distinct if(rel_operator_id=15,msisdn,NULL)) as co, count(distinct if(rel_operator_id=26,msisdn,NULL)) as gt, count(distinct if(rel_operator_id=29,msisdn,NULL)) as hn, count(distinct if(rel_operator_id=27,msisdn,NULL)) as sv, count(distinct if(rel_operator_id=30,msisdn,NULL)) as ni, count(distinct if(rel_operator_id=31,msisdn,NULL)) as pr, count(distinct if(rel_operator_id=33,msisdn,NULL)) as cr, count(distinct if(rel_operator_id=21,msisdn,NULL)) as ec, count(distinct if(rel_operator_id=23,msisdn,NULL)) as ur, count(distinct if(rel_operator_id=22,msisdn,NULL)) as py FROM smp_user where state=1 and last_seen >@_now30;

