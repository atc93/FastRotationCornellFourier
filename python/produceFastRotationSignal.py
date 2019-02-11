#== Module imports ==#

import sys
import ROOT as r
import imports.style as style
import imports.plotting as plotting
import imports.statFluctutation as statFluctuation

#== Parse command line arguments ==#

cmdargs = str(sys.argv)

inputRootFile   = str   (sys.argv[1])
outputRootFile  = str   (sys.argv[2])
histoName       = str   (sys.argv[3])
rebinFactor     = int   (sys.argv[4])
tS              = float (sys.argv[5]) # in mico-sec
tM              = float (sys.argv[6]) # in mico-sec
startFitTime    = int   (sys.argv[7]) # in mico-sec
endFitTime      = int   (sys.argv[8]) # in mico-sec
printPlot       = int   (sys.argv[9])
saveROOT        = int   (sys.argv[10])
tag             = str   (sys.argv[11])
statFluc        = int   (sys.argv[12])
dataType        = str   (sys.argv[13])
nFitParam       = int   (sys.argv[14])
produceFRS      = int   (sys.argv[15])

print ''
print ' =================================='
print ' == Produce Fast Rotation signal =='
print ' =================================='
print ''

#== Retrieve histogram from input ROOT file ==#

inFile  = r.TFile( inputRootFile )
rawHist = inFile.Get( histoName )

#== Create ROOT file to save outputs ==#

outFile = r.TFile( outputRootFile, 'RECREATE' )

#== Apply styles to histograms and canvas ==#

c = r.TCanvas('c','c',900,600)

style.setCanvasStyle( c )
style.setHistogramStyle( rawHist, '', 'Time [#mus]', 'Intensity')

#== Allow or not statistical fluctuation of raw histogram ==#

if ( statFluc == 1 ):
    rawHist = statFluctuation.poisson( rawHist )

rawHist.Write()

#== Plot and save raw Intensity v. Time plot ==#

times = [1,10,50, 100, 150, 200, 250, tM]

##== If signal already is the Fast Rotation signal, plot it and exit code ==##

if ( produceFRS != 1 ):
    outFile.cd()
    rawHist.Write("fr")
    if ( printPlot == 1 ):
        for time in times:
            plotting.plot( c, rawHist, tag+'/FRS', tS, tS+time )
    print '\n--> Exting, Fast Rotation signal indicated by user to already exist\n'
    sys.exit(0)


##== Otherwise continue and produce Fast Rotation signal ==##

if ( printPlot == 1 ):
    for time in times:
        plotting.plot( c, rawHist, tag+'/Intensity', tS, tS+time )

#== Clone raw histogram to produce wiggle plot ==#

cloneHist = rawHist.Clone()
cloneHist.Rebin(rebinFactor)

#== 5-parameter wiggle fit ==#

if ( nFitParam >= 5 ):

    fiveParamFit  = r.TF1("fiveParamFit",  "[0]*exp(-x/[1]) *( 1 + [2]*cos(2*TMath::Pi()*[3]*x) + [4]*sin(2*TMath::Pi()*[3]*x) )", startFitTime, endFitTime)
    fiveParamFit.SetLineColor(4)
    fiveParamFit.SetParameters( cloneHist.GetBinContent( cloneHist.FindBin(startFitTime) )*1.3, 64.4, -0.1, 0.229, -0.1)

    wiggleFit = fiveParamFit
    cloneHist.Fit("fiveParamFit","REMQ")
    
    print '\n=== 5-parameter fit ===\n'
    print 'N0       ',   fiveParamFit.GetParameter(0)
    print 'Tau_m    ',   fiveParamFit.GetParameter(1)
    print 'Acos     ',   fiveParamFit.GetParameter(2)
    print 'Asin     ',   fiveParamFit.GetParameter(4)
    print 'Omega_a  ',   fiveParamFit.GetParameter(3)
    print ''

#== 5-parameter + CBO wiggle fit ==#

