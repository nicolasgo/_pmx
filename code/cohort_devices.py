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
import time

from .retention_index import retention_index
from . import validate
from .dates import set_to_start_of_the_month

from . import clean
from .plot import  radviz_plot
from .plot import engagement_chart as engage_chart
from .plot import devices_chart as d_chart
from .dates import date_from_time

from pandas.tools.plotting import scatter_matrix
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
        udf,sdf = validate.validate(udf, sdf)
        #create cohort column in users df
        #%m is zero-padded month so we can sort the index
        #cohort is a datetime object with the 'day' always equal 1.
        udf['cohort'] = udf.joined.apply( set_to_start_of_the_month)

        #A slightly better age that is normalized so we can do calculations. 
        #to get user engagement rate weight with activity level
        udf['retention_index'] = retention_index(udf)
        #This is the age independent of activity
        udf['age'] = (udf.last_seen.max() - udf.joined).astype('timedelta64[D]')
        #we may need to define an active age as last_seen - joined

        #fill nan values with 0
        cols_to_fill_na = ['friends', 'invites', 'rcvdInv'] 
        udf[cols_to_fill_na] = udf[cols_to_fill_na].fillna(0)

        #add cohort and retention_index column to the sessions dataframe
        sdf = sdf.join(udf[['retention_index','friends', 
                            'rcvdInv', 'age']], how = 'left' )  
        
        #define the engagement_rate column
        sdf['engagement_rate'] = sdf['duration']*sdf['retention_index']
        
        #make instance variables so all the methods have access
        self.udf = udf
        #take only the first three characters of the model to see if we 
        #can group by manufacturer
        sdf['dmake'] = ''
        sdf['dmake'] = sdf['dmodel'].apply(shorten) 
        self.sdf = sdf

        #group by cohorts in init so we only need to do it once
        self.grouped = self.udf.groupby('cohort') 
        
        #list of all cohorts from the grouped users table
        self.all_cohorts = self.grouped.groups.keys()
        print ('Cohorts represented in the '
               'intersection of the data sets:\n'
               '{0}').format(sorted(self.all_cohorts))

        self.all_makes = self.sdf.dmake.reset_index(drop=True
                                                   ).drop_duplicates()
        self.all_makes.sort()

        self.all_makes_models = self.sdf[['dmake','dmodel']
                                        ].set_index('dmake').drop_duplicates()
        self.all_makes_models.sort()

    def get_top_makes(self, top):
        '''get the top makes
        '''
        return    self.sdf.groupby('dmake'
                                  ).duration.sum().sort(ascending=False, 
                                                        inplace = False
                                                       ).head(top).index

    def get_dmodels(self, cohort_range = DEFAULT_COHORT_RANGE, short = False):
        '''method to create a dataframe with cohort as the index and 
           devices as columns.
           Useful for creating a bar chart
           Output: DataFrame
        '''
        if short:
            return self.get_device_attribute( name = 'make', 
                                              cohort_range = cohort_range)
        else:
            return self.get_device_attribute( name = 'model', 
                                              cohort_range = cohort_range)

    def get_dversions(self, cohort_range = DEFAULT_COHORT_RANGE):
        '''method to create a dataframe with cohort as the index and 
           devices as columns.
           Useful for creating a bar chart
           Output: DataFrame
        '''
        return self.get_device_attribute( name = 'version', 
                                          cohort_range = cohort_range)

    def get_dfamilies(self, cohort_range = DEFAULT_COHORT_RANGE):
        '''method to create a dataframe with cohort as the index and 
           devices as columns.
           Useful for creating a bar chart
           Output: DataFrame
        '''
        return self.get_device_attribute( name = 'family', 
                                          cohort_range = cohort_range)

    def get_device_attribute(self, name = 'model', 
                             cohort_range = DEFAULT_COHORT_RANGE):
        '''method to get the attribute in the input parameter 'name'
           Inputs: name, str, name of the attribute of interest
                   cohort_range, list of datetime objects
        '''
        name = 'd'+name #prepend d to indicate device

        if cohort_range == DEFAULT_COHORT_RANGE:
            #use the entire cohort_range from the grouped users table
            cohort_range = self.all_cohorts
        else:
            #validate and use the input cohort_range
            cohort_range = validated_cohort_range( self.all_cohorts, 
                                                   cohort_range)
        
        #create the device dataframe
        df = pd.DataFrame( index = cohort_range, 
                           columns = set(self.sdf[name]))

        for c_name in cohort_range:
            group = self.grouped.get_group(c_name)
            #take only the distinct ids
            cohort_ids = set(group.index)
            cohort_sdf = self.sdf.ix[cohort_ids]

            dmodels = cohort_sdf.groupby(name).duration.count()
            sessions = cohort_sdf.duration.count()
            #make it a percentage
            df.loc[c_name, dmodels.index] = 100 * dmodels/ sessions 

        #drop devices that were never used
        df= df.dropna(axis=1, how='all')

        #fill dfamily that were not used with 0
        return df.fillna(0)
    
    def dversions_chart( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                         top = 5, horizontal = False):
        '''method to create a stacked bar chart for the devices_df.
           Inputs: df, DataFrame or None with device information
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   top, int, top N devices to consider for the chart
        '''   
        axes_labels = ('cohort', ' sessions % ' )
        if df is None: #get models dataframe
            df = self.get_dversions(cohort_range = cohort_range)
        #find the most used dmodels
        top_models = df.sum().sort( ascending = False, 
                                    inplace = False).head(top).index
        #keep only the top models
        df = df[top_models].sort(inplace = False)
        ax = d_chart(df, top, axes_labels, horizontal, name = 'versions')        
        #return the axes for further tweaking
        return ax

    def dmodels_chart( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                       top = 5, horizontal = False):
        '''method to create a stacked bar chart for the devices_df.
           Inputs: df, DataFrame or None with device information
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   top, int, top N devices to consider for the chart
        '''   
        axes_labels = ('cohort', ' sessions % ' )
        if df is None: #get models dataframe
            df = self.get_dmodels(cohort_range = cohort_range)
        #find the most used dmodels
        top_models = df.sum().sort( ascending = False, 
                                    inplace = False ).head(top).index
        #keep only the top models
        df = df[top_models].sort(inplace = False)
        ax = d_chart(df, top, axes_labels, horizontal, name = 'models')        
        #return the axes for further tweaking
        return ax

    def dmakes_chart( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                      top = 5, horizontal = False):
        '''method to create a stacked bar chart for the devices_df.
           Inputs: df, DataFrame or None with device information
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   top, int, top N devices to consider for the chart
        '''   
        axes_labels = ('cohort', ' sessions % ' )
        if df is None: #get models dataframe
            df = self.get_dmodels(cohort_range = cohort_range, short = True)
        #find the most used dmodels
        top_models = df.sum().sort( ascending = False, 
                                    inplace = False).head(top).index
        #keep only the top models
        df = df[top_models].sort(inplace = False)
        ax = d_chart(df, top, axes_labels, horizontal, name = 'makes')        
        #return the axes for further tweaking
        return ax

    def dfamily_chart( self, df = None, cohort_range = DEFAULT_COHORT_RANGE,
                       top = 5, horizontal = False):
        '''method to create a stacked bar chart for the devices_df.
           Inputs: df, DataFrame or None with device information
                   cohort_range, list of datetime.date objects identifying
                                 the cohorts to analyse 
                   top, int, top N devices to consider for the chart
        '''   
        axes_labels = ('cohort', ' sessions % ' )
        if df is None: #get devices dataframe
            df = self.get_dfamilies(cohort_range = cohort_range)
        #find the most used devices
        top_devices = df.sum().sort( ascending = False, 
                                     inplace = False).head(top).index
        #keep only the top devices
        df = df[top_devices].sort(inplace = False)
        ax = d_chart(df, top, axes_labels, horizontal, name = 'families')        
        #return the axes for further tweaking
        return ax

    def report(self, name, cohorts, make, model, family = None, version = None,
               attributes = ['count', 'duration'], min_age = 60, min_size = 1):
        '''generate and report statistics
           Input: cohorts, list of cohort datetime objects for the report
                  name, str, name of the report
                  make, str,  make of the device
                  model, str,  model of the device
                  family, str,  family of the device 
                  version, str, version of the device 
          Output: dataframe and or plot 
        '''
        report_method = {'device_make_model': self.device_make_model_report,
                         'device': self.device_report 
                        }.get(name, self.device_report)

        
        return report_method(cohorts, make, model, family = family, 
                             version = version, attributes = attributes,
                             min_age = min_age, min_size = min_size)

    def device_make_model_report(self, cohorts, make, model, **kwargs):
        '''report on the device make and model'''
        attributes = kwargs.get('attributes', {'count':0.5, 
                                               'duration': 0.5, 
                                               'friends': 0.1 } )
        min_age = kwargs.get('min_age', 60)

        grouped  = self.sdf.groupby(['dmake', 'dmodel'])
        df = None# dataframe for the report
        group  = grouped.get_group((make, model))
        target_users = []
        for cohort in sorted(cohorts):
            my_cohort_df = self.grouped.get_group(cohort)
            #make sure the users are at least a couple cohorts old. 
            cohort_ids = my_cohort_df.ix[my_cohort_df.age > min_age].index

            group_ids = set(group.index).intersection(cohort_ids)
            num_group_ids = len(group_ids)
           
            if num_group_ids > 3:
                cohort_df = group.ix[group_ids]
                my_mask = None
                percentiles = list(set(attributes.values()).union([0.25,0.75]))
                
                describe_df = cohort_df.describe(percentiles = 
                                                 percentiles)
                #print describe_df
                for attribute, percentile in attributes.items():
                    
                    if attribute != 'count':
                        percent = str(int(percentile*100))+'%'
                        if my_mask is None:
                            my_mask = (cohort_df[attribute] > 
                                       describe_df[attribute][percent] ) 
                        else:
                            my_mask = my_mask & ( cohort_df[attribute] > 
                                                  describe_df[attribute
                                                             ][percent])
                #print describe_df
                #print cohort_df.corr(method = 'spearman')
                
                #scatter_matrix(cohort_df, alpha=0.2, figsize=(6, 6), diagonal='kde')
                age = cohort_df.loc[group_ids,'age']
              
                max_ri = (age - 15)/age
                min_ri = (age - 25)/age

                mask = ( my_mask &
                         (cohort_df.retention_index <= max_ri) & 
                         (cohort_df.retention_index >= min_ri)
                       )
                target_cohort = cohort_df.ix[mask]
                
                count = target_cohort.groupby(level=0).duration.count()

                percentile_sessions = count.quantile(attributes['count'])

                if count.any():
                    if 'count' in attributes:
                        mask2 =  count > percentile_sessions 
                        uids = set(target_cohort.ix[mask2].index)
                    else:
                        uids = set(target_cohort.index)
                    if uids:
                        df = self.update_report_df(df, uids, attributes, 
                                                   describe_df, 
                                                   percentile_sessions)
                        #Now we can fill the dataframe
                        df = self.user_fill_report_df( df, 
                                                       target_cohort.ix[uids],
                                                       attributes
                                                     )
                        print 'Target users {0}'.format(uids)
                        target_users.extend(uids)

            else: #too small
                pass
                #print 'Not enough users in cohort for analysis'
        if df is not None:
            df.loc[:,'dmake'] = make
            df.loc[:, 'dmodel'] = model

        return df

    def device_report(self, cohorts,  make, model, version = None, 
                      family = None, **kwargs):
        '''report on the device make
           Note: model is not used currently'''
        min_size = kwargs.get('min_size', 1)

        grouped  = self.sdf.groupby(['dmake', 'dmodel'])

        #dataframe for the group of make, model
        group  = grouped.get_group((make, model))

        df = None# dataframe for the report
        
        for cohort in sorted(cohorts):
            my_cohort_df = self.grouped.get_group(cohort)
            #make sure the users are at least a couple cohorts old. 
            cohort_ids = my_cohort_df.index
            
            group_ids = set(group.index).intersection(cohort_ids)
            #cohort_size
            num_group_ids = len(group_ids)
           
            if num_group_ids > min_size:
                cohort_df = group.ix[group_ids]
                my_mask = None
                percentiles = [] #[0.25, 0.75] # list(set(attributes.values()).union([0.25,0.75]))
                
                describe_df = cohort_df.describe(percentiles = 
                                                 percentiles)
                describe_df.index.name = 'stats'
                describe_df.loc[:,'cohort'] = cohort
                describe_df.loc[:,'dmake'] = make
                describe_df.loc[:,'dmodel'] = model
                describe_df.loc[:,'size'] = num_group_ids
                describe_df.loc[:,'sessions'] = describe_df.at['count','duration']
                describe_df = describe_df.drop(['count', 'std'], 0)
                describe_df = describe_df.set_index(['cohort', 'size', 'dmake',
                                                     'dmodel'], append= True)

                describe_df = describe_df.reorder_levels(['cohort','size',
                                                          'dmake', 'dmodel',
                                                          'stats'])
                if df is None:
                    df = describe_df.copy()
                else:
                    df.append(describe_df)
        return df            

                
    def update_report_df(self, df, target_uids, attributes,
                         describe_df, sessions):
        '''Method to update the dataframe used for the report
           Inputs: df, dataframe or None, user_ids as index
                   target_uids, user_ids of the users targeted for direct action
                   attributes, dict, of { key: val} -> {attribute: percentile}
                   describe_df, statistics df of the cohort sessions
                   sessions, int, number of sessions at the percentile used for
                                  the count attribute if it exists. 
        '''
        
        if df is None:
            #create dataframe
            df = create_report_df(target_uids, attributes)
         
        else:
            df = df.append(create_report_df(target_uids, attributes))
        df = group_fill_report_df(df, target_uids, attributes, describe_df, 
                                  sessions)
        return df

    def user_fill_report_df(self, df, target_cohort_df, attributes):
        '''Method to fill in the user attributes.'''
        uids = set(target_cohort_df.index)
        target_cohort_grouped = target_cohort_df.groupby(level = 0)

        for attribute in attributes:
            if attribute == 'duration':        

                df.loc[uids, 
                       'duration'] = target_cohort_grouped['duration'].max()
            elif attribute == 'count':
                df.loc[uids, 
                       'sessions'] = target_cohort_grouped.duration.count()
            else:
                df.loc[uids, attribute] = self.udf.loc[uids, attribute]  
        always_cols = ['cohort', 'retention_index']
        df.loc[uids, always_cols] = self.udf.loc[uids, always_cols]
                        
        return df

