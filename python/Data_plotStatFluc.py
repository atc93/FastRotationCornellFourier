from importAll import *

cmdargs = str(sys.argv)

inFileName      = str(sys.argv[1])
tag             = str(sys.argv[2])
outFileName     = str(sys.argv[3])

text_file = open(str(outFileName), "w")

t0      = np.loadtxt(inFileName, usecols=1)*1000
tS      = np.loadtxt(inFileName, usecols=3)
tm      = np.loadtxt(inFileName, usecols=5)
fom     = np.loadtxt(inFileName, usecols=9)
xe      = np.loadtxt(inFileName, usecols=11)
width   = np.loadtxt(inFileName, usecols=13)
ce      = np.loadtxt(inFileName, usecols=15)


mean_t0 = 0
std_t0  = 0
mean_ce = 0
std_ce  = 0
mean_xe = 0
std_xe  = 0
mean_width = 0
std_width  = 0

for i in range(0, len(ce)):
    mean_ce += ce[i]
    mean_xe += xe[i]
    mean_width += width[i]
    mean_t0 += t0[i]

mean_ce /= len(ce)
mean_xe /= len(ce)
mean_width /= len(ce)
mean_t0 /= len(ce)

for i in range(0, len(ce)):
    std_ce += ( ce[i] - mean_ce ) * ( ce[i] - mean_ce )
    std_xe += ( xe[i] - mean_xe ) * ( xe[i] - mean_xe )
    std_width += ( width[i] - mean_width ) * ( width[i] - mean_width )
    std_t0 += ( t0[i] - mean_t0 ) * ( t0[i] - mean_t0 )

std_ce /= len(ce)-1
std_ce = math.sqrt(std_ce)
std_xe /= len(ce)-1
std_xe = math.sqrt(std_xe)
std_width /= len(ce)-1
std_width = math.sqrt(std_width)
std_t0 /= len(ce)-1
std_t0 = math.sqrt(std_t0)

print 'x_e = ' + str(mean_xe) + ' +- ' + str(std_xe)
print 'width ' + str(mean_width) + ' +- ' + str(std_width)
print 'C_E = ' + str(mean_ce) + ' +- ' + str(std_ce)

text_file.write('xe %f %f width %f %f ce %f %f t0 %f %f \n' %
                (mean_xe, std_xe, mean_width, std_width, mean_ce, std_ce, mean_t0, std_t0) )
text_file.close()

plt.figure(1)
plt.xlabel('$\mathregular{C_{E}}$ [ppb]')
plt.suptitle('$\mathregular{<C_{E}>}=' + '{0:.1f}'.format(mean_ce) + '$ +- ' + '{0:.1f}'.format(std_ce) + ' ppb')
plt.hist(ce, bins=30)
plt.savefig('plots/eps/' + tag + '_ce.eps', format='eps')

plt.figure(2)
plt.xlabel('$\mathregular{x_{e}}$ [mm]')
plt.suptitle('$\mathregular{<x_{e}>}=' + '{0:.1f}'.format(mean_xe) + '$ +- ' + '{0:.1f}'.format(std_xe) + ' mm')
plt.hist(xe, bins=30)
plt.savefig('plots/eps/' + tag + '_xe.eps', format='eps')

plt.figure(3)
plt.xlabel('$\mathregular{\sigma}$ [mm]')
plt.suptitle('$\mathregular{<\sigma>}=' + '{0:.1f}'.format(mean_width) + '$ +- ' + '{0:.1f}'.format(std_width) + ' mm')
plt.hist(width, bins=30)
plt.savefig('plots/eps/' + tag + '_width.eps', format='eps')

plt.figure(4)
plt.xlabel('$\mathregular{t_{0}}$ [ns]')
plt.suptitle('$\mathregular{<t_{0}>}=' + '{0:.1f}'.format(mean_t0) + '$ +- ' + '{0:.1f}'.format(std_t0) + ' ns')
plt.hist(t0, bins=30)
plt.savefig('plots/eps/' + tag + '_t0.eps', format='eps')
