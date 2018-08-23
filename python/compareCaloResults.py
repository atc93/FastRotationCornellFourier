from importAll import *

tag='60h'

name = 'txt/' + tag + '_fourierAnalysis_perCalo.txt'

fileList    = []
histoList   = []
colorList   = [600, 601, 602, 603, 604, 599, 632, 633, 634, 635, 636, 631, 416, 417, 418, 419, 420, 415, 616, 617, 618, 619, 620, 615]

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )

leg = r.TLegend(0.895,0.28,0.95,0.925)

for i in range(0, 24):
    fileList.append( r.TFile('root/' + tag + '_fourierAnalysis_calo' + str(i+1) + '.root') )
    histoList.append( fileList[i].Get('rad') )
    setHistogramStyle( histoList[i], '', 'Radius [mm]', 'Arbitrary' )
    histoList[i].SetLineColor ( colorList[i] )
    histoList[i].SetMarkerColor ( colorList[i] )
    leg.AddEntry(histoList[i], 'calo ' + str(i+1), "l")
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

innerLine.Draw("same")
outerLine.Draw("same")
magicLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")
pt3.Draw("same")
leg.Draw("same")

c.SaveAs('plots/eps/' + tag + '_radial_allCalos.eps')

caloNum = np.loadtxt(name, usecols=0)
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
avg_ce /= 24
avg_xe /= 24
avg_w /= 24

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

plt.figure(1)
fit = np.polyfit(caloNum,t0,1)
fit_fn = np.poly1d(fit) 
plt.plot(caloNum,t0, 'rx', caloNum, fit_fn(caloNum), 'k')
plt.suptitle('t0 = {0:.3f} * calo # + {1:.3f} ns'.format(fit_fn.c[0], fit_fn.c[1]))
plt.xlabel('Calo #')
plt.ylabel('$\mathregular{t_{0}}$ [ns]')
plt.savefig('plots/eps/' + tag + '_t0_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_t0_vs_caloNum.png', format='png')
plt.close()

plt.figure(2)
plt.plot(caloNum, xe, 'rx')
plt.xlabel('Calo #')
plt.suptitle('$\mathregular{<x_{e}>}=' + '{0:.1f}'.format(avg_xe) + '$ +- ' + '{0:.1f}'.format(std_xe) + ' mm')
plt.ylabel('$\mathregular{x_{e}}$ [mm]')
plt.savefig('plots/eps/' + tag + '_xe_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_xe_vs_caloNum.png', format='png')
plt.close()

plt.figure(3)
plt.plot(caloNum, width, 'rx')
plt.xlabel('Calo #')
plt.suptitle('$\mathregular{<width>}=' + '{0:.1f}'.format(avg_w) + '$ +- ' + '{0:.1f}'.format(std_w) + ' mm')
plt.ylabel('Width [mm]')
plt.savefig('plots/eps/' + tag + '_width_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_width_vs_caloNum.png', format='png')
plt.close()

plt.figure(4)
plt.plot(caloNum, ce, 'rx')
plt.xlabel('Calo #')
plt.suptitle('$\mathregular{<C_{E}>}=' + '{0:.1f}'.format(avg_ce) + '$ +- ' + '{0:.1f}'.format(std_ce) + ' ppb')
plt.ylabel('$\mathregular{C_{E}}$ [ppb]')
plt.savefig('plots/eps/' + tag + '_ce_vs_caloNum.eps', format='eps')
plt.savefig('plots/png/' + tag + '_ce_vs_caloNum.png', format='png')
plt.close()
