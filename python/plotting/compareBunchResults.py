from importAll import *

tag='60h'

name = 'txt/' + tag + '_fourierAnalysis_perBunch.txt'

fileList    = []
histoList   = []
colorList   = [1, 2, 4, 6, 7, 8, 9, 41]

statCeMean = []
statXeMean = []
statWMean  = []
statT0Mean = []
statCeStd = []
statXeStd = []
statWStd  = []
statT0Std = []

for i in range (0, 8):
    filename = 'txt/60h_bunch'+ str(i) + '_statFluc.txt'
    statCeMean.append( float(np.loadtxt(filename, usecols=7)) )
    statCeStd.append( float(np.loadtxt(filename, usecols=8)) )
    statXeMean.append( float(np.loadtxt(filename, usecols=1)) )
    statXeStd.append( float(np.loadtxt(filename, usecols=2)) )
    statWMean.append( float(np.loadtxt(filename, usecols=4)) )
    statWStd.append( float(np.loadtxt(filename, usecols=5)) )
    statT0Mean.append( float(np.loadtxt(filename, usecols=10)) )
    statT0Std.append( float(np.loadtxt(filename, usecols=11)) )


c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )

for i in range(0, 8):
    fileList.append( r.TFile('root/' + tag + '_fourierAnalysis_bunch' + str(i) + '.root') )
    histoList.append( fileList[i].Get('rad') )
    setHistogramStyle( histoList[i], '', 'Radius [mm]', 'Arbitrary' )
    histoList[i].SetLineColor ( colorList[i] )
    histoList[i].SetMarkerColor ( colorList[i] )
    if ( i == 0 ):
        histoList[i].Draw()
    else:
        histoList[i].Draw("samelp")

graphMin = -0.05
graphMax = 1.05

innerLine = r.TLine(7067, histoList[0].GetMinimum(), 7067, histoList[0].GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(7157, histoList[0].GetMinimum(), 7157, histoList[0].GetMaximum())
outerLine.SetLineWidth(3)
magicLine = r.TLine(7112, graphMin, 7112, graphMax)
magicLine.SetLineWidth(1)
magicLine.SetLineStyle(7)

pt=r.TPaveText(7060, graphMax*0.45,7074,graphMax*0.55);
pt2=r.TPaveText(7150,graphMax*0.45,7164,graphMax*0.55);
pt3=r.TPaveText(7113,graphMax*0.04,7121,graphMax*0.11);

setCollimatorAperture( pt, pt2 )
pt3.AddText("magic");
pt3.AddText("radius");
pt3.SetShadowColor(0);
pt3.SetBorderSize(1);
pt3.SetFillColor(0);
pt3.SetLineWidth(1);
pt3.SetLineColor(1);

leg = r.TLegend(0.85,0.71,0.95,0.925)
for i in range (0, 8):
    leg.AddEntry(histoList[i], 'bunch ' + str(i), "l")

leg.Draw("same")
innerLine.Draw("same")
outerLine.Draw("same")
magicLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")
pt3.Draw("same")

c.SaveAs('plots/eps/' + tag + '_radial_allBunches.eps')

bunchNum = np.loadtxt(name, usecols=0)
t0      = np.loadtxt(name, usecols=2)*1000
fom     = np.loadtxt(name, usecols=10)
xe      = np.loadtxt(name, usecols=12)
width   = np.loadtxt(name, usecols=14)
ce      = np.loadtxt(name, usecols=16)

avg_ce = 0
avg_xe = 0
avg_w = 0
for i in ce:
    avg_ce += i
for i in xe:
    avg_xe += i
for i in width:
    avg_w += i
avg_ce /= 8
avg_xe /= 8
avg_w /= 8

std_ce = 0
sum = 0
for i in ce:
    sum += 1
    std_ce += (i-avg_ce) * (i-avg_ce)
std_ce /= sum-1
std_ce = math.sqrt(std_ce)

print 'C_E = ', avg_ce, ' +- ', std_ce

std_xe = 0
sum = 0
for i in xe:
    sum += 1
    std_xe += (i-avg_xe) * (i-avg_xe)
std_xe /= sum-1
std_xe = math.sqrt(std_xe)

print 'x_e = ', avg_xe, ' +- ', std_xe

std_w = 0
sum = 0
for i in width:
    sum += 1
    std_w += (i-avg_w) * (i-avg_w)
std_w /= sum-1
std_w = math.sqrt(std_w)

print 'width = ', avg_w, ' +- ', std_w

sum_weight = 0
for i in range(0,8):
    sum_weight += 1/statCeStd[i]

weightedCe = 0;
for i in range(0, 8):
    weightedCe += 1/statCeStd[i] / sum_weight * statCeMean[i]

weithedSigma = 0
for i in range(0, 8):
    weithedSigma += (1/statCeStd[i]) / (sum_weight) * statCeStd[i]

print weightedCe, math.sqrt(weithedSigma)

plt.figure(1)
fit = np.polyfit(bunchNum,t0,1)
fit_fn = np.poly1d(fit) 
#plt.plot(bunchNum,t0, 'rx', bunchNum, fit_fn(bunchNum), 'k')
plt.plot(bunchNum,t0, 'rx')
#plt.suptitle('t0 = {0:.3f} + {1:.3f} ns'.format(fit_fn.c[0], fit_fn.c[1]))
plt.xlabel('Bunch #')
plt.ylabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '_t0_vs_bunchNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_t0_vs_bunchNum.png', format='png')
plt.close()

