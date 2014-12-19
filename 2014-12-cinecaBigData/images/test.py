#!/usr/bin/env python
# -*- coding: utf8 -*- 

from __future__ import division # no more "zero" integer division bugs!:P
import time
import numpy as np
import veusz.embed as ve

def sm_hist(data, delta=5, n_bin=None, range_=None):
    dataMin = np.floor(data.min())
    dataMax = np.ceil(data.max())
    n_bin = np.ceil(1.*(dataMax-dataMin) / delta)
    range_ = (dataMin, dataMin + n_bin * delta)
    counts, bin_edges = np.histogram(data, n_bin, range_, density = False)
    return counts, bin_edges

def sm_hist2(data, delta=5):
    dataMin = np.floor(data.min())
    dataMax = np.ceil(data.max())
    n_bin = np.ceil(1.*(dataMax-dataMin) / delta) + 1
    idxs = ((data  - dataMin) / delta).astype(int)
    counts = np.zeros(n_bin) 
    bin_edges = np.arange(dataMin, dataMax+2, delta)
    for idx in idxs:
        counts[idx] += 1
    counts = np.hstack((np.array([0]), counts, np.array([0])))
    bin_edges = np.hstack((bin_edges[0], bin_edges, bin_edges[-1]))
    return counts, bin_edges

def plotFunc(inpath="./", outpath="./"):
    font = "Times New Roman"
    colors = [u'blue', u'green']
    xmin = ["auto", "auto"]
    xmax = ["auto", "auto"]
    ymin = ["auto", 0]
    ymax = ["auto", "auto"]

    xData = np.arange(100) 
    yData = np.random.randint(0, 100, size=100) + np.sin(np.arange(100))

    doc = ve.Embedded("doc_1")
    page = doc.Root.Add('page', width = '30cm', height='15cm')
    grid = page.Add('grid', autoadd = False, rows = 1, columns = 2,
                        scaleRows=[0.2],
                        topMargin='1cm',
                        bottomMargin='1cm'
                        )
    graphList = []

    graphList.append(grid.Add('graph', name="scatter", autoadd=False, 
                            hide = False, 
                            Border__width = '2pt',
                            leftMargin = '0.6cm',
                            rightMargin = '0.4cm',
                            topMargin = '0.5cm',
                            bottomMargin = '1cm',
                            ))

    graphList.append(grid.Add('graph', name="hist", autoadd=False, 
                            hide = False, 
                            Border__width = '2pt',
                            leftMargin = '2cm',
                            rightMargin = '0.4cm',
                            topMargin = '0.5cm',
                            bottomMargin = '1cm',
                            ))

    for i in range(len(graphList)):
        graphList[i].Add('axis', name='x', label = "x",
                                min = xmin[i],
                                max = xmax[i],
                                log = False,
                                Label__size = '25pt',
                                Label__font = font,
                                TickLabels__size = '17pt',
                                TickLabels__format = u'Auto',
                                MajorTicks__width = '2pt',
                                MajorTicks__length = '10pt',
                                MinorTicks__width = '1pt',
                                MinorTicks__length = '6pt'
                            )
        graphList[i].Add('axis', name='y', label = "y", 
                                direction = 'vertical',
                                min = ymin[i],
                                max = ymax[i],
                                log = False,
                                autoRange = u'+5%',
                                Label__size = '25pt',
                                Label__font = font,
                                TickLabels__size = '20pt',
                                TickLabels__format = u'Auto',
                                MajorTicks__width = '2pt',
                                MajorTicks__length = '10pt',
                                MinorTicks__width = '1pt',
                                MinorTicks__length = '6pt'
                            )

    graphList[0].Add('xy', key="scatterPlotKey", name='scatterPlotName',
                        marker = u'circle',
                        MarkerFill__color = colors[0],
                        markerSize = u'3pt', 
                        )

    xDataName = "xScatterData"
    yDataName = "yScatterData"
    doc.SetData(xDataName, xData)
    doc.SetData(yDataName, yData)
    graphList[0].scatterPlotName.xData.val = xDataName
    graphList[0].scatterPlotName.yData.val = yDataName


    counts, bin_edges = sm_hist2(yData, delta=5)

    graphList[1].Add('xy', key="histPlotKey", name='histPlotName',
                        xData = bin_edges,
                        yData = counts,
                        marker = 'none',
                        PlotLine__steps = u'left',
                        PlotLine__color = colors[1],
                        PlotLine__style = u"solid",
                        PlotLine__width = u'3',
                        FillBelow__color = colors[1],
                        FillBelow__style = "forward 2",
                        FillBelow__hide = False,
                        FillBelow__transparency = 70,
                        #FillBelow__backtransparency = 50,
                        FillBelow__linewidth = '1pt',
                        FillBelow__linestyle = 'solid',
                        FillBelow__backcolor = "white",
                        FillBelow__backhide = True,
                        Label__posnHorz = 'right',
                        Label__size = '14pt', 
                        Label__color = 'black'
                        )

    histKey = graphList[1].Add('key', autoadd=False, 
                        horzPosn = 'right',
                        vertPosn = 'top',
                        Text__font = font,
                        Text__size = '15',
                        Border__width = '1.5pt'
                        )

    end = raw_input("Press any key to finish...")

    doc.Save("example.vsz")
    doc.Export("example.png", backcolor='#ffffff')
    doc.Export("example.pdf")

if __name__ == "__main__":
    inpath = "./"
    outpath = './'
    tt = time.time()
    plotFunc(inpath, outpath)
    print "Done in ", time.time()-tt, " seconds."
