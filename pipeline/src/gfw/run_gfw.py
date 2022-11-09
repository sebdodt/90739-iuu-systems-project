import pandas as pd
from src.gfw import api, merge

def run_gfw():

    ## load local data
    print(" > Importing local data...")
    loitering = pd.read_csv('pipeline/data/local/loitering.csv')
    encounters = pd.read_csv('pipeline/data/local/encounter.csv')
    port_visits = pd.read_csv('pipeline/data/local/port.csv')

    ## call new data from api
    print(" > Importing API data")
    carriers_new, loitering_new, encounters_new, port_visits_new = api.call_api()

    ## merge _data
    print(" > Merging local and API data...")
    carriers, loitering, encounters, port_visits = merge.merge_local_and_api(
        loitering, encounters, port_visits, carriers_new, loitering_new, encounters_new, port_visits_new)


    return carriers, loitering, encounters, port_visits


if __name__ == "__main__":
    print(" > Importing local data...")
    loitering = pd.read_csv('pipeline/data/local/loitering.csv')
    encounters = pd.read_csv('pipeline/data/local/encounter.csv')
    port_visits = pd.read_csv('pipeline/data/local/port.csv')

    ## call new data from api
    print(" > Importing API data")
    carriers_new, loitering_new, encounters_new, port_visits_new = api.call_api()
    print(loitering.columns)
    print(loitering_new.columns)
