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


resistorsON = True
OneLoop = True

# P = 0 mW
runnumber = [3, 6, 2, 4, 5]
t_lauda   = [12, 14, 16, 25, 30]
t_box     = [16.3, 18.7, 18.3, 21.8, 24.1]
plotsdirname = 'plots/resistorsOFF'

# P = 40 mW
if (resistorsON):
    if (OneLoop == False):
        runnumber = [8, 7, 9, 20, 10, 11]
        t_lauda   = [12, 14, 16, 20, 25, 30]
        t_box     = [13.5, 15.1, 16.4, 20.1, 25, 27.5]
        plotsdirname = 'plots/2Loops/vsWaterTemperature'
    else:
        runnumber = [27, 28, 29, 24, 30]
        t_lauda   = [12, 14, 16, 20, 24]
        t_box     = [13.2, 14.8, 16.4, 19.9, 22.9]
        plotsdirname = 'plots/1Loop/vsWaterTemperature'

    
if ( os.path.exists(plotsdirname) == False ) :
    os.mkdir(plotsdirname)
shutil.copy('index.php', '%s'%plotsdirname)


# -- output file
if (OneLoop == False):
    fout = ROOT.TFile( 'plotsVsTcoolant_2Loops.root', 'recreate' )
if (OneLoop == True):
    fout = ROOT.TFile( 'plotsVsTcoolant_1Loop.root', 'recreate' )

    

# -- plots
h_TminusTin_spread = {}
h_T_spread = {}
for irun,run in enumerate(runnumber):
    h_TminusTin_spread[irun] = ROOT.TH1F('h_TminusTin_spread_run%03d'%run,'h_TminusTin_spread_run%03d'%run,400,-5,5)     
    h_T_spread[irun] = ROOT.TH1F('h_T_spread_run%03d'%run,'h_T_spread_run%03d'%run,400,0,40)     

g_TminusTin_spread_vs_Tin = ROOT.TGraph()
g_T_spread_vs_Tin = ROOT.TGraph()
g_T_spread_vs_Tin.SetName('g_T_spread_vs_Tin')
g_maxDeltaT_vs_Tin = ROOT.TGraph()
g_maxDeltaT_vs_Tin.SetName('g_maxDeltaT_vs_Tin')

g_TminusTin_vs_Tin = {}
g_TminusTin_vs_Tout = {}
g_TminusTin_vs_Tbox = {}

g_TminusTout_vs_Tin = {}
g_TminusTout_vs_Tout = {}
g_TminusTout_vs_Tbox = {}

for ie in range(0,5):
    g_TminusTin_vs_Tin[ie]  = {}
    g_TminusTin_vs_Tout[ie] = {}
    g_TminusTin_vs_Tbox[ie] = {}
    g_TminusTout_vs_Tin[ie]  = {}
    g_TminusTout_vs_Tout[ie] = {}
    g_TminusTout_vs_Tbox[ie] = {}
    for it in range(0,16):
        g_TminusTin_vs_Tin[ie][it] = ROOT.TGraph()
        g_TminusTin_vs_Tout[ie][it] = ROOT.TGraph()
        g_TminusTin_vs_Tbox[ie][it] = ROOT.TGraph()
        g_TminusTout_vs_Tin[ie][it] = ROOT.TGraph()
        g_TminusTout_vs_Tout[ie][it] = ROOT.TGraph()
        g_TminusTout_vs_Tbox[ie][it] = ROOT.TGraph()
        
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
            g_TminusTin_vs_Tin[ie][it].SetPoint(irun, t_in, h_temp[ie][it].GetMean()-t_in ) 
            g_TminusTin_vs_Tout[ie][it].SetPoint(irun, t_out, h_temp[ie][it].GetMean()-t_in ) 
            g_TminusTin_vs_Tbox[ie][it].SetPoint(irun, t_box[irun], h_temp[ie][it].GetMean()-t_in )
            g_TminusTout_vs_Tin[ie][it].SetPoint(irun, t_in, h_temp[ie][it].GetMean()-t_out ) 
            g_TminusTout_vs_Tout[ie][it].SetPoint(irun, t_out, h_temp[ie][it].GetMean()-t_out ) 
            g_TminusTout_vs_Tbox[ie][it].SetPoint(irun, t_box[irun], h_temp[ie][it].GetMean()-t_out ) 

            if (ie<4):
                h_TminusTin_spread[irun].Fill(h_temp[ie][it].GetMean()-t_in)
                h_T_spread[irun].Fill(h_temp[ie][it].GetMean())
                if ( h_temp[ie][it].GetMean() < tmin ):
                    tmin = h_temp[ie][it].GetMean()
                if ( h_temp[ie][it].GetMean() > tmax ):
                    tmax = h_temp[ie][it].GetMean()
                
    g_TminusTin_spread_vs_Tin.SetPoint(irun,t_in,h_TminusTin_spread[irun].GetRMS())
    g_T_spread_vs_Tin.SetPoint(irun,t_in,h_T_spread[irun].GetRMS())
    g_maxDeltaT_vs_Tin.SetPoint(irun, t_in, tmax - tmin)
    
