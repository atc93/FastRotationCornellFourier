import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import math

name = 'frs_60h_T1492_E1500'
filename = 'txt/' + name + '.txt'
t0      = np.loadtxt(filename, usecols=1)
tS      = np.loadtxt(filename, usecols=3)
tm      = np.loadtxt(filename, usecols=5)
fom     = np.loadtxt(filename, usecols=9)
xe      = np.loadtxt(filename, usecols=11)
width   = np.loadtxt(filename, usecols=13)
ce      = np.loadtxt(filename, usecols=15)

nt0 = 16
ntS = 13
ntm = 4

t0_list = []
ce_list = []
xe_list = []
width_list = []

for itm in range(0, ntm):

    color=cm.rainbow(np.linspace(0,1,ntS))
    textstr = '$\mathregular{t_{m}}$ = ' + str(tm[nt0*ntS*itm]) + ' $\mathregular{\mu}$s'

    #############
    # FOM vs t0 #
    #############

    for itS in range(0, ntS):

        lowerEdge =  nt0*ntS*itm + nt0*itS
        upperEdge = nt0*ntS*itm + nt0*itS+nt0
        x = t0      [lowerEdge : upperEdge]*1000
        y1 = fom    [lowerEdge : upperEdge]
        y2 = ce     [lowerEdge : upperEdge]
        y3 = xe     [lowerEdge : upperEdge]
        y4 = width  [lowerEdge : upperEdge]

        # retrieve best t0
        val, idx = min((val, idx) for (idx, val) in enumerate(abs(y1)))
        t0_list     .append(x[idx])
        xe_list     .append(y3[idx])
        width_list  .append(y4[idx])
        ce_list     .append(y2[idx])

        c = color[itS]
        label = '$\mathregular{t_{S}}$ = ' + str(tS[lowerEdge]) + ' $\mathregular{\mu}$s'
        print label

        plt.figure(1)
        plt.plot(x, abs(y1), c=c, label=label, marker='x')

        plt.figure(2)
        plt.plot(x, y2, c=c, label=label, marker='x')

        plt.figure(3)
        plt.plot(x, y3, c=c, label=label, marker='x')

        plt.figure(4)
        plt.plot(x, y4, c=c, label=label, marker='x')

    # save plots

    plt.figure(1)
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.legend(loc=9, bbox_to_anchor=(.0, 1.088, 1.0, .07), ncol=3, mode="expand", prop={'size':6})
    plt.figtext(0.01, 0.01, textstr, fontsize=10)
    plt.savefig('plots/eps/' + name + '_fom_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.eps', format='eps')
    plt.savefig('plots/png/' + name + '_fom_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.png', format='png')
    plt.close()

    plt.figure(2)
    plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.legend(loc=9, bbox_to_anchor=(.0, 1.088, 1.0, .07), ncol=3, mode="expand", prop={'size':6})
    plt.figtext(0.01, 0.01, textstr, fontsize=10)
    plt.savefig('plots/eps/' + name + '_ce_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.eps', format='eps')
    plt.savefig('plots/png/' + name + '_ce_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.png', format='png')
    plt.close()

    plt.figure(3)
    plt.ylabel('$\mathregular{x_{e}}$ [mm]')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.legend(loc=9, bbox_to_anchor=(.0, 1.088, 1.0, .07), ncol=3, mode="expand", prop={'size':6})
    plt.figtext(0.01, 0.01, textstr, fontsize=10)
    plt.savefig('plots/eps/' + name + '_xe_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.eps', format='eps')
    plt.savefig('plots/png/' + name + '_xe_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.png', format='png')
    plt.close()

    plt.figure(4)
    plt.ylabel('$\mathregular{\sigma}$ [mm]')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.legend(loc=9, bbox_to_anchor=(.0, 1.088, 1.0, .07), ncol=3, mode="expand", prop={'size':6})
    plt.figtext(0.01, 0.01, textstr, fontsize=10)
    plt.savefig('plots/eps/' + name + '_width_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.eps', format='eps')
    plt.savefig('plots/png/' + name + '_width_t0Scan_tm' + str(tm[nt0*ntS*itm]) + '.png', format='png')
    plt.close()

print 'Number of C_E   entries: ' + str(len(ce_list))
print 'Number of xe    entries: ' + str(len(xe_list))
print 'Number of width entries: ' + str(len(width_list))

plt.figure(5)
plt.xlabel('$\mathregular{C_{E}}$ [ppb]')
plt.hist(ce_list, bins=30)
plt.savefig('plots/eps/ce.eps', format='eps')
plt.savefig('plots/png/ce.png', format='png')

plt.figure(6)
plt.xlabel('$\mathregular{x_{e}}$ [mm]')
plt.hist(xe_list, bins=30)
plt.savefig('plots/eps/xe.eps', format='eps')
plt.savefig('plots/png/xe.png', format='png')

plt.figure(7)
plt.xlabel('$\mathregular{\sigma}$ [mm]')
plt.hist(width_list, bins=30)
plt.savefig('plots/eps/width.eps', format='eps')
plt.savefig('plots/png/width.eps', format='png')

mean_ce = 0
std_ce  = 0
mean_xe = 0
std_xe  = 0
mean_width = 0
std_width  = 0

for i in range(0, len(ce_list)):
    mean_ce += ce_list[i]
    mean_xe += xe_list[i]
    mean_width += width_list[i]
mean_ce /= len(ce_list)
mean_xe /= len(ce_list)
mean_width /= len(ce_list)

for i in range(0, len(ce_list)):
    std_ce += ( ce_list[i] - mean_ce ) * ( ce_list[i] - mean_ce )
    std_xe += ( xe_list[i] - mean_xe ) * ( xe_list[i] - mean_xe )
    std_width += ( width_list[i] - mean_width ) * ( width_list[i] - mean_width )
std_ce /= len(ce_list)-1    
std_ce = math.sqrt(std_ce)
std_xe /= len(ce_list)-1    
std_xe = math.sqrt(std_xe)
std_width /= len(ce_list)-1    
std_width = math.sqrt(std_width)

print 'x_e = ' + str(mean_xe) + ' +- ' + str(std_xe)
print 'width ' + str(mean_width) + ' +- ' + str(std_width)
print 'C_E = ' + str(mean_ce) + ' +- ' + str(std_ce)
