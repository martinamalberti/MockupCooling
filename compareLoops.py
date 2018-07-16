#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time


import ROOT

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(1110)
ROOT.gStyle.SetStatX(0.89);
ROOT.gStyle.SetStatY(0.89);
ROOT.gStyle.SetStatW(0.4);   
ROOT.gStyle.SetStatH(0.35);   
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetFitFormat("4.3g")
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)


ROOT.gStyle.SetLabelSize(0.05,'X')
ROOT.gStyle.SetLabelSize(0.05,'Y')
ROOT.gStyle.SetLabelSize(0.05,'Z')
ROOT.gStyle.SetTitleSize(0.05,'X')
ROOT.gStyle.SetTitleSize(0.05,'Y')
ROOT.gStyle.SetTitleSize(0.05,'Z')
ROOT.gStyle.SetTitleOffset(1.0,'X')
ROOT.gStyle.SetTitleOffset(1.0,'Y')
ROOT.gStyle.SetPadLeftMargin(0.15)

files1 = ['plotsVsTcoolant_1Loop.root','plotsVsPower_1Loop.root', 'plotsVsFlux_1Loop.root','plots_run024.root' ]
files2 = ['plotsVsTcoolant_2Loops.root', 'plotsVsPower_2Loops.root', 'plotsVsFlux_2Loops.root','plots_run020.root']

leg = ROOT.TLegend(0.75,0.75,0.89, 0.89)
leg.SetBorderSize(0)



# --- vs Tin
c_maxDeltaT_vs_Tin_1or2Loops = ROOT.TCanvas('c_maxDeltaT_vs_Tin_1or2Loops','c_maxDeltaT_vs_Tin_1or2Loops',500,500)
c_spreadT_vs_Tin_1or2Loops = ROOT.TCanvas('c_spreadT_vs_Tin_1or2Loops','c_spreadT_vs_Tin_1or2Loops',500,500)
for i, filename in enumerate([files1[0], files2[0]]):
    f = ROOT.TFile.Open(filename)
    gmax = f.Get('g_maxDeltaT_vs_Tin')
    gspread = f.Get('g_T_spread_vs_Tin')
    if (i==0):
        c_maxDeltaT_vs_Tin_1or2Loops.cd()
        gmax.GetHistogram().GetYaxis().SetRangeUser(0,2.0)
        gmax.Draw('apl')
        c_spreadT_vs_Tin_1or2Loops.cd()
        gspread.GetHistogram().GetYaxis().SetRangeUser(0,1.0)
        gspread.Draw('apl')
        leg.AddEntry(gspread,'one loop', 'PL')
    else:
        c_maxDeltaT_vs_Tin_1or2Loops.cd()
        gmax.SetMarkerColor(ROOT.kGreen+2)
        gmax.SetLineColor(ROOT.kGreen+2)
        gmax.Draw('plsame')
        c_spreadT_vs_Tin_1or2Loops.cd()
        gspread.SetMarkerColor(ROOT.kGreen+2)
        gspread.SetLineColor(ROOT.kGreen+2)
        gspread.Draw('plsame')
        leg.AddEntry(gspread,'two loops', 'PL')


c_maxDeltaT_vs_Tin_1or2Loops.cd()
leg.Draw('same')
c_spreadT_vs_Tin_1or2Loops.cd()
leg.Draw('same')


# --- vs Power consumption
c_maxDeltaT_vs_power_1or2Loops = ROOT.TCanvas('c_maxDeltaT_vs_power_1or2Loops','c_maxDeltaT_vs_power_1or2Loops',500,500)
c_spreadT_vs_power_1or2Loops = ROOT.TCanvas('c_spreadT_vs_power_1or2Loops','c_spreadT_vs_power_1or2Loops',500,500)
for i, filename in enumerate([files1[1], files2[1]]):
    f = ROOT.TFile.Open(filename)
    gmax = f.Get('g_maxDeltaT_vs_power')
    gspread = f.Get('g_T_spread_vs_power')
    if (i==0):
        c_maxDeltaT_vs_power_1or2Loops.cd()
        gmax.GetHistogram().GetYaxis().SetRangeUser(0,4.0)
        gmax.Draw('apl')
        c_spreadT_vs_power_1or2Loops.cd()
        gspread.GetHistogram().GetYaxis().SetRangeUser(0,2.0)
        gspread.Draw('apl')
    else:
        c_maxDeltaT_vs_power_1or2Loops.cd()
        gmax.SetMarkerColor(ROOT.kGreen+2)
        gmax.SetLineColor(ROOT.kGreen+2)
        gmax.Draw('plsame')
        c_spreadT_vs_power_1or2Loops.cd()
        gspread.SetMarkerColor(ROOT.kGreen+2)
        gspread.SetLineColor(ROOT.kGreen+2)
        gspread.Draw('plsame')
        

