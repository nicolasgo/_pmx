'''module for user related code.
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

from . import clean
import pandas as pd
import numpy as np

from .cohort import scale_for_time_units 
from .retention_index import retention_index

from . import initialize

from math import sqrt

class Users(object):
    '''represents Users behaviour on the social network
    '''
    def __init__(self, udf, sdf, validate_dfs = True, 
                 date_str_to_period = False,
                 fraction_of_population = 0.1,
                 trial = True):
        ''' Initialize the class instance.
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
                    validate_dfs, Boolean, to validate or not
                    date_str_to_period, Boolean, to convert datetime like
                                                 str to period objects
                    fraction_of_population, float, the fraction of the 
                                                   population that you
                                                   want to analyse.
                    trial, Boolean, to keep trial users or not
                    
        Note: both validate_df and date_str_to_period
              Booleans should not be True, True 
              in the current use case. For example, data that is not
              validated will have its datetime like string converted
              during the validation process. Validated data will not
              need to be revalidated but may need its datatime like strings 
              (if loaded from .csv file) converted to period objects.
              
        '''
        #may be deprecated.
        self.columns_to_correlate = [ 'retention_index',
                                      'user_engagement_rate', 
                                      'total_duration', 
                                      'activity_level', 
                                      'pv', 'variety',
                                      'friends', 'invites', 
                                      'sessions_per', 
                                      'session_duration']
        
        

        (udf, sdf, null_last_seen_df, 
          trial_df, after_last_seen_df 
         ) = initialize.initialize(udf, sdf, validate_dfs = validate_dfs, 
                                   date_str_to_period = date_str_to_period,
                                   fraction_of_population = 
                                   fraction_of_population,
                                   trial = trial)

        #A slightly better age that is normalized so we can do calculations. 
        #to get user engagement rate weight with duration
        udf['retention_index'] = retention_index(udf)

        
        #not sure which is the best representation (user_id index or time index)
        #keep both for now.
        self.sdf_time = sdf.copy().reset_index().set_index('time'
                                                          ).sort(inplace = 
                                                                 False )

        udf_time = udf.copy().reset_index().set_index('joined') 
        #rename the index
        udf_time.index.name = 'period'
        #We may need to set this on a uniform period range incase there are
        #days where no users joined.
        total_daily_users = udf_time.groupby(udf_time.index
                                            ).last_seen.count().cumsum()

        #slice on from the first session to the last session
        self.total_daily_users = total_daily_users[sdf.time.min():
                                                   sdf.time.max()]
        #short name for daily users
        tdu = self.total_daily_users

        agg_dict = { 'days':  pd.Series.count, 
                     'min' : np.min, 
                     'max' : np.max,
                     'mean' : np.mean }

        self.total_weekly_users = tdu.groupby(tdu.index.asfreq('W')
                                             ).aggregate(agg_dict)
                                             
        self.total_monthly_users = tdu.groupby(tdu.index.asfreq('M')
                                              ).aggregate(agg_dict)

        #We might need to move this above the validation because
        #when placed here it get the total validated users instead of the 
        #total users (if we have invalid users in the dataframe 
        # before validation )
        self.total_users = udf.shape[0]
        self.grouped = sdf.groupby( level = 0) #group by user_id (ie the index)

        
        self.fraction_of_population = fraction_of_population

        self.udf = udf
        
        self.sdf = sdf

    def get_churn_rate(self, time_span = 'D' ):
        '''method to calculate the churn rate based on the time_span
           Inputs: time_span, str in ('D', 'W', 'M')
           Output: df of the churn rate
        '''
        active_df = self.get_active_users(time_span = time_span,
                                          percentage = False)
        total_df = self.get_total_users(time_span)['max']

        churn_df = (total_df-active_df).div(active_df)

        return churn_df

    def get_active_users(self, time_span = 'D', percentage = False):
        '''method to get the active users in the given time_span (period)
           Inputs: time_span, str in ('D', 'W', 'M')
                   percentage, Boolean, flag to represent as a percentage or
                                        not
        '''
        
        df = self.sdf_time.groupby([self.sdf_time.index.asfreq(time_span)]
                                  ).user_id.nunique()
        
        total_users = self.get_total_users(time_span = time_span)

        if percentage:
            #still favors the older data because of new users joining
            #each day
            percentage_users = 100*(df.div(total_users))

            return percentage_users

        else:#return absolute number of users (need to add error estimate)
            return df

    def get_total_users(self, time_span ):
        '''method to get the total users based on the input time_span
           Inputs: time_span, str in ('D', 'W', 'M')
           Output: total_number_of_users, Series
        '''
        total_users = {'D' : self.total_daily_users,
                       'W' : self.total_weekly_users,
                       'M' : self.total_monthly_users }.get(time_span)

        return total_users

            
    def plot_active_users(self,  time_span, percentage = False, df = None):
        '''method to plot the active users for a given time span.
           The plot can be either as a percentage of the population
           of an absolute value.
           Inputs: time_span, str in ('D', 'W', 'M')
                   percentage, Boolean, flag to represent as a percentage or
                                        not
                   df, dataframe, if None the dataframe is calculated.
        '''
        if df is None:
            df = self.get_active_users(time_span = time_span, 
                                       percentage = percentage ) 

        if percentage:
            ylabel = '% Active Users'
            
        else:
            ylabel = 'Total Active Users'
            #scale to the total population
            df = df/self.fraction_of_population

        yerr = df.values/sqrt(self.total_users)
        
        ax = df.plot(figsize = (12,5), yerr = yerr)
        ax.set_ylabel(ylabel)
        ax.set_xlabel('Date')
        
       
    def get_daily(self, units = 'minutes'):
        '''get the daily quantities for all users.
        '''
        #make a copy so we can make modifications and preserve the original
        udf = self.udf.copy()
        udf = self.get_info(udf, time_span = 'D', units = units) #'D' => daily

        return udf

 
    def get_weekly(self, units = 'hours'):
        '''get the weekly quantities for all users.
        '''
        #make a copy so we can make modifications and preserve the original
        udf = self.udf.copy()
        udf = self.get_info(udf, time_span = 'W', units = units) #'W' => weekly

        return udf

    def get_monthly(self, units = 'days'):
        '''get the monthly quantities for all users.
        '''
        #make a copy so we can make modifications and preserve the original
        udf = self.udf.copy()        
        udf = self.get_info(udf, time_span = 'M', units = units) #'M' => monthly

        return udf

    def get_info(self, df, time_span = 'D', units = 'minutes'):
        '''get info does the brunt of the work for get_daily, get_weekly, etc
           Input: df, a copy of the user dataframe 
                  time_span, str, in ('D', 'W', 'M')
           Output: df, user df with additional attributes
        
        '''
        columns = ['duration', 'pv', 'variety', 'inbox', 'home',  
                   'frien', 'info', 'help', 'mymed',
                   'conve', 'media', 'uploa', 'avata',  
                   'activ', 'publi' ]

        columns_to_mean = columns[1:]
        columns_to_mean.append('activity_level')

        #reset/create the attributes before resampling 
        df['activity_level'] = 0.
        df['sessions_per'] = 0
        df['average_session_duration'] =  0
        df = df.join(pd.DataFrame( columns = columns, 
                                   index = df.index).fillna(0))
        
        grouped = self.grouped
        scale = scale_for_time_units(units)

        for user_id, group in grouped:
            #if the user exists add attributes to user table
            if user_id in df.index:
                #change index to time
                time_group_df = group.reset_index().set_index('time')

                #resample the time_group based on the input time_span using sum
                
                #span_df  = time_group_df[columns].resample( time_span, 
                #                                            how='sum')
                span_df = time_group_df
                #resample the time group based on input time_span using count
                #count_df = time_group_df['duration'].resample( time_span, 
                                                               #how='count')
                                                                   
                count_df = time_group_df['duration'].count()
                
                #rename column from duration to activity_level
                span_df = span_df.rename( columns = { 'duration': 
                                                      'activity_level'} )

                #Add the values to the 
                df.loc[ user_id, columns_to_mean ] = span_df.mean()
                #add mean count per span 
                df.loc[user_id, 'sessions_per'] = count_df.mean()

                #calculate the mean session duration, 
                #convert from seconds to minutes add add to user table
            
                df.loc[ user_id,  
                        'session_duration'] =  time_group_df['duration'
                                                            ].mean()/scale
    
        #scale activity level so that it is in minutes instead of seconds
        df['activity_level'] = df['activity_level']/scale

        df['user_engagement_rate'] = user_engagement_rate(df)


        #return the user dataframe with added attributes
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



