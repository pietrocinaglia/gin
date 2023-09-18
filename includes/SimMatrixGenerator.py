# -*- coding: utf-8 -*-

import os
from unipath import Path
import networkx as nx
import random
from decimal import *
import numpy as np
import pandas as pd

getcontext().prec = 5  # decimal precision

###
# @author: Pietro Cinaglia
# @mail: cinaglia@unicz.it
# @description: Introducing noice into a given network, in order to built its complementary for testing.
###

current_path = os.path.dirname( os.path.realpath(__file__) )
current_path = Path( current_path )
workspace = current_path + "/"

data_path1 = input( "MultiLayer Network 1 (source) - Relative Path - :" )
data_path2 = input( "MultiLayer Network 2 (target) - Relative Path - :" )
noise = input( "Do you want apply noise? (e.g., 5% = 0.05) [Default: 0.0]:" )
output_filepath = input( "Output - Relative Path w/ filename (.sm) - :" )

if (noise == ''):
    noise = 0.0
else:
    noise = float(noise)

print( "Loading MLNetwork 1...")
G = nx.read_edgelist( workspace+data_path1, delimiter=' ', data=True )
print( '-- MLNet with ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
print( "Loading MLNetwork 1...")

H = nx.read_edgelist( workspace+data_path2, delimiter=' ', data=True )
print( '-- MLNet with ' + str(H.number_of_nodes()) + ' nodes and ' + str(H.number_of_edges()) + ' edges.')
print( "- [OK]" )
print()

print( "Similarity Matrix construction..." )
G_nodes = list(G.nodes)
H_nodes = list(H.nodes)
sim = []
threshold = 0.90 + ((1-0.90) * noise) # applying the normalized value of the noise.
for g in G_nodes:
    i = H_nodes.index(g)
    g_sim = np.random.uniform(low=0.0, high=threshold, size=len(H_nodes))
    g_sim[i] = random.uniform(0.9, 1.0)
    sim.append(g_sim)

print( "- [OK]" )
print()

print( "Saving Node Similarities as 'Similarity Matrix (.sm)' file format; compression: gzip." )
pd.DataFrame(sim).to_csv(workspace + output_filepath, index=False, compression="gzip")
print( "- [OK]" )
print()

print( "[DONE]" )