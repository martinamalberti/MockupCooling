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

ROOT.gStyle.SetPalette(ROOT.kRainBow)

ROOT.gStyle.SetLabelSize(0.05,'X')
ROOT.gStyle.SetLabelSize(0.05,'Y')
ROOT.gStyle.SetLabelSize(0.05,'Z')
ROOT.gStyle.SetTitleSize(0.05,'X')
ROOT.gStyle.SetTitleSize(0.05,'Y')
ROOT.gStyle.SetTitleSize(0.05,'Z')
ROOT.gStyle.SetTitleOffset(1.0,'X')
ROOT.gStyle.SetTitleOffset(1.0,'Y')


filename = 'plots_run016.root'
print filename
f = ROOT.TFile.Open(filename)

outfile = open('intercalibration_run016.txt','w+')

plotsdirname ='plots/intercalibration/'
if ( os.path.exists(plotsdirname) == False ) :
    os.mkdir(plotsdirname)
shutil.copy('index.php', '%s'%plotsdirname)

#histograms
h_temp = {} # temp for each termometer
h_temperatures_mean = ROOT.TH1F('h_temperatures_mean','h_temperatures_mean',100,0,50) # to get the average temperature across all termometers
h2_dtemp = {} # map of intercalib

# mapping of termometers 
t_map = {0:[1,4],
         2:[1,3],
         4:[1,2],
         6:[1,1],
         8:[2,4],
         10:[2,3],
         12:[2,2],
         14:[2,1],
         1:[3,4],
         3:[3,3],
         5:[3,2],
         7:[3,1],
         9:[4,4],
         11:[4,3],
         13:[4,2],
         15:[4,1]}
         

for ie in range(0,5):
    h_temp[ie] = []
    nt = 16
    if (ie==4): nt = 4

    # - 2D histos, one for each Expander
    if (ie<4):
        h2_dtemp[ie] = ROOT.TH2F('h2_dtemp_%s%d'%(filename,ie+1),'h2_dtemp_%s%d'%(filename,ie+1),4,0.5,4.5,4,0.5,4.5)
    else:
        h2_dtemp[ie] = ROOT.TH2F('h2_dtemp_%s%d'%(filename,ie+1),'h2_dtemp_%s%d'%(filename,ie+1),4,0.5,4.5,1,0.5,1.5)
        
    for it in range(0,nt):
        h_temp[ie].append(f.Get('h_temp_Expander%d_%d'%(ie+1,it)))
        if (h_temp[ie][it].GetMean()==0): continue
        h_temperatures_mean.Fill( h_temp[ie][it].GetMean() )


outfile.write('Expander   Termometer   DeltaT \n')

for ie in range(0,5):
    nt = 16
    if (ie==4): nt = 4
    for it in range(0,nt):
        if (h_temp[ie][it].GetMean()==0): continue
        dt = h_temp[ie][it].GetMean() - h_temperatures_mean.GetMean()
        print '%d %d %.2f'%(ie, it, dt)
        outfile.write('%d %d %.2f\n'%(ie, it, dt))
        binx = t_map[it][0]
        biny = t_map[it][1]
        if (ie==4):
            binx = it+1
            biny = 1
        h2_dtemp[ie].SetBinContent(binx,biny,dt)


c_dtemp_map = ROOT.TCanvas('c_dtemp_map','c_dtemp_map',1200,400)
c_dtemp_map.Divide(4,1)
for ie in range(0,4):
    c_dtemp_map.cd(ie+1)
    c_dtemp_map.cd(ie+1).SetLeftMargin(0.1)
    c_dtemp_map.cd(ie+1).SetRightMargin(0.20)
    h2_dtemp[ie].GetXaxis().SetNdivisions(4)
    h2_dtemp[ie].GetYaxis().SetNdivisions(4)
    h2_dtemp[ie].GetZaxis().SetTitle('#Delta T (^{O}C)')
    minz = h2_dtemp[3].GetBinContent(4,1) - 0.5
    maxz = h2_dtemp[3].GetBinContent(1,1) + 0.5
    h2_dtemp[ie].GetZaxis().SetRangeUser(minz,maxz)
    h2_dtemp[ie].SetStats(ROOT.kFALSE)
    h2_dtemp[ie].Draw('colz')
c_dtemp_map.SaveAs(plotsdirname+'/'+(c_dtemp_map.GetName()).replace('c_','')+'.png')
c_dtemp_map.SaveAs(plotsdirname+'/'+(c_dtemp_map.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')

c_dtemp_map_Expander5 = ROOT.TCanvas('c_dtemp_map_Expander5','c_dtemp_map_Expander5',1200,400)
c_dtemp_map_Expander5.SetRightMargin(0.15) 
h2_dtemp[4].GetZaxis().SetTitle('#Delta T (^{O}C)')
h2_dtemp[4].GetXaxis().SetNdivisions(4)
h2_dtemp[4].GetYaxis().SetNdivisions(0)
h2_dtemp[4].GetZaxis().SetRangeUser(minz,maxz)
h2_dtemp[4].SetStats(ROOT.kFALSE)
h2_dtemp[4].Draw('colz')
c_dtemp_map_Expander5.SaveAs(plotsdirname+'/'+(c_dtemp_map_Expander5.GetName()).replace('c_','')+'.png')
c_dtemp_map_Expander5.SaveAs(plotsdirname+'/'+(c_dtemp_map_Expander5.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')  
