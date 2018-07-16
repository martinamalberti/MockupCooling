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

ROOT.gStyle.SetLabelSize(0.04,'X')
ROOT.gStyle.SetLabelSize(0.04,'Y')
ROOT.gStyle.SetLabelSize(0.04,'Z')
ROOT.gStyle.SetTitleSize(0.04,'X')
ROOT.gStyle.SetTitleSize(0.04,'Y')
ROOT.gStyle.SetTitleSize(0.04,'Z')
ROOT.gStyle.SetTitleOffset(1.0,'X')
ROOT.gStyle.SetTitleOffset(1.0,'Y')


OneLoop = True
#OneLoop = False

if (OneLoop == False):
    #runnumber  = [15, 14, 9]
    #t_lauda    = [16, 16, 16]
    #t_box      = [16.9, 16.9, 16.4]
    #flux       = [0.58, 0.70, 0.75]

    runnumber  = [21, 20]
    t_lauda    = [20, 20]
    t_box      = [20.0, 20.1]
    flux       = [0.60, 0.75]

else:
    #runnumber  = [39, 38, 37,36]
    #t_lauda    = [16, 16, 16, 16]
    #t_box      = [17.8, 17.8, 17.8, 17.8]
    #flux       = [0.53, 0.65, 0.73, 0.76]
    
    runnumber  = [31, 32, 33,34]
    t_lauda    = [20, 20, 20, 20]
    t_box      = [19.9, 19.9, 19.9, 19.9]
    flux       = [0.53, 0.62, 0.70, 0.76]
    

t1 = ROOT.TLatex( 0.18, 0.84,'SiPM power = 40 mW' )
t2 = ROOT.TLatex( 0.18, 0.80,'T_{in} = %.2d ^{o}C'%(t_lauda[0]) )
t1.SetNDC()
t2.SetNDC()
t1.SetTextSize(0.02)
t2.SetTextSize(0.02)

# -- ouput dir for plots
plotsdirname = 'plots/1Loop/vsFlux'
if (OneLoop == False):
    plotsdirname = 'plots/2Loops/vsFlux'
if ( os.path.exists(plotsdirname) == False ) :
    os.mkdir(plotsdirname)
shutil.copy('index.php', '%s'%plotsdirname)



# -- output file
if (OneLoop == False):
    fout = ROOT.TFile( 'plotsVsFlux_2Loops.root', 'recreate' )
if (OneLoop == True):
    fout = ROOT.TFile( 'plotsVsFlux_1Loop.root', 'recreate' )



#plots
h_T_spread = {}
for irun,run in enumerate(runnumber):
    h_T_spread[irun] = ROOT.TH1F('h_T_spread_run%03d'%run,'h_T_spread_run%03d'%run,400,0,40)     

g_T_spread_vs_flux = ROOT.TGraph()
g_T_spread_vs_flux.SetName('g_T_spread_vs_flux')
g_maxDeltaT_vs_flux = ROOT.TGraph()
g_maxDeltaT_vs_flux.SetName('g_maxDeltaT_vs_flux')

g_TminusTin_vs_flux = {}
g_TminusTout_vs_flux = {}

for ie in range(0,5):
    g_TminusTin_vs_flux[ie]  = {}
    g_TminusTout_vs_flux[ie] = {}
    for it in range(0,16):
        g_TminusTin_vs_flux[ie][it] = ROOT.TGraph()
        g_TminusTout_vs_flux[ie][it] = ROOT.TGraph()
        
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
            g_TminusTin_vs_flux[ie][it].SetPoint(irun, flux[irun], h_temp[ie][it].GetMean()-t_in ) 
            g_TminusTout_vs_flux[ie][it].SetPoint(irun, flux[irun], h_temp[ie][it].GetMean()-t_out ) 

            if (ie<4):
                h_T_spread[irun].Fill(h_temp[ie][it].GetMean())
                if ( h_temp[ie][it].GetMean() < tmin ):
                    tmin = h_temp[ie][it].GetMean()
                if ( h_temp[ie][it].GetMean() > tmax ):
                    tmax = h_temp[ie][it].GetMean()
                
    g_T_spread_vs_flux.SetPoint(irun,flux[irun],h_T_spread[irun].GetRMS())
    g_maxDeltaT_vs_flux.SetPoint(irun, flux[irun], tmax - tmin)
    
leg = ROOT.TLegend(0.75,0.75,0.89,0.89)

