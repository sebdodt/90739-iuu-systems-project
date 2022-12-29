import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

sns.set_style('white')
sns.set_context("paper", font_scale = 1)
color = sns.color_palette("tab10", 10)[0]

def data_rfmo(mmsis, loitering):
        ## for Dylan: add 'event_id' to all groupby's
    loitering = loitering.loc[loitering['vessel.mmsi'].isin(mmsis),:]
    plot_data5 = loitering \
        .rename({'regions.rfmo': 'rfmo'}, axis=1) \
        .groupby('rfmo')['id'] \
        .nunique() \
        .reset_index() \
        .sort_values('id')
    plot_data5 = plot_data5.set_index(plot_data5.columns.drop('rfmo',1).tolist()) \
        .rfmo.str.split(',', expand=True) \
        .stack() \
        .reset_index() \
        .rename(columns={0:'rfmo'}) \
        .loc[:, plot_data5.columns] \
        .groupby('rfmo')['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id')
    plot_data5 = plot_data5.set_index(plot_data5.columns.drop('rfmo',1).tolist()) \
        .rfmo.str.split('|', expand=True) \
        .stack() \
        .reset_index() \
        .rename(columns={0:'rfmo'}) \
        .loc[:, plot_data5.columns] \
        .groupby('rfmo')['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id')
    plot_data5['rfmo'] = plot_data5['rfmo'].str.replace(' ','')
    plot_data5 = plot_data5 \
        .groupby('rfmo')['id'] \
        .sum() \
        .reset_index() \
        .sort_values('id', ascending=False)  
    plot_data5['loit_share'] = 100*plot_data5['id']/len(loitering)
    plot_data5 = plot_data5.loc[plot_data5['rfmo']!='ACAP',:]
    plot_data5 = plot_data5.loc[plot_data5['rfmo']!='IWC',:]
    return plot_data5



def data_port(mmsis, port_visits):
    selected = port_visits.loc[port_visits['vessel_ssvid'].isin(mmsis),:]
    grouped = selected.groupby('name1')['event_id'].count().reset_index().sort_values('event_id', ascending=False)
    grouped['name1'] = grouped['name1'].str.title()
    return grouped


