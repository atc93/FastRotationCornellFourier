#== Module imports ==#

import sys
import math
import array
import ROOT as r
import numpy as np
import imports.util as util
import imports.style as style
import imports.fourier as fourier
import imports.plotting as plotting
import imports.constants as constants

#== Parse command line arguments ==#

cmdargs = str(sys.argv)

inputRootFile   = str   (sys.argv[1])
outputRootFile  = str   (sys.argv[2])
outputTextFile  = str   (sys.argv[3])
histoName       = str   (sys.argv[4])
t0              = float (sys.argv[5]) # in mico-sec
tS              = float (sys.argv[6]) # in mico-sec
tM              = float (sys.argv[7]) # in mico-sec
fieldIndex      = float (sys.argv[8])
printPlot       = int   (sys.argv[9])
saveROOT        = int   (sys.argv[10])
tag             = str   (sys.argv[11])
updateTextFile  = int   (sys.argv[12])
runSine         = int   (sys.argv[13])
outputDistFile  = str   (sys.argv[14])
dataType        = str   (sys.argv[15])
compareWithTruth= int   (sys.argv[16])
truthFileName   = str   (sys.argv[17])

print ( '')
print ( ' ==============================' )
print ( ' == Fourier analysis routine ==' )
print ( ' ==============================' )
print ( '    t0 = ', t0 )
print ( '    tS = ', tS )
print ( '    tM = ', tM )
print ( '    n  = ', fieldIndex )
print ( ' ==============================' )
print ( '' )

#== Retrieve histogram from input ROOT file ==#

inFile = r.TFile( inputRootFile )
frHist = inFile.Get( histoName )

#== Apply styles to histograms and canvas ==#

c = r.TCanvas( 'c', 'c', 900, 600 )

style.setTCanvasStyle( c )
style.setTH1Style( frHist, '', 'Time [#mus]', 'Intensity [a.u.]')

#== Copy ROOT histogram to numpy array ==#
binCenter, binContent = util.rootHistToNumpArray( frHist, tS, tM ) # tS and tM provide the histogram range to copy

#== Define ROOT histograms for Cosine and Sine Fourier transforms ==#
cosine  = r.TH1D( "cosine", "cosine", constants.nFreq, constants.lowerFreq, constants.upperFreq )
sine    = r.TH1D( "sine",   "sine",   constants.nFreq, constants.lowerFreq, constants.upperFreq )



#==========================================#
#== FIRST STEP: PERFORM COSINE TRANSFORM ==#
#==========================================#

#== Perform Cosine Fourier transform ==#
fourier.calcCosineTransform( t0, cosine, binContent, binCenter )

#== Perform Sine Fourier transform ==#
if ( runSine == 1 ):
    calcSineTransform( t0, sine, binContent, binCenter )

#== Define histogram names ==#
histoName = [ 'Cosine transform: t_{0} = ' + '{0:.2f} ns'.format(t0*1000), 'Sine transform: t_{0} = ' + '{0:.2f} ns'.format(t0) ]

#== Clone cosine histogram for plotting/styling puporses ==#
cosineClone = cosine.Clone()

#== Clone sine histogram for plotting/styling puporses ==#
sineClone = sine.Clone()

#== Create a list containing both Cosine and Sine histograms ==#
cloneHistList = [ cosineClone, sineClone ]

