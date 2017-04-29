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

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)
PREFIX='all'
PROGRAM_ID='friction'
FIGDIR='pdf'
DATADIR='data'