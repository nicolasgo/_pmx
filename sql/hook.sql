use smp_sns;
SELECT count(*) as fbHook, count(if(rel_operator_id=10,1,NULL)) as mx, count(if(rel_operator_id=18,1,NULL)) as br, count(if(rel_operator_id=20,1,NULL)) as ar, count(if(rel_operator_id=19,1,NULL)) as pe, count(if(rel_operator_id=24,1,NULL)) as cl, count(if(rel_operator_id=16,1,NULL)) as pa, count(if(rel_operator_id=14,1,NULL)) as do, count(if(rel_operator_id=15,1,NULL)) as co, count(if(rel_operator_id=26,1,NULL)) as gt , count(if(rel_operator_id=29,1,NULL)) as hn, count(if(rel_operator_id=27,1,NULL)) as sv, count(if(rel_operator_id=30,1,NULL)) as ni, count(if(rel_operator_id=31,1,NULL)) as pr, count(if(rel_operator_id=33,1,NULL)) as cr, count(if(rel_operator_id=21,1,NULL)) as ec, count(if(rel_operator_id=23,1,NULL)) as uy, count(if(rel_operator_id=22,1,NULL)) as py	
	FROM (select ext_id from smp_sns.sns_facebook_hook inner join sns_user u on rel_user_id = u.sns_user_id where length(session_key) > 0 and valid = 1)
    as x inner join smp.smp_user as uu on x.ext_id=user_id;
SELECT count(*) as twHook, count(if(rel_operator_id=10,1,NULL)) as mx, count(if(rel_operator_id=18,1,NULL)) as br, count(if(rel_operator_id=20,1,NULL)) as ar, count(if(rel_operator_id=19,1,NULL)) as pe, count(if(rel_operator_id=24,1,NULL)) as cl, count(if(rel_operator_id=16,1,NULL)) as pa, count(if(rel_operator_id=14,1,NULL)) as do, count(if(rel_operator_id=15,1,NULL)) as co, count(if(rel_operator_id=26,1,NULL)) as gt , count(if(rel_operator_id=29,1,NULL)) as hn, count(if(rel_operator_id=27,1,NULL)) as sv, count(if(rel_operator_id=30,1,NULL)) as ni, count(if(rel_operator_id=31,1,NULL)) as pr, count(if(rel_operator_id=33,1,NULL)) as cr, count(if(rel_operator_id=21,1,NULL)) as ec, count(if(rel_operator_id=23,1,NULL)) as uy, count(if(rel_operator_id=22,1,NULL)) as py	
	FROM (select ext_id from smp_sns.sns_twitter_hook inner join sns_user u on rel_user_id = u.sns_user_id where length(session_key) > 0 and valid = 1)
    as x inner join smp.smp_user as uu on x.ext_id=user_id;
SELECT count(*) as ytHook, count(if(rel_operator_id=10,1,NULL)) as mx, count(if(rel_operator_id=18,1,NULL)) as br, count(if(rel_operator_id=20,1,NULL)) as ar, count(if(rel_operator_id=19,1,NULL)) as pe, count(if(rel_operator_id=24,1,NULL)) as cl, count(if(rel_operator_id=16,1,NULL)) as pa, count(if(rel_operator_id=14,1,NULL)) as do, count(if(rel_operator_id=15,1,NULL)) as co, count(if(rel_operator_id=26,1,NULL)) as gt , count(if(rel_operator_id=29,1,NULL)) as hn, count(if(rel_operator_id=27,1,NULL)) as sv, count(if(rel_operator_id=30,1,NULL)) as ni, count(if(rel_operator_id=31,1,NULL)) as pr, count(if(rel_operator_id=33,1,NULL)) as cr, count(if(rel_operator_id=21,1,NULL)) as ec, count(if(rel_operator_id=23,1,NULL)) as uy, count(if(rel_operator_id=22,1,NULL)) as py	
	FROM (select ext_id from smp_sns.sns_youtube_hook inner join sns_user u on rel_user_id = u.sns_user_id where length(session_key) > 0 and valid = 1)
    as x inner join smp.smp_user as uu on x.ext_id=user_id;
SELECT count(*) as piHook, count(if(rel_operator_id=10,1,NULL)) as mx, count(if(rel_operator_id=18,1,NULL)) as br, count(if(rel_operator_id=20,1,NULL)) as ar, count(if(rel_operator_id=19,1,NULL)) as pe, count(if(rel_operator_id=24,1,NULL)) as cl, count(if(rel_operator_id=16,1,NULL)) as pa, count(if(rel_operator_id=14,1,NULL)) as do, count(if(rel_operator_id=15,1,NULL)) as co, count(if(rel_operator_id=26,1,NULL)) as gt , count(if(rel_operator_id=29,1,NULL)) as hn, count(if(rel_operator_id=27,1,NULL)) as sv, count(if(rel_operator_id=30,1,NULL)) as ni, count(if(rel_operator_id=31,1,NULL)) as pr, count(if(rel_operator_id=33,1,NULL)) as cr, count(if(rel_operator_id=21,1,NULL)) as ec, count(if(rel_operator_id=23,1,NULL)) as uy, count(if(rel_operator_id=22,1,NULL)) as py	
	FROM (select ext_id from smp_sns.sns_picasa_hook inner join sns_user u on rel_user_id = u.sns_user_id where length(session_key) > 0 and valid = 1)
    as x inner join smp.smp_user as uu on x.ext_id=user_id;
SELECT count(*) as fkHook, count(if(rel_operator_id=10,1,NULL)) as mx, count(if(rel_operator_id=18,1,NULL)) as br, count(if(rel_operator_id=20,1,NULL)) as ar, count(if(rel_operator_id=19,1,NULL)) as pe, count(if(rel_operator_id=24,1,NULL)) as cl, count(if(rel_operator_id=16,1,NULL)) as pa, count(if(rel_operator_id=14,1,NULL)) as do, count(if(rel_operator_id=15,1,NULL)) as co, count(if(rel_operator_id=26,1,NULL)) as gt , count(if(rel_operator_id=29,1,NULL)) as hn, count(if(rel_operator_id=27,1,NULL)) as sv, count(if(rel_operator_id=30,1,NULL)) as ni, count(if(rel_operator_id=31,1,NULL)) as pr, count(if(rel_operator_id=33,1,NULL)) as cr, count(if(rel_operator_id=21,1,NULL)) as ec, count(if(rel_operator_id=23,1,NULL)) as uy, count(if(rel_operator_id=22,1,NULL)) as py	
	FROM (select ext_id from smp_sns.sns_flickr_hook inner join sns_user u on rel_user_id = u.sns_user_id where length(session_key) > 0 and valid = 1)
    as x inner join smp.smp_user as uu on x.ext_id=user_id;

