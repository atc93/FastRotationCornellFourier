#================================================#
#== IMPORT FILE CONTAINING UTILITARY FUNCTIONS ==#
#================================================#

import math
import numpy as np
import imports.constants as constants

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

#== Compute Standard Deviation of an array ==#
def computeRadialSTD( radius, intensity, meanRad ):

    std  = 0
    sumI = 0

    for x,y in zip( radius, intensity ):
        
        #== Discard data point if radius outside of collimator aperture ==#
        if ( x < constants.lowerCollimatorRad or x > constants.upperCollimatorRad ):
            continue

        #== Else compute the STD ==#
        sumI += y
        std  += y * ( x-meanRad ) * ( x-meanRad )

    std /= sumI
    std = math.sqrt(std) 

    return std

#== Compute the E-field correction ==#

def computeEfieldCorrection( n, mean, std ):

    return ( - 2* math.pow( constants.magicBeta, 2 ) * n * ( 1-n ) * ( math.pow ( mean, 2 ) + math.pow ( std, 2 ) ) / ( math.pow ( constants.magicR, 2 ) )* 1e9 )
