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
import datetime

from .retention_index import retention_index

from .dates import set_to_start_of_the_month

from . import clean
from .plot import  radviz_plot
from .plot import engagement_chart as engage_chart
from .plot import devices_chart as d_chart

#from matplotlib.dates import DateFormatter

DEFAULT_COHORT_RANGE = 'all'

class Cohorts(object):
    '''represents Users behaviour on the social network
    '''
    def __init__(self, udf, sdf):
        ''' Initialize the class instance.
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
        '''
        self.columns_to_correlate = [ 'retention_index',
                                      'engagement_rate', 
                                      'total_duration', 
                                      'activity_level', 
                                      'pv', 'variety',
                                      'friends', 'invites', 
                                      'sessions_per', 
                                      'session_duration',
                                      'size', 'rcvdInv']
        #clean the device column because some of the devices have spurious
        #symbols.
        sdf = sdf.sort('time')
        sdf['device'] = clean.clean_device(sdf['device'])
        sdf['dmodel'] = clean.clean_dmodel(sdf['dmodel'])

        #create cohort column in users df
        #%m is zero-padded month so we can sort the index
        #cohort is a datetime object with the 'day' always equal 1.
        udf['cohort'] = udf.joined.apply( set_to_start_of_the_month)

        #create cohort dataframe

        self.cohort_df = pd.DataFrame( index = set(udf['cohort']), 
                                       columns = self.columns_to_correlate)

        #A slightly better age that is normalized so we can do calculations. 
        #to get user engagement rate weight with activity level
        udf['retention_index'] = retention_index(udf)


        #fill nan values with 0
        cols_to_fill_na = ['friends', 'invites', 'rcvdInv'] 
        udf[cols_to_fill_na] = udf[cols_to_fill_na].fillna(0)

        #add cohort and retention_index column to the sessions dataframe
        sdf = sdf.join(udf[['retention_index', 'cohort']], how = 'left' )  
        #define the engagement_rate column
        sdf['engagement_rate'] = sdf['duration']*sdf['retention_index']
 
        #make instance variables so all the methods have access
        self.udf = udf
        self.sdf = sdf

        #group by cohorts in init so we only need to do it once
        self.grouped = self.udf.groupby('cohort') 
        
        #list of all cohorts from the grouped users table
        self.all_cohorts = self.grouped.groups.keys()


    def get_daily(self, cohort_range = 'all', units = 'minutes'):
        '''get the daily mean quantities for all or a range of cohorts.
           
        '''
        cdf = choose_cohorts(cohort_range, self.cohort_df)
        cdf = self.get_info(cdf, time_span = 'D', units = units) #'D' => daily
        return cdf

 
    def get_weekly(self, cohort_range = 'all', units = 'hours'):
        '''get the weekly mean quantities for all cohorts.
        '''
        cdf = choose_cohorts(cohort_range, self.cohort_df)

        cdf = self.get_info(cdf, time_span = 'W', units = units) #'W' => weekly

        return cdf

    def get_monthly(self, cohort_range = 'all', units = 'hours'):
        '''get the monthly mean quantities for all cohorts.
        '''
        #make a copy so we can make modifications and preserve the original
        cdf = choose_cohorts(cohort_range, self.cohort_df)        
        cdf = self.get_info(cdf, time_span = 'M', units = units) #'M' => monthly

        return cdf

    def get_info(self, df, time_span = 'D', units = 'minutes'):
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
        for name in df.index:            
            group = grouped.get_group(name)
            #take only the distinct ids
            cohort_ids = set(group.index)
            cohort_sdf = self.sdf.ix[cohort_ids]
            #change index to time
            time_group_df = cohort_sdf.reset_index().set_index('time')

            #resample the time_group based on the input time_span using sum
            span_df  = time_group_df[['duration',
                                      'pv',
                                      'variety']].resample( time_span, 
                                                            how='sum').dropna()
            #resample the time group based on input time_span using count
            count_df = time_group_df['duration'].resample( time_span, 
                                                           how='count').dropna()
    
            #rename column from duration to activity_level
            span_df = span_df.rename( columns = { 'duration': 
                                                  'activity_level'} )

            #Add the values to the dataframe
            df.loc[ name, 
                    ['activity_level', 'pv', 'variety'] ] = span_df.mean()
                
            #add mean count per span 
            df.loc[ name, 'sessions_per'] = count_df.mean()
        
            #add cohort retention_index, friends and invites
            df.loc[ name, [ 'retention_index', 
                            'friends', 
                            'invites'] ] = group[ ['retention_index', 'friends', 
                                                   'invites'] ].mean()
            
            #calculate the mean session duration, 
            #convert from seconds to minutes add to user table
            df.loc[ name,  
                    'session_duration'] =  time_group_df['duration'].mean()/60

            df.loc[ name, 
                    'total_duration' ] = time_group_df['duration'].sum()/scale

            df.loc[ name, 'size' ] = group.joined.count()
    
        #scale activity level so that it is in minutes instead of seconds
        df['activity_level'] = df['activity_level']/60

        df['engagement_rate'] = engagement_rate(df)

        #sort the dataframe and convert object dtypes to numeric if possible
        return df.sort().convert_objects( convert_numeric = True )

    def get_devices(self, cohort_range = DEFAULT_COHORT_RANGE):
        '''method to create a dataframe with cohort as the index and 
           devices as columns.
           Useful for creating a bar chart
           Output: DataFrame
        '''
        if cohort_range == DEFAULT_COHORT_RANGE:
            #use the entire cohort_range from the grouped users table
            cohort_range = self.all_cohorts
        else:
            #validate and use the input cohort_range
            cohort_range = validated_cohort_range( self.all_cohorts, 
                                                   cohort_range)
        
        #create the device dataframe
        device_df = pd.DataFrame( index = cohort_range, 
                                  columns = set(self.sdf.device))
        for name in cohort_range:
            group = self.grouped.get_group(name)
            #take only the distinct ids
            cohort_ids = set(group.index)
            cohort_sdf = self.sdf.ix[cohort_ids]

            devices = cohort_sdf.groupby('dmodel').duration.count()
            sessions = cohort_sdf.duration.count()
            #make it a percentage
            device_df.loc[name, devices.index] = 100 * devices/ sessions 

        #drop devices that were never used
        device_df=device_df.dropna(axis=1, how='all')

        #fill devices that were not used with 0
        return device_df.fillna(0)

    def get_page_views( self,  cohort_range = DEFAULT_COHORT_RANGE, 
                        columns = None, percent = False):
        '''Method to get the page view information in dataframe format
           Input: df, dataframe or None,
                  cohort_range, 'all' or list of datetime.date objects
                  columns, None or list of strings corresponding to the
                           columns in the sessions dataset
                  percent, Boolean, tally as a percent of the total pageviews
        '''
        
        if cohort_range == DEFAULT_COHORT_RANGE:
            #use the entire cohort_range from the grouped users table
            cohort_range = self.all_cohorts
        else:
            #validate and use the input cohort_range
            cohort_range = validated_cohort_range( self.all_cohorts, 
                                                   cohort_range)

        if columns is None:
            columns = [ 'inbox', 'mymed', 'conve', 'activ', 'home', 'frien', 
                        'info', 'media', 'uploa', 'avata', 'publi', 'help']

        df = pd.DataFrame( index = cohort_range, columns = columns)

        for name in cohort_range:
            group = self.grouped.get_group(name)
            #take only the distinct ids
            cohort_ids = set(group.index)
            cohort_sdf = self.sdf.loc[cohort_ids, columns]
            #sum all the columns so we get totals for the cohort
            pages = cohort_sdf.sum()

            #count the sessions : might be useful if we want to normalize
            # the sum above
            sessions = cohort_sdf['inbox'].count()
            #get the total page views for the cohort
            page_views = self.sdf.ix[cohort_ids, 'pv' ].sum()
            
            df.loc[name, pages.index] = pages

            if percent:
                #create percent of the total page_views.
                df.ix[name] = 100*df.ix[name]/page_views

        return df.fillna(0)
    
    def get_page_views_user( self, cohort_range = DEFAULT_COHORT_RANGE, 
                             columns = None, percent = False):
        '''Method to get the page view information in dataframe format
           Input: df, dataframe or None,
                  cohort_range, 'all' or list of datetime.date objects
                  columns, None or list of strings corresponding to the
                           columns in the sessions dataset
                  percent, Boolean, tally as a percent of the total pageviews
        '''
        
        if cohort_range == DEFAULT_COHORT_RANGE:
            #use the entire cohort_range from the grouped users table
            cohort_range = self.all_cohorts
        else:
            #validate and use the input cohort_range
            cohort_range = validated_cohort_range( self.all_cohorts, 
                                                   cohort_range)

        if columns is None:
            columns = [ 'inbox', 'home',  'frien', 'info', 'help', 'mymed',
                         'conve', 'media', 'uploa', 'avata',  'activ', 'publi' ]

        df = None

        for name in cohort_range:
            group = self.grouped.get_group(name)
            #take only the distinct ids
            cohort_ids = set(group.index)
            cohort_sdf = self.sdf.loc[cohort_ids, columns]
            #sum all the columns so we get totals for the each user
            pages = cohort_sdf.groupby(level = 0).sum()

            #get the total page views for the cohort
            total_page_views = self.sdf.ix[cohort_ids, 'pv' ].sum()
            
            pages['cohort'] = name

            #make multiindex user_id, cohort
            pages = pages.set_index('cohort', append = True)

            #change the order 
            pages = pages.reorder_levels(['cohort', 'user_id'])

            if percent:
                #create percent of the total page_views.
                pages = 100*pages/total_page_views

            if df is None:
                df = pages
            else:
                df = df.append(pages)

        return df.fillna(0)

    def radviz_page_views( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                           percent = False, sort = None ):
        '''method to create a radvis chart of the page views data
           To do: move general code to plot.py so we can reuse

           Inputs: df, DataFrame, with the page views dataset or None
                   percent, Boolean, whether to use a percentage for the
                                     page view dataset or not.
                                     (Only available when df = None)
                   cohort_range, 'all' or list of datetime.date objects
                   sort, None or tuple ( row_sort, column_sort) where 
                         column_sort and row_sort can be None, True,
                         descending. sort the dataframe before plotting
           Output: matplotlib axes
        '''
        
        if df is None:
            df = self.get_page_views( cohort_range = cohort_range, 
                                      percent = percent)
        if sort is not None:
            try:
                row_sort = sort[0]
                column_sort = sort[1]
            
                if row_sort:
                    ascending = {'ascending' : True, 
                                 'descending' : False }.get(row_sort, True)
                    df = df.sort( ascending = ascending )
                if column_sort:
                    ascending = {'ascending' : True, 
                                 'descending' : False }.get(row_sort, True)
                    df = df.sort( axis = 1, ascending = ascending ) 
            except KeyError( ('sort must be None or a tuple '
                              '(row_sort, column_sort)') ):
                print 'continue without sorting'

        #Need cohort as a column not the index so we can use it
        #as the categories.  make sure that the index is named 'cohort'
        df.index.name = 'cohort'
        ax = radviz_plot(df.reset_index(), category = 'cohort')

        #return the axes so the user can change properties if needed.
        return ax


    def devices_chart( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                       top = 5, horizontal = False):
        '''method to create a stacked bar chart for the devices_df.
           Inputs: df, DataFrame or None with device information
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   top, int, top N devices to consider for the chart
        '''   
        axes_labels = ('cohort', ' device % ' )
        if df is None: #get devices dataframe
            df = self.get_devices(cohort_range = cohort_range)
        #find the most used devices
        top_devices = df.sum().sort( ascending = False, 
                                     inplace = False).head(top).index
        #keep only the top devices
        df = df[top_devices].sort(inplace = False)
        ax = d_chart(df, top, axes_labels, horizontal)        
        #return the axes for further tweaking
        return ax

    def engagement_chart( self, df = None, time_span = 'W', 
                          cohort_range = 'all',
                          normalized = False, units = 'minutes',
                          horizontal = False, ax = None, picker = None ):
        '''method to create a stacked bar chart for the engagement_df.
           Inputs: df, DataFrame or None with device information
                   time_span, str, in ('W', 'M')
                   horizontal, boolean, axes orientation
                   The parameters below only work when df = None
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   normalized, boolean, whether to normalize to the size
                                        of the cohort
                   units, str, in ('minutes', 'hours', 'seconds')
                   
        '''   
        if df is None: #get devices dataframe
            df = self.get_engagement_rates( time_span = time_span, 
                                            cohort_range = cohort_range,
                                            normalized = normalized,
                                            units = units)
        
        ax = engage_chart( df, horizontal = horizontal, 
                           ax = ax, picker = picker, units = units)
        #return the axes for further tweaking
        return ax

    def get_engagement_rates( self, time_span = 'W', cohort_range = 'all',
                              normalized = False, units = None, how = 'sum'):
        '''method to get the engagement rate all cohorts resampled
           to the time_span
           Inputs: time_span, str, short name for day, week, month
                                   in ('D', 'W', 'M')
                   normalized, boolean, whether to divide by cohort size or not
                   units, str, engagement rate units in 
                               ('seconds', 'minutes', 'hours', 'days', 'weeks')
                   how, str, how to determine the rate in ('sum, 'mean') 
                   cohort_range, 'all' or pandas date_range
        '''
        
        if cohort_range == DEFAULT_COHORT_RANGE:
            #use the entire cohort_range from the grouped users table
            cohort_range = self.all_cohorts
        else:
            #validate and use the input cohort_range
            cohort_range = validated_cohort_range( self.all_cohorts, 
                                                   cohort_range)

        #create the variable so we can determine whether to append the cohort
        # or not. 
        engagement_df = None 
        
        for name in cohort_range:
            #get the group with cohort name
            group = self.grouped.get_group(name)

            #take only the distinct ids
            cohort_ids = set(group.index)
            #slice the sessions dataframe for the cohort
            cohort_sdf = self.sdf.ix[cohort_ids]

            
            #change index to time
            cohort_sdf = cohort_sdf.reset_index().set_index('time')
        
            #calculate the cohort size
            cohort_size = group.joined.count()
            

            #resample the time_group based on the input time_span using how 
            #the retention index should be identical for each session of the
            #same day so we could use mean, min, max but not sum.
            #Still need a better implementation for weekly time span. For now
            #we will use mean           
            span_df  = cohort_sdf[['engagement_rate', 'retention_index']
                                 ].resample( time_span, 
                                             how = { 'engagement_rate': how,
                                                     'retention_index': 'mean'}
                                           ).dropna()

            if normalized: #scale to cohort size
                span_df = span_df/cohort_size
            
            #add cohort column
            span_df['cohort'] = name
            
            #add the size of the cohort so we can improve the bar chart
            span_df['size'] = cohort_size

            span_df = span_df.set_index(['cohort'], append = True
                                       ).reorder_levels(['cohort', 'time'])

            if engagement_df is None:
                engagement_df = span_df
            else:
                #must assign unlike regular list append
                engagement_df = engagement_df.append(span_df) 
        #add a units column so that other methods can make appropriate decisions
        engagement_df['units'] = units
        #scale enagement rate so that it is in the appropriate units
        scale = scale_for_time_units(units)
        engagement_df.engagement_rate = engagement_df.engagement_rate/scale

        #sort the dataframe and convert object dtypes to numeric if possible
        return engagement_df.sort(inplace = False)

    def correlate(self, df):
        '''method to correlate the columns in columns_to_correlate for the user
           DataFrame
           Input: df, DataFrame
           Output: correlation matrix, DataFrame or Series       
        '''
        return df[self.columns_to_correlate].corr()

