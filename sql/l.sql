use smp;

select 
 (select count(*) from smp_user where joined between '2011-10-01' and '2011-10-08') as Oct1,
 (select count(*) from smp_user where joined between '2011-10-07' and '2011-10-15') as Oct7,
 (select count(*) from smp_user where joined between '2011-10-14' and '2011-10-22') as Oct14,
 (select count(*) from smp_user where joined between '2011-10-21' and '2011-10-29') as Oct21
;
select 
 (select count(*) from smp_user where last_seen between '2011-10-01' and '2011-10-08') as Oct1,
 (select count(*) from smp_user where last_seen between '2011-10-07' and '2011-10-15') as Oct7,
 (select count(*) from smp_user where last_seen between '2011-10-14' and '2011-10-22') as Oct14,
 (select count(*) from smp_user where last_seen between '2011-10-21' and '2011-10-29') as Oct21
;

select 
 (select count(*) from smp_user where joined between '2011-05-01' and '2011-06-01') as May,
 (select count(*) from smp_user where joined between '2011-06-01' and '2011-07-01') as Jun,
 (select count(*) from smp_user where joined between '2011-07-01' and '2011-08-01') as Jul,
 (select count(*) from smp_user where joined between '2011-08-01' and '2011-09-01') as Aug,
 (select count(*) from smp_user where joined between '2011-09-01' and '2011-10-01') as Sep,
 (select count(*) from smp_user where joined between '2011-10-01' and '2011-11-01') as Oct,
 (select count(*) from smp_user where joined between '2011-11-01' and '2011-12-01') as Nov
;
select 
 (select count(*) from smp_user where last_seen between '2011-05-01' and '2011-06-01') as May,
 (select count(*) from smp_user where last_seen between '2011-06-01' and '2011-07-01') as Jun,
 (select count(*) from smp_user where last_seen between '2011-07-01' and '2011-08-01') as Jul,
 (select count(*) from smp_user where last_seen between '2011-08-01' and '2011-09-01') as Aug,
 (select count(*) from smp_user where last_seen between '2011-09-01' and '2011-10-01') as Sep,
 (select count(*) from smp_user where last_seen between '2011-10-01' and '2011-11-01') as Oct,
 (select count(*) from smp_user where last_seen between '2011-11-01' and '2011-12-01') as Nov
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
 (select count(*) from smp_user where last_seen between '2011-10-27' and '2011-10-28') as c27,
 (select count(*) from smp_user where last_seen between '2011-10-28' and '2011-10-29') as c28,
 (select count(*) from smp_user where last_seen between '2011-10-29' and '2011-10-30') as c29,
 (select count(*) from smp_user where last_seen between '2011-10-30' and '2011-10-31') as c30,
 (select count(*) from smp_user where last_seen between '2011-10-31' and '2011-10-32') as c31
;

