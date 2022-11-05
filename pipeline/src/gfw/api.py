import pandas as pd

def call_api():
    '''
    Load all new global fishing watch data since last API call
    '''
    path = 'pipeline/data/api/api_data.xlsx'
    xls = pd.ExcelFile(path)
    dfList = []
    for sheet in ['carriers', 'encounter', 'loitering', 'carrier_ports']:
        dfList.append(pd.read_excel(path, sheet_name=sheet))
    return dfList