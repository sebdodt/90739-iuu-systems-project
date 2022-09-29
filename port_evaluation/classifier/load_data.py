import pandas as pd

def import_data():
    path = 'port_evaluation/data/xlsx/gfw_data.xlsx'
    xls = pd.ExcelFile(path)
    dfList = []
    for sheet in ['carriers', 'encounter', 'loitering']:
        dfList.append(pd.read_excel(path, sheet_name=sheet))
    return dfList