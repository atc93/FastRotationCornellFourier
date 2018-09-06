# coding: utf-8

## Module importS

from importAll import *

## Get command line argumentS

cmdargs = str(sys.argv)

inputRootFile   = str(sys.argv[1])
outputRootFile  = str(sys.argv[2])
outputTextFile  = str(sys.argv[3])
histoName       = str(sys.argv[4])
lowert0         = float(sys.argv[5]) # in mico-sec
uppert0         = float(sys.argv[6]) # in mico-sec
t0StepSize      = float(sys.argv[7]) # in micro-sec
optLevel        = int(sys.argv[8]) 
tS              = float(sys.argv[9]) # in mico-sec
tM              = float(sys.argv[10]) # in mico-sec
printPlot       = int(sys.argv[11])
saveROOT        = int(sys.argv[12])
tag             = str(sys.argv[13])
runSine         = int(sys.argv[14])

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

## Styling and plotting

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )

## Retrieve and plot histogram from ROOT file

inFile = r.TFile( inputRootFile )
fr = inFile.Get( histoName )
setHistogramStyle( fr, '', 'Time [#mus]', 'Intensity [a.u.]')

## Real transform

startBin = fr.FindBin(tS) 
endBin   = fr.FindBin(tM)

# Copy histogram to numpy array
binCenter   = np.empty( int(endBin-startBin+1), dtype=float )
binContent  = np.empty( int(endBin-startBin+1), dtype=float )
for j in range(startBin, endBin):
    binContent[j-startBin] = fr.GetBinContent(j)  
    binCenter[j-startBin] = fr.GetBinCenter(j)   

### Fourier analysis starts here ###

t0Array, minDelta, minDeltaAbs = array( 'd' ), array( 'd' ), array( 'd' )

uppert0 = uppert0 
lowert0 = lowert0 
t0StepSize = t0StepSize

t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1

# Define ROOT histograms
cosine  = r.TH1D("cosine", "cosine", 150, 6630, 6780)
sine    = r.TH1D("sin",    "sine",   150, 6630, 6780)

