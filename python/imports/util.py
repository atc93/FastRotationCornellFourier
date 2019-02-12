#================================================#
#== IMPORT FILE CONTAINING UTILITARY FUNCTIONS ==#
#================================================#

import numpy as np

#== Convert ROOT histogram to Numpy array ==#

def rootHistToNumpArray( hist, tS, tM ):

    startBin = hist.FindBin(tS)
    endBin   = hist.FindBin(tM)

    binCenter   = np.empty( int(endBin-startBin+1), dtype=float )
    binContent  = np.empty( int(endBin-startBin+1), dtype=float )

    for j in range(startBin, endBin):
            binContent[j-startBin]  = hist.GetBinContent(j)
            binCenter[j-startBin]   = hist.GetBinCenter(j)

    return binCenter, binContent            
