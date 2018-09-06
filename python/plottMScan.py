from importAll import *

cmdargs = str(sys.argv)

inFileName      = str(sys.argv[1])
tag             = str(sys.argv[2])

t0      = np.loadtxt(inFileName, usecols=1)*1000
tS      = np.loadtxt(inFileName, usecols=3)
tm      = np.loadtxt(inFileName, usecols=5)
fom     = np.loadtxt(inFileName, usecols=9)
xe      = np.loadtxt(inFileName, usecols=11)
width   = np.loadtxt(inFileName, usecols=13)
ce      = np.loadtxt(inFileName, usecols=15)

plt.figure(1)
plt.plot(tm, t0, 'rx')
plt.xlabel('$\mathregular{t_{M}}$ [$\mathregular{\mu}$s]')
plt.ylabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '_t0_vs_tM.eps', format='eps')
plt.savefig('plots/png/' + tag + '_t0_vs_tM.png', format='png')
plt.close()

plt.figure(2)
plt.plot(tm, xe, 'rx')
plt.xlabel('$\mathregular{t_{M}}$ [$\mathregular{\mu}$s]')
plt.ylabel('$\mathregular{x_{e}}$ [mm]')
plt.savefig('plots/eps/' + tag + '_xe_vs_tM.eps', format='eps')
plt.savefig('plots/png/' + tag + '_xe_vs_tM.png', format='png')
plt.close()

plt.figure(3)
plt.plot(tm, width, 'rx')
plt.xlabel('$\mathregular{t_{M}}$ [$\mathregular{\mu}$s]')
plt.ylabel('width [mm]')
plt.savefig('plots/eps/' + tag + '_width_vs_tM.eps', format='eps')
plt.savefig('plots/png/' + tag + '_width_vs_tM.png', format='png')
plt.close()

plt.figure(4)
plt.plot(tm, ce, 'rx')
plt.xlabel('$\mathregular{t_{M}}$ [$\mathregular{\mu}$s]')
plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
plt.savefig('plots/eps/' + tag + '_ce_vs_tM.eps', format='eps')
plt.savefig('plots/png/' + tag + '_ce_vs_tM.png', format='png')
plt.close()

plt.figure(5)
plt.plot(tm, fom, 'rx')
plt.xlabel('$\mathregular{t_{M}}$ [$\mathregular{\mu}$s]')
plt.ylabel('F.O.M.')
plt.savefig('plots/eps/' + tag + '_fom_vs_tM.eps', format='eps')
plt.savefig('plots/png/' + tag + '_fom_vs_tM.png', format='png')
plt.close()
