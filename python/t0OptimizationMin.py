#== Module imports ==#

import sys
import array
import ROOT as r
import numpy as np
import imports.style as style
import matplotlib.pyplot as plt
import imports.fourier as fourier
import imports.plotting as plotting
import imports.constants as constants

#== Parse command line arguments ==#

cmdargs = str(sys.argv)

inputRootFile   = str   (sys.argv[1])
outputRootFile  = str   (sys.argv[2])
outputTextFile  = str   (sys.argv[3])
histoName       = str   (sys.argv[4])
lowert0         = float (sys.argv[5]) # in mico-sec
uppert0         = float (sys.argv[6]) # in mico-sec
t0StepSize      = float (sys.argv[7]) # in micro-sec
optLevel        = int   (sys.argv[8]) 
tS              = float (sys.argv[9]) # in mico-sec
tM              = float (sys.argv[10]) # in mico-sec
printPlot       = int   (sys.argv[11])
saveROOT        = int   (sys.argv[12])
tag             = str   (sys.argv[13])
runSine         = int   (sys.argv[14])

print ''
print ' ============================= '
print ' == t0 optimization routine == '
print ' ============================= '
print '   lower t0     = ', lowert0, ' ns'
print '   upper t0     = ', uppert0, ' ns'
print '   t0 step size = ', t0StepSize, ' ns'
print '   tS           = ', tS, ' mu-s'
print '   tM           = ', tM, ' mu-s'
print ' ============================= '
print ''

#== Retrieve histogram from input ROOT file ==#

inFile = r.TFile( inputRootFile )
fr = inFile.Get( histoName )

#== Apply styles to histograms and canvas ==#

c = r.TCanvas( 'c', 'c', 900, 600 )
style.setCanvasStyle( c )
style.setHistogramStyle( fr, '', 'Time [#mus]', 'Intensity [a.u.]')

#== Find bin indexes for desire signal start (tS) and end time (tm)

startBin = fr.FindBin(tS) 
endBin   = fr.FindBin(tM)

#== Copy histogram to numpy array (to speed-up downstream processing) ==#

binCenter   = np.empty( int(endBin-startBin+1), dtype=float )
binContent  = np.empty( int(endBin-startBin+1), dtype=float )

for j in range(startBin, endBin):
    binContent[j-startBin] = fr.GetBinContent(j)  
    binCenter [j-startBin] = fr.GetBinCenter(j)   

#== Define ROOT histograms to hold Cosine and Sine transforms ==#

cosine  = r.TH1D("cosine", "cosine", constants.nFreq, constants.lowerFreq, constants.upperFreq)
sine    = r.TH1D("sine",   "sine",   constants.nFreq, constants.lowerFreq, constants.upperFreq)

#== Define function that performs the Fourier transforms and compute the FOM to optimize/loop over t0 ==#

