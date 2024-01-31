import numpy as np
import gdal 
from osgeo import osr

def from_numpy_to_tiff(data, lat, lon, tiff_path):
    assert len(data.shape) == 2, "Shape of data must be 2D."
    xsize = len(lon)
    ysize = len(lat)
    geotransform = (lon[0], np.mean(np.diff(lon)), 0, lat[0], 0, np.mean(np.diff(lat)))
    
    if data.dtype == np.float64:
        gdalType = gdal.GDT_Float64
    elif data.dtype == np.float32:
        gdalType = gdal.GDT_Float32
    elif data.dtype == np.int32:
        gdalType = gdal.GDT_Int32
    elif data.dtype == np.int16:
        gdalType = gdal.GDT_Int16
    elif data.dtype == np.uint16:
        gdalType = gdal.GDT_UInt16
    elif data.dtype == np.uint8:
        gdalType = gdal.GDT_Byte
    else:
        raise TypeError("Data type not supported.")
    
    dst_ds = gdal.GetDriverByName('GTiff').Create(tiff_path, xsize, ysize, 1, gdalType)
    dst_ds.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(srs.ExportToWkt())
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds = None