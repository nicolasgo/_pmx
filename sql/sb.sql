select
     ( SELECT Count(*) FROM smp.smp_usage_log WHERE `rel_operator_id` = 10 AND `time` > '2012-02-29' AND `action` IN (9, 10, 11, 12) AND `miscstr3` = 'sb'  ) as TotalAccess,
     ( SELECT Count(*) FROM smp.smp_usage_log WHERE `rel_operator_id` = 10 AND `time` > '2012-02-29' AND `action` = 11 AND `miscstr3` = 'sb'  ) as Registrations,
     ( SELECT Count(*) FROM smp.smp_usage_log WHERE `rel_operator_id` = 10 AND `time` > '2012-02-29' AND `action` = 10 AND `miscstr3` = 'sb'  ) as Posts,
     ( SELECT Count(DISTINCT msisdn) FROM smp.smp_usage_log WHERE `rel_operator_id` = 10 AND `time` > '2012-02-29' AND `action` IN (9, 10, 11, 12) AND `miscstr3` = 'sb'  ) as UniqueUsers,
     ( SELECT Count(*) FROM smp.smp_usage_log WHERE `rel_operator_id` = 10 AND `time` > '2012-02-29' AND `action` = 9 AND `miscstr3` = 'sb'  ) as GetLastStatus
;

