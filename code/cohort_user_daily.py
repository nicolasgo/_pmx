'''module for user related code.
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import pandas as pd
import numpy as np
import datetime

from .cohort2 import scale_for_time_units, choose_cohorts
from .dates import set_to_start_of_the_month
 
from .retention_index import retention_index
from .resample import resample
from . import regression, categorize
from . import initialize, plot

from .cross_validation import run_cv, accuracy
from .confusion_matrix import confusion_matrices

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.neighbors import KNeighborsClassifier as KNN


class CohortUsers(object):
    '''represents Users behaviour on the social network
    '''
    def __init__(self,  udf, sdf, cohort_range = 'all',
                 validate_dfs = True, 
                 date_str_to_period = False, 
                 fraction_of_population = 0.1,
                 trial = True):
        ''' Initialize the class instance.
            Inputs: udf, dataframe with user data
                    sdf, dataframe with sessions data
                    cohort_range, range of datetime like objects
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

        (udf, sdf, null_last_seen_df, 
          trial_df, after_last_seen_df 
         ) = initialize.initialize(udf, sdf, validate_dfs = validate_dfs, 
                                   date_str_to_period = date_str_to_period,
                                   fraction_of_population = 
                                   fraction_of_population,
                                   trial = trial)      
                                   
        self.sampled_users = udf.shape[0]
        #determine the cohort for each user.
        udf.loc[:,'cohort'] = udf.loc[:,'joined'].copy()
        udf.loc[:,'cohort'] = udf.loc[:,'cohort'
                                     ].apply( set_to_start_of_the_month)

        
        self.udf = udf.copy().reset_index().set_index('cohort')

        #take only user ids in the cohort range
        self.udf = choose_cohorts(cohort_range, self.udf)
        print set(self.udf.index)
        
        #slice the sessions for those users in the validated cohort range
        self.sdf = sdf.ix[self.udf.user_id]

        #now we can add user_id back to the udf index so we have a multiindex df
        self.udf = self.udf.set_index( 'user_id', append= True, inplace = False)
        
        # we currently can't handle the attributes that are categorical strings.
        # Drop for now.
        columns_to_drop = ['dmodel', 'dversion', 'dfamily'] 
        pages_to_drop = ['variety', 'mymed', 'conve', 'media', 
                         'uploa', 'avata', 'publi', 'ip', 'landpage' ]
        columns_to_drop.extend(pages_to_drop)

        self.sdf = self.sdf.drop(columns_to_drop, axis=1)
        print self.sdf.columns

        #for now limit the number of attributes to analyse
        columns_to_keep = [ 'joined','last_seen', 'friends', 'area',
                            'state', 'invites', 'rcvdInv', 'rejectd', 'sim',
                            'twFrs', 'fbFrs', 'yt','pi']

        self.udf = self.udf[columns_to_keep]
        
        #To do: drop columns that have all values the same from columns like
        ucolumns_to_drop = []
        for name in ['state', 'rejectd', 'sim',
                     'twFrs', 'fbFrs', 'yt','pi' ]:
            column = self.udf[name]
            if name == 'state':
                val = 1
            else:
                val = 0
            if self.udf[~(pd.isnull(column)| ( column == val))].empty:
               
                ucolumns_to_drop.append(name)
        if ucolumns_to_drop:
            print ('drop columns {0} because they contain '
                   'no information').format(ucolumns_to_drop)
            self.udf = self.udf.drop(ucolumns_to_drop, axis = 1)

        self.udf = self.udf.fillna(0,inplace=False)
        
        
        #attributes to add. They will be populated either from the sessions 
        #data or combination of sessions and users data
        #we use activity_level in place of duration because we also use the 
        #duration column to calculate the total number of sessions
        #max_inactive will be the maximum number of days that the user 
        #has been inactive max_inactive will be the number of times that 
        #the user has been on max_inactive 
        features = ['retention_index', 'engagement_rate', 'duration', 
                    'sessions', 'pv', 'max_inactive', 'max_inactive_counts',
                    'mean_ri']

        pages = ['activ','frien', 'help', 'home', 'inbox', 'info']

        features.extend(pages)


        features_df = pd.DataFrame(columns = features, 
                                   index = udf.index).fillna(0)

        #merge the users df with the features_df
        self.udf[features] = features_df

        #can't handle resampling the strings at the moment. 
        #To Do: improve the resample method so we can handle 'dmodel', etc
        
        #A slightly better age that is normalized so we can do calculations. 
        #to get user engagement rate weight with activity level
        self.udf['retention_index'] = retention_index(self.udf)

        #add two more feature columns #convert to day float
        most_recent_last_seen_date = udf.last_seen.max()

        #define age so we can slice on age
        self.udf['age'] = (most_recent_last_seen_date - 
                           self.udf.joined)
 
        #candidate for churn 
        self.udf['dust'] = (most_recent_last_seen_date - 
                            self.udf.last_seen) 

        #May need to change this to groupby by cohort
        #for now group by user_id (ie the index)
        self.grouped = self.sdf.groupby( level = 0) 

        #list of all cohorts from the grouped users table
        self.all_cohorts = set(self.udf.index.get_level_values('cohort'))
        

    def get_active_users(self, cohort_range = 'all',
                         time_span = 'D', percentage = False):
        '''method to get the active users in the given time_span (period)
           Inputs: cohort_range, list or index of period object (freq = 'M')
                   time_span, str in ('D', 'W', 'M')
                   percentage, Boolean, flag to represent as a percentage or
                                        not
        '''
        if cohort_range != 'all':
            #This needs work.
            user_ids = self.udf.ix[cohort_range].index
            
        #for now let's get it working
        pieces = {}
        cohort_users = {}
        for cohort in cohort_range:
            #this is a multiindex dataframe with cohort (level 0) 
            #and user_id (level 1)
            #when we slice on cohort we lose the level 0 index
            user_ids = self.udf.ix[cohort].index
            
            sdf_time = self.sdf.ix[user_ids].reset_index().set_index('time')
            
            df = sdf_time.groupby([sdf_time.index.asfreq(time_span)]
                                 ).user_id.nunique()
            if not df.empty:
                
                total_users = len(user_ids)
                cohort_users[cohort] = total_users
                print '{0} users in cohort {1}'.format(total_users,
                                                       cohort )
                
                if percentage:
                    
                    pieces[cohort] = 100*(df.div(total_users))

                else: #return absolute number of users 
                    pieces[cohort] = df
        #this should give us cohort as the level = 0 index    
        pieces_df = pd.concat(pieces)    
        
        return pieces_df, cohort_users
        
    def get_df(self, cohort, day, user_type = 'not_started'):
        '''function to get the user data table for users that have
           not started before a specified day.
           Inputs: cohort, period object 
                   day, int, since joining.
           Output: df, slice of the user dataframe.         
        '''
        #slice of the users dataframe for the specified cohort
        udf = self.udf.ix[cohort]
        #get relevant user_ids to slice the sessions dataframe
        user_ids = udf.index
        #get the relevant sessions
        sdf = self.sdf.ix[user_ids]  
        #add the joined date to the session data so we can
        #quickly extract users that have not been active/have not been active
        sdf = sdf.join(udf['joined'], 
                           how = 'left')  
                           
        true_users, false_users = categorize.user_day_since_joining(udf, sdf, 
                                                                    day = day)
                                                              
        if user_type == 'not_started':
            users = false_users
        else: #users that have started using the service
            users = true_users
            
        return udf.ix[users]          
             
    def get_active_summary(self, cohort_range, day_range, started_day = 28,
                           inactive_days = 30 ):
        '''Method to generate a summary dataframe of active/not active users 
           who have started using the service before the started_day after 
           joining.
           Input: cohort, period object for the cohort of interest
                  started_day, int, day since joining where the user
                                    must have a session to be considered 
                                    as started.
                  day_range, list of int representing days after join+day
                              to be considered active/not active
                  inactive_days, number of days without a session
           Output: df with the number of active and not active users                    
                              
        '''                      
        if cohort_range != 'all':
            #This needs work because we should validate the cohort_range
            user_ids = self.udf.ix[cohort_range].index
            
        #for now let's get it working
        pieces = {}
        for cohort in cohort_range:
            pieces[cohort
                  ] = self.get_active_started_users(cohort, day_range,
                                                    started_day = started_day,
                                                    inactive_days = 
                                                    inactive_days )    
                                                    
        if pieces:
            return pd.concat(pieces)
                                                                                              
    def get_active_started_users(self, cohort,  day_range, started_day = 28,
                                 inactive_days = 30):
        '''Method to get the active/not active users who have started using the
           service.
           Input: cohort, period object for the cohort of interest
                  day, int, day since joining where the user must have a session
                            to be considered as started.
                  day_range, list of int representing days after join+day
                              to be considered active/not active
                              
           Output: df with the number of active and not active users                    
                              
        '''                      
        #need a function to validate the day_range because
        #day_range.min() > inactive_days - started_day
        day_range = [ day for day in day_range if day > 
                      (inactive_days - started_day)]
        
        #slice of the users dataframe for the specified cohort
        udf = self.udf.ix[cohort]
        #get relevant user_ids to slice the sessions dataframe
        user_ids = udf.index
        #get the relevant sessions
        sdf = self.sdf.ix[user_ids]  
        #add the joined date to the session data so we can
        #quickly extract users that have not been active/have not been active
        sdf = sdf.join(udf['joined'], 
                           how = 'left')
        #get the user ids for the users that have started before day and
        #the users ids for the users that nave not started before day
        (started_users, 
         not_started_users ) = categorize.user_day_since_joining(udf, sdf, 
                                                                 day = 
                                                                 started_day)                   
                           
        #now we focus on the started users.
        udf = udf.ix[started_users]
        sdf = sdf.ix[started_users]
        #create an empty data frame to store the summary for each 
        #day in day_range.         
        #in the columns below 'a' is short for 'active' and 'i' is
        #short for 'inactive'.          
        df = pd.DataFrame(index = np.asarray(day_range)+started_day, 
                          columns = ['active', 'inactive', 'all', 
                                     'a_with_friends', 'a_without_friends',
                                     'i_with_friends', 'i_without_friends',
                                    ]
                         ).fillna(0)  
        
        #fill the all_users column                            
        df['all'] = len(udf.index)     
                        
        for day in day_range:
            #cycle through the days. Would be better to do this as a vector
            #operation but it does not seem simple at this time.
            end_date = sdf.joined + started_day + day
            start_date = end_date - inactive_days
            #user ids for active and inactive categories                                           
            (active_users, 
             inactive_users) = categorize.user_day_range(udf, sdf, start_date =
                                                         start_date, end_date = 
                                                         end_date)
            #count the number of users who are active and inactive in the last
            #inactive days.
            
            df.loc[day+started_day, 'active'] = len(active_users)
                   
            df.loc[day+started_day, 'inactive'] = len(inactive_users)
                      
        return df  
                            
    def get_started_summary(self, cohort_range = 'all', day_range = None, 
                            failed_day = None):
        '''Method to get a summary dataframes for when users are starting
           to use the system (ie how many days after joining is there first
                                 session ).
           Inputs: cohort_range, list of period objects or 'all' 
                                 ( all currently not working )
                   day_range, list of ints representing the days since
                              joining
                   failed_day, int (or None) day that represents when we 
                               should categorize the user as having failed
                               to start using the service                         
             
        '''
        
        if cohort_range != 'all':
            #This needs work because we should validate the cohort_range
            user_ids = self.udf.ix[cohort_range].index
            
        #for now let's get it working
        pieces = {}
        pieces2 = {}
        failed_totals = {}
        not_started = {}
        for cohort in cohort_range:
            #this is a multiindex dataframe with cohort (level 0) 
            #and user_id (level 1)
            #when we slice on cohort we lose the level 0 index
            cohort_df = self.udf.ix[cohort]
            
            #get user_ids in the cohort
            user_ids = cohort_df.index
            
            if day_range is not None:
                #We are interested in the users that have not started using
                #the service since joining. 
                not_started[cohort] = self.get_category_summary(cohort_df, 
                                                                day_range,
                                                                failed_day = 
                                                                failed_day,
                                                                verbose = False)
                                
            #use user_ids to get the most_recent_session date for each
            #user in the cohort. Add to cohort_df
            cohort_df['most_recent_session'] = self.sdf.ix[user_ids
                                                          ].groupby(level = 0
                                                                   ).time.max()
                                                                   
            failed_df  = cohort_df[cohort_df.joined >= 
                                   cohort_df.last_seen]
            failed_df2 = cohort_df[cohort_df.joined >= 
                                   cohort_df.most_recent_session]
                                   
            if not failed_df.empty:   
                pieces[cohort] = failed_df
                pieces2[cohort] = failed_df2
                
            num_failed_users = failed_df.shape[0]
            num_failed2_users = failed_df2.shape[0]    
            if not not_started[cohort].empty and (failed_day is None):
                not_started[cohort]['failed'] = num_failed_users
                
            failed_totals[cohort] = (num_failed_users, num_failed2_users)
               
                
        #this should give us cohort as the level = 0 index 
        if pieces:   
            return  (pd.concat(pieces), failed_totals, pd.concat(pieces2),
                     pd.concat(not_started) )
        else:
            return None, failed_totals, None, None      
             
    def get_category_summary(self, udf, day_range, failed_day = None,
                             verbose = False):
        '''method to get the number of users that have not started
           the service X days after joining.
           This method needs to be renamed to better describe what it is doing
           
           Inputs: udf, user dataframe or slice thereof
                   day_range, list of ints representing the days since joining
                   failed_day, int day after which users should be categorized
                               as failed to start the service.
                   verbose, Boolean, to print to screen or not   
                            
           Output: df, dataframe with day as the index and number of users
                       that have not started the service as the column 
        '''               
        user_ids = udf.index
        all_users = udf.shape[0]
        
        #get the relevant sessions
        sdf = self.sdf.ix[user_ids]  
        sdf = sdf.join(udf['joined'], 
                           how = 'left') 
        #create an empty data frame to store the summary for each 
        #day in day_range.         
        #in the columns below 's' is short for 'started' and 'ns' is
        #short for 'not_started'.          
        df = pd.DataFrame(index = day_range, 
                          columns = ['started', 'not_started', 'all', 
                                     's_with_friends', 's_without_friends',
                                     'ns_with_friends', 'ns_without_friends',
                                     'failed']
                         ).fillna(0)  
                              
        #fill the all_users column                            
        df['all'] = all_users     
                        
        for day in day_range:
            #cycle through the days. Would be better to do this as a vector
            #operation but it does not seem simple at this time.
            
            #user ids for started and not_started categories                                           
            (started_users, 
             not_started_users) = categorize.user_day_since_joining(udf, sdf, 
                                                                    day = day)
            #count the number of users who have started and not_started using
            #the service and add to dataframe.
            num_started_users = len(started_users)
            df.loc[day, 'started'] = num_started_users
                   
            num_users_not_started = len(not_started_users)
            df.loc[day, 'not_started'] = num_users_not_started
            
            if verbose: #print some stats if debugging or interested
                print ('{0} users out of {2} users  ( {1:.2f} % )  have '
                       'not started using the service  '
                       '{3} days after joining.' 
                      ).format( num_users_not_started, 
                                100*(num_users_not_started/all_users), 
                                all_users, day  )  
                                
            #this section counts the users with friends and no_friends
            #first for users that have started using the service
            attribute = 'friends'
            split_val = 0
            columns = ['s_with_friends', 's_without_friends']
            df.loc[day, 
                   columns] = get_attribute_summary(udf.ix[started_users],
                                                    attribute = attribute,
                                                    split_val = split_val) 
                                                    
            #then for those users that have not started using the service
            columns = ['ns_with_friends', 'ns_without_friends']
            df.loc[day, 
                   columns] = get_attribute_summary(udf.ix[not_started_users],
                                                    attribute = attribute,
                                                    split_val = split_val)               
                           
        if failed_day is not None:
            #we want to use a fixed fail day so all cohorts will be on
            #the same basis for reporting purposes.   
            (not_failed_users, 
             failed_users) = categorize.user_day_since_joining(udf, sdf, 
                                                               day = failed_day)
             
            num_failed_users = len(failed_users)              
            #failed users are independent of the day range. They only depend
            #on the failed_day value.                
            df.loc[:, 'failed'] = num_failed_users
            
        return df    
                       
    def plot_not_started_users(self, df, percent = True):
        '''function to plot the users who have not started using 
           the service since joining.
           Inputs:  df, multiindex dataframe (level 0 = cohort,
                                              level 1 = day since joining
                                             )
                    percent, Boolean, plot as a percent or absolute number
        '''
        sampling_err = 1/np.sqrt(self.sampled_users)
        print 'Sampling error +/-{0:.1}%'.format(100*sampling_err)
        if percent:
            df['not_started_per_all'] = df['not_started']/df['all']*100
            df['failed_per_not_started'] = df['failed']/df['not_started']*100
            
            columns_to_plot = [ 'not_started_per_all',
                                'fit' ]
                              
            df['yerr'] = 100*sampling_err
                                     
            col_to_fit = 'not_started_per_all'                    
            ylabel = '% of users'           
            title = ( 'Number of users that are not using '
                      'the service as a function of days since joining  ' )      
        else:
            columns_to_plot = [ 'not_started', 'fit' ] 
            df['yerr'] = df[columns_to_plot[0]]*sampling_err
            
            col_to_fit = 'not_started'
            ylabel = 'Number of users'
            
        title = ( '{0} that are not using '
                  'the service '.format(ylabel) )
            
        xlabel = 'days since joining' 
        
        df = self.fit_column(df, col_to_fit, ratio = 0.75, 
                             fit_function = 'pareto', guess = [.1, .2])    
                                                            
        ax = plot.not_started_users(df, columns_to_plot, ylabel = ylabel,
                                    xlabel = xlabel, yerr = df['yerr'])  
                                   
        ax.figure.suptitle(title, fontsize = 16)
                                                    
    def fit_column(self, df, col_to_fit, ratio = .75, started = False,
                   fit_function = None, guess = [1, 0.2]):
        '''Method to fit a single column of a dataframe and add the
           fit to the dataframe in the column named 'fit'
           Input: df, multiindex dataframe with cohort as level 0
                      and day on level 1
                  col_to_fit, column name str  
                  ratio, ratio of y2/y1 to gauge the fit coefficients
                         on something real world.
        '''
        df['fit'] = 0*df.copy()[col_to_fit] 
        residuals_func = regression.residuals
        
        fit = { 'lomax' : regression.lomax, 
                'pareto_cdf' : regression.pareto_cdf,
                'exponential': regression.exponential
               }.get(fit_function, regression.pareto)
            
            
        for cohort in df.index.levels[0]:
            
            x0 = df.loc[cohort, col_to_fit].index
            y = df.loc[cohort, col_to_fit].values
            
            
            (kd, cov,infodict,
             mesg, ier ) = regression.leastsq( residuals_func,
                                               guess, args=(x0,y,fit),
                                               full_output = True )
            print '{0} tail parameter is {1:.2f}'.format(cohort, kd[1]) 
                                             
            df.loc[cohort, 'fit'] =  fit(kd, x0)                    
            
            # y2 = 0.75*y1 => (xm/x2)**alpha = ratio(xm/ x1)**alpha       
            starting_rate = (1/ratio)**(1/kd[1])    
            if fit_function == 'pareto':
                print ('Median number of days since '
                      'joining, {0:.0f}').format(kd[0]*2**(1/kd[1])  ) 
                if kd[1] < 1:
                    print 'Infinite mean value for this distribution'
                                   
        return df       
                            
    def plot_started_users(self, df, percent = True):
        '''function to plot the users who have not started using 
           the service since joining.
           Inputs:  df, multiindex dataframe (level 0 = cohort,
                                              level 1 = day since joining
                                             )
                    percent, Boolean
        '''
        sampling_err = 1/np.sqrt(self.sampled_users)
        print  'Sampling error +/-{0:.1}%'.format(100*sampling_err)
        
        if percent:
            df['started_per_all'] = (1 - df['not_started']/df['all'])*100
            df['started_per_not_started'] = (df['all'] - 
                                             df['not_started']
                                            )/df['not_started']*100
                                            
            columns_to_plot = [ 'started_per_all',
                                'fit' ]
                              
            df['yerr'] = 100*sampling_err
                                     
            col_to_fit = 'started_per_all'
            ylabel = '% of users'                   
        else:
            df['started'] = df['all'] - df['not_started']
            
            columns_to_plot = [ 'started', 'fit' ] 
           
            df['yerr'] = df[columns_to_plot[0]]*sampling_err
            
            col_to_fit = 'started'
            ylabel = 'Number of users'
            
        xlabel = 'days since joining'                      
        df = self.fit_column(df, col_to_fit, ratio = 0.75, 
                             fit_function = 'pareto_cdf' )
                              
        ax = plot.not_started_users(df, columns_to_plot, ylabel = ylabel,
                                   xlabel = xlabel, yerr = df['yerr'] )           
        title = ('Users using the service '
                 'as a function of day since joining')
                 
        ax.figure.suptitle(title, fontsize = 16) 
                
        return ax                   
                    
    def plot_active_summary(self, df, columns_to_plot, percent = True ):
        '''Method to plot the active summary for all cohorts in df
           Inputs: df, multiindex dataframe with cohort level = 0 
                       day since joining level = 1
                   columns_to_plot, list of str
                   xlabel, x-axis label for plot
                   ylabel, y-axis lable for plot
                   yerr, Series to match column in df with the y-axis 
                         error
        '''
        sampling_err = 1/np.sqrt(self.sampled_users)
        print  'Sampling error +/-{0:.1}%'.format(100*sampling_err)
        xlabel = 'days since joining'
        
        if percent:
            
            df['active_per_all'] = (df['active']/df['all'])*100
            df['inactive_per_all'] = df['inactive']/df['all']*100
                                            
            columns_to_plot = [ 'active_per_all',
                                'fit' ]
            col_to_fit = 'active_per_all'
            df = self.fit_column(df, col_to_fit, ratio = 0.75, 
                                 started = False,
                                 fit_function = 'lomax', 
                                 guess = [1, 0.2, 30] )                 
            df['yerr'] = 100*sampling_err
                                     
            #col_to_fit = 'active_per_all'
            ylabel = '% of users'                 
              
        else:
             
           
            #df['yerr'] = df[columns_to_plot[0]]*sampling_err
            
            #col_to_fit = 'started'
            ylabel = 'Number of users'
            
        
        ax = plot.not_started_users(df, columns_to_plot, ylabel = ylabel,
                                    xlabel = xlabel, yerr = df['yerr']
                                    ) 
        return ax                            
        
    def plot_friends_summary(self, df, columns_to_plot):
        ''' function to plot the friends summary'''
        ylabel = 'number of users'
        xlabel = 'day since joining'
        ax = plot.not_started_users(df, columns_to_plot, ylabel = ylabel,
                                    xlabel = xlabel
                                    )           
        return ax
                                                       
    def plot_active_users(self,df, time_span = 'W', user_totals = None):
        '''function to plot the active users for each cohort in 
           the input dataframe. Note the dataframe must have 
           cohort as it's level 0 index in a multiindex dataframe.
           Date must be the level 1 index
           Inputs: df, multiindex dataframe with a daily frequency 
                       for the periodIndex
                   time_span, str in ('D', 'W', 'M')       
        '''
        
        grouped = df.groupby(level=0)
        
        cohorts = sorted(df.index.levels[0])
        return plot.cohort_active_users(cohorts, grouped, 
                                        time_span = time_span, 
                                        user_totals = user_totals)
        
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
        u_uids = df.index.get_level_values('user_id')
        s_uids = grouped.groups.keys()
        print len(s_uids), len(u_uids)

        #This might no longer be necessary now that we have better validation
        ids_not_incommon = set(s_uids).symmetric_difference(u_uids)
        if ids_not_incommon:
            print 'we need to reslice the sessions or users dataframe' 
        
        for cohort, user_id in df.index:            
            group = grouped.get_group(user_id)
            val_counts = group.time.diff().fillna(0.).value_counts()

            dt = (group.time - df.loc[(cohort, user_id), 'joined'])
                
            if dt.shape[0] > 1:
                    
                age = df.loc[(cohort, user_id), 'age']
                
                mean_ri = (dt/dt.shift(-1).fillna(age)).mean()
                
            else:
                mean_ri = 1

            max_inactive = val_counts.index.max()
            
            max_inactive_counts = val_counts.ix[max_inactive]
            
            df.loc[(cohort, user_id), 'max_inactive_counts'
                  ] = max_inactive_counts
            
            #normalize the max_inactive for users that come and go come and go
            df.loc[(cohort, user_id), 
                   'max_inactive'] = max_inactive/max_inactive_counts

            df.loc[(cohort, user_id), 'mean_ri'] = mean_ri
            #change index to time
            sdf = group.set_index('time')
            
            #Need to work out the columns here due to adding the dmodel
            if how == 'median':
                df.loc[(cohort, user_id), 
                       sdf.columns] = resample(time_span, sdf 
                                              ).median().values

            else:
                df.loc[(cohort, user_id), sdf.columns] = resample(time_span, 
                                                                  sdf 
                                                                 ).mean().values

        #scale activity level so that it is in appropriate units
        df['duration'] = df['duration']/scale
        df['engagement_rate'] = user_engagement_rate(df)
        
        #sort the dataframe and convert object dtypes to numeric if possible
        return df

    def drop_outliers(self, df, outliers = {'friends' : 30, 
                                      'activity_level' : 60*60*2,
                                      'pv' : 20 } ):
        '''method to drop outliers from the input dataframe
           Inputs: df, dataframe
                   outliers, dict, Note: default for activity_level
                                         is 2 hours in seconds 
        '''  
        mask = None
        for key, value in outliers.items():
            if mask is None:
                mask =  (df[key] < outliers[key])
            else:
                mask = mask & (df[key] < outliers[key])

        return df.ix[mask]

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

    def scatter_matrix(self, df = None, columns = None):
        '''method to plot a scatter matrix for the input dataframe'''
        if columns is None:
            columns = ['retention_index', 'mean_ri', 'dust', 
                       'age', 'duration', 'pv', 'sessions', 
                       'friends', 'max_inactive', 'info', ]
        vis_df = df[columns]
        plot.scatter_matrix(vis_df, figsize= (16,16))

    def learn(self, X, y):
        '''method to determine if the churn can be determined from the 
           features. It uses three routines to fit the features to 
           churn or retain.
        '''
        results = {'Support vector machines': (y, run_cv(X, y, SVC)),  
                   'Random forest' : (y, run_cv(X, y, RF)),
                   'K-nearest-neighbors' : (y, run_cv(X, y, KNN)) }
        
        for key, values in sorted(results.items()):
            print "{0}: {1:.3f}".format(key, accuracy(*values))
         

        #plot the confusion matrices
       
        confusion_matrices(results)

    def expected_retention_index_plot(self, df, 
                                      feature = ('friends',  20 )):
        '''calculate the expected retention index for the input dataframe '''
        grouped = df[df[feature[0]] < feature[1] 
                    ].groupby(feature[0])
        result =  grouped['retention_index', 'mean_ri'].mean()
        yerr = grouped.retention_index.std()/np.sqrt(grouped.retention_index.count())
        
        yerr2 = grouped.mean_ri.std()/np.sqrt(grouped.mean_ri.count())
        ax = result.retention_index.plot(linestyle = '',markersize = 10, 
                                         marker = 'o', yerr = yerr)
        result.mean_ri.plot(linestyle = '',markersize = 10, 
                            marker = '+', yerr = yerr2)
        ax.set_xlabel(feature[0])
        ax.set_ylabel('expected retention_index')
        #for  value in feature.values():
        #    ri_count = df.groupby('retention_index').retention_index.count()
        #total_counts = ri_count.sum()
        #ri_cumsum = ri_count.cumsum()
        #ri_prob = ri_cumsum/total_counts
        #ri_prob.plot(xlabel = , ylabel = 
       
def user_engagement_rate(df):
    '''function to calculate the user engagement rate from the user dataframe.
       Input: df, DataFrame
       Output: user_engagement_rate, Series
    ''' 
    #determine the user engagement rate: first attempt 
    return df['retention_index']*df['duration']
    
def get_attribute_summary(udf, attribute = 'friend', split_val = None):
        '''Function to get the users that have started the service
           day after joining
           Inputs: udf, slice of the users dataframe
                   attribute, str, column of interest
                   split_val, int/str, category boundary
           Output: tuple, (number of true users, number of false users)
        '''
        (true_users, 
         false_users) = categorize.user_attribute(udf, attribute = attribute,
                                                  split_val =  split_val)
        #return the number of users with/without                                                       
        return  len(true_users), len(false_users)                                                     
                                                         
        



