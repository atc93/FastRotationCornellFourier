# For all the styling

from importAll import *

def setCanvasStyle( c ):
    r.gStyle.SetOptStat(0);
    r.gStyle.SetOptFit(0);
    r.gStyle.SetOptTitle(1);
    r.gStyle.SetStatX(1);
    r.gStyle.SetStatY(1);
    r.gStyle.SetStatH(0.1);
    r.gStyle.SetStatW(0.15);
    r.gPad.SetTicks(1);
    c.SetLeftMargin(0.15);
    c.SetRightMargin(0.05);
    c.SetTopMargin(0.075);
    c.SetBottomMargin(0.15);

def setHistogramStyle( h, title, xAxisTitle, yAxisTitle ):
    h.SetTitle( title );
    h.GetXaxis().CenterTitle();
    h.GetXaxis().SetTitle(xAxisTitle);
    h.GetYaxis().CenterTitle();
    h.GetYaxis().SetTitle(yAxisTitle);
    h.GetXaxis().SetTitleOffset(1.4);
    h.GetYaxis().SetTitleOffset(1.4);
    h.GetXaxis().SetTitleSize(0.055);
    h.GetXaxis().SetLabelSize(0.05);
    h.GetYaxis().SetTitleSize(0.055);
    h.GetYaxis().SetLabelSize(0.05);
    h.SetLineColor(4);
    h.SetLineWidth(2)

def setCollimatorAperture( pt, pt2 ):
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
