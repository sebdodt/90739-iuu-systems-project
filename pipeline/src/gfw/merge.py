


def merge_local_and_api(
        loitering, encounters, port_visits, carriers_new, loitering_new, encounters_new, port_visits_new):
    '''
    Input: pandas.DataFrames for carriers, loitering, encounters, and port_visits from local sources and api calls

    Output: four pandas.DataFrames for combined data of carriers, loitering, encounters, and port_visits
    '''

    ## merge loitering


    ## merge encounters


    ## merge port_visits


    ## create carriers table
    ### --> create new lines in carriers table for missing ships. 
    ###     Make sure a column called 'mmsi' includes all carriers that we have data on.
    ###     carriers['mmsi'] will be used to call data from SeaVision later.


    return carriers, loitering, encounters, port_visits