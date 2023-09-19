# -*- coding: utf-8 -*-
import os
import networkx as nx
import random
from decimal import *
import csv

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
###

getcontext().prec = 5  # decimal precision

def multilayerNetwork(dataset_name:(str), l:(int), n:(int), m:(int), p:(float), q:(float), z:(float), basepath=None, log=dict()):
    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"
    
    layers = []
    log['main'] = {}
    log['main']['layers'] = []
    log['main']['interlayers'] = []

    for i in range(0,l):
        tmp = nx.extended_barabasi_albert_graph(n, m, p, q)
        layer = nx.Graph()
        layer.add_nodes_from(tmp.nodes) #, id=(i+1)
        layer.add_edges_from(tmp.edges, intralayer=(i+1))
        log['main']['layers'].append( {"id":str(i+1), "nodes": str(layer.number_of_nodes()), "edges": str(layer.number_of_edges())} )
        layers.append(layer)

    multiLayerNetwork = nx.Graph()
    interlayer_last_id = 1

    for i in range(0,l-1):
        l1 = layers[i]
        l2 = layers[i+1]
        l1_tag = "L" + str(i+1)
        l2_tag = "L" + str(i+2)

        if i == 0:
            multiLayerNetwork = nx.union(multiLayerNetwork, l1, rename=("", l1_tag))
            
        multiLayerNetwork = nx.union(multiLayerNetwork, l2, rename=("", l2_tag))
        
        rate = int( (layers[i].number_of_edges()+layers[i+1].number_of_edges()) * z / 100 )

        l1_nodes = list(l1.nodes())
        l2_nodes = list(l2.nodes())

        for _ in range(rate):
            v = random.choice(l1_nodes)
            u = random.choice(l2_nodes)
            multiLayerNetwork.add_edge( (l1_tag+str(v)), (l2_tag+str(u)), interlayer=interlayer_last_id)

        log['main']['interlayers'].append( {"id":str(interlayer_last_id), "layers": [str(interlayer_last_id),str(interlayer_last_id+1)], "edges": str(rate)} )

        interlayer_last_id += 1

        if i == 0:
            seed = []
            for node in l1.nodes():
                seed.append([l1_tag+str(node), l1_tag+str(node)])
            with open(basepath + dataset_name + "_seed_" + l1_tag + ".txt", 'w', newline='') as file:
                csv.writer(file).writerows(seed)

        seed = []
        for node in l2.nodes():
            seed.append([l2_tag+str(node), l2_tag+str(node)])
        with open(basepath + dataset_name + "_seed_" + l2_tag + ".txt", 'w', newline='') as file:
            csv.writer(file).writerows(seed)

    nx.write_edgelist(multiLayerNetwork, basepath + dataset_name + ".txt", data=True)
        
    return multiLayerNetwork, log