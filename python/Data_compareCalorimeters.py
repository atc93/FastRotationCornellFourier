import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import math

name = 'txt/60h_fourierAnalysis_perCalo.txt'
tag='60h'

caloNum = np.loadtxt(name, usecols=0)
t0      = np.loadtxt(name, usecols=2)*1000
fom     = np.loadtxt(name, usecols=10)
xe      = np.loadtxt(name, usecols=12)
width   = np.loadtxt(name, usecols=14)
ce      = np.loadtxt(name, usecols=16)

plt.figure(1)
fit = np.polyfit(caloNum,t0,1)
fit_fn = np.poly1d(fit) 
plt.plot(caloNum,t0, 'rx', caloNum, fit_fn(caloNum), 'k')
plt.suptitle('t0 = {0:.3f} + {1:.3f} ns'.format(fit_fn.c[0], fit_fn.c[1]))
plt.xlabel('Calo #')
plt.ylabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '_t0_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_t0_vs_caloNum.png', format='png')
plt.close()
print fit_fn.c[0]

plt.figure(2)
plt.plot(caloNum, xe, 'rx')
plt.xlabel('Calo #')
plt.ylabel('$\mathregular{x_{e}}$ [mm]')
plt.savefig('plots/eps/' + tag + '_xe_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_xe_vs_caloNum.png', format='png')
plt.close()

plt.figure(3)
plt.plot(caloNum, width, 'rx')
plt.xlabel('Calo #')
plt.ylabel('Width [mm]')
plt.savefig('plots/eps/' + tag + '_width_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_width_vs_caloNum.png', format='png')
plt.close()

plt.figure(4)
plt.plot(caloNum, ce, 'rx')
plt.xlabel('Calo #')
plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
plt.savefig('plots/eps/' + tag + '_ce_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_ce_vs_caloNum.png', format='png')
plt.close()

avg_ce = 0
avg_xe = 0
avg_w = 0
for i in ce:
    avg_ce += i
for i in xe:
    avg_xe += i
for i in width:
    avg_w += i
avg_ce /= 24
avg_xe /= 24
avg_w /= 24
print avg_ce, avg_xe, avg_w

std = 0
sum = 0
for i in ce:
    sum += 1
    std += (i-avg_ce) * (i-avg_ce)
std /= sum-1
std = math.sqrt(std)

print 'C_E = ', avg_ce, ' +- ', std

std = 0
sum = 0
for i in xe:
    sum += 1
    std += (i-avg_xe) * (i-avg_xe)
std /= sum-1
std = math.sqrt(std)

print 'x_e = ', avg_xe, ' +- ', std

std = 0
sum = 0
for i in width:
    sum += 1
    std += (i-avg_w) * (i-avg_w)
std /= sum-1
std = math.sqrt(std)

print 'width = ', avg_w, ' +- ', std