#== Styling and Plotting for Cosine and Sine Fourier transform ==#
for idx in range ( 0, 2 ):

    #== Style the Fourier transform histogram ==#
    style.setTH1Style( cloneHistList[ idx ], histoName[ idx ], 'Frequency [kHz]', 'Arbitrary', 1.2, 1.3 )

    #== Define lines to be drawn at collimator apertures (frequency space) ==#
    innerLine, outerLine = style.setCollimatorApertureTLine ( cloneHistList[ idx ].GetMinimum(), cloneHistList[ idx ].GetMaximum(), 'frequency' )

    #== Define pave text to go along the collimator apertures lines ==#
    pt, pt2 = style.setCollimatorAperturePaveText( cloneHistList[ idx ].GetMaximum()*0.38, cloneHistList[ idx ].GetMaximum()*0.52, 'frequency' )

    #== Draw it all ==#
    listToDraw = [ cloneHistList[ idx ], innerLine, outerLine, pt, pt2 ]
    plotting.plotMultipleObjects( '', listToDraw )
    c.Draw()

    #== Save plot if option provided ==#
    if ( idx == 0 and printPlot == 1 ):
        c.Print('plots/eps/'+ tag + '/Cosine_t0_{0:.3f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))
        c.Print('plots/eps/'+ tag + '/Cosine_t0Optimization_tS_{0}_tM_{1}.gif+5'.format(tS, tM))

    #== Save plot if option provided and if sine transform was performed ==#
    if ( idx == 1 and printPlot == 1 and runSine == 1 ):
        c.Print('plots/eps/' + tag + '/Sine_t0_{0:.3f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))



#============================================================#
#== SECOND STEP: BUILD APPROXIMATED FREQUENCY DISTRIBUTION ==#
#============================================================#

approx = cosine.Clone()

#== Extract minima of Cosine Transform distribution ==#
min1, min2, fom, minBinIdx1, minBinIdx2 = fourier.extractMinima( cosine )

minA =  (approx.GetBinContent(minBinIdx1) + approx.GetBinContent(minBinIdx2)) / 2

for iBin in range(1, minBinIdx1):
    approx.SetBinContent(iBin, 0)
    
for iBin in range(minBinIdx2+1, constants.nFreq+1):
    approx.SetBinContent(iBin, 0)    
    
approx.GetXaxis().SetRangeUser(constants.lowerFreq, constants.upperFreq)    

for iBin in range(minBinIdx1, minBinIdx2+1):
    approx.AddBinContent(iBin, -1*minA)

#== Style the approximated frequency distribution histogram ==#
style.setTH1Style( approx, 'Approximation', 'Frequency [kHz]', 'Arbitrary units', 1, 1.3 )    
approx.SetMinimum( -0.5 ) 

#== Define lines to be drawn at collimator apertures (frequency space) ==#
innerLine, outerLine = style.setCollimatorApertureTLine ( approx.GetMinimum(), approx.GetMaximum(), 'frequency' )
#== Define pave text to go along the collimator apertures lines ==#
pt, pt2 = style.setCollimatorAperturePaveText( approx.GetMaximum()*0.38, approx.GetMaximum()*0.52, 'frequency' )

#== Draw it all ==#
listToDraw = [ approx, innerLine, outerLine, pt, pt2 ]
plotting.plotMultipleObjects( '', listToDraw )
c.Draw()

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Approximation_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))



#=============================================#
#== THIRD STEP: COMPUTE PARABOLA CORRECTION ==#
#=============================================#

# Correction
parabola = cosine.Clone()
parabola.Scale(0)

#==  Calculcate parabola correction to the approximated frequency distribution ==#
fourier.calcParabola( t0, tS, approx, parabola )

parabola.Draw()
parabola.SetTitle("Parabola")
c.Update()
c.Draw()


#== Optimize the scale (a) and offset (b) parameter of the parabola to minimize ==#
#== non physical frequencies in the complete frequency distribution ==#
a, b = fourier.minimization( parabola, cosine )

#== Scale and offset the parabola using optimized a and b parameters ==#
for iBin in range( 1, constants.nFreq+1 ):
    parabola.SetBinContent( iBin, -1*( a*parabola.GetBinContent(iBin)+b) )
    
#== Clone parabola histogram for plotting/styling puporses ==#
parabolaClone = parabola.Clone()

#== Style the Parabola transform histogram ==#
style.setTH1Style( parabolaClone, 'Parabola correction', 'Frequency [kHz]', 'Arbitrary units', 0.85, 1.15 )    

#== Define lines to be drawn at collimator apertures (frequency space) ==#
innerLine, outerLine = style.setCollimatorApertureTLine ( parabolaClone.GetMinimum(), parabolaClone.GetMaximum(), 'frequency' )

#== Define pave text to go along the collimator apertures lines ==#
pt, pt2 = style.setCollimatorAperturePaveText( parabolaClone.GetMaximum()*0.38, parabolaClone.GetMaximum()*0.52, 'frequency' )
    
#== Draw it all ==#
listToDraw = [ parabolaClone, innerLine, outerLine, pt, pt2 ]
plotting.plotMultipleObjects( '', listToDraw )
c.Draw()   

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Parabola_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    



#==============================================================#
#== FOURTH STEP: PRODUCE THE COMPLETE FREQUENCY DISTRIBUTION ==#
#==============================================================#


completeFreqDistHist = cosine.Clone()
for iBin in range(1,constants.nFreq+1):
    completeFreqDistHist.AddBinContent( iBin, parabola.GetBinContent(iBin) )

#== Style the Parabola transform histogram ==#
style.setTH1Style( completeFreqDistHist, 'Complete distribution', 'Frequency [kHz]', 'Arbitrary units', 1, 1.15 )    
completeFreqDistHist.SetMinimum( -0.5 ) 

#== Define lines to be drawn at collimator apertures (frequency space) ==#
innerLine, outerLine = style.setCollimatorApertureTLine ( completeFreqDistHist.GetMinimum(), completeFreqDistHist.GetMaximum(), 'frequency' )