leg = ROOT.TLegend(0.75,0.75,0.89,0.89)

#plotting
c_TGBPdiff_vs_Tin = ROOT.TCanvas('c_TGBPdiff_vs_Tin','c_TGBPdiff_vs_Tin',500,500)
c_TGBPdiff_vs_Tin.SetLeftMargin(0.15)
for it in range(0,4):
    g_TminusTin_vs_Tin[4][it].GetXaxis().SetRangeUser(10,31)
    g_TminusTin_vs_Tin[4][it].GetYaxis().SetRangeUser(-2,2)
    g_TminusTin_vs_Tin[4][it].GetXaxis().SetTitle('T_{in} (#circ C)')
    g_TminusTin_vs_Tin[4][it].GetYaxis().SetTitle('T-T_{in} (#circ C)')
    g_TminusTin_vs_Tin[4][it].SetMarkerStyle(20)
    g_TminusTin_vs_Tin[4][it].SetMarkerSize(0.5)
    g_TminusTin_vs_Tin[4][it].SetMarkerColor(it+1)
    g_TminusTin_vs_Tin[4][it].SetLineColor(it+1)
    g_TminusTin_vs_Tin[4][it].SetLineStyle(2)
    leg.AddEntry(g_TminusTin_vs_Tin[4][it],'GBP%d'%(it*2+1),'PL')
    if (it == 0):
        g_TminusTin_vs_Tin[4][it].Draw('apl')
    else:
        g_TminusTin_vs_Tin[4][it].Draw('plsame')
leg.Draw('same')
#raw_input('ok?')

c_TGBPdiff_vs_Tbox = ROOT.TCanvas('c_TGBPdiff_vs_Tbox','c_TGBPdiff_vs_Tbox',500,500)
c_TGBPdiff_vs_Tbox.SetLeftMargin(0.15)
for it in range(0,4):
    g_TminusTin_vs_Tbox[4][it].GetXaxis().SetRangeUser(10,31)
    g_TminusTin_vs_Tbox[4][it].GetYaxis().SetRangeUser(-2,2)
    g_TminusTin_vs_Tbox[4][it].GetXaxis().SetTitle('T_{box} (#circ C)')
    g_TminusTin_vs_Tbox[4][it].GetYaxis().SetTitle('T-T_{in} (#circ C)')
    g_TminusTin_vs_Tbox[4][it].SetMarkerStyle(20)
    g_TminusTin_vs_Tbox[4][it].SetMarkerSize(0.5)
    g_TminusTin_vs_Tbox[4][it].SetMarkerColor(it+1)
    g_TminusTin_vs_Tbox[4][it].SetLineColor(it+1)
    g_TminusTin_vs_Tbox[4][it].SetLineStyle(2)
    if (it == 0):
        g_TminusTin_vs_Tbox[4][it].Draw('apl')
    else:
        g_TminusTin_vs_Tbox[4][it].Draw('plsame')
