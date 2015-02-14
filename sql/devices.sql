use smp;
select count(msisdn) as accesses,count(distinct msisdn) as users, device from smp_usage_log where time regexp '2011-11' group by device having accesses>100 order by accesses desc;