def engagement_rate(df):
    '''function to calculate the user engagement rate from the user dataframe.
       Input: df, DataFrame
       Output: user_engagement_rate, Series
    ''' 
    #determine the user engagement rate: first attempt 
    return df['retention_index']*df['activity_level']

def choose_cohorts(cohort_range, cohort_df):
    '''helper function for choosing the range of chorts to analyse.
       Input: cohort_range, list or index of datetime.date objects
              cohort_df, dataframe with cohort as the index
       Output: modified cohort_df sliced to the validated cohort_range
    '''
    if cohort_range == 'all': # default
        #make a copy so we can make modifications and preserve the original
        return cohort_df.copy()
            
    else: 
        cohort_range = validated_cohort_range(cohort_df.index, cohort_range)
        
        #need to be careful about empty cohort_range. Do we want to return
        #a dataframe with no index or revert back to all?
        return cohort_df.ix[cohort_range]

def validated_cohort_range(all_cohorts, cohort_range):
    '''helper function to validate the cohort_range against all the available
       cohorts. Using the cohort range to select part of the cohort_df
       is not as simple as slicing with the input cohort_range. 
       because all_cohorts may not be continuous
       Example: This occurs when the site was young < 2013
                and there are some months when there are no cohorts
       Note: can return an empty list.
       Input: all_cohorts, list or index of datetime.date objects
              cohort_range, list or index of datetime.date objects
       Output: validated list of datetime.date objects
    '''
    return list( set(cohort_range).intersection(all_cohorts) )

