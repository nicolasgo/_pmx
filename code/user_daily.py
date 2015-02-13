'''module for user related code.
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import datetime

from .cohort import scale_for_time_units 
from .retention_index import retention_index
from .resample import resample
from . import validate
from . import dates

class Users(object):
    '''represents Users behaviour on the social network
    '''
    def __init__(self, udf, sdf, validate_dfs = True, 
                 date_str_to_period = False):
        ''' Initialize the class instance.
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
                    validate_dfs, Boolean, to validate or not
                    date_str_to_period, Boolean, to convert datetime like
                                                 str to period objects
        Note: both Booleans should not be True, True or False,False
              in the current use case. For example, data that is not
              validated will  its datetime like string converted
              during the validation process. Validated data will not
              need to be revalidated but may its datatime like strings 
              (if loaded from .csv file) converted to period objects
              
        '''
        self.columns_to_correlate = [ 'retention_index',
                                      'user_engagement_rate', 
                                      'total_duration', 
                                      'activity_level', 
                                      'pv', 'variety',
                                      'friends', 'invites', 
                                      'sessions_per', 
                                      'session_duration']
        
        if validate_dfs:
            (udf, sdf, null_last_seen_df, 
             trial_df, after_last_seen_df ) = validate.validate(udf, sdf)         
        
        if date_str_to_period and (not validate_dfs):
            udf = dates.to_date(udf)
            sdf = dates.to_date(sdf)

        #A slightly better age that is normalized so we can do calculations. 
        #to get user engagement rate weight with activity level
        udf['retention_index'] = retention_index(udf)

        
        self.udf = udf
        
        self.grouped = sdf.groupby( level = 0) #group by user_id (ie the index)

    def get_daily(self, units = 'minutes', how = 'mean'):
        '''get the daily quantities for all users.
        '''
        
        self.udf = self.get_info(self.udf, time_span = 'D', 
                                 units = units, how = how) #'D' => daily

        return self.udf

 
    def get_weekly(self, units = 'hours', how = 'mean'):
        '''get the weekly quantities for all users.
        '''
        #make a copy so we can make modifications and preserve the original
        
        self.udf = self.get_info(self.udf, time_span = 'W', 
                                 units = units, how = how) #'W' => weekly

        return self.udf

    def get_monthly(self, units = 'days', how = 'mean'):
        '''get the monthly quantities for all users.
        '''
             
        self.udf = self.get_info(self.udf, time_span = 'M', 
                                 units = units, how = how) #'M' => monthly

        return self.udf

    def get_info(self, df, time_span = 'D', units = 'minutes', how = 'mean'):
        '''get info does the brunt of the work for get_daily, get_weekly, etc
           Input: df, a copy of the user dataframe 
                  time_span, str, in ('D', 'W', 'M')
           Output: df, user df with additional attributes
        
        '''
        grouped = self.grouped 
        #scale the time by dividing by scale
        scale = scale_for_time_units(units)
        #use df in case it has been sliced for a range of
        #cohorts that grouped does not know about.
        print len(grouped.groups.keys()), len(df.index)
        ids_incommon = set(grouped.groups.keys()).intersection(df.index)
        print 'session user ids {0}'.format(len(grouped.groups.keys()))
        print 'user ids {0}'.format(len(df.index))
        print 'ids in common {0}'.format( len(ids_incommon))
        for user_id in ids_incommon:            
            group = grouped.get_group(user_id)
            val_counts = group.time.diff().fillna(0.).value_counts()
            max_inactive = val_counts.index.max()
            df.loc[user_id, 'max_inactive'] = max_inactive
            df.loc[user_id, 'max_inactive_counts'] = val_counts.ix[max_inactive]
            #change index to time
            udf = group.set_index('time')
            
            #Need to work out the columns here due to adding the dmodel
            if how == 'median':
                df.loc[user_id, udf.columns] = resample(time_span, udf 
                                                        ).median().values

            else:
                df.loc[user_id, udf.columns] = resample(time_span, udf 
                                                        ).mean().values

            
        #drop any ids that are not in common between the session data
        #and the users data
        print df.shape
        df = df.loc[ids_incommon]
        print df.shape
        
        #scale activity level so that it is in appropriate units
        df['activity_level'] = df['activity_level']/scale
        df['engagement_rate'] = user_engagement_rate(df)
        
        #sort the dataframe and convert object dtypes to numeric if possible
        return df


    def total_duration(self):
        '''method to calculate the total duration from the sessions dataframe
           and add it to the user dataframe (df)
           Input: df, DataFrame (user)
           Output: total_duration, Series
        '''
        #groupby user_id
        return self.grouped.duration.sum()

    def correlate(self, df):
        '''method to correlate the columns in columns_to_correlate for the user
           DataFrame
           Input: df, DataFrame
           Output: correlation matrix, DataFrame or Series       
        '''
        return df[self.columns_to_correlate].corr()

def user_engagement_rate(df):
    '''function to calculate the user engagement rate from the user dataframe.
       Input: df, DataFrame
       Output: user_engagement_rate, Series
    ''' 
    #determine the user engagement rate: first attempt 
    return df['retention_index']*df['activity_level']