def optimizationLoop( t0Step, t0Array, minDelta, minDeltaAbs ):

    #== Loop over the t0 values ==#
    for it0 in range(t0Step):
    
        #== Reset ROOT histograms i.e. clear entries and errors ==#
        cosine  .Reset()
        sine    .Reset()
    
        #== Set t0 value for this iterations ==#
        t0 = lowert0 + it0 * t0StepSize
    
        #== Calculate cosine and sine transforms ==#
        fourier.calc_cosine_dist(t0/1000, cosine, binContent, binCenter) # divide by 1,000 to convert from mu-s ns
        if ( runSine == 1 ):
            fourier.calc_sine_dist(t0/1000, sine, binContent, binCenter)
    
        #== Extract minima of distribution for t0 optimization ==#
        #== First minimum to the left of the peak (peak roughly 6700 kHz) ==#
        #== Second minimum to the right of the peak ==#
        cosine.GetXaxis().SetRangeUser(constants.lowerCollimatorFreq, 6700) # From collimator aperture to magic radius
        minBin1 = cosine.GetMinimum()
        cosine.GetXaxis().SetRangeUser(6700, constants.upperCollimatorFreq) # From magic radius to collimator aperture
        minBin2 = cosine.GetMinimum()
        cosine.GetXaxis().SetRangeUser(constants.lowerFreq, constants.upperFreq) # Back to the full frequency range
        
        #== Calculate F.O.M. ==#
        fom = ( minBin1-minBin2 )
        
        #== Save numbers in arrays ==#
        t0Array.append( t0 )
        minDelta.append( fom )
        minDeltaAbs.append( abs(fom) )
   
        #== Clone cosine histogram for plotting/styling puporses ==#
        cosineClone = cosine.Clone()
        style.setHistogramStyle( cosineClone, 'Cosine transform: t_{0} = ' + '{0:.1f} ns'.format(t0), 'Frequency [kHz]', 'Arbitrary' )
        cosineClone.SetMaximum( cosineClone.GetMaximum()*1.3 ) 
        cosineClone.SetMinimum( cosineClone.GetMinimum()*1.2 ) 

        #== Clone sine histogram for plotting/styling puporses ==#
        sineClone = sine.Clone()
        style.setHistogramStyle( sineClone, 'Sine transform: t_{0} = ' + '{0:.1f} ns'.format(t0), 'Frequency [kHz]', 'Arbitrary' )
        sineClone.SetMaximum( sineClone.GetMaximum()*1.3 ) 
        sineClone.SetMinimum( sineClone.GetMinimum()*1.2 ) 
   
        #== Define lines to be drawn at collimator apertures for cosine plot ==#
        innerLine = r.TLine( constants.lowerCollimatorFreq, cosineClone.GetMinimum(), constants.lowerCollimatorFreq, cosineClone.GetMaximum())
        innerLine.SetLineWidth(3)
        outerLine = r.TLine( constants.upperCollimatorFreq, cosineClone.GetMinimum(), constants.upperCollimatorFreq, cosineClone.GetMaximum())
        outerLine.SetLineWidth(3)    

        #== Define pave text to go along the collimator apertures lines for cosine plot ==#
        pt  = r.TPaveText( constants.lowerCollimatorTextFreq1, cosineClone.GetMaximum()*0.38, constants.lowerCollimatorTextFreq2, cosineClone.GetMaximum()*0.52);
        pt2 = r.TPaveText( constants.upperCollimatorTextFreq1, cosineClone.GetMaximum()*0.38, constants.upperCollimatorTextFreq2, cosineClone.GetMaximum()*0.52);
        style.setCollimatorAperture( pt, pt2 )
   
        #== Draw it all for the cosine transform ==#
        cosineClone.Draw()
        innerLine   .Draw("same")
        outerLine   .Draw("same")
        pt          .Draw("same")
        pt2         .Draw("same")
        c           .Draw()
   
        #== Save plot if option provided ==#
        if ( printPlot == 1 ):
            c.Print('plots/eps/'+ tag + '/Cosine_t0_{0:.4f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))
    
        #== Define lines to be drawn at collimator apertures for sine plot ==#
        innerLine = r.TLine( constants.lowerCollimatorFreq, sineClone.GetMinimum(), constants.lowerCollimatorFreq, sineClone.GetMaximum())
        innerLine.SetLineWidth(3)
        outerLine = r.TLine( constants.upperCollimatorFreq, sineClone.GetMinimum(), constants.upperCollimatorFreq, sineClone.GetMaximum())
        outerLine.SetLineWidth(3)    
    
        #== Define pave text to go along the collimator apertures lines for sine plot ==#
        pt  = r.TPaveText( constants.lowerCollimatorTextFreq1, sineClone.GetMaximum()*0.38, constants.lowerCollimatorTextFreq2, sineClone.GetMaximum()*0.52);
        pt2 = r.TPaveText( constants.upperCollimatorTextFreq1, sineClone.GetMaximum()*0.38, constants.upperCollimatorTextFreq2, sineClone.GetMaximum()*0.52);
        style.setCollimatorAperture( pt, pt2 )
    
        #== Draw it all for the sine transform ==#
        sineClone.Draw()
        innerLine   .Draw("same")
        outerLine   .Draw("same")
        pt          .Draw("same")
        pt2         .Draw("same")
        c           .Draw()
    
        #== Save plot if option provided and if sine transform was performed ==#
        if ( printPlot == 1 and runSine == 1 ):
            c.Print('plots/eps/' + tag + '/Sine_t0_{0:.4f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))

#=============================#
#== First optimization loop ==#
#=============================#

#== Define arrays to store results from optimization loop ==#
t0Array, minDelta, minDeltaAbs = array.array( 'd' ), array.array( 'd' ), array.array( 'd' )

#== Compute the size of the t0 step ==#
t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1

#== Run the optimization loop ==#
optimizationLoop( t0Step, t0Array, minDelta, minDeltaAbs )

#== Fit the results to extract the optimized t0 ==#
fit     = np.polyfit(t0Array,minDelta,1)
fit_fn  = np.poly1d(fit)
optt0   = -fit_fn.c[1]/fit_fn.c[0]

print ' First  optimization done, t0 = ' + '{0:.2f}'.format(optt0) +  ' ns'

#== Plot the optimization results ==#
plt.plot( t0Array, minDelta, 'ro', t0Array, fit_fn(t0Array), 'k')
plt.ylabel('F.O.M.')
plt.xlabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '/t0Opt_coarse_fit_tS_{0}_tM_{1}.eps'.format(tS, tM))
plt.close()

#== Plot the optimization results ==#
plt.plot(t0Array, minDeltaAbs, 'rx', label='data')
plt.ylabel('F.O.M.')
plt.xlabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '/t0Opt_coarse_tS_{0}_tM_{1}.eps'.format(tS, tM))
plt.close()


#==============================#
#== Second optimization loop ==#
#==============================#

