#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

fig,axes = plt.subplots(10,1,figsize=(5,50))
for i,ax in enumerate(axes):
    s = np.random.poisson(1+i*5, 10000)
    count, bins, ignored = ax.hist(s, 14, normed=True,label='$\lambda={:}$'.format(1+i*5))
    ax.legend()

plt.tight_layout()
plt.savefig('poisson.png',dpi=200)