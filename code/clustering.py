#!/usr/bin/python
# -*- coding: utf-8 -*-
"""functions and classes for clustering
   Created by Robert Kruhlak
   # KMeans Code source: Gaël Varoquaux
   # Modified for documentation by Jaques Grobler
   # License: BSD 3 clause

"""

## use floating point division always (ie matlab, python 3.x)
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans

def plot_clusters(X, columns, columns_to_plot = None, n_comp = 4, 
                  logx = False, logy = False, logz = False ):
    '''function to determine clusters via KMeans and plot the result
       Inputs: df, dataframe with three or more data columns and no target 
                   column for unsupervised KMeans
       Output: axes

    '''
    if columns_to_plot is None:
        columns_to_plot = [0, 1, 2]

    np.random.seed(5)

    centers = [[1, 1], [-1, -1], [1, -1]]


    estimators = {'k_means_3': KMeans(n_clusters = 3, n_jobs = 3),
                  'k_means_n': KMeans(n_clusters = n_comp, n_jobs = 3),
                 }

    fignum = 1

    for name, est in estimators.items():
        fig = plt.figure(fignum, figsize=(12, 9))
        plt.clf()
        ax = Axes3D(fig, rect=[0, 0, .99, 1], elev = 10, azim = 190)

        est.fit(X)
        labels = est.labels_
        x = X[:, columns_to_plot[0]]
        if logx:
            x = np.log(x)
        y = X[:, columns_to_plot[1]]
        if logy:
            y = np.log(y)
        z = X[:, columns_to_plot[2]]
        if logz:
            z = np.log(z)

        ax.scatter( x, y, z, c=labels.astype(np.float))

        #ax.w_xaxis.set_ticklabels([])
        #ax.w_yaxis.set_ticklabels([])
        #ax.w_zaxis.set_ticklabels([])
        ax.set_xlabel(columns[columns_to_plot[0]])
        ax.set_ylabel(columns[columns_to_plot[1]])
        ax.set_zlabel(columns[columns_to_plot[2]])
        ax.set_title(name)
        fignum = fignum + 1

    plt.show()
    return labels

def scatter3d(x, y, z,labels = None, fig_num = None, fig_size = (12,9), 
              elev = 10, azim = 190, xlabel = '', ylabel = '', zlabel = ''):
    '''scatter plot in 3D with labels for the clusters from a previous
       KMeans analysis.
    '''
    #This is the unnormalized plot
    fig = plt.figure(fig_num, figsize = fig_size)
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .99, 1], elev = elev, azim = azim)

    
        
    ax.scatter( x, y, z, c = labels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    return ax
