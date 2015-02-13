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

import calendar

from .retention_index import retention_index

from .dates import set_to_start_of_the_month

from .cohort import choose_cohorts

from .plot import  radviz_plot
from .plot import engagement_chart as engage_chart
from .plot import devices_chart as d_chart

from . import validate
from .resample import resample

#from matplotlib.dates import DateFormatter

DEFAULT_COHORT_RANGE = 'all'

class Cohorts(object):
    '''represents Users behaviour on the social network
    '''
    def __init__(self, udf, sdf,  validate_dfs = True, 
                 date_str_to_period = False, fraction_of_population = 0.1,
                 trial = True):
        ''' Initialize the class instance.
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
                    validate_dfs, Boolean, to validate or not
                    date_str_to_period, Boolean, to convert datetime like
                                                 str to period objects
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
        
        
        self.columns_to_correlate = list(sdf.columns[1:])
        self.columns_to_correlate.extend(['retention_index',
                                          'engagement_rate'])
        
        (udf, sdf, null_last_seen_df, 
          trial_df, after_last_seen_df 
         ) = initialize.initialize(udf, sdf, validate_dfs = validate_dfs, 
                                   date_str_to_period = date_str_to_period,
                                   fraction_of_population = 
                                   fraction_of_population,
                                   trial = trial)      
        

        
        #use a datetime column so we get the correct datatype
        #settingwitha copy warning
        udf.loc[:,'cohort'] = udf.loc[:,'joined'].copy()
        #create cohort column in users df
        
        udf.loc[:,'cohort'] = udf.loc[:,'cohort'
                                     ].apply( set_to_start_of_the_month)

        #add two more feature columns 
        most_recent_last_seen_date = udf.last_seen.max()
        
        #define age so we can slice on age
        udf['age'] = (most_recent_last_seen_date - 
                      udf.joined)
 
        #candidate for churn #convert to day float
        udf['dust'] = (most_recent_last_seen_date - 
                          udf.last_seen)
        #create cohort dataframe

        self.cohort_df = pd.DataFrame( index = set(udf['cohort']), 
                                       columns = self.columns_to_correlate)
        
        udf.loc[:,'retention_index'] = retention_index(udf)
        
        #May NOT be necessary
        #add retention_index column to the sessions dataframe
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
           Input: df, a copy of the user dataframe that is sliced for a specific
                      range of cohorts
                  time_span, str, in ('D', 'W', 'M')
           Output: df, user df with additional attributes
        
        '''
        grouped = self.grouped 
        #scale the time by dividing by scale
        scale = scale_for_time_units(units)
        #use df in case it has been sliced for a range of
        #cohorts that grouped does not know about.
        
        pieces = {}
        for name in df.index: #name is the cohort name         
            
            group = grouped.get_group(name)
            #this intersection may no longer be necessary, now that we 
            #have a validation method in the init.
            #take only the distinct ids that intersect with the sessions data
            cohort_ids = set(group.index).intersection(self.sdf.index)
            
            print 'user ids {0}'.format(len(group.index))
            #print 'sessions user ids {0}'.format(len(self.sdf.index))
            print 'ids in common {0}'.format( len(cohort_ids))
            
            cohort_sdf = self.sdf.ix[cohort_ids]
            #change index to time
             
            pieces[name] = resample(time_span, 
                                    cohort_sdf.reset_index().set_index('time') )
           
            pieces[name]['cohort'] = name    
        df = pd.concat(pieces.values())
        #scale the engagment rate for the units provided
        df.engagement_rate = df.engagement_rate/scale
        #sort the dataframe and convert object dtypes to numeric if possible
        return df.sort().convert_objects( convert_numeric = True )


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
                          horizontal = False, ax = None, picker = None,
                          min_retention_index = 0, max_retention_index = 1 ):
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
                                            units = units, 
                                            min_retention_index = 
                                            min_retention_index,
                                            max_retention_index = 
                                            max_retention_index)
        
        ax = engage_chart( df, horizontal = horizontal, 
                           ax = ax, picker = picker, 
                           units = units, time_span = time_span, 
                           normalized = normalized)
            
        #return the axes for further tweaking
        return ax

    def get_users( self,  cohort_range = 'all', sessions = False):
        '''method to get the retention index for all cohorts for the user ids
           that don't appear in the sessions logs.
           Inputs:  cohort_range, 'all' or pandas date_range
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
        pieces = {} 
        sessions_uids = set(self.sdf.index)
        
        for name in sorted(cohort_range):
            #get the group with cohort name
            group = self.grouped.get_group(name)
            users_uids = set(group.index)
            #take only the distinct ids that are in the sessions df
            
            cohort_ids = users_uids.intersection(sessions_uids)
            cohort_size = len(cohort_ids)
            print 'cohort name {0}'.format(name)
            print 'number of users uids = {0}'.format(len(users_uids))
            print 'number of cohort uids = {0}'.format( cohort_size)
            if sessions:
                pieces[name] = group.ix[cohort_ids]
            else:
                #slice the sessions dataframe for the cohort
                non_sessions_uids = users_uids.difference(cohort_ids)
                
                pieces[name] = group.ix[non_sessions_uids]
                print pieces[name].last_seen.max()
            pieces[name]['cohort'] = name
            
        return pd.concat(pieces.values())


    def get_engagement_rates( self, time_span = 'W', cohort_range = 'all',
                              normalized = False, units = None, how = 'sum',
                              min_retention_index = 0, 
                              max_retention_index = 1):
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
        if max_retention_index <= min_retention_index:
            print 'invalid max retention_index. Setting to 1'
            max_retention_index = 1
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
        sessions_uids = set(self.sdf.index)
        print 'number of sessions uids = {0}'.format(len(sessions_uids))
        for name in sorted(cohort_range):
            #get the group with cohort name
            group = self.grouped.get_group(name)
            retention_mask = ((group.retention_index >= min_retention_index) &
                              (group.retention_index <= max_retention_index))
            users_uids = set(group.index)
            print 'original number of user uids {0}'.format(len(users_uids))
            group = group.ix[retention_mask]
            users_uids = set(group.index)
            #take only the distinct ids that are in the sessions df
            
            cohort_ids = users_uids.intersection(sessions_uids)
            cohort_size = len(cohort_ids)
            print 'cohort name {0}'.format(name)
            print 'number of users uids = {0}'.format(len(users_uids))
            print 'number of cohort uids = {0}'.format( cohort_size)
            #slice the sessions dataframe for the cohort
            cohort_sdf = self.sdf.ix[cohort_ids]
            
            #change index to time
            cohort_sdf = cohort_sdf.reset_index().set_index('time')
            
            #seems to work but is telling us about copy vs view
            #how to use loc when you want the entire index
            group.loc[:,'joined'] = group.loc[:,'joined'].apply(lambda x: x.day)
            jcount = group.groupby('joined').joined.count()
            #calendar.monthrange(year,month) returns a tuple. Last day of month
            #is element 1
            last_day_of_month = calendar.monthrange(name.year, name.month)[1]
            

            missing_idx = set(range(1,last_day_of_month+1)
                             ).difference(jcount.index)
            print 'There were no sign-ups on the days {0}'.format(missing_idx)
            for idx in missing_idx:
                #no sign on days during the month
                jcount[idx] = 0

            cum_sum = jcount.cumsum()
            #fit to a linear model 
            model, resid = np.polyfit(cum_sum.index, cum_sum.values,1, 
                                      full=True)[:2]           

            #resample the time_group based on the input time_span using how 
            #the retention index should be identical for each session of the
            #same day so we could use mean, min, max but not sum.
            #Still need a better implementation for weekly time span because
            #it may not correspond to the start of the month
            span_df  = resample(time_span, cohort_sdf[['engagement_rate', 
                                                       'retention_index']],
                                how = how
                               )
            
            cum_sum.index  = [ datetime.date(year = name.year, 
                                             month = name.month,
                                             day = val )
                               for val in cum_sum.index]
            #not the how parameters.This must always be the mean.
            cum_sum = resample(time_span, cum_sum, how = 'mean')            
            
            if normalized: #scale to cohort size
                
                grouped = span_df.groupby(level=0)
                #gps = grouped.groups
                
                for t, group in grouped:
                    #determine if we are looking at the same month the cohort
                    #was born.
                    if ( (t.year == name.year) and 
                         (t.month == name.month) ):
                        #cohort was born this month. So we can't use the 
                        #entire cohort size.
                        if time_span != 'D':
                            current_size = np.polyval(model, t.day-0.5)
                        else:
                            temp_t = datetime.date(t.year,t.month, t.day)
                            try:
                                if t.day != 1:
                                    temp_tm1 = datetime.date( t.year, t.month, 
                                                              t.day-1)
                                    #take the mean value of day-1 and day
                                    current_size = ( cum_sum.loc[temp_tm1] +  
                                                     cum_sum.loc[temp_t] )/2
                                else:#cannot take the mean on the first day
                                    current_size = cum_sum.loc[temp_t]
                            except KeyError as details:
                                print details
                                current_size = np.polyval(model, t.day-0.5)
                        #there can be cases where the fit will return
                        #a slightly negative or 0 intercept. Disregard the
                        #data point until we can determine a better method
                        #for dealing with it.
                        if current_size <= 0:
                            span_df.loc[t] = 0
                        else:
                            span_df.loc[t] = span_df.loc[t]/current_size
                    else:
                        span_df.loc[t] = span_df.loc[t]/cohort_size
            
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





