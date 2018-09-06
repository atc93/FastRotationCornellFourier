# coding: utf-8

## Module imports

from importAll import *

## Get command line argumentS

cmdargs = str(sys.argv)

inputRootFile   = str(sys.argv[1])
outputRootFile  = str(sys.argv[2])
histoName       = str(sys.argv[3])
rebinFactor     = int(sys.argv[4])
tS              = int(sys.argv[5]) # in mico-sec
tM              = int(sys.argv[6]) # in mico-sec
startFitTime    = int(sys.argv[7]) # in mico-sec
endFitTime      = int(sys.argv[8]) # in mico-sec
printPlot       = int(sys.argv[9])
saveROOT        = int(sys.argv[10])
tag             = str(sys.argv[11])
statFluc        = int(sys.argv[12])
dataType        = str(sys.argv[13])

print ''
print ' =================================='
print ' == Produce Fast Rotation signal =='
print ' =================================='
print ''


## Retrieve and plot histogram from ROOT file

inFile      = r.TFile( inputRootFile)
outFile     = r.TFile(outputRootFile,'RECREATE')

signal  = inFile.Get( histoName )

## If MC, do nothing
if ( dataType == "mc"):
    outFile.cd()
    signal.Write("fr")
    print '  doing nothing because MC\n'
    sys.exit(0)

## Allow statistical fluctuaion

if ( statFluc == 1 ):
    signal = statFluctuationPoisson( signal )

## Styling and plotting

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )
setHistogramStyle( signal, '', 'Time [#mus]', 'Intensity')

signal.Write()

times = [1,10,50, 100, tM]

if ( printPlot == 1 ):
    for time in times:
        plot( c, signal, tag+'/Intensity', tS, tS+time )

## Rebin, fit and plot wiggle plot

fr = signal.Clone()
signal.Rebin(rebinFactor)

#fit = r.TF1("fit","[0] * (1+exp(-x/[5])*(1+[6]*cos(2*TMath::Pi()*[7]*x+[8]))) * exp(-x/[1])*(1+[2]*cos(2*TMath::Pi()*[3]*x+[4]))", startFitTime, endFitTime)
#fit.SetParameters( signal.GetBinContent( signal.FindBin(startFitTime) )*1.3, 64.4, 0.4, 0.227, 1, 150, 0.002, 0.370, 1)
fit = r.TF1("fit","[0] * exp(-x/[1])*(1+[2]*cos(2*TMath::Pi()*[3]*x+[4]))", startFitTime, endFitTime)
fit.SetParameters( signal.GetBinContent( signal.FindBin(startFitTime) )*1.3, 64.4, 0.4, 0.227)
fit.SetParLimits(1, 64, 65)
#fit.SetParLimits(5, 140, 160)
#fit.SetParLimits(6, 0, 0.01)
#fit.SetParLimits(7, 0.3, 0.4)
#fit.SetParLimits(8, 0, 7)
fit.SetNpx(10000)
signal.Fit("fit","SREMQ")
print 'N0', fit.GetParameter(0)
print 'Tau_m', fit.GetParameter(1)
print 'A', fit.GetParameter(2)
print 'omega_a', fit.GetParameter(3)
print 'Phi', fit.GetParameter(4)
#print 'Tau_cbo', fit.GetParameter(5)
#print 'A_cbo', fit.GetParameter(6)
#print 'omega_cbo', fit.GetParameter(7)
#print 'Phi_cbo', fit.GetParameter(8)

if ( printPlot == 1 ):
    for time in times:
        plot( c, signal, tag + '/FittedWiggle', startFitTime, startFitTime+time )
    plot( c, signal, tag + '/FittedWiggle', endFitTime-200, endFitTime )
    plot( c, signal, tag + '/FittedWiggle', endFitTime-100, endFitTime )


## Produce finely binned and normalized wiggle plot to original intensity histogram

nBins = fr.GetXaxis().GetNbins()
norm = r.TH1D("norm","norm",nBins,0, fr.GetBinCenter( nBins ) + 0.5*fr.GetBinWidth(1) )
norm.SetLineColor(4)
setHistogramStyle( norm, '', 'Time [#mus]', 'Intensity')

for i in range(nBins):
    norm.SetBinContent(i,fit.Eval(norm.GetBinCenter(i))/rebinFactor)
    
if ( printPlot == 1 ):
    for time in times:
        plot( c, norm, tag + '/WiggleFRS', tS, tS+time )

norm.Write("wiggleHistogram")


## Generate FRS (correct original histogram by wiggle fit)

fr.Divide(norm)
fr.Write("fr")

## Print and save FRS histogram

if ( printPlot == 1 ):
    for time in times:
        plot( c, fr, tag+'/FRS', tS, tS+time )

## Close output ROOT file

outFile.Close()
