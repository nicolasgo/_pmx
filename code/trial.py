'''Module for functions, classes etc related to trial users.
   Created by Robert Kruhlak
'''
from .retention_index import retention_index

def create_users(udf, sdf, sub_types = ['inactive','active']):
    '''function to create user of a specified type. It is assumed that
       the udf and sdf have been validated and thus have the same user_ids.
       Inputs: udf, user dataframe
               sdf, session dataframe
               utype, type of user to create
       Output: user_dict, dict of user dataframes        
    '''
    sdf = sdf.fillna(0)
    udf['retention_index'] = retention_index(udf)
    
    #index of sdf is user_id. Calculate the last session for each user
    udf['last_session'] = sdf.groupby(level=0).time.max()

    user_dict = {}
    ujoined = udf.joined
    for utype in sub_types:
        if utype == 'inactive':
            user_dict[utype] =  udf[ujoined > udf.last_session]

        elif utype == 'active':

            user_dict[utype] = udf[ujoined <= udf.last_session]
    
        sessions = sdf.ix[user_dict[utype].index]
        print '{0} {1} sessions'.format(sessions.shape[0], utype)
        grouped = sessions.groupby(level = 0)
        if utype == 'active':
            user_dict[utype]['above'] = 0

        user_dict[utype]['below'] = 0
        s_columns = ['frien','help', 'publi', 'info', 'home']
        med_columns = ['activity_level', 'pv']
        for name, group in grouped:
            njoined = ujoined.ix[name]
            user_dict[utype].loc[name, 'below'] = group[group.time < njoined
                                                       ].activity_level.count()
            if utype == 'active':
                user_dict[utype].loc[name, 
                                     'above'] = group[group.time >= 
                                                      njoined].activity_level.count()
        if utype == 'inactive':
            user_dict[utype]['between'] = (user_dict[utype]['joined'] - 
                                           user_dict[utype]['last_session']
                                          ).astype('timedelta64[D]')
 

        group_median = grouped[med_columns].median()
        group_sum = grouped[s_columns].sum()
        user_dict[utype][med_columns] = group_median
        user_dict[utype][s_columns] = group_sum

    return user_dict