plt.figure(2)
plt.errorbar(bunchNum, statXeMean, yerr=statXeStd, fmt='o', label='pseudo-data', zorder=1)
plt.plot(bunchNum, xe, 'rx', label='data', zorder=2)
plt.legend(loc=9, bbox_to_anchor=(.1, 1.01, 0.75, .07), ncol=2, mode="", prop={'size':7})
plt.xlabel('Bunch #')
plt.ylabel('$\mathregular{x_{e}}$ [mm]')
#plt.suptitle('$\mathregular{<x_{e}>}=' + '{0:.1f}'.format(avg_xe) + '$ +- ' + '{0:.1f}'.format(std_xe) + ' mm')
plt.savefig('plots/eps/' + tag + '_xe_vs_bunchNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_xe_vs_bunchNum.png', format='png')
plt.close()

plt.figure(3)
plt.errorbar(bunchNum, statWMean, yerr=statWStd, fmt='o', label='pseudo-data', zorder=1)
plt.plot(bunchNum, width, 'rx', label='data', zorder=2)
plt.legend(loc=9, bbox_to_anchor=(.1, 1.01, 0.75, .07), ncol=2, mode="", prop={'size':7})
plt.xlabel('Bunch #')
plt.ylabel('Width [mm]')
#plt.suptitle('$\mathregular{<width>}=' + '{0:.1f}'.format(avg_w) + '$ +- ' + '{0:.1f}'.format(std_w) + ' mm')
plt.savefig('plots/eps/' + tag + '_width_vs_bunchNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_width_vs_bunchNum.png', format='png')
plt.close()

plt.figure(4)
plt.errorbar(bunchNum, statCeMean, yerr=statCeStd, fmt='o', label='pseudo-data', zorder=1)
plt.plot(bunchNum, ce, 'rx', label='data', zorder=2)
plt.legend(loc=9, bbox_to_anchor=(.1, 1.01, 0.75, .07), ncol=2, mode="", prop={'size':7})
plt.xlabel('Bunch #')
plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
#plt.suptitle('$\mathregular{<C_{E}>}=' + '{0:.1f}'.format(avg_ce) + '$ +- ' + '{0:.1f}'.format(std_ce) + ' ppb')
plt.savefig('plots/eps/' + tag + '_ce_vs_bunchNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_ce_vs_bunchNum.png', format='png')
plt.close()
