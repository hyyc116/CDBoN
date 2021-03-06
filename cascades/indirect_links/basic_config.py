#coding:utf-8
import os
import sys
import json
from collections import defaultdict
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import math
import numpy as np
import random
import logging
import networkx as nx
from itertools import combinations
import pylab
import itertools
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
from scipy.interpolate import spline
from multiprocessing.dummy import Pool as ThreadPool
from networkx.algorithms import isomorphism
from matplotlib import cm as CM
from collections import Counter
# from viz_graph import plot_a_subcascade
from scipy.signal import wiener
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.patheffects import withStroke
import matplotlib.colors as colors
from matplotlib.colors import LogNorm
from matplotlib.colors import LinearSegmentedColormap
from networkx.algorithms.core import core_number
from networkx.algorithms.core import k_core

mpl.rcParams['agg.path.chunksize'] = 10000


color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
PREFIX='all'
PROGRAM_ID='cascade'
FIGDIR='pdf'
DATADIR='data'

params = {'legend.fontsize': 8,
         'axes.labelsize': 15,
         'axes.titlesize':20,
         'xtick.labelsize':15,
         'ytick.labelsize':15}
pylab.rcParams.update(params)


def circle(ax,x,y,radius=0.15):

    circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                    edgecolor='black', facecolor=(0, 0, 0, .0125),
                    path_effects=[withStroke(linewidth=5, foreground='w')])
    ax.add_artist(circle)

def power_low_func(x,a,b):
    return b*(x**(-a))

def exponential_func(x,a,b):
    return b*np.exp(-a*x)

def square_x(x,a,b,c):
  return a*pow(x,2)+b*x+c

def autolabel(rects,ax,total_count=None,step=1,):
    """
    Attach a text label above each bar displaying its height
    """
    for index in np.arange(len(rects),step=step):
        rect = rects[index]
        height = rect.get_height()
        # print height
        if not total_count is None:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '{:}\n({:.6f})'.format(int(height),height/float(total_count)),
                    ha='center', va='bottom')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '{:.2f}'.format(height),
                    ha='center', va='bottom')

def plot_heat_scatter(xs,ys,ax,fig):

    xyz = defaultdict(lambda: defaultdict(int))
    for i,x in enumerate(xs):
        y = ys[i]

        xyz[x][y]+=1

    xs = []
    ys = []
    zs = []
    for x in xyz.keys():
        yz = xyz[x]
        for y in yz.keys():
            z = xyz[x][y]

            xs.append(x)
            ys.append(y)
            zs.append(z)

    zs = np.array(zs)
    print zs[:10],max(zs)
    print len(xs),len(ys),len(zs)
    norm = mpl.colors.LogNorm(vmin=min(zs),vmax=max(zs))

    ccs = [colors.to_rgba(color_sequence[0]),colors.to_rgba(color_sequence[2]),colors.to_rgba(c='y')]
    cm = LinearSegmentedColormap.from_list('my_list', ccs)

    ax.scatter(xs, ys, c=cm(norm(zs)), marker='o', s = norm(zs)+1,alpha=0.7)

    colmap = CM.ScalarMappable(norm=norm, cmap=cm)
    colmap.set_array(zs)
    plt.colorbar(colmap,ax=ax)

def paras_square(xs,ys,tag,total):

    rxs=[]
    rys=[]
    rzs=[]

    max_y = np.log(np.max(ys))
    min_y = np.log(np.min(ys))
    norm_ys = (np.log(ys)-min_y)/(max_y-min_y)


    x_is = np.arange(10,100,2)
    y_is = np.arange(110,len(xs),10)

    ROWS = len(x_is)
    COLS = len(y_is)

    # fig,axes = plt.subplots(ROWS,COLS,figsize=(COLS*5,ROWS*5))
    max_start=0
    max_end =0
    max_z = 0

    for i,start in enumerate(x_is):
        for j,end in enumerate(y_is):

            x = xs[start:end]
            y = ys[start:end]

            popt,pcov = curve_fit(power_low_func,x,y)
            fit_y = power_low_func(x, *popt)
            r2 = r2_score(np.log(y),np.log(fit_y))

            normed_y = (np.log(y)-min_y)/(max_y-min_y)
            # print start,end,float(len(y))/len(ys)

            # percent = np.sum(normed_y)/float(np.sum(norm_ys))*((float(len(y))/len(ys))**(-0.2))
            percent = np.sum(normed_y)/float(np.sum(norm_ys))*(1-(float(len(y))/len(ys)))

            # percent = np.sum(normed_y)/float(np.sum(norm_ys))*(np.exp(-5*(float(len(y))/len(ys))))


            r2 = r2*percent

            rxs.append(x[0])
            rys.append(x[-1])
            rzs.append(r2)

            if r2>max_z:
                max_start = x[0],start
                max_end = x[-1],end
                max_z = r2

    fig=plt.figure(figsize=(14,10))
    ax = Axes3D(fig)
    ax.view_init(60, 240)
    X = np.reshape(rys,(ROWS,COLS))
    Y = np.reshape(rxs,(ROWS,COLS))
    Z = np.reshape(rzs,(ROWS,COLS))
    ax.set_xlabel('$x_{max}$')
    ax.set_ylabel('$x_{min}$')
    ax.set_zlabel('Global $R^2$')
    ax.set_zscale('log')
    ax.set_title('$x_{min}$:'+'{:}'.format(max_start[0])+' - $x_{max}$:'+'{:}'.format(max_end[0])+', $R^2={:.4f}$'.format(max_z))
    surf = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=CM.coolwarm)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    # plt.tight_layout()
    plt.savefig('pdf/para_space_{:}.pdf'.format(tag),dpi=200)
    print max_start,max_end,max_z
    return max_start[-1],max_end[-1]

