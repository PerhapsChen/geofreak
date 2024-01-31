import os
import numpy as np
import matplotlib.pyplot as plt

from .plot_framework import PlotFramework
from .trend_plot import gen_trend_plot_json, TrendPlot
from .geoaxes_plot import gen_geoaxes_json, GeoAxesPlot

def quick_trend_plot(x, y=None):
    """
    快速画出x,y的折线图，并给出拟合直线的图。其中x,y均为一维数据，若y为空，则默认为0,1,2,3...
    """
    if y is None:
        y = np.arange(0, len(x))
        a = x
        x = y
        y = a

    assert len(x) == len(y), "Length of x and y must be equal!"
    
    fig = plt.figure(figsize=(8, 4), dpi=300)
    ax = fig.add_subplot(111)
    
    if not os.path.exists('./hydroJson/quickTrendPlot.json'):
        gen_trend_plot_json('./hydroJson/quickTrendPlot.json')
            
    tp = TrendPlot(ax, './hydroJson/quickTrendPlot.json')
    tp.plot(x, y)
    
    
def quick_map(lat, lon, data, cmap='hot_r', cmappcs=10, vmin=None, vmax=None, unit='Unit ($unit$)', **kwargs):
    '''
    快速绘制地图
    '''
        
    pf = PlotFramework()
    ax = pf.addMainAxes(isGeo=True, **kwargs)
    
    if not os.path.exists('hydroJson/quick_map.json'):
        gen_geoaxes_json('hydroJson/quick_map.json')
    
    if vmin == None and vmax == None:
        vmin = np.nanpercentile(data, 1)
        vmax = np.nanpercentile(data, 99)
        
    gp = GeoAxesPlot(ax, 'hydroJson/quick_map.json')
    
    gp.base_map()
    gp.stack_image(data, lat, lon, cmap, cmappcs, vmin, vmax)
    
    cax = pf.addDeputyPlot('Right', 0.01, 0.03, 1.0, 0.0)
    if cmappcs == -1:
        gp.add_colorbar(cax, 5, 'neither', unit, cbarLabelSize=9, cbarShrinkTicks=False, **kwargs)
    else:
        gp.add_colorbar(cax, cmappcs+1, 'neither', unit, cbarLabelSize=9,cbarShrinkTicks=False, **kwargs)
