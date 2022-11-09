import pandas as pd


def merge_local_and_api(
        loitering, encounters, port_visits, carriers_new, loitering_new, encounters_new, port_visits_new):
    '''
    Input: pandas.DataFrames for carriers, loitering, encounters, and port_visits from local sources and api calls

    Output: four pandas.DataFrames for combined data of carriers, loitering, encounters, and port_visits
    '''

    ## merge loitering
    print(' > Now updating loitering')
    loitering_new = loitering_new.rename({
    'event_id': 'id',
    'event_type': 'type',
    'event_start': 'start',
    'event_end': 'end',
    'event_lat': 'lat',
    'event_lon': 'lon',
    'rfmo': 'regions.rfmo',
    'vessel_id': 'vessel.id',
    'vessel_flag': 'vessel.flag',
    'vessel_name': 'vessel.name',
    'vessel_type': 'vessel.type',
    'vessel_ssvid': 'vessel.mmsi',
    },
    axis = 1)
    frames3 = [loitering,loitering_new[~loitering_new['id'].isin(loitering['id'])]]

    loitering_result = pd.concat(frames3)


    ## merge encounters
    print(' > Now updating encounters')
    encounters_new = encounters_new.rename({
    'event_id': 'id',
    'event_type': 'type',
    'event_start': 'start',
    'event_end': 'end',
    'event_lat': 'lat',
    'event_lon': 'lon',
    'rfmo': 'regions.rfmo',
    'vessel1_id': 'vessel.id',
    'vessel1_flag': 'vessel.flag',
    'vessel1_name': 'vessel.name',
    'vessel1_type': 'vessel.type',
    'vessel1_ssvid': 'vessel.mmsi',
    'vessel2_id': 'encounter.encountered_vessel.id',
    'vessel2_flag': 'encounter.encountered_vessel.flag',
    'vessel2_name': 'encounter.encountered_vessel.name',
    'vessel2_type': 'encounter.encountered_vessel.type',
    'vessel2_ssvid': 'encounter.encountered_vessel.mmsi',
    },
    axis = 1)

    encounter = encounters_new[encounters_new['encounter_type']=='carrier-fishing'].copy()
    encounter2 = encounters.copy()
    encounter2['start'] = pd.to_datetime(encounters['start'].str[:-4])
    encounter2['end'] = pd.to_datetime(encounters['end'].str[:-4])
    # (encounter['encounter.encountered_vessel.id'].isin(encounter2['encounter.encountered_vessel.id'])).sum()
    # (encounter['vessel.id'].isin(encounter2['encounter.encountered_vessel.id'])).sum()

    dfdf = encounter[~((encounter['start'].isin(encounter2['start'])) & (encounter['vessel.id'].isin(encounter2['vessel.id'])) & (encounter['encounter.encountered_vessel.id'].isin(encounter2['encounter.encountered_vessel.id'])))]
    dfdf = dfdf[~((dfdf['start'].isin(encounter2['start'])) & (dfdf['vessel.id'].isin(encounter2['encounter.encountered_vessel.id'])) & (dfdf['vessel.id'].isin(encounter2['encounter.encountered_vessel.id'])))]
    # dfdf['id'].count()
    frames = [encounter2,dfdf]

    encounter_result = pd.concat(frames)


    ## merge port_visits
    print(' > Now updating port_visits')
    port_visits_new = port_visits_new.drop_duplicates(subset=['event_id'])
    port_visits[['id', 'type', 'start', 'end', 'lat', 'lon', 'vessel.id', 'vessel.type',
       'vessel.mmsi', 'vessel.name', 'vessel.flag', 'port.lat', 'port.lon',
       'port.country', 'port.name']]
    port_visits.columns = ['event_id', 'event_type', 'event_start', 'event_end', 'event_lat',
       'event_lon','vessel_id', 'vessel_type','vessel_ssvid','vessel_name', 'vessel_flag', 'lat','lon','flag','name']
    
    port_visits2 = port_visits[~port_visits['event_id'].isin(port_visits_new['event_id'])]
    framesvisit = [port_visits2,port_visits_new]
    port_visits_result = pd.concat(framesvisit)

    ## create carriers table
    ### --> create new lines in carriers table for missing ships. 
    ###     Make sure a column called 'mmsi' includes all carriers that we have data on.
    ###     carriers['mmsi'] will be used to call data from SeaVision later.
    print(' > Now updating carriers')
    carrier_from_loitering = loitering_result[['vessel.id', 'vessel.type','vessel.mmsi', 'vessel.name', 'vessel.flag']].copy()
    carrier_from_loitering = carrier_from_loitering[carrier_from_loitering['vessel.type']=='carrier']
    carrier_from_loitering.columns = ['id', 'vesselType', 'mmsi', 'shipname', 'flag']
    carrier_from_loitering = carrier_from_loitering.drop_duplicates(subset=['mmsi'])
    carrier_from_loitering = carrier_from_loitering[~carrier_from_loitering['mmsi'].isin(carriers_new['mmsi'])]
    carrier_from_loitering['dataset'] = 'API-loitering'
    frames_carr_loi = [carriers_new,carrier_from_loitering]

    carrier1 = pd.concat(frames_carr_loi)
    
    carrier_from_encounters = encounter_result[['vessel.id', 'vessel.type','vessel.mmsi', 'vessel.name', 'vessel.flag']].copy()
    carrier_from_encounters = carrier_from_encounters[carrier_from_encounters['vessel.type']=='carrier']
    carrier_from_encounters.columns = ['id', 'vesselType', 'mmsi', 'shipname', 'flag']
    carrier_from_encounters = carrier_from_encounters.drop_duplicates(subset=['mmsi'])
    carrier_from_encounters = carrier_from_encounters[~carrier_from_encounters['mmsi'].isin(carriers_new['mmsi'])]
    carrier_from_encounters['dataset'] = 'API-encounters'
    frames_carr_enc = [carrier1,carrier_from_encounters]

    carrier2 = pd.concat(frames_carr_enc)

    carrier_from_port = port_visits_result[['vessel_id','vessel_type','vessel_ssvid','vessel_name','vessel_flag']].copy()
    carrier_from_port = carrier_from_port[carrier_from_port['vessel_type']=='carrier']
    carrier_from_port.columns = ['id', 'vesselType', 'mmsi', 'shipname', 'flag']
    carrier_from_port = carrier_from_port.drop_duplicates(subset=['mmsi'])
    carrier_from_port = carrier_from_port[~carrier_from_port['mmsi'].isin(carriers_new['mmsi'])]
    carrier_from_port['dataset'] = 'API-port'
    frames_carr_por = [carrier2,carrier_from_port]

    carrier3 = pd.concat(frames_carr_por)




    return carrier3, loitering_result, encounter_result, port_visits_result