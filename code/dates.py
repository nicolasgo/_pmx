'''module for handling dates, date_ranges, etc.
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import pandas as pd
import datetime
import time


def cohort_range( start_year, end_year, start_month = 1, end_month = 1, 
                  keep_last = True):
    '''function to calculate a range of cohorts to select from a dataframe
       given a start_year and end_year. Optionally, a start_month and end_month
       can be submitted. Note this is not like the python  range function. This
       function includes the end_year or the end_year and end_month when 
       specified. 
       To drop the end point pass keep_last = False
       Input: start_year: str, year to start the range with in yyyy format
              end_year: str, year to end the range with in yyyy format
              start_month, str, month for the first cohort
              end_month, str, month for the final cohort 
       Output: an array of date objects
    '''
     
    start_period = pd.Period( year=start_year, month = start_month,  
                              freq = 'M')
    end_period = pd.Period( year = end_year, month = end_month,  
                            freq = 'M')
    period_rng = pd.period_range(start_period,
                                 end_period, 
                                 freq = 'M') #Monthly frequency

    #may need to convert to a list.
    period_rng = list(period_rng)
     
    if keep_last:
        return period_rng
    else: #drop the end point like python range
        return period_rng
    

def date_from_time(t):
    '''make a date object from a time struct
       Used when resampling so we don't create empty days/weeks etc
       like pd.resample
       Input: t, time_struct
       Output date object
    ''' 
    return datetime.date.fromtimestamp(time.mktime(t))


def set_to_start_of_the_month(myperiod):
    '''function to set a period object to the start of the month
        This function is used to determine
       the cohort for the users table.
       Input: myperiod, Pandas Period  object
       Output: Period with 'M' frequency with 's' meaning start of the month
    '''
    return myperiod.asfreq('M','s')
    
def to_datetime(df, columns):
    '''function to convert 'datetime' like columns from strings to date objects
       Inputs: df, dataframe with one or more columns that are time like
               columns, columns to convert from string objects to date objects
       Output: df
    '''
    #convert strings representations of the 'datetime' to datetime objects
    
    for index, val in enumerate(df[columns].dtypes == 
                                'object'):
        if val:
            column = columns[index]
            #use coerce to we get NaT objects instead of the input string
            #when pandas can't sort out the conversion
            df.loc[:,column] = pd.to_datetime(df[column], unit='ns', 
                                              coerce = True
                                             )
    
    return df

def to_date(df, columns, obj = False):
    '''function to convert 'datetime' like columns from strings to date objects
       Inputs: df, dataframe with one or more columns that are time like
               columns, columns to convert from string objects to date objects
       Output: df
    '''
    #convert timestamp objects to period objects
    #This should make it easier to compare the sessions dates with the users
    #table dates.

    #there is currently a bug in pandas 15.x ( #7557) where periodNaT  
    #is not handled correctly by isnull and hence dropna. So we need to make
    #sure that
    #we don't have any nan values before calling this function. 2015-01-25
    #we need to integrate a test for the columns already being Period objects
    #because the conversion does not like it if it is already the correct type.
    if obj:
        for index, val in enumerate(df[columns].dtypes == 
                                    'object'):
            if val:
                column = columns[index]
                #convert str to datetime object first
                df.loc[:,column] = pd.to_datetime(df[column]).dt.to_period('D')
    else:
        for index, val in enumerate(df[columns].dtypes != 
                                'object'):
            if val:
                column = columns[index]
            
                df.loc[:,column] =df[column].dt.to_period('D')
    
    return df