c_maxDeltaT_vs_power_1or2Loops.cd()
leg.Draw('same')
c_spreadT_vs_power_1or2Loops.cd()
leg.Draw('same')

# --- vs flux
c_maxDeltaT_vs_flux_1or2Loops = ROOT.TCanvas('c_maxDeltaT_vs_flux_1or2Loops','c_maxDeltaT_vs_flux_1or2Loops',500,500)
c_spreadT_vs_flux_1or2Loops = ROOT.TCanvas('c_spreadT_vs_flux_1or2Loops','c_spreadT_vs_flux_1or2Loops',500,500)
for i, filename in enumerate([files1[2], files2[2]]):
    f = ROOT.TFile.Open(filename)
    gmax = f.Get('g_maxDeltaT_vs_flux')
    gspread = f.Get('g_T_spread_vs_flux')
    if (i==0):
        c_maxDeltaT_vs_flux_1or2Loops.cd()
        gmax.GetHistogram().GetYaxis().SetRangeUser(0,2.0)
        gmax.GetHistogram().GetXaxis().SetRangeUser(0.5,0.8)
        gmax.Draw('apl')
        c_spreadT_vs_flux_1or2Loops.cd()
        gspread.GetHistogram().GetXaxis().SetRangeUser(0.5,0.8)
        gspread.GetHistogram().GetYaxis().SetRangeUser(0,1.0)
        gspread.Draw('apl')
    else:
        c_maxDeltaT_vs_flux_1or2Loops.cd()
        gmax.SetMarkerColor(ROOT.kGreen+2)
        gmax.SetLineColor(ROOT.kGreen+2)
        gmax.Draw('plsame')
        c_spreadT_vs_flux_1or2Loops.cd()
        gspread.SetMarkerColor(ROOT.kGreen+2)
        gspread.SetLineColor(ROOT.kGreen+2)
        gspread.Draw('plsame')
        

c_maxDeltaT_vs_flux_1or2Loops.cd()
leg.Draw('same')
c_spreadT_vs_flux_1or2Loops.cd()
leg.Draw('same')



# -- temperature uniformity vs phi
#p = []
#c_temperatures_profile_1or2Loops = ROOT.TCanvas('c_temperatures_profile_1or2Loops','c_temperatures_profile_1or2Loops')
#for i, filename in enumerate([files1[3], files2[3]]):
#    f = ROOT.TFile.Open(filename)
#    p.append(f.Get('p_temperatures').Clone('p%d'%i))
#    if (i==0):
#        #c_temperatures_profile_1or2Loops.cd()
#        p[i].GetYaxis().SetRangeUser(20,25)
#        p[i].SetMarkerColor(ROOT.kBlue)
#        p[i].SetLineColor(ROOT.kBlue)
#        p[i].Draw('')
#    else:
#        p[i].SetMarkerColor(ROOT.kGreen+2)
#        p[i].SetLineColor(ROOT.kGreen+2)
#        #p.Draw('same')
        

##c_temperatures_profile_1or2Loops.cd()


# -- temperature uniformity vs phi
p = {}
c_temperatures_profile_1or2Loops = ROOT.TCanvas('c_temperatures_profile_1or2Loops','c_temperatures_profile_1or2Loops',1200,350)
c_temperatures_profile_1or2Loops.SetGridx()
c_temperatures_profile_1or2Loops.SetGridy()

#for i, filename in enumerate([files1[3], files2[3]]):
#    f = ROOT.TFile.Open(filename)
#    p.append(f.Get('p_temperatures').Clone('p%d'%i))

f1 =  ROOT.TFile.Open(files1[3])
f2 =  ROOT.TFile.Open(files2[3])
p[0] = f1.Get('p_temperatures')   
p[1] =  f2.Get('p_temperatures')
c_temperatures_profile_1or2Loops.cd()
p[0].GetYaxis().SetRangeUser(21,25)
p[0].SetMarkerColor(ROOT.kBlue)
p[0].SetLineColor(ROOT.kBlue)
p[0].Draw('')
p[1].SetMarkerColor(ROOT.kGreen+2)
p[1].SetLineColor(ROOT.kGreen+2)
p[1].Draw('same')
leg.Draw('same')        

raw_input('ok?')





for canvas in c_maxDeltaT_vs_Tin_1or2Loops, c_spreadT_vs_Tin_1or2Loops,c_maxDeltaT_vs_power_1or2Loops, c_spreadT_vs_power_1or2Loops, c_maxDeltaT_vs_flux_1or2Loops, c_spreadT_vs_flux_1or2Loops, c_temperatures_profile_1or2Loops:
    canvas.SaveAs((canvas.GetName()).replace('c_','')+'.png')
    canvas.SaveAs((canvas.GetName()).replace('c_','')+'.pdf')
