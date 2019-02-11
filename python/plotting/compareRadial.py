from importAll import *

#import ROOT as r
#import math
#from array import array
#import numpy as np
#import thread
#import matplotlib.pyplot as plt
#import sys
#from scipy.optimize import curve_fit

c = r.TCanvas('c1','c1',900,600)
c.SetTicks(1)
r.gStyle.SetOptStat(0)
c.SetLeftMargin(0.15);
c.SetRightMargin(0.05);
c.SetTopMargin(0.05);
c.SetBottomMargin(0.15);

def shiftRadius(rad):
    nPoint = rad.GetN()
    for i in range(0, nPoint):
        x, y = r.Double(), r.Double()
        rad.GetPoint(i, x, y)
        rad.SetPoint(i, x-7112, y)


file9d    = r.TFile('plots/eps/9d/9d.root')
fr9d      = file9d.Get('radial')
fr9d.SetLineColor(2)
fr9d.SetMarkerColor(2)
shiftRadius(fr9d)

fr9d.SetTitle('')
fr9d.GetXaxis().SetTitle("Radius [mm]")
fr9d.GetYaxis().SetTitle("Arbitrary units")
fr9d.GetXaxis().CenterTitle()
fr9d.GetYaxis().CenterTitle()
fr9d.GetXaxis().SetTitleOffset(1.4)
fr9d.GetXaxis().SetTitleSize(0.055);
fr9d.GetXaxis().SetLabelSize(0.05);
fr9d.GetYaxis().SetTitleOffset(1.4)
fr9d.GetYaxis().SetTitleSize(0.055);
fr9d.GetYaxis().SetLabelSize(0.05);

fileEndGame    = r.TFile('plots/eps/endGame/endGame.root')
frEndGame      = fileEndGame.Get('radial')
frEndGame.SetLineColor(4)
frEndGame.SetMarkerColor(4)

fileHighKick    = r.TFile('plots/eps/highKick/highKick.root')
frHighKick      = fileHighKick.Get('radial')
frHighKick.SetLineColor(616)
frHighKick.SetMarkerColor(616)

shiftRadius(frHighKick)

frHighKick.SetTitle('')
frHighKick.GetXaxis().SetTitle("Radius [mm]")
frHighKick.GetYaxis().SetTitle("Arbitrary units")
frHighKick.GetXaxis().CenterTitle()
frHighKick.GetYaxis().CenterTitle()
frHighKick.GetXaxis().SetTitleOffset(1.4)
frHighKick.GetXaxis().SetTitleSize(0.055);
frHighKick.GetXaxis().SetLabelSize(0.05);
frHighKick.GetYaxis().SetTitleOffset(1.4)
frHighKick.GetYaxis().SetTitleSize(0.055);
frHighKick.GetYaxis().SetLabelSize(0.05);

fileLowKick0h    = r.TFile('plots/eps/60h/60h.root')
fr60h      = fileLowKick0h.Get('radial')
fr60h.SetLineColor(1)
fr60h.SetMarkerColor(1)

fileSuperLowKick    = r.TFile('plots/eps/superLowKick/superLowKick.root')
frSuperLowKick      = fileSuperLowKick.Get('radial')
frSuperLowKick.SetLineColor(419)
frSuperLowKick.SetMarkerColor(419)

fileLowKick    = r.TFile('plots/eps/lowKick/lowKick.root')
frLowKick      = fileLowKick.Get('radial')
frLowKick.SetLineColor(434)
frLowKick.SetMarkerColor(434)


shiftRadius(frEndGame)
shiftRadius(fr60h)
shiftRadius(frSuperLowKick)
shiftRadius(frLowKick)

fr9d.GetXaxis().SetRangeUser(-45,45)
frHighKick.GetXaxis().SetRangeUser(-45,45)

#fr9d.Draw()
#frEndGame.Draw("samepl")
frHighKick.Draw()
#fr60h.Draw("samepl")
frSuperLowKick.Draw("samepl")
frLowKick.Draw("samepl")

graphMin = -0.05
graphMax = 1.05

leg = r.TLegend(0.8,0.75,0.95,0.95)
#leg.AddEntry(fr60h, "60-hour ", "lp")
leg.AddEntry(frHighKick, "High Kick", "lp")
#leg.AddEntry(fr9d, "9-day", "lp")
leg.AddEntry(frLowKick, "Low Kick ", "lp")
leg.AddEntry(frSuperLowKick, "Super Low Kick ", "lp")
#leg.AddEntry(frEndGame, "End Game", "lp")

leg2 = r.TLegend(0.15,0.71,0.45,0.95)
#leg2.AddEntry(fr60h, "x_{e} = 6.2 mm, #sigma = 9.1 mm ", "lp")
leg2.AddEntry(frHighKick, "x_{e} = 5.2 mm, #sigma = 8.5 mm ", "lp")
#leg2.AddEntry(fr9d, "x_{e} = 6.3 mm, #sigma = 8.9 mm ", "lp")
leg2.AddEntry(frLowKick, "x_{e} = 5.5 mm, #sigma = 8.8 mm ", "lp")
leg2.AddEntry(frSuperLowKick, "x_{e} = 7.7 mm, #sigma = 8.3 mm ", "lp")
#leg2.AddEntry(frEndGame, "x_{e} = 7.1 mm, #sigma = 8.2 mm ", "lp")

leg3 = r.TLegend(0.15,0.45,0.45,0.69)
#leg3.AddEntry(fr60h, "Kick strength: 128-132 kV ", "lp")
leg3.AddEntry(frHighKick, "Kick strength: 136-138 kV ", "lp")
#leg3.AddEntry(fr9d, "Kick strength: 128-132 kV ", "lp")
leg3.AddEntry(frLowKick, "Kick strength: 123-127 kV ", "lp")
leg3.AddEntry(frSuperLowKick, "Kick strength: 117-119 kV ", "lp")
#leg3.AddEntry(frEndGame, "Kick strength: 122-127 kV ", "lp")

leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")

innerLine = r.TLine(7067, graphMin, 7067, graphMax)
innerLine.SetLineWidth(2)
outerLine = r.TLine(7157, graphMin, 7157, graphMax)
outerLine.SetLineWidth(2)
magicLine = r.TLine(0, graphMin, 0, graphMax)
magicLine.SetLineWidth(2)
magicLine.SetLineStyle(7)

pt=r.TPaveText(7060, graphMax*0.45,7074,graphMax*0.55);
pt2=r.TPaveText(7150,graphMax*0.45,7164,graphMax*0.55);
pt3=r.TPaveText(1,graphMax*0.04,9,graphMax*0.11);
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

#innerLine.Draw("same")
#outerLine.Draw("same")
magicLine.Draw("same")
#pt.Draw("same")
#pt2.Draw("same")
pt3.Draw("same")
leg.Draw("same")

c.SaveAs("comparison.eps")
