#coding:utf-8

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
import statsmodels.api as sm
import statsmodels.formula.api as smf
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)
PREFIX='all'
PROGRAM_ID='friction'
FIGDIR='pdf'
DATADIR='data'

params = {'legend.fontsize': 15,
         'axes.labelsize': 15,
         'axes.titlesize':20,
         'xtick.labelsize':15,
         'ytick.labelsize':15,
         'font.family':'Times New Roman'}
pylab.rcParams.update(params)


def power_low_func(x,a,b):
    return b*(x**(-a))

def autolabel(rects,ax,total_count=None,step=1):
    """
    Attach a text label above each bar displaying its height
    """
    for index in np.arange(len(rects),step=step):
        rect = rects[index]
        height = rect.get_height()
        # print height
        if not total_count is None:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '{:}\n({:.3f})'.format(float(height),height/float(total_count)),
                    ha='center', va='bottom')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                    '{:.3f}'.format(float(height)),
                    ha='center', va='bottom')