import numpy as np
from tqdm.notebook import tqdm
from .trend_1d import trend_1d

def trend_3d(arr, method='sen', usetqdm=True):
    """
    Args:
        arr (_type_): Please guarantee time-coord is the zero-th axis
    """
    if type(arr) != np.ndarray:
        arr = np.array(arr)
    assert len(arr.shape)==3
    
    changeValue2D   = np.full_like(arr[0], np.nan, dtype=np.float32)
    mean2D          = np.full_like(arr[0], np.nan, dtype=np.float32)
    changeRatio2D   = np.full_like(arr[0], np.nan, dtype=np.float32)
    pValue2D        = np.full_like(arr[0], np.nan, dtype=np.float32)
    slope2D         = np.full_like(arr[0], np.nan, dtype=np.float32)
    intercept2D     = np.full_like(arr[0], np.nan, dtype=np.float32)
    
    NTime = arr.shape[0]
    NLat = arr.shape[1]
    NLon = arr.shape[2]
    
    if usetqdm:
        for i in tqdm(range(NLat)):
            for j in range(NLon):
                arr1D = arr[:,i,j]
                resDict = trend_1d(arr1D)
                changeValue2D[i,j]  = resDict['changeValue']
                mean2D[i,j]         = resDict['mean']
                changeRatio2D[i,j]  = resDict['changeRatio']
                pValue2D[i,j]       = resDict['pValue']
                slope2D[i,j]        = resDict['slope']
                intercept2D[i,j]    = resDict['intercept']
    else:
        for i in range(NLat):
            for j in range(NLon):
                arr1D = arr[:,i,j]
                resDict = trend_1d(arr1D)
                changeValue2D[i,j]  = resDict['changeValue']
                mean2D[i,j]         = resDict['mean']
                changeRatio2D[i,j]  = resDict['changeRatio']
                pValue2D[i,j]       = resDict['pValue']
                slope2D[i,j]        = resDict['slope']
                intercept2D[i,j]    = resDict['intercept']
            
    return {'changeValue': changeValue2D,
            'mean'       : mean2D,
            'changeRatio': changeRatio2D,
            'pValue'     : pValue2D,
            'slope'      : slope2D,
            'intercept'  : intercept2D}
                