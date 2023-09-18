# -*- coding: utf-8 -*-
import os
import networkx as nx
import random
from decimal import *
import math

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
# @description: Introducing noice into a given network, in order to built its complementary for testing.
###

getcontext().prec = 5  # decimal precision

# Remove, or Remove-and-Add
def _removing_adding(G, noise:(float) = 0.1, offset:(bool)=False):
    log = {"added" : [], "removed": []}

    noise:int = math.floor(G.number_of_edges() * noise)
    edges = list(G.edges)
    nonedges = list(nx.non_edges(G))

    for i in range(noise):
        chosen_edge = random.choice(edges)
        if G.degree(chosen_edge[0]) > 1 and G.degree(chosen_edge[1]) > 1:
            try:
                G.remove_edge(chosen_edge[0], chosen_edge[1])
            except nx.NetworkXError: # jump
                i = i - 1
                continue
        else: # jump
            i = i - 1
            continue
        
        log['removed'].append(chosen_edge)
        print("(" + str(chosen_edge[0]) + "," + str(chosen_edge[1]) + ") REMOVED" )

        if offset:
            chosen_nonedge = random.choice([x for x in nonedges if chosen_edge[0] == x[0]])
            G.add_edge(chosen_nonedge[0], chosen_nonedge[1])
            log['added'].append(chosen_nonedge)
            print("(" + str(chosen_nonedge[0]) + "," + str(chosen_nonedge[1]) + ") ADDED" )

    return G, log

# Shuffling
def _shuffling(G, noise:(float) = 0.1):
    exchanges:int = int(math.floor(G.number_of_edges() * noise) / 2)
    edges = list(G.edges(data=True))
    
    log = {"shuffles:" : []}

    for i in range(exchanges):
        chosen_edge1 = random.choice(edges)
        chosen_edge2 = random.choice(edges)
        
        if ('layer' not in chosen_edge1[2] or 'layer' not in chosen_edge2[2]):
            i = i - 1
            continue

        if (chosen_edge1[2]['layer'] == chosen_edge2[2]['layer']):
            G.add_edge(chosen_edge1[0], chosen_edge2[1], layer=chosen_edge1[2]['layer'])
            G.add_edge(chosen_edge1[1], chosen_edge2[0], layer=chosen_edge1[2]['layer'])
            log['shuffles'].append( (str(chosen_edge1),str(chosen_edge2)) )
        else:
            i = i - 1
            continue

    return G, log

def noising(dataset_name, network, noises, type, basepath=None):

    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"

    for noise in noises:
        noise = float(noise) / 100
        output = None
        log = None
        if type == 'removing':
            output, log = _removing_adding( network, noise, False )
        elif type == 'removing_adding':
            output, log = _removing_adding( network, noise, True )
        elif type == "shuffling":
            output, log = _shuffling( network, noise )
        else:
            break
        
        nx.write_edgelist( output, basepath + dataset_name  + "_" + str(int(noise*100)) + ".txt", data=True)