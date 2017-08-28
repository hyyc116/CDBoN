import numpy as np
import statsmodels.api as sm
lowess = sm.nonparametric.lowess
x = sorted(np.random.uniform(low = -2*np.pi, high = 2*np.pi, size=500))
y = np.sin(x) + np.random.normal(size=len(x))
z = zip(*lowess(y,x))[1]
w = zip(*lowess(y,x,frac=0.6))[1]
print z
print w

plt.plot(x,y,label='original')
plt.plot(x,z,label='default')
plt.plot(x,w,label='1/3')
plt.legend()
plt.savefig('test.png')