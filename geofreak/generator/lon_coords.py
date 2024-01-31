import numpy as np

def lon_coords(start, end, resolution):
    """
    Given (start, end, resolution) to generate the latitude,
    
    e.g. given (40,50,0.1) can get [40.05, .... 49.85, 49.95] for a total of 100.
    """
    assert resolution>0, "resolution must be positive."
    
    if start > end:
        print("[Warning] Bad for longitude: start > end.")
        S = start - resolution/2
        E = end + resolution/2 - 1e-5
        R = -resolution
    else:
        S = start + resolution/2
        E = end - resolution/2 + 1e-5
        R = resolution
        
    return np.arange(S, E, R)