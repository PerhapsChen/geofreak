import numpy as np

def lat_coords(start, end, resolution):
    """
    Given (start, end, resolution) to generate the latitude,
    
    e.g. given (30,20,0.1) can get [29.95, 29.85, ..., 20.15, 20.05] for a total of 100.
    """
    assert resolution>0, "resolution must be positive."
    if start > end:
        S = start - resolution/2
        E = end + resolution/2 - 1e-5
        R = -resolution
    else:
        print("[Warning] Bad for latitude: start < end.")
        S = start + resolution/2
        E = end - resolution/2 + 1e-5
        R = resolution
    return np.arange(S, E, R)