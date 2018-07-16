#! /usr/bin/env python
import os
import shutil
import glob
import math
import array
import sys
import time

from readIntercalibration import readIntercalibration

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

ROOT.gStyle.SetPalette(ROOT.kRainBow)

ROOT.gStyle.SetLabelSize(0.05,'X')
ROOT.gStyle.SetLabelSize(0.05,'Y')
ROOT.gStyle.SetLabelSize(0.05,'Z')
ROOT.gStyle.SetTitleSize(0.05,'X')
ROOT.gStyle.SetTitleSize(0.05,'Y')
ROOT.gStyle.SetTitleSize(0.05,'Z')
ROOT.gStyle.SetTitleOffset(1.0,'X')
ROOT.gStyle.SetTitleOffset(0.75,'Y')
ROOT.gStyle.SetTitleOffset(0.75,'Z')

#read termometers intercalibration values
nterm = [16,16,16,16,4]
applyIntercalibrations = True
ic = []
for ie in range(0,5):
    ic.append([])
    for it in range(0,nterm[ie]):
        ic[ie].append(0.0)
        
if (applyIntercalibrations):
    readIntercalibration('intercalibration_run016.txt', ic)


# -- input files
runnumber = sys.argv[1]
dirname   = 'runs/run%s/'%runnumber
filename  = 'Expander'

filenames = []
for ie in range(0,5):
    filenames.append(dirname+filename+'%d.txt'%(ie+1))
    print ie,filenames[ie]


# -- output dir to save plots
plotsdirname = 'plots/1Loop/run%s/'%runnumber
if (int(runnumber) < 24 ) :
    plotsdirname = 'plots/2Loops/run%s/'%runnumber
if ( os.path.exists(plotsdirname) == False ) :
    os.mkdir(plotsdirname)
shutil.copy('index.php', '%s'%plotsdirname)


# -- output file
fout = ROOT.TFile( 'plots_run%s.root'%runnumber, 'recreate' )


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
         
t_map_canvas = {0:1, 8:2, 1:3, 9:4, 2:5, 10:6, 3:7, 11:8, 4:9, 12:10, 5:11, 13:12, 6:13, 14:14, 7:15, 15:16}



# -- histograms
h2_temp = {}
h2_rms_temp = {}
h_temperatures_spread = ROOT.TH1F('h_temperatures_spread','h_temperatures_spread',300,10,40)
h2_temperatures = ROOT.TH2F('h2_temperatures','h2_temperatures',16,0.5,16.5,4,0.5,4.5)
h2_temperatures_rms = ROOT.TH2F('h2_temperatures_rms','h2_temperatures_rms',16,0.5,16.5,4,0.5,4.5)
p_temperatures = ROOT.TProfile('p_temperatures','p_temperatures',16,0.5,16.5)