def make_plot(name, start, end, top_n, edge_threshold, encounters, mmsi, loitering, port_visits):
    loitering = loitering.loc[loitering['start'] >= start,:]
    loitering = loitering.loc[loitering['start'] <= end,:]
    port_visits = port_visits.loc[port_visits['event_start'] >= start,:]
    port_visits = port_visits.loc[port_visits['event_start'] <= end,:]
    loitered_grouped = loitering.groupby(['vessel.mmsi'])['id'] \
        .count().reset_index() \
        .rename({'id':'loitering', 'vessel.mmsi':'mmsi'}, axis=1) # , 'vessel.name':'Name'
    loitered_grouped.sort_values('loitering', ascending=False, inplace=True)
    top_100_loiterers = loitered_grouped['mmsi'].head(top_n)
    # top_100_names = loitered_grouped['Name'].head(top_n).reset_index(drop=True)
    n_loitering = np.log(loitered_grouped['loitering'].head(top_n).reset_index(drop=True)) # maybe add log
    # top_100_flags = mmsi['Flag'].head(top_n).reset_index(drop=True)
    # top_100_owner = mmsi['Registered Owner'].head(top_n).reset_index(drop=True)
    encounters = encounters.loc[encounters['vessel.mmsi'].isin(top_100_loiterers),:]
    encounters = encounters.loc[encounters['start'] >= start,:]
    encounters = encounters.loc[encounters['start'] <= end,:]
    ship_indices = list(encounters['vessel.mmsi'].unique())
    ship_names = {}
    for ship in ship_indices:
        ship_names[ship] = encounters.loc[encounters['vessel.mmsi']==ship,'vessel.name'].head(1).values[0]
    
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
            i)#, 
            #label=top_100_names.reset_index(drop=True)[i])
            #size=n_loitering[i]/max(n_loitering) * 5)
    for i in ship_idx:
        for j in ship_idx:
            if i > j:
                if (E[i,j]) >= edge_threshold:
                    if (E[i,j]) >= edge_threshold:
                        G.add_edge(i,j,weight=(E[i,j]+E[j,i])/40)
    net = Network(notebook=False)
    net.from_nx(G)
    # net.show('port_evaluation/output/networks/new_{name}_weighted_logged.html'.format(name=name))

    ## new attempt multiple plots

    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)
    networks = sorted(nx.connected_components(G), key=len, reverse=True)

    chinese = [
        'China National Fisheries Corporation',
        'Wei Fong Shipping Co Ltd',
        'Pingtairong Ocean Fishery',
        'Zhoushan Ningtai Ocean Fish',
        'Pingtan Marine Enterprise Ltd',
        'Fujian Gangshun Pelagi',
        'Zhoushan Zhongju Ocean',
        'Rongcheng Marine Fishery Co',
        'Rongcheng East China Fisheries',
        'Zhoushan Haili Ocean Fisheries'
        ]


    for i_net in range(len(networks)):
        if len(networks[i_net]) >= 4:
            fig = plt.figure("Degree of a random graph", figsize=(10.7, 6))
            axgrid = fig.add_gridspec(18, 32)

            ax0 = fig.add_subplot(axgrid[:, -18:])
            Gcc = G.subgraph(networks[i_net])
            pos = nx.spring_layout(Gcc, seed=10396953)

            pos_labels = {}
            label_names = {}
            node_weight = []
            mmsis = []
            for node, coords in pos.items():
                pos_labels[node] = (coords[0], coords[1] + 0.05)
                label_names[node] = ship_names[ship_indices[node]].title()
                mmsis.append(ship_indices[node])
                node_weight.append(loitered_grouped.loc[loitered_grouped['mmsi']==ship_indices[node],'loitering'].values[0] /max(n_loitering) * 1.8)
            edge_weights = list(nx.get_edge_attributes(G,'weight').values())

            nx.draw_networkx_nodes(Gcc, pos, ax=ax0,  label=True, node_size=node_weight) # node_size=20, 
            nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.25, width=edge_weights)
            nx.draw_networkx_labels(Gcc,pos_labels, ax=ax0, labels=label_names, font_size=7)
            ax0.set_title("Network {i} in {year}".format(i=i_net+1, year=start[:4]))
            ax0.set_axis_off()

            ports = data_port(mmsis, port_visits)
            rfmos = data_rfmo(mmsis, loitering)

            ax1 = fig.add_subplot(axgrid[:6, :12])
            sns.barplot(data=rfmos.head(10), 
                x='rfmo', 
                y='loit_share', 
                ax = ax1,
                color=color)
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, horizontalalignment='right')
            ax1.yaxis.set_major_formatter(mtick.PercentFormatter())
            ax1.set_title("RFMO of Dark Encounters")
            ax1.set_ylabel("% of dark encounters")
            ax1.set_xlabel("")

            ax2 = fig.add_subplot(axgrid[10:16, :12])
            sns.barplot(data = ports.head(10), x='name1', y='event_id', ax=ax2, color=color)
            ax2.tick_params(labelrotation=90)
            ax2.set_title("Port visits")
            ax2.set_ylabel("# of Port Visits in {year}".format(year=start[:4]))
            ax2.set_xlabel('')
            fig.tight_layout()
            plt.rcParams['savefig.transparent'] = True
            plt.savefig('port_evaluation/output/networks/10 dec/new_{name}_export2_{i}_p_trans.png'.format(name=name, i=i_net+1), dpi=800)
            plt.clf()


if __name__=='__main__':
    encounters = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/encounters.csv')
    loitering = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/loitering.csv')
    port_visits = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/unified/port_visit.csv')
    mmsi = pd.read_csv('/Users/sebastiandodt/Desktop/final table (1).csv')
    sv = pd.read_csv('/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/90739-iuu-systems-project/pipeline/data/seavision/lists-Reefers-2022-11-11_04-40.csv')
    not_reefer = sv.loc[sv['Vessel Type'] == '30-Fishing','MMSI']
    
    encounters.loc[~(encounters['vessel.mmsi'].isin(not_reefer)),:]
    loitering.loc[~(loitering['vessel.mmsi'].isin(not_reefer)),:]
    port_visits.loc[~(port_visits['vessel_ssvid'].isin(not_reefer)),:]


    for year in [2022]: #range(2012,2023):
        for edge_threshold in [20]:# [11,12,13,14,15,16,17,18,19]:# [5, 7, 10, 20]:
            print(" > Generating network for {year} and thre. {t}...".format(year=year, t=edge_threshold))
            start = '{year}-01-01'.format(year=year)
            end = '{year}-12-31'.format(year=year)
            for top_n in [130]:
                # top_n = 140
                # edge_threshold = 7
                
                name = '{year}_{t}_{n}'.format(year=year, t=edge_threshold, n=top_n)
                make_plot(name, start, end, top_n, edge_threshold, encounters, mmsi, loitering, port_visits)
    print(" > Done.")