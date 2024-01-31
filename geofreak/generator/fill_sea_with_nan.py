import numpy as np
from .land_sea_mask import land_sea_mask

def fill_sea_with_nan(arr, latlst, lonlst):
    """
    Given a 2D/3D array, remove the sea area as nan.
    """
    assert len(arr.shape) in [2, 3], "Shape of data must be 2 or 3."
    landMask = land_sea_mask(latlst, lonlst, boolType=False)
    if len(arr.shape)==2:
        arr = arr * landMask
    else:
        arr = arr * landMask[np.newaxis, :, :]
    
    return arr