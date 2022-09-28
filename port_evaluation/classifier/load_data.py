import pandas as pd

def import_data():
    gfw_data = pd.read_excel('port_evaluation/data/xlsx/gfw_data.xlsx')
    return gfw_data