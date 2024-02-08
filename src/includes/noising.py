# -*- coding: utf-8 -*-
import os
import networkx as nx
import random
from decimal import *
import math

import csv

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
# @description: Introducing random noice into a given network, to built its complementary for testing.
# @url: https://github.com/pietrocinaglia/gin
###

getcontext().prec = 5  # decimal precision

# Shuffling
def __shuffling(G, noise:(float) = 0.1, basepath=None):
    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"

    G_noised = G.copy()
    edges = [] # only interlayer edges
    for n1, n2, data in G_noised.edges(data=True):
        if 'intralayer' in data:
            edges.append((n1,n2,data))
    
    exchanges = math.floor( len(edges) * noise / (1+noise) )
   
    shuffles = []
    diff = 0
    while diff < noise:
        chosen_edge1 = random.choice(edges)
        chosen_edge2 = random.choice(edges)

        if (chosen_edge1[2]['intralayer'] == chosen_edge2[2]['intralayer']):
            G_noised.add_edge(chosen_edge1[0], chosen_edge2[1], intralayer=chosen_edge1[2]['intralayer'])
            G_noised.add_edge(chosen_edge1[1], chosen_edge2[0], intralayer=chosen_edge1[2]['intralayer'])
            shuffles.append( (str(chosen_edge1[:2]),str(chosen_edge2[:2])) )
            diff = nx.difference(G_noised, G).number_of_edges() / G_noised.number_of_edges()
    
    ged = nx.graph_edit_distance(G, G_noised)
    #
    log = dict()
    log['diff'] = round(diff, 3)
    log['ged'] = ged
    log['shuffles'] = shuffles

    return G_noised, log

def noising(dataset_name, network, noises, noise_type, data=True, basepath=None, log=dict()):
    
    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"

    log['noise'] = {}

    for noise in noises:
        noise_decimal = float(noise) / 100
        output = None
        
        if noise_type == "shuffling":
            output, output_log = __shuffling( network, noise_decimal, basepath )
        else:
            break

        nx.write_edgelist( output, basepath + dataset_name  + "_" + str(noise) + ".txt", data=data)
        log['noise'][str(noise)] = output_log
    
    return log