leg.Draw('same')
#raw_input('ok?')


            
c_TminusTin_vs_Tin = ROOT.TCanvas('c_TminusTin_vs_Tin','c_TminusTin_vs_Tin',1200,500)
c_TminusTin_vs_Tin.Divide(4,1)
miny = g_TminusTin_vs_Tin[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTin_vs_Tin[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTin_vs_Tin.cd(ie+1)
    c_TminusTin_vs_Tin.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTin_vs_Tin[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTin_vs_Tin[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTin_vs_Tin[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTin_vs_Tin[ie][it].GetXaxis().SetTitle('T_{in} (#circ C)')
        g_TminusTin_vs_Tin[ie][it].SetMarkerStyle(20)
        g_TminusTin_vs_Tin[ie][it].SetMarkerSize(0.5)
        g_TminusTin_vs_Tin[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTin_vs_Tin[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTin_vs_Tin[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTin_vs_Tin[ie][it].Draw('apl')
        else:
            g_TminusTin_vs_Tin[ie][it].Draw('plsame')
#raw_input('ok?')


c_TminusTin_vs_Tout = ROOT.TCanvas('c_TminusTin_vs_Tout','c_TminusTin_vs_Tout',1200,500)
c_TminusTin_vs_Tout.Divide(4,1)
miny = g_TminusTin_vs_Tout[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTin_vs_Tout[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTin_vs_Tout.cd(ie+1)
    c_TminusTin_vs_Tout.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTin_vs_Tout[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTin_vs_Tout[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTin_vs_Tout[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTin_vs_Tout[ie][it].GetXaxis().SetTitle('T_{out} (#circ C)')
        g_TminusTin_vs_Tout[ie][it].SetMarkerStyle(20)
        g_TminusTin_vs_Tout[ie][it].SetMarkerSize(0.5)
        g_TminusTin_vs_Tout[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTin_vs_Tout[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTin_vs_Tout[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTin_vs_Tout[ie][it].Draw('apl')
        else:
            g_TminusTin_vs_Tout[ie][it].Draw('plsame')
#raw_input('ok?')



c_TminusTin_vs_Tbox = ROOT.TCanvas('c_TminusTin_vs_Tbox','c_TminusTin_vs_Tbox',1200,500)
c_TminusTin_vs_Tbox.Divide(4,1)
miny = g_TminusTin_vs_Tbox[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTin_vs_Tbox[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTin_vs_Tbox.cd(ie+1)
    c_TminusTin_vs_Tbox.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTin_vs_Tbox[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTin_vs_Tbox[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTin_vs_Tbox[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTin_vs_Tbox[ie][it].GetXaxis().SetTitle('T_{box} (#circ C)')
        g_TminusTin_vs_Tbox[ie][it].SetMarkerStyle(20)
        g_TminusTin_vs_Tbox[ie][it].SetMarkerSize(0.5)
        g_TminusTin_vs_Tbox[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTin_vs_Tbox[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTin_vs_Tbox[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTin_vs_Tbox[ie][it].Draw('apl')
        else:
            g_TminusTin_vs_Tbox[ie][it].Draw('plsame')
#raw_input('ok?')



c_TminusTout_vs_Tin = ROOT.TCanvas('c_TminusTout_vs_Tin','c_TminusTout_vs_Tin',1200,500)
c_TminusTout_vs_Tin.Divide(4,1)
miny = g_TminusTout_vs_Tin[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTout_vs_Tin[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTout_vs_Tin.cd(ie+1)
    c_TminusTout_vs_Tin.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTout_vs_Tin[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTout_vs_Tin[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTout_vs_Tin[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTout_vs_Tin[ie][it].GetXaxis().SetTitle('T_{in} (#circ C)')
        g_TminusTout_vs_Tin[ie][it].SetMarkerStyle(20)
        g_TminusTout_vs_Tin[ie][it].SetMarkerSize(0.5)
        g_TminusTout_vs_Tin[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTout_vs_Tin[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTout_vs_Tin[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTout_vs_Tin[ie][it].Draw('apl')
        else:
            g_TminusTout_vs_Tin[ie][it].Draw('plsame')
#raw_input('ok?')


c_TminusTout_vs_Tout = ROOT.TCanvas('c_TminusTout_vs_Tout','c_TminusTout_vs_Tout',1200,500)
c_TminusTout_vs_Tout.Divide(4,1)
miny = g_TminusTout_vs_Tout[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTout_vs_Tout[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTout_vs_Tout.cd(ie+1)
    c_TminusTout_vs_Tout.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTout_vs_Tout[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTout_vs_Tout[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTout_vs_Tout[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTout_vs_Tout[ie][it].GetXaxis().SetTitle('T_{out} (#circ C)')
        g_TminusTout_vs_Tout[ie][it].SetMarkerStyle(20)
        g_TminusTout_vs_Tout[ie][it].SetMarkerSize(0.5)
        g_TminusTout_vs_Tout[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTout_vs_Tout[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTout_vs_Tout[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTout_vs_Tout[ie][it].Draw('apl')
        else:
            g_TminusTout_vs_Tout[ie][it].Draw('plsame')
#raw_input('ok?')


c_TminusTout_vs_Tbox = ROOT.TCanvas('c_TminusTout_vs_Tbox','c_TminusTout_vs_Tbox',1200,500)
c_TminusTout_vs_Tbox.Divide(4,1)
miny = g_TminusTout_vs_Tbox[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTout_vs_Tbox[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTout_vs_Tbox.cd(ie+1)
    c_TminusTout_vs_Tbox.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTout_vs_Tbox[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTout_vs_Tbox[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTout_vs_Tbox[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTout_vs_Tbox[ie][it].GetXaxis().SetTitle('T_{box} (#circ C)')
        g_TminusTout_vs_Tbox[ie][it].SetMarkerStyle(20)
        g_TminusTout_vs_Tbox[ie][it].SetMarkerSize(0.5)
        g_TminusTout_vs_Tbox[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTout_vs_Tbox[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTout_vs_Tbox[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTout_vs_Tbox[ie][it].Draw('apl')
        else:
            g_TminusTout_vs_Tbox[ie][it].Draw('plsame')
#raw_input('ok?')



#c_spread = []
for irun,run in enumerate(runnumber):
    cc = ROOT.TCanvas('c_TminusTin_spread_run%03d'%run,'c_TminusTin_spread_run%03d'%run,500,500) 
    h_TminusTin_spread[irun].Draw()
    cc.SaveAs(plotsdirname+'/'+(cc.GetName()).replace('c_','')+'.png')
    cc.SaveAs(plotsdirname+'/'+(cc.GetName()).replace('c_','')+'.pdf')

    ccc = ROOT.TCanvas('c_T_spread_run%03d'%run,'c_T_spread_run%03d'%run,500,500) 
    h_T_spread[irun].Draw()
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.png')
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.pdf')

    
c_TminusTin_spread_vs_Tin = ROOT.TCanvas('c_TminusTin_spread_vs_Tin','c_TminusTin_spread_vs_Tin',500,500)
c_TminusTin_spread_vs_Tin.SetLeftMargin(0.15)
c_TminusTin_spread_vs_Tin.SetBottomMargin(0.13)
miny = 0.0
maxy = g_TminusTin_spread_vs_Tin.GetHistogram().GetMaximum()+0.2
g_TminusTin_spread_vs_Tin.GetXaxis().SetTitle('T_{in} (#circ C)')
g_TminusTin_spread_vs_Tin.GetYaxis().SetTitle('RMS(T - T_{in}) (#circ C)')
g_TminusTin_spread_vs_Tin.GetYaxis().SetTitleOffset(1.2)
g_TminusTin_spread_vs_Tin.GetYaxis().SetRangeUser(miny,maxy)
g_TminusTin_spread_vs_Tin.SetMarkerStyle(20)
g_TminusTin_spread_vs_Tin.SetMarkerSize(0.5)
g_TminusTin_spread_vs_Tin.SetMarkerColor(ROOT.kBlue)
g_TminusTin_spread_vs_Tin.SetLineColor(ROOT.kBlue)
g_TminusTin_spread_vs_Tin.SetLineStyle(2)
g_TminusTin_spread_vs_Tin.Draw('apl')
#raw_input('ok?')


c_T_spread_vs_Tin = ROOT.TCanvas('c_T_spread_vs_Tin','c_T_spread_vs_Tin',500,500)
c_T_spread_vs_Tin.SetLeftMargin(0.15)
c_T_spread_vs_Tin.SetBottomMargin(0.13)
miny = 0.0
maxy = g_T_spread_vs_Tin.GetHistogram().GetMaximum()+0.2
g_T_spread_vs_Tin.GetXaxis().SetTitle('T_{in} (#circ C)')
g_T_spread_vs_Tin.GetYaxis().SetTitle('RMS(T) (#circ C)')
g_T_spread_vs_Tin.GetYaxis().SetTitleOffset(1.2)
g_T_spread_vs_Tin.GetYaxis().SetRangeUser(miny,maxy)
g_T_spread_vs_Tin.SetMarkerStyle(20)
g_T_spread_vs_Tin.SetMarkerSize(0.5)
g_T_spread_vs_Tin.SetMarkerColor(ROOT.kBlue)
g_T_spread_vs_Tin.SetLineColor(ROOT.kBlue)
g_T_spread_vs_Tin.SetLineStyle(2)
g_T_spread_vs_Tin.Draw('apl')
#raw_input('ok?')



c_maxDeltaT_vs_Tin = ROOT.TCanvas('c_maxDeltaT_vs_Tin','c_maxDeltaT_vs_Tin',500,500)
c_maxDeltaT_vs_Tin.SetLeftMargin(0.15)
c_maxDeltaT_vs_Tin.SetBottomMargin(0.13)
miny = 0.0
maxy = g_maxDeltaT_vs_Tin.GetHistogram().GetMaximum()+0.2
g_maxDeltaT_vs_Tin.GetXaxis().SetTitle('T_{in} (#circ C)')
g_maxDeltaT_vs_Tin.GetYaxis().SetTitle('max(#Delta T) (#circ C)')
g_maxDeltaT_vs_Tin.GetYaxis().SetTitleOffset(1.2)
g_maxDeltaT_vs_Tin.GetYaxis().SetRangeUser(miny,maxy)
g_maxDeltaT_vs_Tin.SetMarkerStyle(20)
g_maxDeltaT_vs_Tin.SetMarkerSize(0.5)
g_maxDeltaT_vs_Tin.SetMarkerColor(ROOT.kBlue)
g_maxDeltaT_vs_Tin.SetLineColor(ROOT.kBlue)
g_maxDeltaT_vs_Tin.SetLineStyle(2)
g_maxDeltaT_vs_Tin.Draw('apl')
#raw_input('ok?')


for canvas in c_TGBPdiff_vs_Tin, c_TGBPdiff_vs_Tbox, c_TminusTin_vs_Tin, c_TminusTin_vs_Tout, c_TminusTin_vs_Tbox, c_TminusTout_vs_Tin, c_TminusTout_vs_Tout, c_TminusTout_vs_Tbox, c_TminusTin_spread_vs_Tin, c_T_spread_vs_Tin, c_maxDeltaT_vs_Tin:
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.png')
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.pdf')



fout.cd()
g_T_spread_vs_Tin.Write()
g_maxDeltaT_vs_Tin.Write()