# -- read each file for this run
for ie,fname in enumerate(filenames):

    # - check if file exists
    if ( os.path.exists(fname) == False ) :
        print 'File %s not found !!!!'%fname
        continue

    if ('Expander5' in fname):
        t_map_canvas = {0:1, 1:2, 2:3, 3:4}
    

    temperatures = {}
    temperatures_plateau = {}

    # --- book histograms    
    # - 1D histograms for one termometer in each Expander
    g_temp_vs_time = {}
    g_temp_diff_vs_time = {}
    h_temp = {}
    h_temp_diff = {}
    
    for it in range(0,nterm[ie]):
        temperatures[it] = []
        h_temp[it] = ROOT.TH1F('h_temp_%s%d_%d'%(filename,ie+1,it),'h_temp_%s%d_%d'%(filename,ie+1,it),120,10,40)
        h_temp_diff[it] = ROOT.TH1F('h_temp_diff_%s%d_%d'%(filename,ie+1,it),'h_temp_diff_%s%d_%d'%(filename,ie+1,it),100,-10,10)
        g_temp_vs_time[it] = ROOT.TGraph()
        g_temp_vs_time[it].SetName('g_temp_vs_time_%s%d_%d'%(filename,ie+1,it))
        g_temp_diff_vs_time[it] = ROOT.TGraph()
        g_temp_diff_vs_time[it].SetName('g_temp_diff_vs_time_%s%d_%d'%(filename,ie+1,it))

    # - 2D maps, one for each Expander
    if (ie<4):
        h2_temp[ie] = ROOT.TH2F('h2_temp_%s%d'%(filename,ie+1),'h2_temp_%s%d'%(filename,ie+1),4,0.5,4.5,4,0.5,4.5)
        h2_rms_temp[ie] = ROOT.TH2F('h2_rms_temp_%s%d'%(filename,ie+1),'h2_rms_temp_%s%d'%(filename,ie+1),4,0.5,4.5,4,0.5,4.5)
    else:
        h2_temp[ie] = ROOT.TH2F('h2_temp_%s%d'%(filename,ie+1),'h2_temp_%s%d'%(filename,ie+1),4,0.5,4.5,1,0.5,1.5)
        h2_rms_temp[ie] = ROOT.TH2F('h2_rms_temp_%s%d'%(filename,ie+1),'h2_rms_temp_%s%d'%(filename,ie+1),4,0.5,4.5,1,0.5,1.5)
        
    # --- open file for this Expander
    f = open(fname)
    n = 0
    iref = 0
    if (nterm[ie] == 4):
        iref = 3

    for line in f:
        if ('T1' in line or 'GBP' in line): continue
        #sanity check: number of elements in the line must be = nterm[ie] (last element of the list is '\r\n', skip it)
        if ( len(line.split('\t')[:-1] )!= nterm[ie]): continue
        for it in range(0,nterm[ie]):
            t = float(line.split('\t')[it])
            if (t > 0 and t < 200):
                temperatures[it].append(float(line.split('\t')[it]) - ic[ie][it]) # subtract DeltaT from calibration run
                    
    #fill histograms
    for it in range(0,nterm[ie]):    
        for k in range(0, len(temperatures[it])):
            g_temp_vs_time[it].SetPoint(k,k,temperatures[it][k])
            g_temp_diff_vs_time[it].SetPoint(k,k,temperatures[it][k]-temperatures[iref][k])
            
    for it in range(0,nterm[ie]):    
        #take only the last 60*5 = 300 measurements ~ 5 minutes...
        temperatures_plateau[it] = temperatures[it][-300:]
                
    for it in range(0,nterm[ie]):    
        for k in range(0, len(temperatures_plateau[it])):
            h_temp[it].Fill(temperatures_plateau[it][k])
            h_temp_diff[it].Fill(temperatures_plateau[it][k]-temperatures_plateau[iref][k])
            if (  nterm[ie] != 4 ):
                h_temperatures_spread.Fill(temperatures_plateau[it][k])
        binx = t_map[it][0]
        biny = t_map[it][1]
        if ('Expander5' in fname):
            binx = it+1
            biny = 1
        h2_temp[ie].SetBinContent(binx,biny,h_temp[it].GetMean())
        h2_rms_temp[ie].SetBinContent(binx,biny,h_temp[it].GetRMS())

        if (ie < 4):
            binx = t_map[it][0]+4*ie
            biny = t_map[it][1]
            h2_temperatures.Fill(binx,biny,h_temp[it].GetMean())
            h2_temperatures_rms.Fill(binx,biny,h_temp[it].GetRMS())
            if (h_temp[it].GetMean()!=0): p_temperatures.Fill( binx,  h_temp[it].GetMean() )
            
       
        fout.cd()
        h_temp[it].Write()
        
        
    # -- plotting    
    canvasW = 1200
    canvasH = 1000
    if ('Expander5' in fname):
        canvasW = 1200
        canvasH = 400

    line = {}
        
    c1 = ROOT.TCanvas('c_temperatures_%s%d'%(filename,ie+1),'c_temperatures_%s%d'%(filename,ie+1),canvasW,canvasH)
    c1.Divide(4,nterm[ie]/4)
    for it in range(0,nterm[ie]):
        #c1.cd(it+1)
        c1.cd(t_map_canvas[it])
        h_temp[it].GetYaxis().SetRangeUser(0., h_temp[it].GetMaximum()*1.4)
        h_temp[it].GetXaxis().SetTitle('T (^{O}C)')
        h_temp[it].Draw()
    #raw_input('ok?')    
    c1.SaveAs(plotsdirname+'/'+(c1.GetName()).replace('c_','')+'.png')
    c1.SaveAs(plotsdirname+'/'+(c1.GetName()).replace('c_','')+'.pdf')

        
    c2 = ROOT.TCanvas('c_temperatures_difference_%s%d'%(filename,ie+1),'c_temperatures_difference_%s%d'%(filename,ie+1),canvasW,canvasH)
    c2.Divide(4,nterm[ie]/4)
    for it in range(0,nterm[ie]):
        #c2.cd(it+1)
        c2.cd(t_map_canvas[it])
        h_temp_diff[it].GetYaxis().SetRangeUser(0., h_temp_diff[it].GetMaximum()*1.4)
        h_temp_diff[it].GetXaxis().SetTitle('T (^{O}C)')
        h_temp_diff[it].Draw()
    #raw_input('ok?')    
    c2.SaveAs(plotsdirname+'/'+(c2.GetName()).replace('c_','')+'.png')
    c2.SaveAs(plotsdirname+'/'+(c2.GetName()).replace('c_','')+'.pdf')

    
    c3 = ROOT.TCanvas('c_temperatures_vs_time_%s%d'%(filename,ie+1),'c_temperatures_vs_time_%s%d'%(filename,ie+1),canvasW,canvasH)
    c3.Divide(4,nterm[ie]/4)
    miny = g_temp_vs_time[0].GetHistogram().GetMinimum()-1.0
    maxy = g_temp_vs_time[0].GetHistogram().GetMaximum()+1.0
    for it in range(0,nterm[ie]):
        #c3.cd(it+1)
        c3.cd(t_map_canvas[it])
        g_temp_vs_time[it].SetMarkerStyle(20)
        g_temp_vs_time[it].SetMarkerSize(0.2)
        g_temp_vs_time[it].SetMarkerColor(ROOT.kBlue)
        g_temp_vs_time[it].SetLineColor(ROOT.kBlue)
        g_temp_vs_time[it].GetHistogram().GetYaxis().SetRangeUser(miny,maxy)
        g_temp_vs_time[it].GetHistogram().GetXaxis().SetTitle('time (s)')
        g_temp_vs_time[it].GetHistogram().GetYaxis().SetTitle('T(^{O}C)')
        g_temp_vs_time[it].Draw('apl')
        line[it] = ROOT.TLine(len(temperatures[it])-len(temperatures_plateau[it]), miny,len(temperatures[it])-len(temperatures_plateau[it]), maxy)
        line[it].SetLineColor(ROOT.kGray)
        line[it].SetLineStyle(2)
        line[it].Draw('same')
    #raw_input('ok?')    
    c3.SaveAs(plotsdirname+'/'+(c3.GetName()).replace('c_','')+'.png')
    c3.SaveAs(plotsdirname+'/'+(c3.GetName()).replace('c_','')+'.pdf')


    c4 = ROOT.TCanvas('c_temperatures_difference_vs_time_%s%d'%(filename,ie+1),'c_temperatures_difference_vs_time_%s%d'%(filename,ie+1),canvasW,canvasH)
    c4.Divide(4,nterm[ie]/4)
    miny = g_temp_diff_vs_time[0].GetHistogram().GetMinimum()-0.5
    maxy = g_temp_diff_vs_time[0].GetHistogram().GetMaximum()+0.5
    for it in range(0,nterm[ie]):
        #c4.cd(it+1)
        c4.cd(t_map_canvas[it])
        g_temp_diff_vs_time[it].SetMarkerStyle(20)
        g_temp_diff_vs_time[it].SetMarkerSize(0.2)
        g_temp_diff_vs_time[it].SetMarkerColor(ROOT.kBlue)
        g_temp_diff_vs_time[it].SetLineColor(ROOT.kBlue)
        g_temp_diff_vs_time[it].GetHistogram().GetYaxis().SetRangeUser(miny,maxy)
        g_temp_diff_vs_time[it].GetHistogram().GetXaxis().SetTitle('time (s)')
        g_temp_diff_vs_time[it].GetHistogram().GetYaxis().SetTitle('T(^{O}C)')
        g_temp_diff_vs_time[it].Draw('apl')
        line[it] = ROOT.TLine(len(temperatures[it])-len(temperatures_plateau[it]), miny,len(temperatures[it])-len(temperatures_plateau[it]), maxy)
        line[it].SetLineColor(ROOT.kGray)
        line[it].SetLineStyle(2)
        line[it].Draw('same')
    #raw_input('ok?')    
    c4.SaveAs(plotsdirname+'/'+(c4.GetName()).replace('c_','')+'.png')
    c4.SaveAs(plotsdirname+'/'+(c4.GetName()).replace('c_','')+'.pdf')


