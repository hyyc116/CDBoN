#coding:utf-8
import sys
import json
from collections import defaultdict
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
import random


def subplot_line(ax,xs,ys,title,xls,yls):
    ax.plot(xs,ys)
    ax.set_title(title,fontsize=15)
    ax.set_xlabel(xls,fontsize=10)
    ax.set_ylabel(yls,fontsize=10)


