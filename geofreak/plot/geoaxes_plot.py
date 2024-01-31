import os
import json

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from .colorbar_from_fig import colorbar_from_fig

def gen_geoaxes_json(output_json_path='./hydroJson/DefaultGeoAxes.json', return_dict=False):
    PARAMETERS = {
        'box_lw'            : 1,  
        'facecolor'         : 'none',
        'set_global'        : True,
        'has_stock_img'     : False,
        'has_coastlines'    : True,
        'coast_line_width'  : 0.5,
        'has_land'          : False,
        'has_ocean'         : False,
        'extent'            : [-180.001, 180.001, -90.0, 90.0],
        'stack_Image'          :
            {
                'remap'             : False,
            },
    }
    
    if not os.path.exists(os.path.dirname(output_json_path)):
        os.mkdir(os.path.dirname(output_json_path))
        
    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump(PARAMETERS, f, indent=2)  
    
    print("Json file of parameters has written to [{}]".format(output_json_path))
    
    if return_dict:
        return PARAMETERS

class GeoAxesPlot:
    
    def __init__(self, ax, jsonPath='./hydroJson/DefaultGeoAxes.json'):
        assert os.path.isfile(jsonPath), "Json file doesn't exist! "
        assert ax.__class__.__name__ == 'GeoAxes', \
            "Input ax must be GeoAxes, but given {}".format(ax.__class__.__name__)
        self.jsonPath = jsonPath
        self.ax = ax
        with open(jsonPath) as f:
            self.paraDict = json.load(f)
            
    def reload_json(self):
        with open(self.jsonPath) as f:
            self.paraDict = json.load(f)  
    
    def gen_default_json(self):
        """
        go back to default json
        """
        gen_geoaxes_json(self.jsonPath)
        
    def save_current_json(self, outputJsonPath='./hydroJson/currentGeoAxesMap.json'):
        if not os.path.exists(os.path.dirname(outputJsonPath)):
            os.mkdir(os.path.dirname(outputJsonPath))
            
        with open(outputJsonPath, "w", encoding='utf-8') as f:
            json.dump(self.paraDict, f, indent=2)  
        
        print("Current parameters has written to [{}]".format(outputJsonPath)) 
        
    def list_china_extent(self):
        return [70, 140, 15, 55]
        
    def base_map(self):
        self.reload_json()
        PARAS = self.paraDict
        
        if PARAS['set_global']:
            self.ax.set_global()     
        if PARAS['has_stock_img']:
            self.ax.stock_img()
        if PARAS['has_coastlines']:
            self.ax.coastlines(lw=PARAS['coast_line_width'])
        if PARAS['has_land']:
            self.ax.add_feature(cfeature.LAND)
        if PARAS['has_ocean']:
            self.ax.add_feature(cfeature.OCEAN)
            
        self.ax.set_extent(tuple(PARAS['extent']), crs=ccrs.PlateCarree())
        plt.setp(self.ax.spines.values(), linewidth=PARAS['box_lw'])
    
    def add_lonlat_ticks(self, lon_ticks=None, lat_ticks=None, 
                       lon_grids=None, lat_grids=None,
                       lat_pos='bottom', lon_pos='left',
                       **kwargs):
        
        from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
        if lon_ticks is not None:
            self.ax.set_xticks(lon_ticks, crs=ccrs.PlateCarree())
        if lat_ticks is not None:
            self.ax.set_yticks(lat_ticks, crs=ccrs.PlateCarree())

        if lat_pos=='bottom':
            self.ax.xaxis.set_ticks_position('bottom')
        elif lat_pos=='top':
            self.ax.xaxis.set_ticks_position('top')
        else:
            raise ValueError("lat_pos must be 'bottom' or 'top', but given {}".format(lat_pos))
        
        if lon_pos=='left':
            self.ax.yaxis.set_ticks_position('left')
        elif lon_pos=='right':
            self.ax.yaxis.set_ticks_position('right')
        else:
            raise ValueError("lon_pos must be 'left' or 'right', but given {}".format(lon_pos))
        
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)
        self.ax.gridlines(xlocs=lon_grids, ylocs=lat_grids, **kwargs)
    
    def stack_image(self, data, lat, lon, cmap='viridis', cmappcs=None, vmin=None, vmax=None):
        assert all(np.diff(lat) < 0), "Latitude is not descending!"
        assert len(data.shape)==2, "Only support 2D data, but given {}D".format(len(data.shape))
        assert data.shape[0]==len(lat) and data.shape[1]==len(lon),\
            "Shape of lat [{}], lon[{}], data[{}] are not matched.".format(len(lat),len(lon),data.shape)
        
        self.reload_json()
        PARAS = self.paraDict['stack_Image'] # 使用stackImg的参数
        
        if type(cmap) == str:
            if '.' in cmap:
                cbff = colorbar_from_fig(cmap, piece=cmappcs, reverse=False, inputPcs=cmappcs)
                cmap = cbff.getColorBar()
            else:
                if cmappcs==-1:
                    cmap = plt.get_cmap(cmap)
                else:
                    cmap = plt.get_cmap(cmap, cmappcs)
        
        dx = np.diff(lon).mean() / 2
        dy = np.diff(lat).mean() / 2
        extent = [max(np.min(lon) - dx, -179.99), 
                  min(np.max(lon) + dx, 179.99), 
                  max(np.min(lat) + dy, -89.99),
                  min(np.max(lat) - dy, 89.99)]
        
        if PARAS['remap']:
            self.ax.set_extent(extent,crs=ccrs.PlateCarree())
        
        im = self.ax.imshow(data, extent=extent, transform=ccrs.PlateCarree(), cmap=cmap)

        if vmin==None or vmax==None:
            vmin = np.nanmin(data)
            vmax = np.nanmax(data)
            
        im.set_clim(vmin=vmin, vmax=vmax)
        
        self.vmax = vmax
        self.vmin = vmin
        self.cmap = cmap
        self.cmap_pcs = cmappcs
        
    def add_colorbar(self, cax, tickNums=None, 
                    cbarExtend='both', 
                    cbarUnit='Unit ($unit$)', 
                    cbarShrinkTicks=False,
                    cbarOrientation='V',
                    cbarLabelSize=12,
                    cbarLineWidth=0.5,
                    **kwargs
                    ):
        if tickNums==None:
            ticks = list(np.linspace(self.vmin, self.vmax, 6))
        elif type(tickNums)==int:
            ticks = list(np.linspace(self.vmin, self.vmax, tickNums))
        else:
            ticks = tickNums
        
        # 避免colobar两边ticks过于靠边
        if cbarShrinkTicks:
            self.vmin = self.vmin - (ticks[1] - ticks[0]) / 2
            self.vmax = self.vmax + (ticks[1] - ticks[0]) / 2

        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        # pos = self.ax.get_position()
        # orientation = PARAS['cbar_orientation']
        assert cbarOrientation in ['V', 'H'],\
            "Orientation of colorbar only support 'V'(vertical) and 'H'(horizontal)."
            
        if cbarOrientation == 'V': # vertical
            cbar = mpl.colorbar.ColorbarBase(cax, cmap=self.cmap, norm=norm, 
                                             extend=cbarExtend, orientation='vertical', **kwargs)
            cbar.ax.set_ylabel(cbarUnit)
            cbar.outline.set_linewidth(cbarLineWidth)
            
        elif cbarOrientation == 'H': # horizontal
            cbar = mpl.colorbar.ColorbarBase(cax, cmap=self.cmap, norm=norm, 
                                             extend=cbarExtend, orientation='horizontal', **kwargs)
            cbar.ax.set_xlabel(cbarUnit, fontsize=cbarLabelSize)
            cbar.outline.set_linewidth(cbarLineWidth)
        
        cbar.set_ticks(ticks)
        cbar.ax.tick_params(labelsize=cbarLabelSize)