import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import date
from operator import attrgetter
import numpy as np
warnings.filterwarnings("ignore")

def createcolumns(carriers, loitering, encounters, port_visits):
    '''
    Input: pandas.DataFrames for carriers, loitering, encounters, port_visits

    Output: 1 pandas.DataFrames for new carriers
    '''
    print('Step 1/6: Creating MMSI based table')
    id = carriers[['mmsi','imo','dataset']].copy()
    id[id.dataset == 'API-port']
    id = id.drop_duplicates(subset=['mmsi'])
    id = id.set_index('mmsi')
    id = id.fillna(-1)
    id = id.join(loitering.groupby(['vessel.mmsi'])['id'].count())
    id = id.rename({
        'id': 'loitering',
        },
        axis = 1)

    #loitering and encounter number with types
    print('Step 2/6: Calcuate loitering and encounter number with types')
    a = encounters.groupby(['vessel.mmsi','encounter.authorization_status'])['id'].count().reset_index()
    b = encounters.groupby(['encounter.encountered_vessel.mmsi','encounter.authorization_status'])['id'].count().reset_index()
    a = a.pivot(index='vessel.mmsi', columns='encounter.authorization_status', values='id')
    b = b.pivot(index='encounter.encountered_vessel.mmsi', columns='encounter.authorization_status', values='id')
    tmp = pd.concat([a, b]).reset_index().groupby(['index'])['authorized','partial','pending','unknown'].sum()
    tmp = tmp.rename({
        'authorized': 'authorized_encounter',
        'partial': 'partial_encounter',
        'pending': 'pending_encounter',
        'unknown': 'unknown_encounter',
        },
        axis = 1)

    id2 = id.join(tmp)
    id2['encounter'] = id2['authorized_encounter'] + id2['partial_encounter'] + id2['pending_encounter'] + id2['unknown_encounter']
    id2 = id2.fillna(0)


    # last 6 month and 12 month
    print('Step 3/6: Calcuate last 6 month and 12 month meetups')
    loitering['month'] = pd.to_datetime(loitering['start'].str.replace('UTC','')).dt.to_period('M')
    encounters['month'] = pd.to_datetime(encounters['start'].str.replace('UTC','')).dt.to_period('M')
    l = loitering[loitering['month'] >= loitering['month'].max()-6]
    e = encounters[encounters['month'] >= encounters['month'].max()-6]

    id3 = id2.join(l.groupby(['vessel.mmsi'])['id'].count())
    id3 = id3.rename({
        'id': 'loitering_06',
        },
        axis = 1)
    id3 = id3.join(e.groupby(['vessel.mmsi'])['id'].count())
    id3 = id3.rename({
        'id': 'encounters_06',
        },
        axis = 1)
    l = loitering[loitering['month'] >= loitering['month'].max()-12]
    e = encounters[encounters['month'] >= encounters['month'].max()-12]
    id3 = id3.join(l.groupby(['vessel.mmsi'])['id'].count())
    id3 = id3.rename({
        'id': 'loitering_12',
        },
        axis = 1)
    id3 = id3.join(e.groupby(['vessel.mmsi'])['id'].count())
    id3 = id3.rename({
        'id': 'encounters_12',
        },
        axis = 1)
    id3 = id3.fillna(0)

    # most frequent port_visit 
    print('Step 4/6: Calcuate most frequent port_visit')
    visit=port_visits.groupby(['vessel_ssvid','name','flag'])['event_id'].count().sort_values().groupby(level=0).tail(1)
    visit
    id4 = id3.join(visit.reset_index().set_index('vessel_ssvid'))
    id4 = id4.rename({
        'name': 'port_name',
        'event_id': 'visit_times',
        'flag':'port_country'
        },
        axis = 1)

    # last port_visit
    port_visits.groupby(['vessel_ssvid'])['event_id'].count()
    port_visits['month'] = pd.to_datetime(port_visits['event_start'].str.replace('UTC','')).dt.to_period('D')
    last = port_visits.groupby(['vessel_ssvid','name','flag'])['month'].max().sort_values().groupby(level=0).tail(1)

    id5 = id4.join(last.reset_index().set_index('vessel_ssvid'))

    id5 = id5.rename({
        'name': 'last_port_name',
        'month': 'last_visit_times',
        'flag' : 'last_port_country'
        },
        axis = 1)

    id5['total_meetup'] = id5[['loitering', 'authorized_encounter', 'partial_encounter', 'pending_encounter', 'unknown_encounter']].sum(axis=1)
    id5['imo'] = id5['imo'].replace(0, np.nan).replace(-1, np.nan)
    id5['average_meetup'] = port_visits.groupby(['vessel_ssvid'])['event_id'].count()
    id5['average_meetup'] = id5['total_meetup']/id5['average_meetup']
    id5.reset_index().rename({
        'index': 'MMSI',
        },
        axis = 1)

    ## The meetup likelihood
    print('Step 5/6: Calcuate the next meetup likelihood')
    port_visits['month'] = pd.to_datetime(port_visits['event_start'].str.replace('UTC','')).dt.to_period('M')
    id5['last_port_visit_month'] = port_visits.groupby(['vessel_ssvid'])['month'].max().to_frame()
    id5['avg_month_port_visit'] = encounters[['vessel.mmsi', 'month']].groupby(['vessel.mmsi', 'month'])['month'].count() \
        .to_frame().rename({'month': 'count',},axis = 1) \
        .add(encounters[['encounter.encountered_vessel.mmsi', 'month']] \
            .groupby(['encounter.encountered_vessel.mmsi', 'month'])['month'].count() \
            .to_frame().rename({'month': 'count',},axis = 1) \
            .reset_index().rename({'encounter.encountered_vessel.mmsi': 'vessel.mmsi',},axis = 1) \
            .set_index(['vessel.mmsi','month']), fill_value=0) \
        .add(loitering[['vessel.mmsi', 'month']] \
            .groupby(['vessel.mmsi', 'month'])['month'].count() \
            .to_frame().rename({'month': 'count',},axis = 1), fill_value=0).reset_index() \
    .groupby(['vessel.mmsi'])['count'].mean().to_frame()
    id5['meetup_since_last_port'] = 0
    id5.loc[566041000]['meetup_since_last_port'] = 1

    m = []
    for i in id5.index:
        ttl = 0
        ttl += loitering[(loitering['vessel.mmsi'] == i) & (loitering['month']>=id5.loc[i]['last_port_visit_month'])]['id'].count()
        ttl += encounters[(encounters['vessel.mmsi'] == i) & (encounters['month']>=id5.loc[i]['last_port_visit_month'])]['id'].count()
        ttl += encounters[(encounters['encounter.encountered_vessel.mmsi'] == i) & (encounters['month']>=id5.loc[i]['last_port_visit_month'])]['id'].count()
        m.append(ttl)
    m
    id5['meetup_since_last_port'] = m
    id5['month_since_last_port'] = (pd.Period(date.today(), freq='M').to_timestamp()-id5['last_port_visit_month'].dt.to_timestamp())//np.timedelta64(1, 'M')
    id5['likely_remaining_meetup'] = id5['month_since_last_port']*id5['avg_month_port_visit'] - id5['meetup_since_last_port']
    

    print('Step 6/6: eez and rfmo analysis')
    additional = {
        '8487': 'Japanese Exclusive Economic Zone',
        '8492': 'Indonesian Exclusive Economic Zone',
        '48950': 'Kuril Islands (Japan v. Russia)',
        '8471': 'Guinea Bissau Exclusive Economic Zone',
        '8463': 'United States Exclusive Economic Zone (Alaska)',
        '8488': 'Kiribati Exclusive Economic Zone',
        '8486': 'Chinese Exclusive Economic Zone',
        '8493': 'Canadian Exclusive Economic Zone',
    }
    loitering.loc[loitering.eez =='48964, 8471','eez'] = '8471'
    loitering.loc[loitering.eez =='48962, 8431','eez'] = '8431'
    loitering.loc[loitering.eez =='48967, 5696','eez'] = '5696'
    loitering.loc[loitering.eez =='8435, 48967','eez'] = '8435'
    loitering.loc[loitering.eez =='8467, 48961','eez'] = '8467'
    loitering.loc[loitering.eez =='48967, 8435','eez'] = '8435'
    loitering.loc[loitering.eez =='8431, 48962','eez'] = '8431'
    loitering.loc[loitering.eez =='8371, 48964','eez'] = '8371'
    loitering.loc[loitering.eez =='5696, 48967','eez'] = '5696'
    loitering.loc[loitering.eez =='8471, 48964','eez'] = '8471'
    loitering.loc[loitering.eez =='48969, 8418','eez'] = '8418'
    loitering.loc[loitering.eez =='48964, 8371','eez'] = '8371'
    loitering.loc[loitering.eez =='48961, 8467','eez'] = '8467'
    loitering.loc[loitering.eez =='48974, 8431','eez'] = '8431'
    loitering.loc[loitering.eez =='48962, 8432','eez'] = '8432'
    loitering.loc[loitering.eez =='8431, 48974','eez'] = '8431'
    loitering.loc[loitering.eez =='48970, 8426','eez'] = '8426'
    loitering.eez = loitering.eez.astype('float64')
    encounters.eez =encounters.eez.astype('float64')

    # mmsi + eez
    eez = encounters[['vessel.mmsi', 'eez']].groupby(['vessel.mmsi', 'eez'])['eez'].count() \
        .to_frame().rename({'eez': 'count',},axis = 1) \
        .add(encounters[['encounter.encountered_vessel.mmsi', 'eez']] \
            .groupby(['encounter.encountered_vessel.mmsi', 'eez'])['eez'].count() \
            .to_frame().rename({'eez': 'count',},axis = 1) \
            .reset_index().rename({'encounter.encountered_vessel.mmsi': 'vessel.mmsi',},axis = 1) \
            .set_index(['vessel.mmsi','eez']), fill_value=0) \
        .add(loitering[['vessel.mmsi', 'eez']] \
            .groupby(['vessel.mmsi', 'eez'])['eez'].count() \
            .to_frame().rename({'eez': 'eez_visit',},axis = 1), fill_value=0).reset_index()
    eez.eez = eez.eez.astype('int').astype('str')
    eez = eez[eez['eez'].isin(additional)].set_index(['vessel.mmsi','eez']).unstack().rename(additional,
        axis = 1)
    id6 = id5.join(eez)

    plot_data5 = loitering \
        .rename({'regions.rfmo': 'rfmo'}, axis=1) \
        .groupby(['rfmo','vessel.mmsi'])['id'] \
        .nunique() \
        .reset_index() \
        .sort_values('id')
    plot_data5 = plot_data5.set_index(plot_data5.columns.drop('rfmo',1).tolist()) \
        .rfmo.str.split(',', expand=True) \
        .stack() \
        .reset_index() \
        .rename(columns={0:'rfmo'}) \
        .loc[:, plot_data5.columns] \
        .groupby(['rfmo','vessel.mmsi'])['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id')
    plot_data5 = plot_data5.set_index(plot_data5.columns.drop('rfmo',1).tolist()) \
        .rfmo.str.split('|', expand=True) \
        .stack() \
        .reset_index() \
        .rename(columns={0:'rfmo'}) \
        .loc[:, plot_data5.columns] \
        .groupby(['rfmo','vessel.mmsi'])['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id')
    plot_data5['rfmo'] = plot_data5['rfmo'].str.replace(' ','')
    plot_data5 = plot_data5 \
        .groupby(['vessel.mmsi','rfmo'])['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id').rename({'id': 'rfmo_visit'}, axis=1)

    rfmo = plot_data5.set_index(['vessel.mmsi','rfmo']).unstack()
    id6 = id6.join(rfmo)

    print(id6.columns)
    return id6

