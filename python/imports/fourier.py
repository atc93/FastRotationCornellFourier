#==============================================================#
#== IMPORT FILE CONTAINING THE MATH FOR THE FOURIER ANALYSIS ==#
#==============================================================#

import math
import numpy as np
import imports.constants as constants

#== Extract the two minima of the Cosine Fourier transform ==#
def extractMinima( hist ):
    hist.GetXaxis().SetRangeUser( constants.lowerFreq, constants.magicFreq )
    min1 = hist.GetMinimum()
    minBinIdx1 = hist.GetMinimumBin()
    hist.GetXaxis().SetRangeUser( constants.magicFreq, constants.upperFreq )
    min2 = hist.GetMinimum()
    minBinIdx2 = hist.GetMinimumBin()
    hist.GetXaxis().SetRangeUser( constants.lowerFreq, constants.upperFreq )
    return min1, min2, abs( min1-min2 ), minBinIdx1, minBinIdx2

#== Compute the Cosine Fourier transform ==#
def calcCosineTransform(t0, cosine, binContent, binCenter):
    for i in range(0, constants.nFreq):
        frequency   = ( constants.lowerFreq/1000 + constants.freqStep/1000/2) + i*constants.freqStep/1000 # in MHz
        integral    = binContent*np.cos(2*math.pi*frequency*(binCenter-t0))*0.001 # time hist in micro-sec
        cosine.SetBinContent(i+1, (np.sum(integral)))

#== Compute the Sine Fourier transform ==#
def calcSineTransform(t0, sine, binContent, binCenter):
    for i in range(0, constants.nFreq):
        frequency   = ( constants.lowerFreq/1000 + constants.freqStep/1000/2) + i*constants.freqStep/1000 # in MHz
        integral    = binContent*np.sin(2*math.pi*frequency*(binCenter-t0))*constants.freqStep/1000
        sine.SetBinContent(i+1, (np.sum(integral)))

#== Compute the Parabola correction distribution ==#
def calcParabola(t0, tS, firstApprox, parabola):
    for i in range(0, constants.nFreq):
        frq = ( constants.lowerFreq + constants.freqStep/2) + i*constants.freqStep # in MHz
        integral = 0
        for j in range(1, constants.nFreq+1):
            if (firstApprox.GetBinCenter(j)-frq) != 0:
                integral += firstApprox.GetBinContent(j)*np.sin(2*math.pi*(frq-firstApprox.GetBinCenter(j))*(tS-t0)/1000)/(1000*(frq-firstApprox.GetBinCenter(j))  )
            else:
                integral += 2*math.pi*firstApprox.GetBinContent(j)*(tS-t0)/1000000
        parabola.SetBinContent(i+1,integral)

#== Perform the background minimization ==#
def minimization(parabola, cosine):

    x = []
    y = []

    for i in range(1, constants.nFreq+1):
        if ( cosine.GetBinCenter(i) < constants.lowerCollimatorFreq or cosine.GetBinCenter(i) > constants.upperCollimatorFreq ):
            x.append(parabola.GetBinContent(i))
            y.append(cosine.GetBinContent(i))
            x.append(parabola.GetBinContent(i))
            y.append(cosine.GetBinContent(i))

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y,rcond=-1)[0]

    return m, c

#== Convert Frequency to Radius ==#
#== Assume velocity corresponding to magic momentum for all the muons. Velocity depends very little on momentum ==#
def convertFreqToRadius( freqHist, radius, intensity ):
    for i in range( 1, constants.nFreq+1 ):
        radius.append   ( constants.speedOfLight * constants.magicBeta / ( 2*math.pi*freqHist.GetBinCenter(i) ) )
        intensity.append( freqHist.GetBinContent(i))

