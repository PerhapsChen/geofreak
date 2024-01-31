import numpy as np
from global_land_mask import globe

def land_sea_mask(latlst, lonlst, boolType=True):
    """
    Given list of lat, lon, return the land or sea matrix .
    If boolType is True, return bool matrix, else return 1 for land and nan for sea (easy for multiply).
    """
    lat_mesh, lon_mesh = np.meshgrid(latlst, lonlst)
    land_mask = globe.is_land(lat_mesh, lon_mesh).T
    
    if boolType:
        return land_mask
    else:
        return np.where(land_mask, 1, np.nan)