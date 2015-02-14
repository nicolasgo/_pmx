# country codes: 
# 52 - Mexico
# 54 - Argentina
# 55 - Brazil
# 51 - Peru
# 56 - Chile
# 57 - Colombia
# 58 - Venezuela
# 501 - Belize
# 504 - Honduras
# 505 - Nicaragua
# 506 - Costa Rica
# 507 - Panama
# 593 - Bolivia
# 593 - Ecuador
# 595 - Paraguay
# 598 - Uruguay
# 1809 - 1829 - 1849 - Dominican Republic
# http://travel.airwise.com/info/intl_numbers.html
# here
SELECT 
    (select count(*) from smp.smp_user where state = 1) as TotalRegSinceLaunch,
    (select count(*) from smp.smp_user where msisdn REGEXP '^52' and state=1) as Mex,
    (select count(*) from smp.smp_user where msisdn REGEXP '^55' and state=1) as Br,
    (select count(*) from smp.smp_user where msisdn REGEXP '^54' and state=1) as Ar,
    (select count(*) from smp.smp_user where msisdn REGEXP '^51' and state=1) as Pe,
    (select count(*) from smp.smp_user where  msisdn REGEXP '^56' and state=1) as Ch,
    (select count(*) from smp.smp_user where  msisdn REGEXP '^507' and state=1) as Pa,
    (select count(*) from smp.smp_user where  msisdn REGEXP '^18' and state=1) as Do,
    (select count(*) from smp.smp_user where  msisdn REGEXP '^57' and state=1) as Co,
    (select count(*) from smp_sns.sns_facebook_hook where valid=1) as facebook,
    (select count(*) from smp_sns.sns_twitter_hook where valid=1) as twitter,
    (select count(*) from smp_sns.sns_youtube_hook where valid=1) as youtube,
    (select count(*) from smp_sns.sns_picasa_hook where valid=1) as picasa,
    (select count(*) from smp_sns.sns_wordpress_hook where valid=1) as wordpress;

