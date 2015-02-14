use smp;

select 
 (select count(*) from smp_user where joined between '2011-10-01' and '2011-10-02') as j01,
 (select count(*) from smp_user where joined between '2011-10-02' and '2011-10-03') as j02,
 (select count(*) from smp_user where joined between '2011-10-03' and '2011-10-04') as j03,
 (select count(*) from smp_user where joined between '2011-10-04' and '2011-10-05') as j04,
 (select count(*) from smp_user where joined between '2011-10-05' and '2011-10-06') as j05,
 (select count(*) from smp_user where joined between '2011-10-06' and '2011-10-07') as j06,
 (select count(*) from smp_user where joined between '2011-10-07' and '2011-10-08') as j07,
 (select count(*) from smp_user where joined between '2011-10-08' and '2011-10-09') as j08,
 (select count(*) from smp_user where joined between '2011-10-09' and '2011-10-10') as j09,
 (select count(*) from smp_user where joined between '2011-10-10' and '2011-10-11') as j10,
 (select count(*) from smp_user where joined between '2011-10-11' and '2011-10-12') as j11,
 (select count(*) from smp_user where joined between '2011-10-12' and '2011-10-13') as j12,
 (select count(*) from smp_user where joined between '2011-10-13' and '2011-10-14') as j13,
 (select count(*) from smp_user where joined between '2011-10-14' and '2011-10-15') as j14,
 (select count(*) from smp_user where joined between '2011-10-15' and '2011-10-16') as j15,
 (select count(*) from smp_user where joined between '2011-10-16' and '2011-10-17') as j16,
 (select count(*) from smp_user where joined between '2011-10-17' and '2011-10-18') as j17,
 (select count(*) from smp_user where joined between '2011-10-18' and '2011-10-19') as j18,
 (select count(*) from smp_user where joined between '2011-10-19' and '2011-10-20') as j19,
 (select count(*) from smp_user where joined between '2011-10-20' and '2011-10-21') as j20,
 (select count(*) from smp_user where joined between '2011-10-21' and '2011-10-22') as j21,
 (select count(*) from smp_user where joined between '2011-10-22' and '2011-10-23') as j22,
 (select count(*) from smp_user where joined between '2011-10-23' and '2011-10-24') as j23,
 (select count(*) from smp_user where joined between '2011-10-24' and '2011-10-25') as j24,
 (select count(*) from smp_user where joined between '2011-10-25' and '2011-10-26') as j25,
 (select count(*) from smp_user where joined between '2011-10-26' and '2011-10-27') as j26,
 (select count(*) from smp_user where joined between '2011-10-27' and '2011-10-28') as j27
;

select 
 (select count(*) from smp_user where last_seen between '2011-10-01' and '2011-10-02') as c01,
 (select count(*) from smp_user where last_seen between '2011-10-02' and '2011-10-03') as c02,
 (select count(*) from smp_user where last_seen between '2011-10-03' and '2011-10-04') as c03,
 (select count(*) from smp_user where last_seen between '2011-10-04' and '2011-10-05') as c04,
 (select count(*) from smp_user where last_seen between '2011-10-05' and '2011-10-06') as c05,
 (select count(*) from smp_user where last_seen between '2011-10-06' and '2011-10-07') as c06,
 (select count(*) from smp_user where last_seen between '2011-10-07' and '2011-10-08') as c07,
 (select count(*) from smp_user where last_seen between '2011-10-08' and '2011-10-09') as c08,
 (select count(*) from smp_user where last_seen between '2011-10-09' and '2011-10-10') as c09,
 (select count(*) from smp_user where last_seen between '2011-10-10' and '2011-10-11') as c10,
 (select count(*) from smp_user where last_seen between '2011-10-11' and '2011-10-12') as c11,
 (select count(*) from smp_user where last_seen between '2011-10-12' and '2011-10-13') as c12,
 (select count(*) from smp_user where last_seen between '2011-10-13' and '2011-10-14') as c13,
 (select count(*) from smp_user where last_seen between '2011-10-14' and '2011-10-15') as c14,
 (select count(*) from smp_user where last_seen between '2011-10-15' and '2011-10-16') as c15,
 (select count(*) from smp_user where last_seen between '2011-10-16' and '2011-10-17') as c16,
 (select count(*) from smp_user where last_seen between '2011-10-17' and '2011-10-18') as c17,
 (select count(*) from smp_user where last_seen between '2011-10-18' and '2011-10-19') as c18,
 (select count(*) from smp_user where last_seen between '2011-10-19' and '2011-10-20') as c19,
 (select count(*) from smp_user where last_seen between '2011-10-20' and '2011-10-21') as c20,
 (select count(*) from smp_user where last_seen between '2011-10-21' and '2011-10-22') as c21,
 (select count(*) from smp_user where last_seen between '2011-10-22' and '2011-10-23') as c22,
 (select count(*) from smp_user where last_seen between '2011-10-23' and '2011-10-24') as c23,
 (select count(*) from smp_user where last_seen between '2011-10-24' and '2011-10-25') as c24,
 (select count(*) from smp_user where last_seen between '2011-10-25' and '2011-10-26') as c25,
 (select count(*) from smp_user where last_seen between '2011-10-26' and '2011-10-27') as c26,
 (select count(*) from smp_user where last_seen between '2011-10-27' and '2011-10-28') as c27
;

select 
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-01' and time < '2011-11-02') as m01,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-02' and time < '2011-11-03') as m02,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-03' and time < '2011-11-04') as m03,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-04' and time < '2011-11-05') as m04,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-05' and time < '2011-11-06') as m05,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-06' and time < '2011-11-07') as m06,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-07' and time < '2011-11-08') as m07,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-08' and time < '2011-11-09') as m08,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-09' and time < '2011-11-10') as m09
;

select 
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-10' and time < '2011-11-11') as m10,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-11' and time < '2011-11-12') as m11,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-12' and time < '2011-11-13') as m12,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-13' and time < '2011-11-14') as m13,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-14' and time < '2011-11-15') as m14,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-15' and time < '2011-11-16') as m15,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-16' and time < '2011-11-17') as m16,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-17' and time < '2011-11-18') as m17,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-18' and time < '2011-11-19') as m18,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-19' and time < '2011-11-20') as m19
;

select 
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-20' and time < '2011-11-21') as m20,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-21' and time < '2011-11-22') as m21,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-22' and time < '2011-11-23') as m22,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-23' and time < '2011-11-24') as m23,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-24' and time < '2011-11-25') as m24,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-25' and time < '2011-11-26') as m25,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-26' and time < '2011-11-27') as m26,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-27' and time < '2011-11-28') as m27,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-28' and time < '2011-11-29') as m28,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-29' and time < '2011-11-30') as m29,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-30' and time < '2011-11-31') as m30,
  (select count(distinct msisdn) from smp_usage_log where time > '2011-11-31' and time < '2011-11-32') as m31
;

