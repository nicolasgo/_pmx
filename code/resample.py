#!/usr/bin/env python
'''module for cohort related code.
   Created by Robert Kruhlak
   Note: cohorts are defined by a datetime.date object. This appears to be
         working well but all of the code has not been tested.
         They can be changed to a TimeStamp object (includes hours, mins, secs
         etc) with a couple changes. 
         1) in the set_to_start_of_month function
            uncomment: return mydatetime.replace( day = 1, minute = 0, hour = 0, 
                              second = 0, microsecond = 0) and comment the
                    current return statement.
         2) in dates.py uncomment:  comment the current the list comprehension
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division
import pandas as pd
import numpy as np
import time

from .split_csv import get_first_chars
from .dates import date_from_time

class Resample(object):
    '''Represents the resample class'''
    def __init__(self, users_filename, sessions_filename, first_chars = None):
        '''initialize the class instance. Currently, we don't do anything with
           the user data but it could be used to validate the user ids in the
           session log.'''
        self.udf = pd.read_csv(users_filename)
        #users dataframe can be processed normally.
        #Need it for creating daily_df, weekly_df, etc
        #sessions is too big to process at once
        #get the columns so we can create a dataframe from the 
        #.csv files because the shell script does not place a header
        # None of the 55 .csv files have a header so we take a risk
        fname2  = 'data/sessions23.pv.a.csv'
        temp_df = pd.read_csv(fname2, nrows=2)
        #The original 23 file has the ua column but the 55 files don't
        #and the *23 2014-11 does not.
        #In addition the *23 and *55 2014-11 files have headers but the 
        #aug, sept, oct *55 files don't
        if '55' in sessions_filename:
            temp_df = temp_df.drop('ua', axis = 1)
        if ('23' in sessions_filename) and ('1411' in sessions_filename):
            temp_df = temp_df.drop('ua', axis = 1)
        self.columns = temp_df.columns
        print self.columns
        #We need to coerce the 'time' like columns to TimeStamps so we can
        #do math on them

        user_date_cols = ['joined', 'last_seen']
        self.udf[user_date_cols] = self.udf[user_date_cols].astype('datetime64')

        #the sessions .csv file is split by the first character of the
        #user_id
        if first_chars is None:
            self.first_chars = get_first_chars()
        else:
            self.first_chars = first_chars
        pieces = sessions_filename.split('.')
        #insert an input location so we can increment the 
        #filename
        self.sessions_i_fn = pieces[0]+'_{0}.'+ '.'.join(pieces[1:])
        self.sessions_i_out_fn = (pieces[0] + '_{0}_daily_sums.' +
                                  '.'.join(pieces[1:]) )

    def daily(self, nrows = None):
        '''create daily dataframe'''
        columns_to_sum  = [ 'activity_level', 'pv', 'variety', 'inbox', 'home',  
                            'frien', 'info', 'help', 'mymed',
                            'conve', 'media', 'uploa', 'avata',  
                            'activ', 'publi' ]

        columns_to_count = ['duration']

        columns_to_value_count = ['dmodel', 'dversion', 'dfamily']
        
        self.run('D', columns_to_sum, columns_to_count,
                 columns_to_value_count, nrows = nrows)

    def run(self, time_span, columns_to_sum, columns_to_count, 
            columns_to_value_count, nrows = None):
        '''resample
           Input: time_span, str, in ('D', 'W', 'M')
                  how, str or dict, {'column_name':'how_to_resample',...}
           Output: df, resampled data
        '''
        #concatenate all the columns 
        columns_to_analyse = list(columns_to_sum)
        columns_to_analyse.extend(columns_to_value_count)
        columns_to_analyse.extend(columns_to_count)
        
        for char in self.first_chars:
            df = None
            span = {}
            #sessions dataframe
            print char
            #while testing only take 100 rows from each file
            sdf = pd.read_csv(self.sessions_i_fn.format(char), 
                              names = self.columns, nrows = nrows
                             ).fillna('Other')

            #sub_udf = udf.ix[set(sdf.user_id)]
            #convert time column from object to datetime 
            sdf.time = pd.to_datetime(sdf.time)

            #create an activity_level column
            sdf['activity_level'] = sdf['duration']
            #create groupby object
            user_grouped = sdf.groupby('user_id')
            start = time.time()
            
            for user_id, group in user_grouped:
                if 1: #user_id in sub_udf.index:
                    #change index to time
                    time_group_df = group.set_index('time')[columns_to_analyse]
                    time_grouped = time_group_df.groupby(lambda d: d.date())
                    span[user_id] = time_grouped[columns_to_sum].sum()
                    #This should be a single column 
                    if len(columns_to_count) == 1:
                        span[user_id]['count'] = time_grouped[columns_to_count
                                                             ].count()

                    
                    for col in columns_to_value_count:
                        span[user_id
                            ][col] = time_grouped[col
                                                 ].agg(lambda x: 
                                                       x.value_counts(
                                                                     ).index[0])
                    span[user_id] = span[user_id].reset_index()
                 
                    span[user_id]['user_id'] = user_id
            
            df = pd.concat( span.values(), ignore_index = True)
            df.to_csv(self.sessions_i_out_fn.format(char))
            print 'time to create: {0:.2} minutes'.format((time.time()-start)/60)    

def main( users_fname = None, sessions_fname = None, first_chars = None, 
          nrows = None):
    '''main function of the module. Purpose is to resample large .csv files
       that have been split by the first char of 
       the user_id. This is accomplished using 
       a bash command in  a subprocess (see split_csv.py or .ipynb for details).
    
       Input: fname, str, filename of interest
              first_chars, list of first characters of the user_id. Currently,
                           0 .. f (hex)
    '''       
    if users_fname is None:
        #filenames for the two .csv files version 2 located in the data folder

        users_fname = 'data/users55.a.csv'

    if sessions_fname is None:
        sessions_fname = 'data/sessions55.pv.a.1410.csv'

    resamp = Resample(users_fname, sessions_fname, first_chars)

    return resamp.daily(nrows = nrows)

def resample(time_span, time_df, how = 'sum'):
    '''resample the data from daily to daily, weekly, monthly
       use this if you don't want dates with no activity added.
       df.resample add new dates where there was no activity
       This can penalize users that only engage with the service on
       weekends. To Do: better method for dealing with how.
       Inputs: time_span, str, in ('D','W','M')
               time_df, df with a date/timestamp index
               how, str, method to use for resampling 
       Output, df resampled        
    '''
    if time_span == 'M':
        #groupby month and sum all the users's contributions
        grouped = time_df.groupby(lambda x :x.strftime('%Y %m')
                                 )
        if how == 'sum':
            df = grouped.sum()
        else:
            df = grouped.mean()
        df.index = [ date_from_time( time.strptime(val, '%Y %m') )
                     for val in df.index ]    
    elif time_span == 'W':
        #groupby week and sum all the user's contributions        
        grouped = time_df.groupby(lambda x :x.strftime('%Y %W') )
        if how == 'sum':
            df = grouped.sum()
        else:
            df = grouped.mean()

        #must have a week day for the strptime to work
        df.index = [ date_from_time(time.strptime(val+' 1', '%Y %W %w') )
                     for val in df.index]
                
    else: #assume default 'D' daily
          #we already have the daily sums for each user. 
          #group by the index and sum all the user's contributions
        grouped = time_df.groupby(level=0)
        if how == 'sum':
            df = grouped.sum()
        elif how == 'median':
            df = grouped.median()
        else:
            df = grouped.mean()
               
        #df = df#/time_df.sessions #mean engagement per session
    df.index.name = 'time'

    return df

def random_sample(df, fraction_of_population):
    '''function to randomly sample a dataframe
       given a fraction of the total population.
       Inputs: df, dataframe with a unique index so that the 
                   total population is given by the size of index of the
                   dataframe or .shape[0]
               fraction_of_population, float
       Output: randomly sampled dataframe
    '''
    #Need a way to get users across all cohorts
    total_population = df.shape[0]
        
    samples = int(fraction_of_population*total_population)

    sampled_index = np.random.choice(df.index.values, samples, 
                                     replace = False)
    #slice the dataframe for the sampled users
    return df.ix[sampled_index]

if __name__ == '__main__':
    
    main(nrows = None)
