import numpy as np
import gdal 

def from_tiff_to_numpy(tiff_path, return_lat_lon=False):
    ds = gdal.Open(tiff_path)
    data = ds.GetRasterBand(1).ReadAsArray()
    if return_lat_lon:
        geotransform = ds.GetGeoTransform()
        lat = np.arange(data.shape[0]) * geotransform[5] + geotransform[3]
        lon = np.arange(data.shape[1]) * geotransform[1] + geotransform[0]
        return data, lat, lon
    else:
        return data