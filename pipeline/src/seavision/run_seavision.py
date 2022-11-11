import pandas as pd
from src.seavision import api

def get_info(carriers):
    '''
    Input: pandas.DataFrame of carrier data with column 'mmsi'.

    Output: pandas.DataFrame of all SeaVision info on carriers.

    '''
    result = pd.DataFrame()
    for i in range(len(carriers)):
        rowData = carriers.iloc[i]
        mmsi = carriers.loc[i, 'mmsi'].astype(int)
        result = result.append(api.get_vessel_history(mmsi))
    return result


def get_history(carriers):
    '''
    Input: pandas.DataFrame of carrier data with column 'mmsi'.

    Output: pandas.DataFrame of 90-day history of carriers.
    '''
    pass

### Test case
# carriers = get_vessels(17.5, -120.3)
# print(get_info(carriers).columns)


