# coding: utf-8

## Module importS

from importAll import *

## Get command line argumentS

cmdargs = str(sys.argv)

inputRootFile   = str(sys.argv[1])
outputRootFile  = str(sys.argv[2])
outputTextFile  = str(sys.argv[3])
histoName       = str(sys.argv[4])
t0              = float(sys.argv[5]) # in mico-sec
tS              = float(sys.argv[6]) # in mico-sec
tM              = float(sys.argv[7]) # in mico-sec
fieldIndex      = float(sys.argv[8])
printPlot       = int(sys.argv[9])
saveROOT        = int(sys.argv[10])
tag             = str(sys.argv[11])
updateTextFile  = int(sys.argv[12])
runSine         = int(sys.argv[13])
outputDistFile  = str(sys.argv[14])

print ''
print ' =============================='
print ' == Fourier analysis routine =='
print ' =============================='
print '    t0 = ', t0
print '    tS = ', tS
print '    tM = ', tM
print '    n  = ', fieldIndex
print ' =============================='
print ''

## Styling and plotting

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )

## Retrieve and plot histogram from ROOT file

inFile = r.TFile( inputRootFile )
fr = inFile.Get( histoName )
setHistogramStyle( fr, '', 'Time [#mus]', 'Intensity [a.u.]')

#fr.Scale(1/66666.);

## Real transform

startBin = fr.FindBin(tS) 
endBin   = fr.FindBin(tM)

# Copy histogram to numpy array
binCenter   = np.empty( int(endBin-startBin+1), dtype=float )
binContent  = np.empty( int(endBin-startBin+1), dtype=float )
for j in range(startBin, endBin):
    binContent[j-startBin] = fr.GetBinContent(j)
    binCenter[j-startBin] = fr.GetBinCenter(j)

# Fourier analysis starts here

intensity, radius = array( 'd' ), array( 'd' )

cosine  = r.TH1D("cosine",  "cosine",   constants.nFreq, constants.lowerFreq, constants.upperFreq)
sine    = r.TH1D("sin",     "sine",     constants.nFreq, constants.lowerFreq, constants.upperFreq)

calc_cosine_dist(t0, cosine, binContent, binCenter)
if ( runSine == 1 ):
    print 'run sine calculation'
    calc_sine_dist  (t0, sine, binContent, binCenter )

# Extract minimum of distributions for t0 optimization
cosine.GetXaxis().SetRangeUser(constants.lowerFreq, 6700)
minBin1 = cosine.GetMinimum()
cosine.GetXaxis().SetRangeUser(6700, constants.upperFreq)
minBin2 = cosine.GetMinimum()
cosine.GetXaxis().SetRangeUser(constants.lowerFreq, constants.upperFreq)

# Calculate F.O.M.
fom = abs( minBin1-minBin2 )


cosineClone = cosine.Clone()
#setHistogramStyle( cosineClone, 'Cosine transform (t_{0}' + '= {0:.1f} ns)'.format(t0*1000), 'Frequency [kHz]', 'Arbitrary' )
setHistogramStyle( cosineClone, 'Cosine transform', 'Frequency [kHz]', 'Arbitrary' )
cosineClone.SetMaximum( cosineClone.GetMaximum()*1.3 ) 
cosineClone.SetMinimum( cosineClone.GetMinimum()*1.2 ) 

sineClone = sine.Clone()
setHistogramStyle( sineClone, 'Sine transform (t0= {0:.1f} ns)'.format(t0*1000), 'Frequency [kHz]', 'Arbitrary' )
sineClone.SetMaximum( sineClone.GetMaximum()*1.3 ) 
sineClone.SetMinimum( sineClone.GetMinimum()*1.2 ) 

innerLine = r.TLine(constants.lowerCollimatorFreq, cosineClone.GetMinimum(), constants.lowerCollimatorFreq, cosineClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(constants.upperCollimatorFreq, cosineClone.GetMinimum(), constants.upperCollimatorFreq, cosineClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,cosineClone.GetMaximum()*0.38,6674,cosineClone.GetMaximum()*0.52);
pt2=r.TPaveText(6737,cosineClone.GetMaximum()*0.38,6759,cosineClone.GetMaximum()*0.52);
setCollimatorAperture( pt, pt2 )

cosineClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")

c.Draw()
if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Cosine_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))

