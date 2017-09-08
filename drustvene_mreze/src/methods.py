# coding = utf-8

from collections import OrderedDict
from operator import itemgetter
from collections import Counter
import csv
import networkx as nx
from networkx.algorithms import centrality as central

__author__ = "Tamara Komnenic"


def filter_nodes(attrs, edges):
    nodes = attrs.keys()
    keys = edges.iloc[:, 0]
    values = edges.iloc[:, 1]

    for_remove = []
    l = []

    for key in keys:
        l.append(key)
    for value in values:
        l.append(value)
    for node in nodes:
        if node in l:
            continue
        else:
            for_remove.append(node)
    for key in for_remove:
        attrs.pop(key)
    return


def sort_dictionary_by_value_asc(input_dict):
    output_dict = OrderedDict(sorted(input_dict.items(), key=itemgetter(1)))
    return output_dict


def sort_dictionary_by_value_desc(input_dict):
    output_dict = OrderedDict(sorted(input_dict.items(), key=itemgetter(1)))
    return output_dict


def write_highest_degrees(temp, file_degree, stop):
    degrees_high = sort_dictionary_by_value_desc(temp.degree())
    degrees_high_count = Counter(degrees_high)
    writer = csv.writer(file_degree, delimiter=';')
    row = [stop.date()]
    for k, v in degrees_high_count.most_common(5):
        row.append('%s: %i (%i + %i)' % (k.replace(',', ''), v, temp.in_degree(k), temp.out_degree(k)))
    writer.writerow(row)
    return


def write_highest_k(temp, file_katz, stop):
    k_high = sort_dictionary_by_value_desc(nx.katz_centrality_numpy(temp))
    k_high_count = Counter(k_high)
    writer = csv.writer(file_katz, delimiter=';')
    row = [stop.date()]
    for k, v in k_high_count.most_common(5):
        row.append('%s: %f' % (k.replace(',', ''), v))
    writer.writerow(row)
    return


def write_highest_degree_cent(temp, file_degree_centr, stop):
    dc_high = sort_dictionary_by_value_desc(central.degree_centrality(temp))
    dc_high_count = Counter(dc_high)
    writer = csv.writer(file_degree_centr, delimiter=';')
    row = [stop.date()]
    for k, v in dc_high_count.most_common(5):
        row.append('%s: %f' % (k.replace(',', ''), v))
    writer.writerow(row)
    return


def write_highest_ev_cent(temp, file_eigenvector, stop):
    ev_high = sort_dictionary_by_value_desc(nx.eigenvector_centrality_numpy(temp))
    ev_high_count = Counter(ev_high)
    writer = csv.writer(file_eigenvector, delimiter=';')
    row = [stop.date()]
    for k, v in ev_high_count.most_common(5):
        row.append('%s: %f' % (k.replace(',', ''), v))
    writer.writerow(row)
    return


def collect_cluster_coef(datelist, stop, temp, cluster_dict):
    datelist.append(stop.date())
    clustering_high = sort_dictionary_by_value_desc(nx.clustering(temp))
    clustering_high_count = Counter(clustering_high)
    for k, v in clustering_high_count.most_common():
        if k in cluster_dict.keys():
            cluster_dict.get(k.replace(',', '')).append(v)
        else:
            cluster_dict[k.replace(',', '')] = [v]
    return


def write_all_cluster_coef(datelist, file_clustering, cluster_dict):
    writer = csv.writer(file_clustering, delimiter=';')
    datelist.append("propis/godina")
    writer.writerow(datelist[::-1])
    for k in cluster_dict.keys():
        writer.writerow([k.replace(',', ''), ','.join(str(v) for v in cluster_dict.get(k)[::-1])])
    return


def write_avg_clustering(file_global_clustering, global_clust):
    writer = csv.writer(file_global_clustering, delimiter=';')
    writer.writerow(['Date', 'Avg coefficient'])
    for k in global_clust.keys():
        writer.writerow([k, global_clust.get(k)])
    return
