import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats.mstats import theilslopes
from scipy.stats import kendalltau

def trend_1d(arr, method='sen'):
    '''
    return a dict with keys:
    'changeValue', 'mean', 'changeRatio', 'pValue', 'slope', 'intercept'  
    '''
    if type(arr) != np.ndarray:
        arr = np.array(arr)
    assert len(arr.shape)==1
    
    if np.all(arr==0) or np.sum(np.isnan(arr))+np.sum(np.isinf(arr))>=(arr.shape[0]/2): 
    # the number of nan and inf should less than half of array lenth
        return {    'changeValue': np.nan,
                    'mean'       : np.nan,
                    'changeRatio': np.nan,
                    'pValue'     : np.nan,
                    'slope'      : np.nan,
                    'intercept'  : np.nan   }

            
    
    dataX= np.arange(arr.shape[0])
    dataY = arr.copy()
    isFinite = np.isfinite(arr)
    dataX = dataX[isFinite]
    dataY = dataY[isFinite]
    isNotNan = ~np.isnan(dataY)
    dataX = dataX[isNotNan]
    dataY = dataY[isNotNan]
    
    if method == 'linear':
        fit = np.polyfit(dataX, dataY, 1)
        model = np.poly1d(fit)
        df = pd.DataFrame(columns=['y', 'x'])
        df['x'] = dataX
        df['y'] = dataY
        results = smf.ols(formula='y ~ model(x)', data=df).fit()
        pValue = results.f_pvalue
        slope = fit[0]
        intercept = fit[1]
        
    elif method=='sen':
        _, pValue = kendalltau(dataX, dataY)
        slope, intercept, _, _ = theilslopes(dataY)
        
    return {'changeValue': slope*len(arr),
            'mean'       : np.nanmean(dataY),
            'changeRatio': (slope * len(arr)) / np.nanmean(dataY) * 100,
            'pValue'     : pValue,
            'slope'      : slope,
            'intercept'  : intercept}