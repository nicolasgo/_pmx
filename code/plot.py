'''module for user related code.
   Created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

import pandas as pd
import numpy as np
from scipy import stats
import pandas.core.common as com # for local radviz

import matplotlib.pyplot as plt
from pandas.tools.plotting import radviz as radviz_p
from pandas.tools.plotting import _get_standard_colors
from .regression import  weighted_exponential_fit

from pandas.tools.plotting import scatter_matrix 

from . import dates
from dateutil.relativedelta import relativedelta


def plot_column( df, column, nonnumeric_index = True, 
                 marker = '.', markersize = 10, linestyle = '' ):
    '''function to plot a column of a dataframe
       Inputs: df, DataFrame 
               column, str
    '''    
    sorted_df = df[column].copy()
    #sort cannot be chained as it does it inplace
    sorted_df.sort()
    
    axes = sorted_df.plot( marker = marker, markersize = markersize, 
                           linestyle = linestyle)
    axes.set_ylabel(column)

    if nonnumeric_index: #remove the xaxes labels
        axes.get_xaxis().set_ticklabels([])  
        axes.set_xlabel('User Rank (ascending)')
      
    return axes

def stacked_bar(df, horizontal = False, ax = None, picker = None):
    '''function to create a stacked bar chart from a pandas dataframe
       Input: DataFrame
       Output: axes
    '''
    short_dates = [dt.strftime('%b %y') for dt in df.index]

    if horizontal:
         
        ax = df.plot(kind = 'barh', stacked = True, ax = ax, picker = picker)
        ax.set_yticklabels(short_dates)
    else:
        ax = df.plot(kind = 'bar', stacked = True, ax  = ax, picker = picker)
        ax.set_xticklabels(short_dates)
    #move legend to the side 
    ax.legend(bbox_to_anchor=(0.96, 1), loc=2, borderaxespad=0.)

    return ax

def histogram_subplots( cohort_range, df, log = True, xlabel = None,
                        ylabel = None, min_x = 0, 
                        column_name = 'retention_index',
                        sharey = True):
    '''function to create an odd number of subplots centered around a 
       chosen cohort. Used in conjuction with IPython.html.interact

       Input: cohort_range, np array of datetime.date objects representing 
                            cohorts to be plotted
              df, dataframe with retetion_index series data
              
              log, Boolean, to use a log scale for the y axis or not.
              xlabel, str, label for the x-axis
              ylabel, str, label for the y-axis
              min_x, float, describes where to truncate the x-data on the low
                            end
              column_name, str, column_name to plot in the dataframe, df
 
       Output: matplotlib axes  
              
    ''' 
    #create figure (fig) and axes array (ax)        
    fig, ax = plt.subplots(1, len(cohort_range), figsize = (16,4),  
                           sharey = sharey)
        
    for key, cohort in enumerate(cohort_range):
        #dataframe slice for the specific cohort
        #drop the first and last day because it most likely does not contain
        #the full 24 hours of information

        cdf = df.ix[cohort] #'retention_index', 
        mask = cdf[column_name] >= min_x    
        #plot the original data    
        ax[key] = cdf.loc[mask, column_name].plot( kind = 'hist', log = log,
                                                   ax=ax[key], bins = 20)
        #add title
        ax[key].set_title('Cohort {0}'.format(cohort))
        ax[key].set_xlabel(xlabel)

        
    #add the ylabel to left most axes        
    ax[0].set_ylabel(ylabel)   
    for axis in ax:
        plt.setp( axis.xaxis.get_majorticklabels(), rotation= 75 )

    for my_ax in ax[1:]:
        my_ax.set_ylabel('')
    
    return ax

def histogram_plot( cohort, df, log = True, xlabel = None,
                    ylabel = None, min_x = 0, 
                    column_name = 'retention_index'):
    '''function to create an odd number of subplots centered around a 
       chosen cohort. Used in conjuction with IPython.html.interact

       Input: cohort_range, np array of datetime.date objects representing 
                            cohorts to be plotted
              df, dataframe with retetion_index series data
              
              log, Boolean, to use a log scale for the y axis or not.
              xlabel, str, label for the x-axis
              ylabel, str, label for the y-axis
              min_x, float, describes where to truncate the x-data on the low
                            end
              column_name, str, column_name to plot in the dataframe, df
 
       Output: matplotlib axes  
              
    ''' 
    #create figure (fig) and axes array (ax)        
    fig, ax = plt.subplots(1, len(cohort_range), figsize = (16,4),  
                           sharey = True)
        
    
    #dataframe slice for the specific cohort
    
    cdf = df.ix[cohort] #'retention_index', 
    mask = cdf[column_name] >= min_x    
    #plot the data    
    ax = cdf.loc[mask, column_name].plot( kind = 'hist', log = log, 
                                          ax = ax, bins = 20)
    #add title
    ax.set_title('Cohort {0}'.format(cohort))
    ax.set_xlabel(xlabel)

    #add the ylabel to left most axes        
    ax[0].set_ylabel(ylabel)   
    
    return ax

def engagement_subplots( cohort_range, df, units = 'minutes',  
                         normalized = True, window = 7, time_span = 'W',
                         drop_first = True, drop_last = True):
    '''function to create an odd number of subplots centered around a 
       chosen cohort. Used in conjuction with IPython.html.interact

       Input: cohort_range, np array of datetime.date objects representing 
                            cohorts to be plotted
              df, dataframe with engagement rate time series data
              
              units, str, in ['minutes', 'hours', 'days']
              normalized, Boolean, to normalize the data to cohort size or not.
              window, int, number of points for the rolling mean (7 is typical),
              time_span, str, in ('D', 'W', 'M')
              drop_first, Boolean,  to drop or keep the first index of the
                                   df dataframe.
              drop_last, Boolean, to drop or keep the last index of the
                                   df dataframe.
 
       Output: matplotlib axes  
              
    ''' 
    #create figure (fig) and axes array (ax)        
    fig, ax = plt.subplots(1, len(cohort_range), figsize = (16,4),  
                           sharey = True)
    max_xlim = None
    min_xlim = None    
    for key, cohort in enumerate(cohort_range):
        #dataframe slice for the specific cohort
        #drop the first and last day because it most likely does not contain
        #the full 24 hours of information
        
        cdf = get_cohort_column(df, cohort, column = 'engagement_rate', 
                                drop_first = drop_first, drop_last = drop_last )
        if max_xlim is None:
            max_xlim = cdf.index.max()
        elif max_xlim < cdf.index.max():
            max_xlim = cdf.index.max()
        if min_xlim is None:
            min_xlim = cdf.index.min()
        elif min_xlim < cdf.index.min():
            min_xlim = cdf.index.min()
        #rolling std deviation
        yerr = pd.rolling_std(cdf, window = window, min_periods = 1)
        #Calculate the rolling_mean and plot with error bars                
        ax[key] = pd.rolling_mean(cdf, window = window, min_periods = 1, 
                                 ).plot(yerr=yerr, ax = ax[key])
            
        #plot the original data    
        ax[key] = cdf.plot(ax=ax[key],marker = 'o', markersize = 8, 
                           linestyle = '')
        #add title
        ax[key].set_title('Cohort {0} '.format(cohort))
        ax[key].set_xlabel('date')

    time_span_text = {'D' : 'daily',
                      'W' : 'weekly',
                      'M' : 'monthly'}.get(time_span, 'weekly')
    if normalized:
        ylabel = '{0} engagement rate ({1})/user'.format(time_span_text, units)
    else:    
        ylabel = '{0} engagement rate ({1})'.format(time_span_text, units)   
    
    #add the ylabel to left most axes        
    ax[0].set_ylabel(ylabel)  
    print 'x limits = ({0}, {1})'.format(min_xlim, max_xlim )
    for axis in ax:
        plt.setp( axis.xaxis.get_majorticklabels(), rotation= 75 )
        axis.set_xlim((min_xlim,max_xlim))

    return ax

def engagement_plot( cohort, df, time_units = 'minutes', 
                     normalized = True, window = 7, 
                     visible = True, time_span = 'W', drop_first = True,
                     drop_last = True ):
    '''function to plot the engagement for a single cohort along with the 
       rolling mean and std.
       Input: cohort, datetime.date obj (not the index)
              df, dateframe containing engagement_rate time series data  (daily)
              time_units, str, units for the engagement rate
              normalized, Boolean, to normalize the data to cohort size or not.
              window, int, number of points for the rolling mean (7 is typical),
              time_span, str, in ('D', 'W', 'M')
              drop_first, Boolean,  to drop or keep the first index of the
                                   df dataframe.
              drop_last, Boolean, to drop or keep the last index of the
                                   df dataframe.
       Output: ax, matplotlib, axes
    '''
    fig = plt.figure('cohort', figsize = (16,6))
    ax = fig.add_subplot(1,1,1)
    #slice the data frame for the cohort and engagement_rate
    df = get_cohort_column(df, cohort, column = 'engagement_rate', 
                           drop_first = drop_first, drop_last = drop_last )

    yerr = pd.rolling_std(df, window = window, min_periods = 1)
    ax = pd.rolling_mean(df, window = window, min_periods = 1).plot(yerr=yerr)
    
    ax = df.plot(ax=ax, marker = 'o', markersize = 10, linestyle = '')
    time_span_text = {'D' : 'daily',
                      'W' : 'weekly',
                      'M' : 'monthly'}.get(time_span, 'weekly')
    if normalized:
        ylabel = '{0} engagement rate ({1})/user'.format(time_span_text,
                                                         time_units)
    else:    
        ylabel = '{0} engagement rate ({1})'.format(time_span_text, time_units)

    ax.set_ylabel(ylabel)
    ax.set_xlabel('date')
    ax.set_title('Cohort {0}'.format(cohort))
    plt.setp( ax.xaxis.get_majorticklabels(), rotation= 75 )
    ax.set_visible(visible)
    
    return ax
     
def cohort_growth_subplots( area_range, df ):
    '''function to create an odd number of subplots centered around a 
       chosen area. Used in conjuction with IPython.html.interact

       Input: area_range, np array of strs  representing 
                          geographic areas to be plotted
              df, dataframe with engagement rate time series data
              
       Output: matplotlib axes  
              
    ''' 
    #create figure (fig) and axes array (ax)        
    fig, ax = plt.subplots(1, len(area_range), figsize = (16,4),  
                           sharey = True)
        
    for key, area in enumerate(area_range):
        #dataframe slice for the specific cohort
        #drop the last cohort because it is not complete
        adf = df.loc[area][:-1]
        #plot the original data    
        ax[key] = cohort_growth_chart(adf, ax=ax[key], ylabel = False,
                                      next_month = False, text_loc = 'left')
        #add title
        ax[key].set_title('Area {0}'.format(area))
        ax[key].set_xlabel('cohort')
    
    #add the ylabel to left most axes        
    #ax[0].set_ylabel(ylabel)   
    return ax

def cohort_active_users(cohorts, grouped, time_span = 'W', 
                        user_totals = None):
    '''function to plot the active users as a function of time 
       for each cohort in cohorts
    '''
    
    fig = plt.figure(figsize = (16,8))
    ax = plt.subplot(111)
    colors = [] 
    window = {'D' : 1,
              'W' : 7,
              'M' : 30 }.get(time_span)
    for cohort, group in grouped:
        group.index = group.index.droplevel(0)
        if user_totals is not None:
            df = 100*pd.rolling_mean(group, window, center = True
                                )/user_totals[cohort]
        else:
            df = pd.rolling(group, window, center = True)
            
        line, = ax.plot(df, label = cohort)
        colors.append(plt.getp(line,'color'))
        
        #handles.append(h[0])
    leg = ax.legend(loc = 'best')        
    ax.set_xlabel('Day from beginning of the cohort')
    ax.set_ylabel('% Active Users: {0} day mean'.format(window))
    for color,text in zip(colors,leg.get_texts()):
        text.set_color(color)
    
    #lgd =plt.legend(handles, cohorts)
    return ax       
    
def not_started_users(df, columns_to_plot, xlabel = None, ylabel = None, 
                      yerr= None):
    '''function to plot users that have not started using the service
       as a function of days since joining the service.
    '''
    
    fig = plt.figure(figsize = (16,8))
    ax = plt.subplot(111)
    colors = [] 
    for cohort in df.index.levels[0]:
        for column in columns_to_plot:
            if column == 'fit':
                linestyle = '--'
                marker = ''
                label = '{0} fit'.format(cohort)
                _yerr = None
            else:
                linestyle = ''
                marker = 'o'
                label = cohort
                if yerr is not None:
                    _yerr = yerr.ix[cohort].values
                else:
                    _yerr = yerr
                
            containers  = ax.errorbar(df.ix[cohort].index, 
                                      df.ix[cohort, column].values, 
                                      label = label, marker = marker, 
                                      linestyle = linestyle,
                                      yerr = _yerr)
                        
            colors.append(plt.getp(containers[0],'color'))
            
        
    leg = ax.legend(loc = 'best')        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for color,text in zip(colors,leg.get_texts()):
        text.set_color(color)

    return ax       
            
def engagement_chart( df, ax = None, horizontal = False,  picker = None, 
                      units = 'minutes', time_span = 'W', normalized = True):
    '''function to create an interactive stacked bar chart
       Input: df, dataframe with column named 'engagement_rate'
              ax, matplotlib axes to attach the chart to
              horizontal, boolean, to orient the bars horizontally or not
              picker, int or None, size of spot where a click is associated.
                                   when generating additional plots by a
                                   mouseclick. Use None to deactivate
              
              units, str, in ('seconds', 'minutes, 'hours', 'days')
              normalized, Boolean, to normalize the data to cohort size or not.
              time_span, str, in ('D', 'W', 'M')
       Output: modified matplotlib axes with the chart attached.     
    '''
    #create axis labels    
    time_span_text = {'D' : 'daily',
                      'W' : 'weekly',
                      'M' : 'monthly'}.get(time_span, 'weekly')
    if normalized:
        ylabel = 'engagement rate ({0})/user'.format(units)
    else:    
        ylabel = 'engagement rate ({0})'.format(units)   
    
    axes_labels = ('cohort', ylabel )
    #create the        
    ax = stacked_bar( df[['engagement_rate']].unstack(), 
                      horizontal = horizontal, ax = ax, picker = picker)

    #rearrange if horizontal
    xlabel, ylabel = flip_labels(horizontal, axes_labels)        

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if not horizontal:
        if 1: 
            #we can add the size of the cohort above the bars
            erlen = len(set(df.reset_index().cohort))
            sizes = df.groupby(level=0).mean().size
            #for some cases we have more than one bar per cohort
            #so we need to get the bars from the last back to 
            #last - cohort_size
            ax = autolabel(ax, ax.patches[-erlen:], sizes)

    estr = '(engagement_rate, '
    ler = 0 #default
    #get handles and labels so we can improve the legend
    handles, labels = ax.get_legend_handles_labels()
    if estr in labels[0]:
        ler = len(estr)

    #11 is the length of the date string
    labels = [ label[ler:ler+10] for label in labels ]
       
    ax.legend(handles, labels,
              bbox_to_anchor=(0.98, 1), loc=2, borderaxespad=0.)
    title = '{0} engagement rates'.format(time_span_text )
    ax.set_title(title)
    return ax

def radviz_plot(df, category = 'cohort'):
    '''radviz visualisation of multiaxial data
        df, dataframe to plotfig, ax = plt.subplots(1)
    '''    
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)
    #pandas version of radviz
    ax = radviz_p(df, category)
    #move legend outside because it is so big
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return ax

def devices_chart(df, top, axes_labels, horizontal = False, name = 'devices' ):
    '''function to create a bar chart for the devices used when accessing
       the site
    '''
    ax = stacked_bar(df, horizontal = horizontal)

    xlabel, ylabel = flip_labels(horizontal, axes_labels)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    title = 'Top {0} {1} '.format(top, name)
    ax.set_title(title)

    return ax


def autolabel(ax, rects, names, scale = 1.05):
    '''autolabel  rectangles in a barchart with text
       Input: ax, matplotlib axes
              rects, group of matplotlib rectangles
              names, list of strs that will be placed. Must be same number 
                     as the number of rectangles.
              scale, scale the height of the rectangles so we place the labels
                     above the rectangles.
       Output: modified matplotlib axes with the text annotates
    '''
    # attach some text labels
    for ii, rect in enumerate(rects):
        height = rect.get_height()
      
        ax.text( rect.get_x()+rect.get_width()/2., 
                 rect.get_y() + scale*(height), 
                 '%s'% (names[ii]),
                 ha='center', va='bottom', color = 'g', rotation = 'vertical')
    return ax

def flip_labels(horizontal, axes_labels):
    '''helper function to flip labels based on the value of horizontal
       Input: horizontal, boolean
              axes_labels, tuple (xlabel, ylabel)
       Output: xlabel, ylabel
    '''
    if horizontal: #flip axes labels
        xlabel = axes_labels[1]
        ylabel = axes_labels[0]
    else: #normal axes labels
        xlabel = axes_labels[0]
        ylabel = axes_labels[1]

    return xlabel, ylabel

def page_views_subplots( cohort_range, df ):
    '''function to create an odd number of subplots centered around a 
       chosen cohort. Used in conjuction with IPython.html.interact

       Input: cohort_range, np array of datetime.date objects representing 
                            cohorts to be plotted
              df, dataframe with engagement rate time series data
              
              percentage, Boolean, plot pageviews as a percentage of the total.
              window, int, number of points for the rolling mean (7 is typical)

       Output: matplotlib axes  
              
    ''' 
    #create figure (fig) and axes array (ax)        
    fig, ax = plt.subplots(1, len(cohort_range), figsize = (16,4) )
    category = 'user_id'    
    #from pudb import set_trace; set_trace()
    for key, cohort in enumerate(cohort_range):
        #dataframe slice for the specific cohort
        cdf = df.ix[cohort]
    
        #plot the original data    
        radviz(cdf.reset_index(), category, ax = ax[key], use_legend = False)
        #ax[key].legend().set_visible(False)
        #move legend outside because it is so big
        #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        #add title
        ax[key].set_title('Cohort {0}'.format(cohort))
        #ax[key].set_xlabel('date')

    
    #add the ylabel to left most axes        
    #ax[0].set_ylabel(ylabel)   
    return ax

def page_views_plot( cohort, df ):
    '''function to create an odd number of subplots centered around a 
       chosen cohort. Used in conjuction with IPython.html.interact

       Input: cohort_range, np array of datetime.date objects representing 
                            cohorts to be plotted
              df, dataframe with engagement rate time series data
              
              percentage, Boolean, plot pageviews as a percentage of the total.
              window, int, number of points for the rolling mean (7 is typical)

       Output: matplotlib axes  
              
    ''' 
    fig = plt.figure('cohort', figsize = (8,5))
    ax = fig.add_subplot(1,1,1)

    category = 'user_id'    
   
    cdf = df.loc[cohort]
     
    #plot the original data    
    #use local copy of radviz-- see page_views_subplots
    ax = radviz(cdf.reset_index(), category, ax = ax, use_legend = False)
    #ax.legend().set_visible(False) 
    #move legend outside because it  is so big
    #ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


def cohort_growth_chart(cohort_size, model = [0.1, 2.5], ax = None, 
                        ylabel = True, next_month = True, 
                        text_loc = 'center'):
    '''chart of cohort size for cohorts from youngest to oldest
       Input: cohort_size, Series with cohort name as the index
    '''
    #simple exponential growth model. Needs to be improved to account for 
    #the retention index (ie some of each cohort stop will stop 
    #using the service each month)
    #this is the xaxis but it may not be continuous (ie in the early days)
    #there may be no cohort for a given month.
    idx = cohort_size.index
    #create a continuous cohort range
    cont_cohort_range = dates.cohort_range(start_year = idx.min().year,
                                           end_year = idx.max().year, 
                                           start_month = idx.min().month, 
                                           end_month = idx.max().month )

    #make an x axis that only contains the indices of the valid cohorts
    #must be an array or series
    xaxis = np.array([ k for k, v in enumerate(cont_cohort_range) if v in idx])   
    
    x, logytheory, model, mse, success = weighted_exponential_fit(xaxis, 
                                                                  cohort_size, 
                                                                  model)

    n = len(xaxis)
    n_m2 = n - 2
    x_next = xaxis[-1]+1
    tscore = stats.t.ppf(0.975, n_m2)
    expected_next_cohort_size = np.exp(model[1])*np.exp(model[0]*x_next )
    next_cohort = cohort_size.index[-1] +relativedelta(months = 1)
    
    if ax is None:
        fig = plt.figure('cohort', figsize = (10, 6))
        ax = fig.add_subplot(1,1,1)
    
    myx = cohort_size.index
    ytheory = np.exp(logytheory) 
    ax.plot(myx, ytheory)
    #sqrt of mse
    se = np.sqrt(np.sum((ytheory - cohort_size)**2)/n_m2)

    xmean = np.mean(xaxis)
    #error in the vertical direction    
    sy = se*np.sqrt(1 + 1/n + 
                    (x_next - xmean)**2/np.sum((xaxis - xmean)**2))

    y_next = np.exp(np.polyval(model, x_next))
    if next_month:
        print 'next month [{0:.2} {1:.2}]'.format(y_next+tscore*sy,
                                                  y_next-tscore*sy)

    ax.errorbar( next_cohort, expected_next_cohort_size, 
                 yerr = tscore*sy, color='blue', fmt = 'o', markersize = 14,
                 capsize = 4,
                 elinewidth = 3)
    

    ax = cohort_size.plot(marker = '.', markersize = 12, linestyle = '', ax=ax)
    #if the above plot method does not work. 
    #Try plt.plot_date(cohort_size.index, cohort_size)
    if ylabel:
        ax.set_ylabel('users')
    ax.set_xlabel('cohort')
    doubling_time = np.log(2)/model[0]
    annotate_str = ('initial cohort size = {0:.1f}, \n '
                    'growth rate = {1:.2f} 1/month, \n '
                    'rmsd = {2:.2e}\n'
                    'doubling time ~ {3:.1f} months').format( np.exp(model[1]), 
                                                              model[0], 
                                                              se, 
                                                              doubling_time )
    if text_loc == 'left':
        xpos = cohort_size.index[0]
    else:
        xpos = cohort_size.index[1]

    max_size = cohort_size.max()
    ax.annotate( annotate_str, xy = (xpos, 0.6*max_size), 
                 xytext = (xpos, 0.8*max_size))

    plt.setp( ax.xaxis.get_majorticklabels(), rotation= 75 )

    
    plt.title('Cohort size and A exp(g x) fit, \n where A is the initial size '
              'and g is the viral growth per month.' )
    
    return ax

#from pandas.tools.plotting.
#Need to disable the legend for the page_views data
def radviz(frame, class_column, ax=None, color=None, colormap=None, **kwds):
    """RadViz - a multivariate data visualization algorithm

    Parameters:
    -----------
    frame: DataFrame
    class_column: str
        Column name containing class names
    ax: Matplotlib axis object, optional
    color: list or tuple, optional
        Colors to use for the different classes
    colormap : str or matplotlib colormap object, default None
        Colormap to select colors from. If string, load colormap with that name
        from matplotlib.
    kwds: keywords
        Options to pass to matplotlib scatter plotting method

    Returns:
    --------
    ax: Matplotlib axis object
    """
    
    import matplotlib.patches as patches
    #added by rjk
    use_legend = kwds.pop('use_legend', True)

    def normalize(series):
        a = min(series)
        b = max(series)
        return (series - a) / (b - a)

    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]
    df = frame.drop(class_column, axis=1).apply(normalize)

    if ax is None:
        ax = plt.gca(xlim=[-1, 1], ylim=[-1, 1])

    to_plot = {}
    colors = _get_standard_colors(num_colors=len(classes), colormap=colormap,
                                  color_type='random', color=color)

    for kls in classes:
        to_plot[kls] = [[], []]

    m = len(frame.columns) - 1
    s = np.array([(np.cos(t), np.sin(t))
                  for t in [2.0 * np.pi * (i / float(m))
                            for i in range(m)]])

    for i in range(n):
        row = df.iloc[i].values
        row_ = np.repeat(np.expand_dims(row, axis=1), 2, axis=1)
        y = (s * row_).sum(axis=0) / row.sum()
        kls = class_col.iat[i]
        to_plot[kls][0].append(y[0])
        to_plot[kls][1].append(y[1])

    for i, kls in enumerate(classes):
        ax.scatter(to_plot[kls][0], to_plot[kls][1], color=colors[i],
                   label=com.pprint_thing(kls), **kwds)
    if use_legend:    
        ax.legend()

    ax.add_patch(patches.Circle((0.0, 0.0), radius=1.0, facecolor='none'))

    for xy, name in zip(s, df.columns):

        ax.add_patch(patches.Circle(xy, radius=0.025, facecolor='gray'))

        if xy[0] < 0.0 and xy[1] < 0.0:
            ax.text(xy[0] - 0.025, xy[1] - 0.025, name,
                    ha='right', va='top', size='small')
        elif xy[0] < 0.0 and xy[1] >= 0.0:
            ax.text(xy[0] - 0.025, xy[1] + 0.025, name,
                    ha='right', va='bottom', size='small')
        elif xy[0] >= 0.0 and xy[1] < 0.0:
            ax.text(xy[0] + 0.025, xy[1] - 0.025, name,
                    ha='left', va='top', size='small')
        elif xy[0] >= 0.0 and xy[1] >= 0.0:
            ax.text(xy[0] + 0.025, xy[1] + 0.025, name,
                    ha='left', va='bottom', size='small')

    ax.axis('equal')
    return ax

def get_cohort_column(df, cohort, column = 'engagement_rate', 
                      drop_first = False, drop_last = False ):
    '''get a column for plotting when the cohort is the index of 
       the dataframe.
    '''
    if drop_last and drop_first:
        return  df.loc[cohort, column][1:-1]
    elif drop_last:
        return df.loc[cohort, column][:-1]
    elif drop_first:
        return df.loc[cohort, column][1:]
    else:
        return df.loc[cohort, column]


        
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

