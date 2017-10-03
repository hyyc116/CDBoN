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
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
from scipy.interpolate import spline
from multiprocessing.dummy import Pool as ThreadPool
from networkx.algorithms import isomorphism
from matplotlib import cm as CM
from collections import Counter
from viz_graph import plot_a_subcascade
from scipy.signal import wiener
import matplotlib as mpl
from matplotlib.patches import Circle
from matplotlib.patheffects import withStroke
import matplotlib.colors as colors
from matplotlib.colors import LogNorm

mpl.rcParams['agg.path.chunksize'] = 10000


color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)
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
                    '{:}'.format(int(height)),
                    ha='center', va='bottom')

cdict = {'red': ((0.0, 1.0, 1.0),   # Full red at the first stop
                 (0.5, 0.0, 0.0),   # No red at second stop
                 (1.0, 1.0, 1.0)),  # Full red at final stop
        #
        'green': ((0.0, 0.0, 0.0),  # No green at all stop
                 (0.5, 0.0, 0.0),   # 
                 (1.0, 0.0, 0.0)),  # 
        #
        'blue': ((0.0, 0.0, 0.0),   # No blue at first stop
                 (0.5, 1.0, 1.0),   # Full blue at second stop
                 (1.0, 0.0, 0.0))}



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

    yellow = colors.to_rgba(color_sequence[2])
    blue = colors.to_rgba(color_sequence[0])
    ccs = [blue,yellow]
    cm = LinearSegmentedColormap.from_list('my_list', ccs)

    ax.scatter(xs, ys, c=cm(norm(zs)), marker='o')

    colmap = CM.ScalarMappable(norm=norm, cmap=cm)
    colmap.set_array(zs)
    plt.colorbar(colmap,ax=ax)