c_temperatures_profile = ROOT.TCanvas('c_temperatures_profile','c_temperatures_profile',1200,350)
c_temperatures_profile.SetLeftMargin(0.10)
c_temperatures_profile.SetRightMargin(0.15)
p_temperatures.GetXaxis().SetNdivisions(16)
p_temperatures.GetYaxis().SetTitle('T (^{O}C)')
p_temperatures.SetStats(ROOT.kFALSE)
miny = int(p_temperatures.GetBinContent(14)) - 1.0
maxy = int(p_temperatures.GetBinContent(14)) + 2.0
p_temperatures.GetYaxis().SetRangeUser(miny,maxy)
p_temperatures.SetMarkerStyle(20)
p_temperatures.SetMarkerSize(0.8)
p_temperatures.Draw('p')
ll1= ROOT.TLine(4.5, miny, 4.5, maxy)
ll2= ROOT.TLine(8.5, miny, 8.5, maxy)
ll3= ROOT.TLine(12.5, miny, 12.5, maxy)
for l in ll1, ll2, ll3:
    l.SetLineColor(ROOT.kGray)
    l.SetLineStyle(2)
    l.Draw('same')
c_temperatures_profile.SaveAs(plotsdirname+'/'+(c_temperatures_profile.GetName()).replace('c_','')+'.png')
c_temperatures_profile.SaveAs(plotsdirname+'/'+(c_temperatures_profile.GetName()).replace('c_','')+'.pdf')    
fout.cd()
p_temperatures.Write()
#raw_input('ok?')