#== Define pave text to go along the collimator apertures lines ==#
pt, pt2 = style.setCollimatorAperturePaveText( completeFreqDistHist.GetMaximum()*0.38, completeFreqDistHist.GetMaximum()*0.52, 'frequency' )

#== Draw it all ==#
listToDraw = [ completeFreqDistHist, innerLine, outerLine, pt, pt2, ]
plotting.plotMultipleObjects( '', listToDraw )

#== Compare radial and frequency distribution with truth level ones (if simulated data) ==#
if ( compareWithTruth == 1 ):

    #== Normalize the integral of the frequency distribution to 1 ==#
    completeFreqDistHist.Scale( 1/completeFreqDistHist.Integral() )

    #== Retrieve the truth level frequency distribution ==#
    truthFile = r.TFile( truthFileName )
    truth = truthFile.Get( "freq" )

    #== Rebin the truth level distribution if needed ==#
    if ( constants.freqStep > truth.GetBinWidth(1) ):
        truth.Rebin( int( constants.freqStep / truth.GetBinWidth(1) ) )

    #== Normalize the integral of the frequency distribution to 1 ==#
    truth.Scale( 1/truth.Integral() )

    #== Restyle the reconstructed level frequency distribution ==#
    style.setTH1Style( completeFreqDistHist, 'Truth/Reconstructed levels comparison', 'Frequency [kHz]', 'Arbitrary units' )

    #== Limit the a-axis to the collimator aperture ==#
    completeFreqDistHist.GetXaxis().SetRangeUser( constants.lowerCollimatorFreq, constants.upperCollimatorFreq )

    #== Draw reconstructed level distribution ==#
    completeFreqDistHist.Draw("hist")

    #== Style the truth level distribution ==#
    truth.SetMarkerColor(2)
    truth.SetLineColor(2)
    truth.SetLineStyle(1)
    truth.SetLineWidth(1)
    truth.SetMarkerStyle(20)
    truth.SetMarkerSize(1.15)

    #== Draw the markers of the truth level distribution ==#
    truth.Draw("samehistP0")

    #== Draw the line of the truth level distribution ==#
    truth.Draw("samehist")

    #== Define pave text to go display truth/reco level mean frequencies ==#
    pt = style.setRecTruthFrequenciesPaveText( completeFreqDistHist.GetMean(), truth.GetMean(), 
            completeFreqDistHist.GetMaximum()*1., completeFreqDistHist.GetMaximum()*0.8 )

    #== Draw the TPaveText ==#
    pt.Draw("same") 

#== Draw TCanvas ==#
c.Draw()   

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/CompleteDistribution_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    
    c.Print('plots/eps/' + tag + '/CompleteDistribution_t0_{0:.5f}_tS_{1}_tM_{2}.C'.format(t0, tS, tM))    


#=================================================#
#== FIFTH STEP: PRODUCE THE RADIAL DISTRIBUTION ==#
#=================================================#

#== Define arrays containing radius and intensity information ==#
#== The array will be used to produce a TGraph (required since non equidistance radial points) ==#
intensity, radius = array.array( 'd' ), array.array( 'd' )

#== Fill radius and intensity arrays from the frequency distribution ==#
fourier.convertFreqToRadius( completeFreqDistHist, radius, intensity )

#== Extract equilibirum radius (average radius) ==#
eqRadius = util.computeRadialMean( radius, intensity )   

#== Extract maximum intensity for normalization purpose ==#
maxIntensity = np.amax(intensity)

#== Normalize intensity to 1 ==#
intensity /= maxIntensity

#== Create TGraph to store radial distribution ==#
graph    = r.TGraph( constants.nFreq, radius,intensity )
graphMin = -0.05
graphMax = 1.05
style.setTGraphStyle( graph, '', 'Radius [mm]', 'Arbitrary units', graphMin, graphMax )

#== Save TGraph to a ROOT file if option specified ==#
if ( saveROOT == 1 ):
    outFile = r.TFile( outputRootFile, "RECREATE" )
    graph.Write("rad")
    outFile.Close()

#== Define lines to be drawn at collimator apertures (frequency space) ==#
innerLine, outerLine = style.setCollimatorApertureTLine( graphMin, graphMax, 'radial' )

#== Define pave text to go along the radial collimator apertures lines ==#
pt, pt2 = style.setCollimatorAperturePaveText( graphMax*0.45, graphMax*0.55, 'radial' )

#== Define line to be draw at the magic radius ==# 
magicLine = style.setMagicRadiusTLine( graphMin, graphMax)

#== Define pave text to go along the magic radius line ==# 
magicRadiusPaveText = style.setMagicRadiusPaveText( graphMax*0.04, graphMax*0.11 );