def scale_for_time_units(units):
    '''function to get the time scale factor 
       assuming the time to be converted is in seconds. The returned 
       value is seconds/units
       Input: units, str, in ('minutes', 'hours', 'days')
       Output: scale, int, in seconds/units
    '''
    hours = 3600
    days = hours*24
    weeks = days*7
    return { 'seconds' : 1,
             'minutes' : 60,
             'hours' : hours,
             'days' : days, 
             'weeks' : weeks
           }.get(units, 1)

def sub_range( center_index, cohort_range, num_cohorts = None, 
               max_cohorts = 5):
    '''function to create a sub range given an array of cohorts and the 
       index to center the range on
       Input: center_index, int
              cohort_range, np array 
              num_cohorts, int, number of cohorts in cohort range. 
                                if None len(cohort_range)
       Ouput: np array       
    '''
    
    if num_cohorts is None:
        num_cohorts = len(cohort_range)
        
    #determine if the number of cohorts is odd    
    odd = is_odd(num_cohorts)
    
    if odd:
        to_view = min(max_cohorts, num_cohorts)
        
    else:
        to_view = min(max_cohorts, num_cohorts - 1)
            
    limit = int((to_view - 1)/2)    
    #ensure that the indexes wrap aroun the end points using modulo
    view_index = np.arange(center_index-limit, center_index+limit+1, 
                           1) % num_cohorts 
    
    #make a list so get_engagement_rates can handle
    return list(cohort_range[view_index])

def is_odd(num):
    '''determine if the number is odd'''
    return num % 2
