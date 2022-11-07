import pandas as pd


def merge_local_and_api(
        loitering, encounters, port_visits, carriers_new, loitering_new, encounters_new, port_visits_new):
    '''
    Input: pandas.DataFrames for carriers, loitering, encounters, and port_visits from local sources and api calls

    Output: four pandas.DataFrames for combined data of carriers, loitering, encounters, and port_visits
    '''

    ## merge loitering
    print(' > Now updating loitering')
    loitering_new.columns = ['id', 'type', 'start', 'end', 'lat', 'lon','mpa', 'eez', 'regions.rfmo','fao', 'major_fao', 'eez12nm',
       'boundingBox', 'startDistanceFromShoreKm', 'endDistanceFromShoreKm',
       'startDistanceFromPortKm', 'endDistanceFromPortKm','vessel.id','vessel.flag','vessel.name','vessel.type','vessel.mmsi',
                     'totalTimeHours',
       'totalDistanceKm', 'averageSpeedKnots', 'averageDistanceFromShoreKm']
    frames3 = [loitering,loitering_new[~loitering_new['id'].isin(loitering['id'])]]

    loitering_result = pd.concat(frames3)


    ## merge encounters
    print(' > Now updating encounters')
    encounters_new.columns = ['id', 'type', 'start', 'end', 'lat', 'lon','mpa', 'eez', 'regions.rfmo','fao', 'major_fao', 'eez12nm',
       'boundingBox', 'startDistanceFromShoreKm', 'endDistanceFromShoreKm',
       'startDistanceFromPortKm', 'endDistanceFromPortKm','vessel.id','vessel.flag','vessel.name','vessel.type','vessel.mmsi',
                  'encounter.encountered_vessel.id', 'encounter.encountered_vessel.flag', 'encounter.encountered_vessel.name',
                    'encounter.encountered_vessel.type','encounter.encountered_vessel.mmsi','medianDistanceKilometers', 'medianSpeedKnots',
       'encounter_type']

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
    port_visits = port_visits[port_visits.columns[:11].append(port_visits.columns[-4:])]
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