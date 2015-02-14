use smp

 select count(1) as fb_hook from smp_sns.sns_facebook_hook where valid=1; 
 select count(1) as tw_hook from smp_sns.sns_twitter_hook where valid=1; 
 select count(1) as pi_hook from smp_sns.sns_picasa_hook where valid=1; 
 select count(1) as yt_hook from smp_sns.sns_youtube_hook where valid=1; 
 select count(1) as wp_hook from smp_sns.sns_wordpress_hook where valid=1; 

use smp
 select count(1) as facebookPostsCo from smp.smp_usage_log where (action=2 or action=3) and miscid1=29 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^57' ;
 select count(1) as twPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=47 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^57' ;
 select count(1) as Picasa from smp.smp_usage_log where (action=2 or action=3) and miscid1=58 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^57' ;
 select count(1) as Youtube from smp.smp_usage_log where (action=2 or action=3) and miscid1=27 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^57' ;
 select count(1) as wordpress from smp.smp_usage_log where (action=2 or action=3) and miscid1=59 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^57' ;
asdjhasdgkhg24398y
use smp
 select count(1) as facebookPostsMex from smp.smp_usage_log where (action=2 or action=3) and miscid1=29 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^52' ;
 select count(1) as twPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=47 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^52' ;
 select count(1) as Picasa from smp.smp_usage_log where (action=2 or action=3) and miscid1=58 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^52' ;
 select count(1) as Youtube from smp.smp_usage_log where (action=2 or action=3) and miscid1=27 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^52' ;
 select count(1) as wordpress from smp.smp_usage_log where (action=2 or action=3) and miscid1=59 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^52' ;

use smp
 select count(1) as facebookPostsPe from smp.smp_usage_log where (action=2 or action=3) and miscid1=29 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^51' ;
 select count(1) as twPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=47 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^51' ;
 select count(1) as Picasa from smp.smp_usage_log where (action=2 or action=3) and miscid1=58 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^51' ;
 select count(1) as Youtube from smp.smp_usage_log where (action=2 or action=3) and miscid1=27 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^51' ;
 select count(1) as wordpress from smp.smp_usage_log where (action=2 or action=3) and miscid1=59 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^51' ;

use smp
 select count(1) as facebookPostsAr from smp.smp_usage_log where (action=2 or action=3) and miscid1=29 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^54' ;
 select count(1) as twPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=47 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^54' ;
 select count(1) as Picasa from smp.smp_usage_log where (action=2 or action=3) and miscid1=58 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^54' ;
 select count(1) as Youtube from smp.smp_usage_log where (action=2 or action=3) and miscid1=27 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^54' ;
 select count(1) as wordpress from smp.smp_usage_log where (action=2 or action=3) and miscid1=59 and time >= '2011-11-01' and time < '2011-12-01' and msisdn regexp '^54' ;

use smp
 select count(1) as facebookPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=29 and time >= '2011-11-01' and time < '2011-12-01';
 select count(1) as twPosts from smp.smp_usage_log where (action=2 or action=3) and miscid1=47 and time >= '2011-11-01' and time < '2011-12-01';
 select count(1) from smp.smp_usage_log where (action=2 or action=3) and miscid1=58 and time >= '2011-11-01' and time < '2011-12-01';
 select count(1) from smp.smp_usage_log where (action=2 or action=3) and miscid1=27 and time >= '2011-11-01' and time < '2011-12-01';
 select count(1) from smp.smp_usage_log where (action=2 or action=3) and miscid1=59 and time >= '2011-11-01' and time < '2011-12-01';

#const PAGE_VIEW       = 1;        //miscstr1: URL | miscstr3: web/mobile/sms/mms
#const PRESENCE        = 2;        //miscstr1: message | miscid1: sns id | miscstr3: web/mobile/sms/mms/sb
#const UPLOAD          = 3;        //miscstr1: content name | miscstr2: message | miscstr3: web/mobile/sms/mms | miscid1: snsid
#const LIKE            = 4;        //miscstr3: web/mobile/sms/mms | miscid1: sns id
#const COMMENT         = 5;        //miscstr1: message | miscstr3: web/mobile/sms/mms | miscid1: sns id
#const U2U             = 6;        //miscstr1: message | miscstr3: web/mobile/sms/mms | miscid1: sender user id | miscid2: recipient user id
#const ACTIVATION      = 7;        //miscstr1: name | miscstr3: web/mobile/na/sb | miscid1: operator id
#const REGISTRATION    = 8;        //miscstr1: name | miscstr3: sms/mms/na/sb | miscid1: operator id
#const API_GETSTATUS   = 9;        //miscstr1: error message | miscstr3: sms/mms/na/sb | miscid1: 0 if success, 1 if error
#const API_SETSTATUS   = 10;       //miscstr1: error message | miscstr3: sms/mms/na/sb | miscid1: 0 if success, 1 if error 
#const API_REGISTRATION= 11;       //miscstr1: error message | miscstr3: sms/mms/na/sb | miscid1: 0 if success, 1 if error
#const API_CONNECTSNS  = 12;       //miscstr1: error message | miscstr3: sms/mms/na/sb | miscid1: 0 if success, 1 if error 

# const GENERIC_SNS = 68;
# const YOUTUBE    = 27;
# const FLICKR     = 28;
# const FACEBOOK   = 29;
# const BEBO       = 30;
# const MYSPACE    = 31;
# const SMP  = 42;
# const TWITTER  = 47;
# const FRIENDSTER  = 48;
# const PICASA = 58;
# const BLOGGER = 61;
# const WORDPRESS  = 59;
# const HI5 = 63;
# const BIALEM = 64;
# const ORKUT = 65;
