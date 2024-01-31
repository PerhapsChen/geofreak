import numpy as np
from .land_sea_mask import land_sea_mask

def fill_land_with_nan(arr, latlst, lonlst):
    """
    Given a 2D/3D array, remove the land area as nan.
    """
    assert len(arr.shape) in [2, 3], "Shape of data must be 2 or 3."
    seaMask = land_sea_mask(latlst, lonlst, boolType=False)
    seaMask = np.where(seaMask==1, np.nan, 1)
    
    if len(arr.shape)==2:
        arr = arr * seaMask
    else:
        arr = arr * seaMask[np.newaxis, :, :]
    
    return arr
        