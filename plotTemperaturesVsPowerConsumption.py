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


#OneLoop = True
OneLoop = False

# change Vresistors -- > changes P
runnumber  = [2, 13, 9, 12]
t_lauda    = [16, 16, 16, 16]
t_box      = [18.3, 16.9, 18.3, 16.9]
Vresistors = [0.0, 7.5, 10.0, 15.0]
power      = [ (40. * v/Vresistors[2]*v/Vresistors[2]) for v in Vresistors]  

if (OneLoop):
    runnumber  = [26, 24, 25]
    t_lauda    = [20, 20, 20]
    t_box      = [19.9, 20.0, 19.9]
    Vresistors = [7.5, 10.0, 15.0]
    power      = [ (40. * v/Vresistors[1]*v/Vresistors[1]) for v in Vresistors]  

    
t1 = ROOT.TLatex( 0.18, 0.84,'water flux = 0.75 cm^{3}s^{-1}' )
t2 = ROOT.TLatex( 0.18, 0.80,'T_{in} = %.2d ^{o}C'%(t_lauda[0]) )
t1.SetNDC()
t2.SetNDC()
t1.SetTextSize(0.02)
t2.SetTextSize(0.02)


#-- output dir for plots
plotsdirname = 'plots/1Loop/vsPower'
if (OneLoop == False):
    plotsdirname = 'plots/2Loops/vsPower'
if ( os.path.exists(plotsdirname) == False ) :
    os.mkdir(plotsdirname)
shutil.copy('index.php', '%s'%plotsdirname)

# -- output file
if (OneLoop == False):
    fout = ROOT.TFile( 'plotsVsPower_2Loops.root', 'recreate' )
if (OneLoop == True):
    fout = ROOT.TFile( 'plotsVsPower_1Loop.root', 'recreate' )



#plots
h_T_spread = {}
for irun,run in enumerate(runnumber):
    h_T_spread[irun] = ROOT.TH1F('h_T_spread_run%03d'%run,'h_T_spread_run%03d'%run,400,0,40)     

g_T_spread_vs_power = ROOT.TGraph()
g_T_spread_vs_power.SetName('g_T_spread_vs_power')
g_maxDeltaT_vs_power = ROOT.TGraph()
g_maxDeltaT_vs_power.SetName('g_maxDeltaT_vs_power')
   
g_TminusTin_vs_power = {}
g_TminusTout_vs_power = {}

for ie in range(0,5):
    g_TminusTin_vs_power[ie]  = {}
    g_TminusTout_vs_power[ie] = {}
    for it in range(0,16):
        g_TminusTin_vs_power[ie][it] = ROOT.TGraph()
        g_TminusTout_vs_power[ie][it] = ROOT.TGraph()

t_in = 0

for irun,run in enumerate(runnumber):
    filename = 'plots_run%03d.root'%run
    print filename
    f = ROOT.TFile.Open(filename)
       
    h_temp = {}
    for ie in range(0,5):
        h_temp[ie] = []
        nt = 16
        if (ie==4): nt = 4
        for it in range(0,nt):
            h_temp[ie].append(f.Get('h_temp_Expander%d_%d'%(ie+1,it)))


    t_in  =  h_temp[4][3].GetMean()
    t_out =  h_temp[4][0].GetMean()

    tmin = 999.;
    tmax = -999.;
    
    for ie in range(0,5):
        nt = 16
        if (ie==4): nt = 4
        for it in range(0,nt):
            if (h_temp[ie][it].GetMean()==0): continue
            if (ie == 2 and it == 15): continue #termometro bacato
            g_TminusTin_vs_power[ie][it].SetPoint(irun, power[irun], h_temp[ie][it].GetMean()-t_in ) 
            g_TminusTout_vs_power[ie][it].SetPoint(irun, power[irun], h_temp[ie][it].GetMean()-t_out ) 

            if (ie<4):
                h_T_spread[irun].Fill(h_temp[ie][it].GetMean())
                if ( h_temp[ie][it].GetMean() < tmin ):
                    tmin = h_temp[ie][it].GetMean()
                if ( h_temp[ie][it].GetMean() > tmax ):
                    tmax = h_temp[ie][it].GetMean()
                
    g_T_spread_vs_power.SetPoint(irun,power[irun],h_T_spread[irun].GetRMS())
    g_maxDeltaT_vs_power.SetPoint(irun, power[irun], tmax - tmin)



leg = ROOT.TLegend(0.75,0.75,0.89,0.89)

