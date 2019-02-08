# For the fourier computation

import math
import constants
import numpy as np

def calc_cosine_dist(t0, cosine, binContent, binCenter):
    for i in range(0, constants.nFreq):
        frequency   = ( constants.lowerFreq/1000 + constants.freqStep/1000/2) + i*constants.freqStep/1000 # in MHz
        integral    = binContent*np.cos(2*math.pi*frequency*(binCenter-t0))*0.001 # time hist in micro-sec
        cosine.SetBinContent(i+1, (np.sum(integral)))

def calc_sine_dist(t0, sine, binContent, binCenter):
    for i in range(0, constants.nFreq):
        frequency   = ( constants.lowerFreq/1000 + constants.freqStep/1000/2) + i*constants.freqStep/1000 # in MHz
        integral    = binContent*np.sin(2*math.pi*frequency*(binCenter-t0))*constants.freqStep/1000
        sine.SetBinContent(i+1, (np.sum(integral)))

def calc_parabola_dist(t0, tS, firstApprox, parabola):
    for i in range(0, constants.nFreq):
        frq = ( constants.lowerFreq + constants.freqStep/2) + i*constants.freqStep # in MHz
        integral = 0
        for j in range(1, constants.nFreq+1):
            if (firstApprox.GetBinCenter(j)-frq) != 0:
                integral += firstApprox.GetBinContent(j)*np.sin(2*math.pi*(frq-firstApprox.GetBinCenter(j))*(tS-t0)/1000)/(1000*(frq-firstApprox.GetBinCenter(j))  )
            else:
                integral += 2*math.pi*firstApprox.GetBinContent(j)*(tS-t0)/1000000
        parabola.SetBinContent(i+1,integral)

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
    m, c = np.linalg.lstsq(A, y,rcond=None)[0]

    return m, c
