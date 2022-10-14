import pandas as pd


def seavision_ships_in_radius(
    lat,
    lon,
    datetime,
    radius = 30,  #km
    time_period = 12 #hours
):
    '''
    Output: One dataframe with all ships and all location within radius and time
        Columns: MMSI number, datetime, location
    '''
    NotImplemented