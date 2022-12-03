import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx


def make_plot(name, start, end, top_n, edge_threshold, encounters, mmsi, loitering):
    loitering = loitering.loc[loitering['start'] >= start,:]
    loitering = loitering.loc[loitering['start'] <= end,:]
    loitered_grouped = loitering.groupby(['vessel.mmsi', 'vessel.name'])['id'] \
        .count().reset_index() \
        .rename({'id':'loitering', 'vessel.mmsi':'mmsi', 'vessel.name':'Name'}, axis=1)
    loitered_grouped.sort_values('loitering', ascending=False, inplace=True)
    top_100_loiterers = loitered_grouped['mmsi'].head(top_n)
    top_100_names = loitered_grouped['Name'].head(top_n).reset_index(drop=True)
    # top_100_flags = mmsi['Flag'].head(top_n).reset_index(drop=True)
    # top_100_owner = mmsi['Registered Owner'].head(top_n).reset_index(drop=True)
    encounters = encounters.loc[encounters['vessel.mmsi'].isin(top_100_loiterers),:]
    encounters = encounters.loc[encounters['start'] >= start,:]
    encounters = encounters.loc[encounters['start'] <= end,:]
    ship_indices = list(encounters['vessel.mmsi'].unique())
    E = np.zeros((len(ship_indices),len(ship_indices)))
    for x in range(len(ship_indices)):
        for y in range(len(ship_indices)):
            encounters_of_y = encounters.loc[encounters['vessel.mmsi']==ship_indices[y],:]
            fishers_of_y = encounters_of_y['encounter.encountered_vessel.mmsi']
            encounters_of_fishers = encounters.loc[encounters['encounter.encountered_vessel.mmsi'].isin(fishers_of_y),:]
            encounters_of_x = len(encounters_of_fishers.loc[encounters_of_fishers['vessel.mmsi']==ship_indices[x],:])
            E[x,y] = encounters_of_x

    G = nx.Graph()
    ship_idx = range(len(ship_indices))
    for i in ship_idx:
        G.add_node(
            i, 
            label=top_100_names.reset_index(drop=True)[i])
    for i in ship_idx:
        for j in ship_idx:
            if i > j:
                if (E[i,j]+E[i,j]) >= edge_threshold:
                    G.add_edge(i,j,weight=(E[i,j]+E[j,i])/40)
    net = Network(notebook=False)
    net.from_nx(G)
    net.show('port_evaluation/output/networks/{name}.html'.format(name=name))

if __name__=='__main__':
    encounters = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/encounters.csv')
    loitering = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/loitering.csv')
    port_visits = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/port_visit.csv')
    mmsi = pd.read_csv('/Users/sebastiandodt/Desktop/final table (1).csv')

    print(len)

    for year in range(2012,2023):
        for edge_threshold in [5, 10, 50, 100]:
            print(" > Generating network for {year} and thre. {t}...".format(year=year, t=edge_threshold))
            start = '{year}-01-01'.format(year=year)
            end = '{year}-12-31'.format(year=year)
            top_n = 140
            # edge_threshold = 7
            name = '{year}_{t}'.format(year=year, t=edge_threshold)
            make_plot(name, start, end, top_n, edge_threshold, encounters, mmsi, loitering)
    print(" > Done.")