if ( nFitParam >= 9 ):
    cboFit          = r.TF1("cbo",      "1+exp(-x/[0])*([1]*cos(2*TMath::Pi()*[2]*x)+[3]*sin(2*TMath::Pi()*[2]*x))", startFitTime, endFitTime)
    nineParamFit    = r.TF1("nineParamFit", "fiveParamFit*cbo", startFitTime, endFitTime)

    ##== 5-parameter fit ==#
    nineParamFit.SetParameter( 0, fiveParamFit.GetParameter(0) )
    nineParamFit.SetParameter( 1, fiveParamFit.GetParameter(1) )
    nineParamFit.SetParameter( 2, fiveParamFit.GetParameter(2) )
    nineParamFit.SetParameter( 3, fiveParamFit.GetParameter(3) )
    nineParamFit.SetParameter( 4, fiveParamFit.GetParameter(4) )

    ##== CBO fit ==#
    nineParamFit.SetParameter( 5, 150 )
    nineParamFit.SetParameter( 6, 0.004 )
    nineParamFit.SetParameter( 7, 0.370 )
    nineParamFit.SetParameter( 8, 0.004 )
    nineParamFit.SetNpx(10000)

    wiggleFit = nineParamFit
    cloneHist.Fit("nineParamFit","REMQ")

    print '\n=== 9-parameter fit ===\n'
    print 'N0       ',   nineParamFit.GetParameter(0)
    print 'Tau_m    ',   nineParamFit.GetParameter(1)
    print 'Acos     ',   nineParamFit.GetParameter(2)
    print 'Asin     ',   nineParamFit.GetParameter(4)
    print 'Omega_a  ',   nineParamFit.GetParameter(3)
    print 'Tau_cbo  ',   nineParamFit.GetParameter(5)
    print 'Acos_cbo ',   nineParamFit.GetParameter(6)
    print 'Asin_cbo ',   nineParamFit.GetParameter(8)
    print 'Omega_cbo',   nineParamFit.GetParameter(7)
    print ''


#== Plot and save wiggle plot ==#

if ( printPlot == 1 ):
    for time in times:
        plotting.plot( c, cloneHist, tag + '/FittedWiggle', startFitTime, startFitTime+time )
    plotting.plot( c, cloneHist, tag + '/FittedWiggle', endFitTime-200, endFitTime )
    plotting.plot( c, cloneHist, tag + '/FittedWiggle', endFitTime-100, endFitTime )

#== Produce histogram of fit residuals ==#

residual = cloneHist.Clone()
residual.Reset()
residual.GetYaxis().SetTitle('Residual [%]')

for i in range(1, cloneHist.GetNbinsX()):
    if ( cloneHist.GetBinContent(i) != 0 ):
        residual.SetBinContent( i, (cloneHist.GetBinContent(i)-wiggleFit.Eval(cloneHist.GetBinCenter(i)))/cloneHist.GetBinContent(i)*100)

#== Plot histogram of fit residuals ==#

if ( printPlot == 1 ):
    for time in times:
        plotting.plot( c, residual, tag + '/FitResidual', startFitTime, startFitTime+time)    
        plotting.plot( c, residual, tag + '/FitResidual', tS, tS+time)    

#== Produce finnely binned wiggle plot normalized to raw intensity histogram ==#

nBins = rawHist.GetXaxis().GetNbins()
norm = r.TH1D( "norm", "norm", nBins, 0, rawHist.GetBinCenter( nBins ) + 0.5*rawHist.GetBinWidth(1) )
style.setHistogramStyle( norm, '', 'Time [#mus]', 'Intensity')

for i in range(nBins):
    norm.SetBinContent( i, wiggleFit.Eval( norm.GetBinCenter(i) ) / rebinFactor )
    
if ( printPlot == 1 ):
    for time in times:
        plotting.plot( c, norm, tag + '/WiggleFRS', tS, tS+time )
        plotting.plot( c, residual, tag + '/FitResidual', startFitTime, startFitTime+time)    
        plotting.plot( c, residual, tag + '/FitResidual', tS, tS+time)    

norm.Write("wiggleHistogram")


#== Produce Fast Rotation signal (correct raw histogram from wiggle fit) ==#

rawHist.Divide(norm)
rawHist.Write("fr")

#== Print and save FRS histogram ==#

if ( printPlot == 1 ):
    for time in times:
        plotting.plot( c, rawHist, tag+'/FRS', tS, tS+time )

#== Close output ROOT file ==#

inFile.Close()
outFile.Close()
