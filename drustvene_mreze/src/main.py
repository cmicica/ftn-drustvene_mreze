# coding = utf-8

import pandas as pd
import graphistry
import warnings
import datetime
import dateutil.relativedelta as relativedelta
from methods import *

__author__ = "Tamara Komnenic"

# Definisati putanju do projekta
prefix_path = "/home/cm/PycharmProjects/drustvene_mreze/"

# setup
warnings.filterwarnings('ignore')
api_key = open(prefix_path + 'API_key.txt').read()
graphistry.register(key=api_key)


edges = pd.read_csv(prefix_path + 'dataset/new_data/all_text_lines.txt', sep='\t\t\t', names=['src', 'dest'])
graph = nx.from_pandas_dataframe(edges, source='src', target='dest', create_using=nx.DiGraph())
attributes = pd.read_csv(prefix_path + 'dataset/new_data/name_date.txt', sep='\t', names=['node', 'value'])

attrs = attributes.set_index('node')['value'].to_dict()

filter_nodes(attrs, edges)


stop = datetime.datetime(1801, 1, 1)
current = datetime.datetime.now()

nx.set_node_attributes(graph, 'timestamp', attrs)

# Eksportovanje grafa za ucitavanje u Gephi
nx.write_gexf(graph, prefix_path + 'dataset/results/lg_network.gexf', version='1.2draft')

# Kreiranje grafa i pokretanje alata u browser-u

# graphistry.bind(source='src', destination='dst', node='nodeid').plot(graph)


file_degree = open(prefix_path + 'dataset/results/highest_degrees.csv', 'w+')
file_katz = open(prefix_path + 'dataset/results/katz_centrality.csv', 'w+')
file_degree_centr = open(prefix_path + 'dataset/results/degree_centrality.csv', 'w+')
file_eigenvector = open(prefix_path + 'dataset/results/eigenvector_centrality.csv', 'w+')
file_clustering = open(prefix_path + 'dataset/results/clustering_coefficient.csv', 'w+')
file_global_clustering = open(prefix_path + 'dataset/results/avg_clustering_coefficient.csv', 'w+')

datelist = []
cluster_dict = {}
global_clust = {}


while current > stop:
    temp = graph.subgraph([n for n, attrdict in graph.node.items() if 'timestamp' in attrdict and
                           datetime.datetime.strptime(attrdict['timestamp'], "%Y-%m-%d %H:%M:%S") < stop])
    #write degrees
    write_highest_degrees(temp, file_degree, stop)
    #write K
    write_highest_k(temp, file_katz, stop)
    #write highest degrees
    write_highest_degree_cent(temp, file_degree_centr, stop)

    # collect avg clustering coefficient
    global_clust[stop.date()] = nx.transitivity(temp)

    temp = temp.to_undirected()

    #write eigenvector
    write_highest_ev_cent(temp, file_eigenvector, stop)

    #collect individual clustering coefficient
    collect_cluster_coef(datelist, stop, temp, cluster_dict)

    # korak promene vremena izmedju 2 racunanja
    stop = stop + relativedelta.relativedelta(months=6)

# write cluster
write_all_cluster_coef(datelist, file_clustering, cluster_dict)
# write avg cluster
write_avg_clustering(file_global_clustering, global_clust)

file_degree.close()
file_katz.close()
file_degree_centr.close()
file_eigenvector.close()
file_clustering.close()
file_global_clustering.close()
