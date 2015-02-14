use smp;
select count(1) as accesses,msisdn as users, device from smp_usage_log where time regexp '2011-11' and device <> 'sms' and device <> 'mms' group by users having accesses>50 order by accesses desc;

