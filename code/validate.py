'''module for cohort related code.
   Created by Robert Kruhlak
   Note: cohorts are defined by a datetime.date object. This appears to be
         working well but all of the code has not been tested.
         They can be changed to a TimeStamp object (includes hours, mins, secs
         etc) with a couple changes. 
         1) in the set_to_start_of_the_month function
            uncomment: return mydatetime.replace( day = 1, minute = 0, hour = 0, 
                              second = 0, microsecond = 0) and comment the
                    current return statement.
         2) in dates.py uncomment:  comment the current the list comprehension
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import pandas as pd
import numpy as np
from scipy.stats import mode

import datetime
from code import dates


def validate(udf, sdf, trial = False):
    ''' Initialize the class instance.
        Inputs: udf, dataframe with user data
                sdf, dataframe with sessions data
        Outputs, validated udf and sdf
    '''
    #will be used to store 'trial' users that converted to
    #another category of user during the sessions time frame.
    trial_df = pd.DataFrame() #empty dataframe
    #will be used to store users that have a null last_seen date
    null_last_seen_df = pd.DataFrame() 

    #will be used to store users that have a joined date after
    #their last_seen date
    after_last_seen_df = pd.DataFrame()

    #if the device column has crept into the sdf dataframe
    #remove it.
    if 'device' in sdf.columns:
        sdf = sdf.drop('device', axis = 1)
    print 'users table size {0}'.format(udf.shape)
    print 'sessions table size {0}'.format(sdf.shape)
    #This must come first due to bug #7557 in pandas 15.x
    #because once we convert to Period the dropna and
    #pd.isnull don't work properly.
    udf = udf.dropna(axis = 0, subset = ['joined'])
    
    null_mask = pd.isnull(udf['last_seen'])
    if null_mask.any():
        null_last_seen_df = udf[null_mask]
        print ('We have {0} users with a null '
               'value for the last_seen date'
              ).format(null_last_seen_df.shape[0])

    
        print 'Removing null last seen users'
        udf = udf[~null_mask]

    #We need to coerce the 'time' like columns to TimeStamps 
    #so we can do math on them. Do this for both dataframes
    columns_to_convert = ['joined', 'last_seen']
    
    
    #convert datetime like strings to period objects (date only)
    udf = dates.to_date(dates.to_datetime(udf, columns = columns_to_convert
                                         ).dropna(subset=['last_seen']), 
                        columns = columns_to_convert)

    sdf = dates.to_date(dates.to_datetime(sdf, columns =['time']
                                         ).dropna(subset=['time']), 
                        columns = ['time'])
    
    #check for users that joined after their last_seen date
    
    mask = udf.joined > udf.last_seen 
    if mask.any():   
        after_last_seen_df = udf[mask]
        print ('Users that joined '
               'after last seen, {0}'
              ).format(after_last_seen_df.shape[0])
    
        #keep only valid users
        udf = udf.ix[~mask]

    #There is the possibility that the user data set and sessions data set
    #do not overlap completely in user_ids. We want to take the intersection
    #to get the set of valid user ids
    user_uids = set(udf.index)
    session_uids = set(sdf.index)
    ids_in_common = session_uids.intersection(user_uids)
    
    #slice the users and sessions dataframe
    udf = udf.ix[ids_in_common]
    sdf = sdf.ix[ids_in_common]

    print ('size of sessions data set after intersection {0} with {1} ' 
           'users remaining.').format(sdf.shape, udf.shape[0])

    #determine most recent last seen date from the users table
    most_recent_last_seen_date = udf.last_seen.max()
    #determine the most recent session date
    most_recent_session = sdf.time.max()

    print ('most recent "last seen" date, {0} and the most '
           'recent session date, {1}').format(most_recent_last_seen_date,
                                              most_recent_session)

    #This needs to happen after the intersection otherwise we could generate
    # last_seen dates before the joined date.
    if most_recent_last_seen_date > most_recent_session:
        print ('We need to adjust the last_seen date to calculate '
               'the users age at the time of the last session. ')
        #do we need the conversion to datetime now that we are using
        #period to represent the last_seen, joined and time.
        udf['last_seen'] = [min(val, most_recent_session) 
                            for val in 
                            udf.last_seen.values ]

        #check just in case
        uafter_index = udf[(udf.joined > udf.last_seen)].index
        num_users_with_joined_after_last_seen = len(uafter_index)

        if num_users_with_joined_after_last_seen:
            print ('We have {0} users that have joined after last seen '
                   'due to adjustment of last seen date to correspond with '
                   'the last session. Dropping those users.'
                  ).format(num_users_with_joined_after_last_seen) 

            udf = udf.drop(uafter_index)
            sdf = sdf.drop(uafter_index)

    
        #update the most_recent_last_seen_date
        most_recent_last_seen_date = udf.last_seen.max()
        most_recent_session = sdf.time.max()

    #In case we are the other way around where we have the most recent_session
    #>most recent last seen. 
    #take only session data that is on or before the most recent date  
    most_recent_mask = sdf.time > most_recent_last_seen_date      
    if most_recent_mask.any():
        #keep only those sessions that occur on or before the most recent
        #last seen date
        sdf = sdf[~most_recent_mask]

        print ('size of sessions dataset {0} after '
               'removing sessions that occur after the '
               'most recent "last seen" date').format(sdf.shape)

    
    #trial users that have joined -- converted category?
    first_session = sdf.groupby(level = 0).time.min()
    udf['trial'] =   udf.joined - first_session
    trial_mask = udf.trial > 0
    if trial_mask.any():
        print ('{0} trial users with a join date after their initial '
               'session. ').format(udf[trial_mask].shape[0])
        trial_df = udf[trial_mask]
        
    if not trial: #flag whether to drop this group of users or not
        print udf.shape
        udf = udf[~trial_mask]
        #print udf.shape
        #print len(set(sdf.index))
        sdf = sdf.ix[udf.index]
        #print len(set(sdf.index))
        print ('size of sessions dataset {0} and {1} users  remaining '
               'after removing trial users that joined after their ' 
               'initial session '
              ).format(sdf.shape, udf.shape[0])
    elif not trial_df.empty: 
        #for trial users adjust the sessions so that the first 
        #session occurs on 
        #or after the joined date.
        trial_uids = udf[trial_mask].index
        (valid_trial_sessions_df, 
         trial_df )= get_valid_sessions(sdf.copy().ix[trial_uids], 
                                        trial_df)
        #replace the trial user sessions with the valid sessions
        #that occur on or after the join date
        
        sdf = pd.concat([sdf.drop(trial_uids), 
                         valid_trial_sessions_df])
        #keep only the users in sdf in the udf
        udf = udf.ix[set(sdf.index)]
        
    columns_to_fill = [ u'disk_usage', u'state', u'friends', u'invites',
                        u'rcvdInv', u'rejectd', u'sim', u'twFrs', u'fbFrs', 
                        u'yt', u'pi', u'fk' ]
    udf[columns_to_fill] = udf[columns_to_fill].fillna(0)
    
    return udf, sdf, null_last_seen_df, trial_df, after_last_seen_df

def get_valid_sessions(sdf, udf):
    '''function to get the valid sessions when we
       have trial users that have a joined date 
       after their first session
    '''
    pieces = {}
    grouped = sdf.groupby(level = 0)
    
    for uid in udf.index:
        group = grouped.get_group(uid)
        temp = group[group.time >= udf.loc[uid, 'joined'] ]
        if not temp.empty:
            pieces[uid] = temp
            
    pieces_df = pd.concat(pieces.values())
    
    #check if we lost some users
    index_diff = set(udf.index).difference(set(pieces_df.index)) 
    if index_diff:
        print ('We dropped {0} trial users because they did not have '
               'a session on or after the joined date'
              ).format(len(index_diff))
        #drop invalid trial users
        trial_df = udf.drop(index_diff)
        
    return pieces_df, trial_df
