from importAll import *

cmdargs = str(sys.argv)

inFileName      = str(sys.argv[1])
outFileName     = str(sys.argv[2])

text_file = open(str(outFileName), "w")

radius      = np.empty( 149, dtype=float )
intensity   = np.empty( 149, dtype=float )

for i in range(1, 150):
    radius[i-1] = np.average( np.loadtxt(inFileName, usecols=(2*(i-1))), axis=0)
    intensity[i-1] = np.average( np.loadtxt(inFileName, usecols=(2*(i-1)+1)), axis=0)

#for i in range(0, 149):
#    print radius[i], intensity[i]

plt.plot(radius, intensity, 'ro--')   
plt.savefig('test.eps')
