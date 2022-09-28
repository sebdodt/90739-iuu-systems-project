import pandas as pd

def import_data():
    path = 'port_evaluation/data/xlsx/gfw_data.xlsx'
    xls = pd.ExcelFile(path)
    dfList = []
    sheetsList = xls.sheet_names
    for sheet in sheetsList:
        dfList.append(pd.read_excel(path, sheet_name=sheet))
    return dfList