if ( optLevel > 1 ):

    t0ArrayFine, minDeltaFine, minDeltaFineAbs = array.array( 'd' ), array.array( 'd' ), array.array( 'd' )
    
    lowert0 = optt0 - 0.2
    uppert0 = optt0 + 0.2
    t0StepSize = 0.02
    
    t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1

    optimizationLoop( t0Step, t0ArrayFine, minDeltaFine, minDeltaFineAbs )
    
    fit = np.polyfit(t0ArrayFine,minDeltaFine,1)
    fit_fn = np.poly1d(fit)
    plt.plot(t0ArrayFine, minDeltaFine, 'ro', t0ArrayFine, fit_fn(t0ArrayFine), 'k')
    optt0 = -fit_fn.c[1]/fit_fn.c[0]
    print ' Second optimization done, t0 = ' + '{0:.2f}'.format(optt0) +  ' ns'
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.savefig('plots/eps/' + tag + '/t0Opt_fine_fit_tS_{0}_tM_{1}.eps'.format(tS, tM))
    plt.close()
    plt.plot(t0ArrayFine, minDeltaFineAbs, 'ro', label='data')
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.savefig('plots/eps/' + tag + '/t0Opt_fine_tS_{0}_tM_{1}.eps'.format(tS, tM))
    plt.close()

## Run third optimization

if ( optLevel > 2 ):

    ## Find minimum
    
    minFOM =  minDeltaFine.index(min(minDeltaFine))
    
    lowert0 = -fit_fn.c[1]/fit_fn.c[0] - 0.00005
    uppert0 = -fit_fn.c[1]/fit_fn.c[0] + 0.00005
    t0StepSize = 0.00001
    
    t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1
    
    t0ArrayVeryFine, minDeltaVeryFine, minDeltaVeryFineAbs = array.array( 'd' ), array.array( 'd' ), array.array( 'd' )

    optimizationLoop( t0Step, t0ArrayVeryFine, minDeltaVeryFine, minDeltaVeryFineAbs )
    
    fit = np.polyfit(t0ArrayVeryFine,minDeltaVeryFine,1)
    fit_fn = np.poly1d(fit)
    plt.plot(t0ArrayVeryFine, minDeltaVeryFine, 'ro', t0ArrayVeryFine, fit_fn(t0ArrayVeryFine), 'k')
    optt0 = -fit_fn.c[1]/fit_fn.c[0]
    print ' Third  optimization done, t0 = ' + '{0:.2f}'.format(optt0) +  ' ns'
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.savefig('plots/eps/' + tag + '/t0Opt_veryFine_fit_tS_{0}_tM_{1}.eps'.format(tS, tM))
    plt.close()
    plt.plot(t0ArrayVeryFine, minDeltaVeryFineAbs, 'ro', label='data')
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [ns]')
    plt.savefig('plots/eps/' + tag + '/t0Opt_veryFine_tS_{0}_tM_{1}.eps'.format(tS, tM))
    plt.close()
    
    ## Find minimum
    
    minFOM =  minDeltaVeryFine.index(min(minDeltaVeryFine))
    
    lowert0 = t0ArrayVeryFine[minFOM] - 0.0001
    uppert0 = t0ArrayVeryFine[minFOM] + 0.0001
    t0StepSize = 0.00001
    
    t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1
    
    t0ArrayUltraFine, minDeltaUltraFine = array( 'd' ), array( 'd' )

## Run fourth optimization

if ( optLevel > 3 ):
    optimizationLoop( t0Step, t0ArrayUltraFine, minDeltaUltraFine )
    
    print ' Fourth optimization done'
    
    plt.plot(t0ArrayUltraFine, minDeltaUltraFine, 'ro', label='data')
    plt.ylabel('F.O.M.')
    plt.xlabel('$\mathregular{t_{0}}$ [$\mathregular{\mu}$s]')
    plt.savefig('plots/eps/' + tag + '/t0Opt_ultraFine_tS_{0}_tM_{1}.eps'.format(tS, tM))
    plt.close()
    
    minFOM =  minDeltaVeryFine.index(min(minDeltaVeryFine))

## All the steps on one plot

if ( optLevel > 1 ):
    t0Array.extend( t0ArrayFine )
    minDelta.extend( minDeltaFine )
if ( optLevel > 2 ):
    t0Array.extend( t0ArrayVeryFine )
    minDelta.extend( minDeltaVeryFine )

plt.plot(t0Array, minDelta, 'ro', label='data')
plt.ylabel('F.O.M.')
plt.xlabel('$\mathregular{t_{0}}$ [$\mathregular{\mu}$s]')
plt.savefig('plots/eps/' + tag + '/t0Opt_tS_{0}_tM_{1}.eps'.format(tS, tM))
plt.close()

text_file = open(str(outputTextFile), "w")

optt0 /= 1000

if ( optLevel > 3 ):
    text_file.write( '%f\n' % optt0 )
elif ( optLevel > 2 ):
    text_file.write( '%f\n' % optt0 )
elif ( optLevel > 1 ):
    text_file.write( '%f\n' % optt0 )
else:
    text_file.write( '%f\n' % optt0 )

text_file.close()
