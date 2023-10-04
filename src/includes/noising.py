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
# @description: Introducing noice into a given network, in order to built its complementary for testing.
###

getcontext().prec = 5  # decimal precision

# Remove, or Remove-and-Add
'''
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
'''

# Shuffling
def _shuffling(G, noise:(float) = 0.1, basepath=None):
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

    # only for testing
    '''
    f = open( basepath + '../../results.log' , 'a')
    writer = csv.writer(f)
    writer.writerow( [ noise, log['diff'], log['ged'], len(shuffles) ] )
    f.close()
    '''

    return G_noised, log

def noising(dataset_name, network, noises, noise_type, data=True, basepath=None, log=dict()):
    
    if basepath is None:
        basepath = os.path.dirname(__file__) + "/"

    log['noise'] = {}

    for noise in noises:
        noise_decimal = float(noise) / 100
        output = None
        
        if noise_type == "shuffling":
            output, output_log = _shuffling( network, noise_decimal, basepath )
        '''
        elif noise_type == 'removing_adding':
            output, output_log = _removing_adding( network, noise_decimal, True )
        elif noise_type == 'removing':
            output, output_log = _removing_adding( network, noise_decimal, False )
        else:
            break
        '''

        nx.write_edgelist( output, basepath + dataset_name  + "_" + str(noise) + ".txt", data=data)
        log['noise'][str(noise)] = output_log
    
    return log