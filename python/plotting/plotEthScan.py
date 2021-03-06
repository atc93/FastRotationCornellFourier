from importAll import *

cmdargs = str(sys.argv)

inFileName      = str(sys.argv[1])
tag             = str(sys.argv[2])

eth     = np.loadtxt(inFileName, usecols=1)
t0      = np.loadtxt(inFileName, usecols=3)*1000
tS      = np.loadtxt(inFileName, usecols=5)
tm      = np.loadtxt(inFileName, usecols=7)
fom     = np.loadtxt(inFileName, usecols=11)
xe      = np.loadtxt(inFileName, usecols=13)
width   = np.loadtxt(inFileName, usecols=15)
ce      = np.loadtxt(inFileName, usecols=17)

plt.figure(1)
plt.plot(eth, t0, 'rx')
plt.xlabel('$\mathregular{E_{th}}$ [MeV]')
plt.ylabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '_t0_vs_tS.eps', format='eps')
plt.savefig('plots/png/' + tag + '_t0_vs_tS.png', format='png')
plt.close()

plt.figure(2)
plt.plot(eth, xe, 'rx')
plt.xlabel('$\mathregular{E_{th}}$ [MeV]')
plt.ylabel('$\mathregular{x_{e}}$ [mm]')
plt.savefig('plots/eps/' + tag + '_xe_vs_tS.eps', format='eps')
plt.savefig('plots/png/' + tag + '_xe_vs_tS.png', format='png')
plt.close()

plt.figure(3)
plt.plot(eth, width, 'rx')
plt.xlabel('$\mathregular{E_{th}}$ [MeV]')
plt.ylabel('width [mm]')
plt.savefig('plots/eps/' + tag + '_width_vs_tS.eps', format='eps')
plt.savefig('plots/png/' + tag + '_width_vs_tS.png', format='png')
plt.close()

plt.figure(4)
plt.plot(eth, ce, 'rx')
plt.xlabel('$\mathregular{E_{th}}$ [MeV]')
plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
plt.savefig('plots/eps/' + tag + '_ce_vs_tS.eps', format='eps')
plt.savefig('plots/png/' + tag + '_ce_vs_tS.png', format='png')
plt.close()

plt.figure(5)
plt.plot(eth, fom, 'rx')
plt.xlabel('$\mathregular{E_{th}}$ [MeV]')
plt.ylabel('F.O.M.')
plt.savefig('plots/eps/' + tag + '_fom_vs_tS.eps', format='eps')
plt.savefig('plots/png/' + tag + '_fom_vs_tS.png', format='png')
plt.close()
