import numpy as np


def grid_area_map(latlst, lonlst):
    """
    Given list of lat, lon, return the area matrix.
    """
    R = 6371.4e3
    lat_j_rad = np.deg2rad(latlst)
    cos_j = np.cos(lat_j_rad)
    Sj = 2 * np.pi**2 * cos_j * R**2 / (180 * 360)
    Sij = np.repeat(Sj.reshape(-1, 1), len(lonlst), axis=1)
    
    return Sij