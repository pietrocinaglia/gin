# -*- coding: utf-8 -*-
import os
import networkx as nx
from random import sample
from decimal import *
import csv

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
###

getcontext().prec = 5  # decimal precision

def multilayerNetwork(dataset_name:(str), l:(int), n:(int), m:(int), p:(float), q:(float), z:(float), basepath=None):
    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"
    
    layers = []
    log = []
    for i in range(0,l):
        tmp = nx.extended_barabasi_albert_graph(n, m, p, q)
        layer = nx.Graph()
        layer.add_nodes_from(tmp.nodes) #, id=(i+1)
        layer.add_edges_from(tmp.edges, intralayer=(i+1))
        log.append( "- Layer " + str(i+1) + " - nodes:" + str(layer.number_of_nodes()) + ", edges:" + str(layer.number_of_edges()) )
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

        l1_r = sample(list(l1.nodes()), rate)
        l2_r = sample(list(l1.nodes()), rate)

        for r in range(rate):
            multiLayerNetwork.add_edge( (l1_tag+str(l1_r[r])), (l2_tag+str(l2_r[r])), interlayer=interlayer_last_id)

        interlayer_last_id += 1

        log.append( "- Interlayer " + str(interlayer_last_id) + " (" + l1_tag + "-" + l2_tag + ") - edges:" + str(rate) )

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
    
    # multiLayerNetwork_edgelist = nx.generate_edgelist(multiLayerNetwork, data=False)
    
    return multiLayerNetwork