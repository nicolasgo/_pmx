# users Missing in Action cohort #1
SELECT 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as cohort1, #7671
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-01 05' and last_seen < '2011-08-08 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk1, #4260,4343,4465
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-08 05' and last_seen < '2011-08-15 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk2, #703,745,784
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-15 05' and last_seen < '2011-08-22 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk3, #410,435,475
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-22 05' and last_seen < '2011-08-29 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk4, #366,398,456
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-29 05' and last_seen < '2011-09-05 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk5, #532,594,706
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk6, #331,400,693
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk7, #401,637
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk8, #555,58
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk9,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk10,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk11,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk12,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk13,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-08-01 05' and joined < '2011-08-08 05') as wk14#
;
# users MiA cohort #2
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as cohort2, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-08 05' and last_seen < '2011-08-15 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk1, #2956,3029,3096
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-15 05' and last_seen < '2011-08-22 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk2, #429,458,486
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-22 05' and last_seen < '2011-08-29 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk3, #299,317,355
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-29 05' and last_seen < '2011-09-05 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk4, #390,444,532
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk5, #328,400,587
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk6, #281,491,181
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk7, #464,67
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk8,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk9, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk10,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk11,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk12,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-08-08 05' and joined < '2011-08-15 05') as wk13#
;
# users MiA cohort #3
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as cohort3, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-15 05' and last_seen < '2011-08-22 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk1, #2512,2580,2682
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-22 05' and last_seen < '2011-08-29 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk2, #406,433,483
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-29 05' and last_seen < '2011-09-05 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk3, #370,419,510
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk4, #293,354,521
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk5, #341,203
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk6, #386,71
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk7,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk8, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk9,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk10,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk11,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-08-15 05' and joined < '2011-08-22 05') as wk12#
    ;
# users MiA cohort #4
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as cohort4, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-22 05' and last_seen < '2011-08-29 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk1, #8687,9019,9494
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-29 05' and last_seen < '2011-09-05 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk2, #3872,4309,5070
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk3, #1812,2283,3688
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk4, #2024,3457,1340
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk5, #2881,489
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk6,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk7, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk8,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk9,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk10,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-08-22 05' and joined < '2011-08-29 05') as wk11#
;
# users MiA cohort #5
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as cohort5, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-08-29 05' and last_seen < '2011-09-05 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk1, #70978
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk2, #11296
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk3, #8494
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk4,  #10259
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk5, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk6, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk7,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk8,
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk9,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-08-29 05' and joined < '2011-09-05 05') as wk10#
;
# users MiA cohort #6
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as cohort6, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-05 05' and last_seen < '2011-09-12 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk1, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk2, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk3, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk4,  #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk5,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk6,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk7,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk9,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-09-05 05' and joined < '2011-09-12 05') as wk10#
;
# users MiA cohort #7
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as cohort7, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-12 05' and last_seen < '2011-09-19 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk1, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk2, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk3,  #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk4,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk5,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk6,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk7,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-09-12 05' and joined < '2011-09-19 05') as wk8#
;

# users MiA cohort #8
SELECT
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as cohort8, 
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-19 05' and last_seen < '2011-09-26 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk1, #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-09-26 05' and last_seen < '2011-10-03 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk2,  #
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-03 05' and last_seen < '2011-10-10 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk3,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-10 05' and last_seen < '2011-10-17 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk4,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-17 05' and last_seen < '2011-10-24 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk5,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-24 05' and last_seen < '2011-10-31 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk6,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-10-31 05' and last_seen < '2011-11-07 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk7,#
    (select count(msisdn) from smp.smp_user where msisdn REGEXP '^52' and last_seen > '2011-11-07 05' and last_seen < '2011-11-14 05' and joined > '2011-09-19 05' and joined < '2011-09-26 05') as wk8#
;