def fitOptimization( t0Step, t0Array, minDelta, minDeltaAbs ):
    for it0 in range(t0Step):
    
        # Reset ROOT histograms
        cosine.Reset()
        sine.Reset()
    
        # Initialize t0
        t0 = lowert0 + it0 * t0StepSize
    
        # Calculate cosine and sine transform
        calc_cosine_dist(t0/1000, cosine, binContent, binCenter)
        if ( runSine == 1 ):
            print 'run sine calculation'
            calc_sine_dist(t0, sine, binContent, binCenter)
    
        # Extract minimum of distributions for t0 optimization
        cosine.GetXaxis().SetRangeUser(6630, 6700)
        minBin1 = cosine.GetMinimum()
        cosine.GetXaxis().SetRangeUser(6700, 6780)
        minBin2 = cosine.GetMinimum()
        cosine.GetXaxis().SetRangeUser(6630, 6780)
        
        # Calculate F.O.M.
        fom = ( minBin1-minBin2 )
        
        t0Array.append( t0 )
        #minDelta.append( fom )
        #minDeltaAbs.append( abs(fom) )
    
        cosineClone = cosine.Clone()
        setHistogramStyle( cosineClone, 'Cosine transform (t0= {0:.1f} ns)'.format(t0), 'Frequency [kHz]', 'Arbitrary' )
        cosineClone.SetMaximum( cosineClone.GetMaximum()*1.3 ) 
        cosineClone.SetMinimum( cosineClone.GetMinimum()*1.2 ) 

        graph= r.TGraphErrors(0);
        cpt = 0
        for i in range (1, 151):
            if ( cosineClone.GetBinCenter( i ) < 6662 or cosineClone.GetBinCenter( i ) > 6747 ):
                graph.SetPoint( cpt, cosineClone.GetBinCenter( i ), cosineClone.GetBinContent( i ) )
                graph.SetPointError( cpt, 0, 0.025 )
                cpt += 1
        pol3 = r.TF1("pol3", "pol3",6630, 6780);
        pol4 = r.TF1("pol4", "pol4",6630, 6780);
        graph.Fit("pol3", "r")
        pol4.SetParameter(0, pol3.GetParameter(0) )
        pol4.SetParameter(1, pol3.GetParameter(1) )
        pol4.SetParameter(2, pol3.GetParameter(2) )
        pol4.SetParameter(3, pol3.GetParameter(3) )
        #graph.Fit("pol4", "r")
        minDelta.append(    pol3.GetChisquare()/pol3.GetNDF() )
        minDeltaAbs.append( pol3.GetChisquare()/pol3.GetNDF() )
    
        sineClone = sine.Clone()
        setHistogramStyle( sineClone, 'Sine transform (t0= {0:.1f} ns)'.format(t0), 'Frequency [kHz]', 'Arbitrary' )
        sineClone.SetMaximum( sineClone.GetMaximum()*1.3 ) 
        sineClone.SetMinimum( sineClone.GetMinimum()*1.2 ) 
    
        innerLine = r.TLine(6662.799323395121, cosineClone.GetMinimum(), 6662.799323395121, cosineClone.GetMaximum())
        innerLine.SetLineWidth(3)
        outerLine = r.TLine(6747.651727400435, cosineClone.GetMinimum(), 6747.651727400435, cosineClone.GetMaximum())
        outerLine.SetLineWidth(3)    
    
        pt  = r.TPaveText(6650, cosineClone.GetMaximum()*0.38, 6674, cosineClone.GetMaximum()*0.52);
        pt2 = r.TPaveText(6737, cosineClone.GetMaximum()*0.38, 6759, cosineClone.GetMaximum()*0.52);
        setCollimatorAperture( pt, pt2 )
    
        cosineClone.Draw()
        innerLine   .Draw("same")
        outerLine   .Draw("same")
        pt          .Draw("same")
        pt2         .Draw("same")
        graph       .Draw("same")
        c           .Draw()
    
        if ( printPlot == 1 ):
            c.Print('plots/eps/'+ tag + '/Cosine_t0_{0:.4f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))
    
        innerLine = r.TLine(6662.799323395121, sineClone.GetMinimum(), 6662.799323395121, sineClone.GetMaximum())
        innerLine.SetLineWidth(3)
        outerLine = r.TLine(6747.651727400435, sineClone.GetMinimum(), 6747.651727400435, sineClone.GetMaximum())
        outerLine.SetLineWidth(3)    
    
        pt  = r.TPaveText(6650, sineClone.GetMaximum()*0.38, 6674, sineClone.GetMaximum()*0.52);
        pt2 = r.TPaveText(6737, sineClone.GetMaximum()*0.38, 6759, sineClone.GetMaximum()*0.52);
        setCollimatorAperture( pt, pt2 )
    
        sineClone.Draw()
        innerLine   .Draw("same")
        outerLine   .Draw("same")
        pt          .Draw("same")
        pt2         .Draw("same")
        c           .Draw()
    
        if ( printPlot == 1 ):
            c.Print('plots/eps/' + tag + '/Sine_t0_{0:.4f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))

optimizationLoop( t0Step, t0Array, minDelta, minDeltaAbs )

fit = np.polyfit(t0Array,minDelta,2)
fit_fn = np.poly1d(fit)
plt.plot( t0Array, minDelta, 'ro', t0Array, fit_fn(t0Array), 'k')
print fit_fn.r
#optt0 = -fit_fn.c[1]/fit_fn.c[0]
optt0 = fit_fn.r[0]
print ' First  optimization done, t0 = ' + '{0:.2f}'.format(optt0) +  ' ns'
plt.ylabel('F.O.M.')
plt.xlabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '/t0Opt_coarse_fit_tS_{0}_tM_{1}.eps'.format(tS, tM))
plt.close()
plt.plot(t0Array, minDeltaAbs, 'rx', label='data')
plt.ylabel('F.O.M.')
plt.xlabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '/t0Opt_coarse_tS_{0}_tM_{1}.eps'.format(tS, tM))
plt.close()

## Find Minimum

minFOM =  minDelta.index(min(minDelta))

lowert0 = -fit_fn.c[1]/fit_fn.c[0] - 0.00015
uppert0 = -fit_fn.c[1]/fit_fn.c[0] + 0.00015
t0StepSize = 0.00005

t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1

t0ArrayFine, minDeltaFine, minDeltaFineAbs = array( 'd' ), array( 'd' ), array( 'd' )

## Run second optimization

if ( optLevel > 1 ):
    optimizationLoop( t0Step, t0ArrayFine, minDeltaFine, minDeltaFineAbs )
    
    fit = np.polyfit(t0ArrayFine,minDeltaFine,2)
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
    
    ## Find minimum
    
    minFOM =  minDeltaFine.index(min(minDeltaFine))
    
    lowert0 = -fit_fn.c[1]/fit_fn.c[0] - 0.00005
    uppert0 = -fit_fn.c[1]/fit_fn.c[0] + 0.00005
    t0StepSize = 0.00001
    
    t0Step = int ( (uppert0 - lowert0 ) / t0StepSize ) + 1
    
    t0ArrayVeryFine, minDeltaVeryFine, minDeltaVeryFineAbs = array( 'd' ), array( 'd' ), array( 'd' )

## Run third optimization

if ( optLevel > 2 ):
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