c_temperatures_map = ROOT.TCanvas('c_temperatures_map','c_temperatures_map',1200,350)
c_temperatures_map.SetLeftMargin(0.10)
c_temperatures_map.SetRightMargin(0.15)
h2_temperatures.GetXaxis().SetNdivisions(16)
h2_temperatures.GetYaxis().SetNdivisions(4)
h2_temperatures.GetZaxis().SetTitle('T (^{O}C)')
minz = h2_temperatures.GetBinContent(16,1) - 1.0
maxz = h2_temperatures.GetBinContent(13,1) + 1.0
h2_temperatures.GetZaxis().SetRangeUser(minz,maxz)
h2_temperatures.SetStats(ROOT.kFALSE)
h2_temperatures.Draw('colz')
ll1= ROOT.TLine(4.5, 0.5, 4.5, 4.5)
ll2= ROOT.TLine(8.5, 0.5, 8.5, 4.5)
ll3= ROOT.TLine(12.5, 0.5, 12.5, 4.5)
for l in ll1, ll2, ll3:
    l.SetLineColor(ROOT.kGray)
    l.SetLineStyle(2)
    l.Draw('same')
c_temperatures_map.SaveAs(plotsdirname+'/'+(c_temperatures_map.GetName()).replace('c_','')+'.png')
c_temperatures_map.SaveAs(plotsdirname+'/'+(c_temperatures_map.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')

c_temperatures_map_Expander5 = ROOT.TCanvas('c_temperatures_map_Expander5','c_temperatures_map_Expander5',1200,350)
c_temperatures_map_Expander5.SetLeftMargin(0.05) 
c_temperatures_map_Expander5.SetRightMargin(0.15) 
h2_temp[4].GetZaxis().SetTitle('T (^{O}C)')
h2_temp[4].GetXaxis().SetNdivisions(4)
h2_temp[4].GetYaxis().SetNdivisions(0)
minz = h2_temp[4].GetBinContent(4,1) - 1.0
maxz = h2_temp[4].GetBinContent(1,1) + 1.0
h2_temp[4].GetZaxis().SetRangeUser(minz,maxz)
h2_temp[4].SetStats(ROOT.kFALSE)
h2_temp[4].Draw('colz')
c_temperatures_map_Expander5.SaveAs(plotsdirname+'/'+(c_temperatures_map_Expander5.GetName()).replace('c_','')+'.png')
c_temperatures_map_Expander5.SaveAs(plotsdirname+'/'+(c_temperatures_map_Expander5.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')


c_temperatures_rms_map = ROOT.TCanvas('c_temperatures_rms_map','c_temperatures_rms_map',1200,350)
c_temperatures_rms_map.SetLeftMargin(0.05)
c_temperatures_rms_map.SetRightMargin(0.15)
h2_temperatures_rms.GetXaxis().SetNdivisions(16)
h2_temperatures_rms.GetYaxis().SetNdivisions(4)
h2_temperatures_rms.GetZaxis().SetTitle('T (^{O}C)')
minz = 0
maxz = h2_temperatures_rms.GetBinContent(13,1) + 0.2
h2_temperatures_rms.GetZaxis().SetRangeUser(minz,maxz)
h2_temperatures_rms.SetStats(ROOT.kFALSE)
h2_temperatures_rms.Draw('colz')
ll1= ROOT.TLine(4.5, 0.5, 4.5, 4.5)
ll2= ROOT.TLine(8.5, 0.5, 8.5, 4.5)
ll3= ROOT.TLine(12.5, 0.5, 12.5, 4.5)
for l in ll1, ll2, ll3:
    l.SetLineColor(ROOT.kGray)
    l.SetLineStyle(2)
    l.Draw('same')
c_temperatures_rms_map.SaveAs(plotsdirname+'/'+(c_temperatures_rms_map.GetName()).replace('c_','')+'.png')
c_temperatures_rms_map.SaveAs(plotsdirname+'/'+(c_temperatures_rms_map.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')

c_temperatures_rms_map_Expander5 = ROOT.TCanvas('c_temperatures_rms_map_Expander5','c_temperatures_rms_map_Expander5',1200,350)
c_temperatures_rms_map_Expander5.SetLeftMargin(0.05)
c_temperatures_rms_map_Expander5.SetRightMargin(0.15)
h2_rms_temp[4].GetZaxis().SetTitle('rms T (^{O}C)')
h2_rms_temp[4].GetXaxis().SetNdivisions(4)
h2_rms_temp[4].GetYaxis().SetNdivisions(0)
minz = 0
maxz = h2_rms_temp[4].GetBinContent(1,1) + 0.2
h2_rms_temp[4].GetZaxis().SetRangeUser(minz,maxz)
h2_rms_temp[4].SetStats(ROOT.kFALSE)
h2_rms_temp[4].Draw('colz')
c_temperatures_rms_map_Expander5.SaveAs(plotsdirname+'/'+(c_temperatures_rms_map_Expander5.GetName()).replace('c_','')+'.png')
c_temperatures_rms_map_Expander5.SaveAs(plotsdirname+'/'+(c_temperatures_rms_map_Expander5.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')


c_temperatures_spread = ROOT.TCanvas('c_temperatures_spread','c_temperatures_spread')
h_temperatures_spread.GetXaxis().SetTitle('T (^{O}C)')
h_temperatures_spread.Draw()
c_temperatures_spread.SaveAs(plotsdirname+'/'+(c_temperatures_spread.GetName()).replace('c_','')+'.png')
c_temperatures_spread.SaveAs(plotsdirname+'/'+(c_temperatures_spread.GetName()).replace('c_','')+'.pdf')
#raw_input('ok?')