#== Compute Standard Deviation of the radial distribution (within the collimator aperture) ==#
std = util.computeRadialSTD( radius, intensity, eqRadius )

#== Convert radius to beam coordinate, i.e. 7112 mm corresponds to x = 0 ==#
eqRadius -= 7112

#== Compute E-field correction
CE = util.computeEfieldCorrection( fieldIndex, eqRadius, std )

#== Define pave text with x_e, width and CE information ==#
resultsPaveText = style.setRadialResultsPaveText( eqRadius, std, CE, graphMax*0.7, graphMax*0.96 )

#== Draw it all ==#
listToDraw = [ graph, magicLine, innerLine, outerLine, pt, pt2, magicRadiusPaveText, resultsPaveText ]
plotting.plotMultipleObjects( 'APL', listToDraw )

#== Extract truth radial information if running on MC data ==#
if ( compareWithTruth == 1 ):

    #== Open truth ROOT file
    truthFile = r.TFile( truthFileName )

    #== Retrieve truth radial TGraph
    truth = truthFile.Get( "r" )

    #== Normalize truth TGraph to 1 ==#
    nPoint = truth.GetN()
    maxA = max(truth.GetY())
    for i in range(1, nPoint):
        x, y = r.Double(), r.Double()
        truth.GetPoint(i, x, y)
        truth.SetPoint(i, x, y/maxA)

    #style.setTGraphStyle( truth, '', 'Radius [mm]', 'Arbitrary units' )
    truth.SetMarkerColor(4)
    truth.SetLineColor(4)
    truth.SetMarkerStyle(20)
    truth.Draw("sameP")

    #== Define truth array to compute x_e and width ==#
    truthIntensity, truthRadius = array.array( 'd' ), array.array( 'd' )

    for i in range(1, nPoint):
        x, y = r.Double(), r.Double()
        truth.GetPoint(i, x, y)
        truthRadius.append( x )
        truthIntensity.append( y )

    truthEqRadius = np.average( truthRadius, axis=0, weights=truthIntensity)
    truthSTD = util.computeRadialSTD( truthRadius, truthIntensity, truthEqRadius ) 

    pt5=r.TPaveText(7130, graphMax*0.7,7155, graphMax*0.96);
    pt5.AddText('Truth level');
    pt5.AddText('x_{e} = ' + '{0:.1f}'.format(truthEqRadius-7112) + ' mm');
    pt5.AddText(' #sigma = ' + '{0:.1f}'.format(truthSTD) + ' mm');
#    pt5.AddText('      C_{E} = ' + '{0:.1f}'.format(C_E_reco) + ' ppb ');
    pt5.SetShadowColor(0);
    pt5.SetBorderSize(1);
    pt5.SetFillColor(0);
    pt5.SetLineWidth(1);
    pt5.SetLineColor(4);
    pt5.SetTextColor(4);
    pt5.SetTextAngle(90);
    pt5.Draw("same")
    graph.Draw("sameP")

c.Draw()

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    
    c.Print('plots/eps/' + tag + '/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.C'.format(t0, tS, tM))    
    c.Print('plots/png/' + tag + '/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.png'.format(t0, tS, tM))    

print ( '' )
print (' =============' )
print (' == Results ==' )
print (' =============' )
print ( '' )

print ( 'Estimated average frequency: \t{0:.2f} kHz'.format( completeFreqDistHist.GetMean() ) )
print ( 'Estimated average radius: \t{0:.1f} mm'.format( eqRadius ) )
print ( 'Estimated width: \t\t{0:.1f} mm'.format( std ) )
print ( 'Estimated E-field correction \t{0:.0f} ppb'.format( CE ) )

#== Save radial distribution to a ROOT file ==#
outRootFile = r.TFile( 'plots/eps/' + tag + '/Results.root', "RECREATE")
graph.Write('radialDistribution')
outRootFile.Close()

#== Save various information to a text file ==#
##== Option to keep updating the file (useful for ensemble tests for instance) ==##
if ( updateTextFile == 1 ):
    text_file = open(str(outputTextFile), "a")
    textFileDist = open(str(outputDistFile), "a")
    for i, j in zip(radius, intensity):
        textFileDist.write('%f %f ' % (i, j) )
    textFileDist.write('\n')    
##== Or over-write previous file ==##    
else:
    text_file = open(str(outputTextFile), "w")

##== Write information to text file ==##
text_file.write('t0 %f tS %f tM %f fieldIndex %f fom %f eqRadius_reco %f std_reco %f C_E_reco %f \n' % 
        (t0, tS, tM, fieldIndex, fom, eqRadius, std, CE) )

##== Close text file ==##
text_file.close()