#plotting
c_TminusTin_vs_flux = ROOT.TCanvas('c_TminusTin_vs_flux','c_TminusTin_vs_flux',1200,500)
c_TminusTin_vs_flux.Divide(4,1)
miny = g_TminusTin_vs_flux[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTin_vs_flux[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTin_vs_flux.cd(ie+1)
    c_TminusTin_vs_flux.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTin_vs_flux[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTin_vs_flux[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTin_vs_flux[ie][it].GetYaxis().SetTitle('T - T_{in} (#circ C)')
        g_TminusTin_vs_flux[ie][it].GetXaxis().SetTitle('flux (cm^{3}/s)')
        g_TminusTin_vs_flux[ie][it].SetMarkerStyle(20)
        g_TminusTin_vs_flux[ie][it].SetMarkerSize(0.5)
        g_TminusTin_vs_flux[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTin_vs_flux[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTin_vs_flux[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTin_vs_flux[ie][it].Draw('apl')
        else:
            g_TminusTin_vs_flux[ie][it].Draw('plsame')
#raw_input('ok?')


c_TminusTout_vs_flux = ROOT.TCanvas('c_TminusTout_vs_flux','c_TminusTout_vs_flux',1200,500)
c_TminusTout_vs_flux.Divide(4,1)
miny = g_TminusTout_vs_flux[0][0].GetHistogram().GetMinimum()-1.
maxy = g_TminusTout_vs_flux[0][0].GetHistogram().GetMaximum()+1.
for ie in range(0,4):
    c_TminusTout_vs_flux.cd(ie+1)
    c_TminusTout_vs_flux.cd(ie+1).SetLeftMargin(0.13)
    for it in range(0,16):
        g_TminusTout_vs_flux[ie][it].GetYaxis().SetRangeUser(miny,maxy)
        g_TminusTout_vs_flux[ie][it].GetXaxis().SetRangeUser(10,31)
        g_TminusTout_vs_flux[ie][it].GetYaxis().SetTitle('T - T_{out} (#circ C)')
        g_TminusTout_vs_flux[ie][it].GetXaxis().SetTitle('flux (cm^{3}/s)')
        g_TminusTout_vs_flux[ie][it].SetMarkerStyle(20)
        g_TminusTout_vs_flux[ie][it].SetMarkerSize(0.5)
        g_TminusTout_vs_flux[ie][it].SetMarkerColor(ROOT.kBlue)
        g_TminusTout_vs_flux[ie][it].SetLineColor(ROOT.kBlue)
        g_TminusTout_vs_flux[ie][it].SetLineStyle(2)
        if (it==0) :
            g_TminusTout_vs_flux[ie][it].Draw('apl')
        else:
            g_TminusTout_vs_flux[ie][it].Draw('plsame')
#raw_input('ok?')




for irun,run in enumerate(runnumber):
    ccc = ROOT.TCanvas('c_T_spread_run%03d'%run,'c_T_spread_run%03d'%run,500,500) 
    h_T_spread[irun].Draw()
    t1.Draw()
    t2.Draw()
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.png')
    ccc.SaveAs(plotsdirname+'/'+(ccc.GetName()).replace('c_','')+'.pdf')

   
c_T_spread_vs_flux = ROOT.TCanvas('c_T_spread_vs_flux','c_T_spread_vs_flux',500,500)
c_T_spread_vs_flux.SetLeftMargin(0.15)
c_T_spread_vs_flux.SetBottomMargin(0.13)
miny = 0.0
maxy = g_T_spread_vs_flux.GetHistogram().GetMaximum()+0.2
g_T_spread_vs_flux.GetXaxis().SetTitle('flux (cm^{3}/s)')
g_T_spread_vs_flux.GetYaxis().SetTitle('RMS(T) (#circ C)')
g_T_spread_vs_flux.GetYaxis().SetTitleOffset(1.2)
g_T_spread_vs_flux.GetYaxis().SetRangeUser(miny,maxy)
g_T_spread_vs_flux.SetMarkerStyle(20)
g_T_spread_vs_flux.SetMarkerSize(0.5)
g_T_spread_vs_flux.SetMarkerColor(ROOT.kBlue)
g_T_spread_vs_flux.SetLineColor(ROOT.kBlue)
g_T_spread_vs_flux.SetLineStyle(2)
g_T_spread_vs_flux.Draw('apl')
t1.Draw()
t2.Draw()
#raw_input('ok?')



c_maxDeltaT_vs_flux = ROOT.TCanvas('c_maxDeltaT_vs_flux','c_maxDeltaT_vs_flux',500,500)
c_maxDeltaT_vs_flux.SetLeftMargin(0.15)
c_maxDeltaT_vs_flux.SetBottomMargin(0.13)
miny = 0.0
maxy = g_maxDeltaT_vs_flux.GetHistogram().GetMaximum()+0.2
g_maxDeltaT_vs_flux.GetXaxis().SetTitle('flux (cm^{3}/s)')
g_maxDeltaT_vs_flux.GetYaxis().SetTitle('max(#Delta T) (#circ C)')
g_maxDeltaT_vs_flux.GetYaxis().SetTitleOffset(1.2)
g_maxDeltaT_vs_flux.GetYaxis().SetRangeUser(miny,maxy)
g_maxDeltaT_vs_flux.SetMarkerStyle(20)
g_maxDeltaT_vs_flux.SetMarkerSize(0.5)
g_maxDeltaT_vs_flux.SetMarkerColor(ROOT.kBlue)
g_maxDeltaT_vs_flux.SetLineColor(ROOT.kBlue)
g_maxDeltaT_vs_flux.SetLineStyle(2)
g_maxDeltaT_vs_flux.Draw('apl')
g_maxDeltaT_vs_flux.GetXaxis().SetLimits(0.0,1.0)
g_maxDeltaT_vs_flux.Draw('apl')
t1.Draw()
t2.Draw()
c_maxDeltaT_vs_flux.Update()
#raw_input('ok?')


for canvas in c_TminusTin_vs_flux, c_TminusTout_vs_flux, c_T_spread_vs_flux, c_maxDeltaT_vs_flux:
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.png')
    canvas.SaveAs(plotsdirname+'/'+(canvas.GetName()).replace('c_','')+'.pdf')


fout.cd()
g_T_spread_vs_flux.Write()
g_maxDeltaT_vs_flux.Write()