innerLine = r.TLine(constants.lowerCollimatorFreq, sineClone.GetMinimum(), constants.lowerCollimatorFreq, sineClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(constants.upperCollimatorFreq, sineClone.GetMinimum(), constants.upperCollimatorFreq, sineClone.GetMaximum())
outerLine.SetLineWidth(3)

pt=r.TPaveText(6650,    sineClone.GetMaximum()*0.38,    6674,   sineClone.GetMaximum()*0.52);
pt2=r.TPaveText(6737,   sineClone.GetMaximum()*0.38,    6759,   sineClone.GetMaximum()*0.52);
setCollimatorAperture( pt, pt2 )

sineClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")

c.Draw()
if ( printPlot == 1 ):
        c.Print('plots/eps/' + tag + '/Sine_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))

## First Apprxomiation

approx = cosine.Clone()

maxBin = approx.GetMaximumBin()

approx.GetXaxis().SetRangeUser(constants.lowerFreq, 6700)
minBin1 = approx.GetMinimumBin()

approx.GetXaxis().SetRangeUser(6700, constants.upperFreq)
minBin2 = approx.GetMinimumBin()

#print minBin1, freq.GetBinContent(minBin1), minBin2, freq.GetBinContent(minBin2)

minA =  (approx.GetBinContent(minBin1) + approx.GetBinContent(minBin2)) / 2

for iBin in range(1, minBin1):
    approx.SetBinContent(iBin, 0)
    
for iBin in range(minBin2+1, constants.nFreq+1):
    approx.SetBinContent(iBin, 0)    
    
approx.GetXaxis().SetRangeUser(constants.lowerFreq, constants.upperFreq)    

for iBin in range(minBin1, minBin2+1):
    approx.AddBinContent(iBin, -1*minA)
    
approxClone = approx
    
setHistogramStyle( approxClone, 'First approximation', 'Frequency [kHz]', 'Arbitrary' )    
approxClone.SetMaximum( approxClone.GetMaximum()*1.3 ) 
approxClone.SetMinimum( -0.5 ) 
    
innerLine = r.TLine(constants.lowerCollimatorFreq, approxClone.GetMinimum(), constants.lowerCollimatorFreq, approxClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(constants.upperCollimatorFreq, approxClone.GetMinimum(), constants.upperCollimatorFreq, approxClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,approxClone.GetMaximum()*0.9,6674,approxClone.GetMaximum()*1);
pt2=r.TPaveText(6737,approxClone.GetMaximum()*0.9,6759,approxClone.GetMaximum()*1);
setCollimatorAperture( pt, pt2 )

approxClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")   
c.Draw()    

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/FirstApproximation_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))


# # Delta Correction

# In[ ]:


# Correction
parabola = cosine.Clone()
parabola.Scale(0)

calc_parabola_dist(t0, tS, approx, parabola)

parabola.Draw()
parabola.SetTitle("Parabola")
c.Update()
c.Draw()


# # 'a' and 'b'optimization

a, b = minimization(parabola, cosine)

# In[ ]:

cosine.Draw()
c.Draw()

# # Scaled parabola

for iBin in range(1, constants.nFreq+1):
    parabola.SetBinContent(iBin, -1*( a*parabola.GetBinContent(iBin)+b) )
    
    
parabolaClone = parabola.Clone()
setHistogramStyle( parabolaClone, 'Parabola', 'Frequency [kHz]', 'Arbitrary' )    
parabolaClone.SetMaximum( parabolaClone.GetMaximum()*1.15 ) 
parabolaClone.SetMinimum( parabolaClone.GetMinimum()*0.85 ) 
    
innerLine = r.TLine(constants.lowerCollimatorFreq, parabolaClone.GetMinimum(), constants.lowerCollimatorFreq, parabolaClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(constants.upperCollimatorFreq, parabolaClone.GetMinimum(), constants.upperCollimatorFreq, parabolaClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,parabolaClone.GetMaximum()*0.9,6674,parabolaClone.GetMaximum()*1);
pt2=r.TPaveText(6737,parabolaClone.GetMaximum()*0.9,6759,parabolaClone.GetMaximum()*1);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    
    
parabolaClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")    
c.Draw()    
if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Parabola_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    


# # Complete distribution

# In[ ]:


full = cosine.Clone()
for iBin in range(1,constants.nFreq+1):
    full.AddBinContent(iBin, parabola.GetBinContent(iBin) )
full.SetTitle("Complete distribution")    

fullClone = full.Clone()
setHistogramStyle( fullClone, 'Complete distribution', 'Frequency [kHz]', 'Arbitrary' )    
fullClone.SetMaximum( fullClone.GetMaximum()*1.15 ) 
fullClone.SetMinimum( -0.5 ) 
    
innerLine = r.TLine(constants.lowerCollimatorFreq, fullClone.GetMinimum(), constants.lowerCollimatorFreq, fullClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(constants.upperCollimatorFreq, fullClone.GetMinimum(), constants.upperCollimatorFreq, fullClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,fullClone.GetMaximum()*0.9,6674,fullClone.GetMaximum()*1);
pt2=r.TPaveText(6737,fullClone.GetMaximum()*0.9,6759,fullClone.GetMaximum()*1);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    
    
fullClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")    
c.Draw()    
if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/CompleteDistribution_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    


# # Conversion frequency -> radius

# In[ ]:


muonMass = .105658
magicP = 3.094
E = math.sqrt(muonMass*muonMass+magicP*magicP)
gamma = E / muonMass
beta = magicP / ( gamma * muonMass )
speed = beta * 299792458
#print 'Total Energy = ', E
#print 'Gamma = ', gamma
#print 'Beta = ', beta
#print 'Speed = ', speed, ' m/s'


# In[ ]:


intensity, radius = array( 'd' ), array( 'd' )

for i in range(1, constants.nFreq+1):
    radius.append( speed / (2*math.pi*full.GetBinCenter(i)) )
    intensity.append( full.GetBinContent(i))


xe = np.average(radius, axis=0, weights=intensity)   
maxI = np.amax(intensity)
intensity = intensity/maxI

graph = r.TGraph(constants.nFreq,radius,intensity)
graph.SetTitle('')
graph.GetXaxis().SetTitle("Radius [mm]")
graph.GetYaxis().SetTitle("Arbitrary unitS")
graph.GetXaxis().CenterTitle()
graph.GetYaxis().CenterTitle()
graph.GetXaxis().SetTitleOffset(1.4)
graph.GetXaxis().SetTitleSize(0.055);
graph.GetXaxis().SetLabelSize(0.05);
graph.GetYaxis().SetTitleOffset(1.4)
graph.GetYaxis().SetTitleSize(0.055);
graph.GetYaxis().SetLabelSize(0.05);
graph.GetXaxis().SetRangeUser(7052,7172)
graph.SetMarkerStyle(20)
graph.SetMarkerSize(0.6)
graph.SetMarkerColor(4)
graph.SetLineColor(4)
graphMin = -0.05
graphMax = 1.05
graph.SetMaximum(graphMax)
graph.SetMinimum(graphMin)

innerLine = r.TLine(7067, graphMin, 7067, graphMax)
innerLine.SetLineWidth(2)
outerLine = r.TLine(7157, graphMin, 7157, graphMax)
outerLine.SetLineWidth(2)
magicLine = r.TLine(7112, graphMin, 7112, graphMax)
magicLine.SetLineWidth(1)
magicLine.SetLineStyle(7)

pt=r.TPaveText(7060, graphMax*0.45,7074,graphMax*0.55);
pt2=r.TPaveText(7150,graphMax*0.45,7164,graphMax*0.55);
pt3=r.TPaveText(7113,graphMax*0.04,7121,graphMax*0.11);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);
pt3.AddText("magic");
pt3.AddText("radius");
pt3.SetShadowColor(0);
pt3.SetBorderSize(1);
pt3.SetFillColor(0);
pt3.SetLineWidth(1);
pt3.SetLineColor(1);


if ( saveROOT == 1 ):
    file = r.TFile(outputRootFile, "RECREATE")
    graph.Write("rad")
    file.Close()

std = 0
sum = 0
for i,j in zip(radius,intensity):
    if ( i < constants.lowerCollimatorRad or i > constants.upperCollimatorRad ):
        continue
    sum += j
    std += (j) * (i-xe) * (i-xe)

std /= sum
std = math.sqrt(std)

sum = 0
msd = 0
for i,j in zip(radius,intensity):
    if ( i < constants.lowerCollimatorRad or i > constants.upperCollimatorRad ):
        continue
    sum += j
    msd += (j) * (i-7112) * (i-7112 )
    
msd /= sum

xe -= 7112

C_E_reco  = -2*beta*beta*fieldIndex*(1-fieldIndex)*msd/(7112*7112)*1e9

#print std

graph.Draw('APL')
innerLine.Draw("same")
outerLine.Draw("same")
magicLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")
pt3.Draw("same")

pt4=r.TPaveText(7070, graphMax*0.7,7095, graphMax*0.96);
pt4.AddText('x_{e} = ' + '{0:.1f}'.format(xe) + ' mm');
pt4.AddText(' #sigma = ' + '{0:.1f}'.format(std) + ' mm');
pt4.AddText('      C_{E} = ' + '{0:.1f}'.format(C_E_reco) + ' ppb ');
pt4.SetShadowColor(0);
pt4.SetBorderSize(1);
pt4.SetFillColor(0);
pt4.SetLineWidth(1);
pt4.SetLineColor(1);
pt4.SetTextAngle(90);

pt4.Draw("same")

c.Draw()

if ( printPlot == 1 ):
    c.Print('plots/eps/' + tag + '/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    
    c.Print('plots/png/' + tag + '/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.png'.format(t0, tS, tM))    


#for x,y in zip(radius, intensity):
#    print x, y

#print 'a = ', a
#print 'b = ', b
#print 'C_E reco  ', C_E_reco, ' ppb'

if ( updateTextFile == 1 ):
    text_file = open(str(outputTextFile), "a")
    textFileDist = open(str(outputDistFile), "a")
else:
    text_file = open(str(outputTextFile), "w")

text_file.write('t0 %f tS %f tM %f fieldIndex %f fom %f xe_reco %f std_reco %f C_E_reco %f \n' % 
        (t0, tS, tM, fieldIndex, fom, xe, std, C_E_reco) )
text_file.close()

for i, j in zip(radius, intensity):
    textFileDist.write('%f %f ' % (i, j) )
textFileDist.write('\n')    
