import ROOT as r
import math
from array import array
import numpy as np
import thread
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit

c = r.TCanvas('c1','c1',900,600)
c.SetTicks(1)
r.gStyle.SetOptStat(0)
c.SetLeftMargin(0.15);
c.SetRightMargin(0.05);
c.SetTopMargin(0.05);
c.SetBottomMargin(0.15);

file1    = r.TFile('rad_nominal.root')
fr1      = file1.Get('rad')

file2    = r.TFile('rad_5p.root')
fr2      = file2.Get('rad')
fr2.SetLineColor(2)
fr2.SetMarkerColor(2)

file3    = r.TFile('rad_15p.root')
fr3      = file3.Get('rad')
fr3.SetLineColor(8)
fr3.SetMarkerColor(8)

file4    = r.TFile('rad_20p.root')
fr4      = file4.Get('rad')
fr4.SetLineColor(1)
fr4.SetMarkerColor(1)

file5    = r.TFile('rad_30p.root')
fr5      = file5.Get('rad')
fr5.SetLineColor(6)
fr5.SetMarkerColor(6)

fr1.Draw()
fr2.Draw("samepl")
fr3.Draw("samepl")
fr4.Draw("samepl")
fr5.Draw("samepl")

graphMin = -0.05
graphMax = 1.1

leg = r.TLegend(0.75,0.75,0.99,0.99)
leg.AddEntry(fr1, "nominal, x_{e}=6.9 mm", "l")
leg.AddEntry(fr2, "+5%,      x_{e}=5.8 mm", "l")
leg.AddEntry(fr3, "+15%,    x_{e}=3.8 mm", "l")
leg.AddEntry(fr4, "+20%,    x_{e}=2.8 mm", "l")
leg.AddEntry(fr5, "+30%,    x_{e}=1.4 mm", "l")

leg.Draw("same")

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

innerLine.Draw("same")
outerLine.Draw("same")
magicLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")
pt3.Draw("same")
leg.Draw("same")

c.SaveAs("comparison.eps")