def group_fill_report_df(df, uids, attributes, describe_df, 
                         sessions):
    '''fill the input df with the group values for the given attributes'''
    for attribute, percentile in attributes.items():
        percentile_str = '{0}%'.format(int(100*percentile))
        if attribute != 'count':
            att_percentile = '{0} {1}'.format(percentile_str, attribute)
            df.loc[uids, att_percentile] = describe_df.loc[percentile_str,
                                                           attribute]
        else:
            sessions_percentile = '{0} {1}'.format(percentile_str, 'sessions')
            df.loc[uids, sessions_percentile] = sessions 
        
    return df


def create_report_df(target_users, attributes):
    '''method to create the dataframe for the report'''
    columns = ['cohort', 'dmake', 'dmodel', 'retention_index']
    attribute_list = [ key.replace('count','sessions') 
                       for key in attributes.keys() ]
    
    columns.extend(attribute_list) 
               
    for attribute, percentile in attributes.items():
        int_percentile = int(100*percentile)
        if attribute != 'count':
            percentile_str = '{0}% {1}'.format(int_percentile, attribute)
        else:
            percentile_str = '{0}% sessions'.format(int_percentile)

        columns.append(percentile_str)
    return pd.DataFrame(index = target_users, columns = columns)

def shorten(name):
    '''function to shorten the name to 2 or three characters'''
    x = name[:3]
    x = x.replace('-', ' '
                 ).replace('GT ', 'Sam'
                 ).replace('ONE', 'ALC'
                 ).upper()
    return x

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

def resample(time_span, time_df):
    '''resample a dataframe based on the time_span of interest.
       Inputs: time_span, str, in  [ 'M', 'W', 'D' ]
               time_df, dataframe with time (datatime.date objects) as the index
    '''
    if time_span == 'M':
        df = time_df.groupby(lambda x :x.strftime('%Y %m')
                                               ).sum()
        df.index = [date_from_time( time.strptime(val, '%Y %m') )
                                 for val in df.index]    
    elif time_span == 'W':
                
        df = time_df.groupby(lambda x :x.strftime('%Y %W')
                                               ).sum()
        #must have a week day for the strptime to work
        df.index = [ date_from_time(time.strptime(val+' 1', 
                                                       '%Y %W %w') )
                          for val in df.index]
                
    else: #assume default 'D' daily
          #we already have the daily sums. 
          #Just need to divide by the count to get the mean
                
        df = time_df#/time_group_df.sessions
    df.index.name = 'time'
    return df