#plotting
c_TminusTin_vs_power = ROOT.TCanvas('c_TminusTin_vs_power','c_TminusTin_vs_power',1200,500)
c_TminusTin_vs_power.Divide(4,1)
miny = g_TminusTin_vs_power[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTin_vs_power[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTin_vs_power.cd(ie+1)
    c_TminusTin_vs_power.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTin_vs_power[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTin_vs_power[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTin_vs_power[ie][it].GetXaxis().SetTitle('SiPM power consumption (mW)')
        g_TminusTin_vs_power[ie][it].SetMarkerStyle(20)
        g_TminusTin_vs_power[ie][it].SetMarkerSize(0.5)
        g_TminusTin_vs_power[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTin_vs_power[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTin_vs_power[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTin_vs_power[ie][it].Draw('apl')
            g_TminusTin_vs_power[ie][it].GetXaxis().SetLimits(0,100)
            g_TminusTin_vs_power[ie][it].Draw('apl')
        else:
            g_TminusTin_vs_power[ie][it].Draw('plsame')
            
#raw_input('ok?')


c_TminusTout_vs_power = ROOT.TCanvas('c_TminusTout_vs_power','c_TminusTout_vs_power',1200,500)
c_TminusTout_vs_power.Divide(4,1)
miny = g_TminusTout_vs_power[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTout_vs_power[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTout_vs_power.cd(ie+1)
    c_TminusTout_vs_power.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTout_vs_power[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTout_vs_power[ie][it].GetYaxis().SetTitle('T - T_{out} (#circ C)')
        g_TminusTout_vs_power[ie][it].GetXaxis().SetTitle('SiPM power consumption (mW)')
        g_TminusTout_vs_power[ie][it].SetMarkerStyle(20)
        g_TminusTout_vs_power[ie][it].SetMarkerSize(0.5)
        g_TminusTout_vs_power[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTout_vs_power[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTout_vs_power[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTout_vs_power[ie][it].Draw('apl')
            g_TminusTout_vs_power[ie][it].GetXaxis().SetLimits(0,100)
            g_TminusTout_vs_power[ie][it].Draw('apl')
            t1.Draw('same')
            t2.Draw('same')
        else:
            g_TminusTout_vs_power[ie][it].Draw('plsame')
            t1.Draw('same')
            t2.Draw('same')
#raw_input('ok?')




for irun,run in enumerate(runnumber):
    ccc = ROOT.TCanvas('c_T_spread_run%03d'%run,'c_T_spread_run%03d'%run,500,500) 
    h_T_spread[irun].Draw()
    t1.Draw('same')
    t2.Draw('same')
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.png')
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.pdf')

   
c_T_spread_vs_power = ROOT.TCanvas('c_T_spread_vs_power','c_T_spread_vs_power',500,500)
c_T_spread_vs_power.SetLeftMargin(0.15)
c_T_spread_vs_power.SetBottomMargin(0.13)
miny = 0.0
maxy = g_T_spread_vs_power.GetHistogram().GetMaximum()+0.2
g_T_spread_vs_power.GetXaxis().SetTitle('SiPM power consumption (mW)')
g_T_spread_vs_power.GetYaxis().SetTitle('RMS(T) (#circ C)')
g_T_spread_vs_power.GetYaxis().SetTitleOffset(1.2)
g_T_spread_vs_power.GetYaxis().SetRangeUser(miny,maxy)
g_T_spread_vs_power.SetMarkerStyle(20)
g_T_spread_vs_power.SetMarkerSize(0.5)
g_T_spread_vs_power.SetMarkerColor(ROOT.kBlue)
g_T_spread_vs_power.SetLineColor(ROOT.kBlue)
g_T_spread_vs_power.SetLineStyle(2)
g_T_spread_vs_power.Draw('apl')
g_T_spread_vs_power.GetXaxis().SetLimits(0.0,100)
g_T_spread_vs_power.Draw('apl')
t1.Draw('same')
t2.Draw('same')
c_T_spread_vs_power.Update()
#raw_input('ok?')



c_maxDeltaT_vs_power = ROOT.TCanvas('c_maxDeltaT_vs_power','c_maxDeltaT_vs_power',500,500)
c_maxDeltaT_vs_power.SetLeftMargin(0.15)
c_maxDeltaT_vs_power.SetBottomMargin(0.13)
miny = 0.0
maxy = g_maxDeltaT_vs_power.GetHistogram().GetMaximum()+0.2
g_maxDeltaT_vs_power.GetXaxis().SetTitle('SiPM power consumption (mW)')
g_maxDeltaT_vs_power.GetYaxis().SetTitle('max(#Delta T) (#circ C)')
g_maxDeltaT_vs_power.GetYaxis().SetTitleOffset(1.2)
g_maxDeltaT_vs_power.GetYaxis().SetRangeUser(miny,maxy)
g_maxDeltaT_vs_power.SetMarkerStyle(20)
g_maxDeltaT_vs_power.SetMarkerSize(0.5)
g_maxDeltaT_vs_power.SetMarkerColor(ROOT.kBlue)
g_maxDeltaT_vs_power.SetLineColor(ROOT.kBlue)
g_maxDeltaT_vs_power.SetLineStyle(2)
g_maxDeltaT_vs_power.Draw('apl')
g_maxDeltaT_vs_power.GetXaxis().SetLimits(0.0,100)
g_maxDeltaT_vs_power.Draw('apl')
t1.Draw('same')
t2.Draw('same')
c_maxDeltaT_vs_power.Update()
#raw_input('ok?')


for canvas in c_TminusTin_vs_power, c_TminusTout_vs_power, c_T_spread_vs_power, c_maxDeltaT_vs_power:
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.png')
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.pdf')


fout.cd()
g_maxDeltaT_vs_power.Write()
g_T_spread_vs_power.Write() 
