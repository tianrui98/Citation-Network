"""
This module is intended to integrate the MCL clustering process with the main program.
This module is not implemented because the MCL clustering library
gives different clusters from those generated in Cytoscape with the same inflation values.
"""
#pip install markov-clustering

import markov_clustering as mc
import networkx as nx
import numpy as np
import pandas as pd

input_file = input("enter edge list excel file.")
df = pd.read_excel(input_file,index_col= 0)

#create network
G = nx.from_pandas_edgelist(df,
                            source='Source',
                            target='Target',
                            edge_attr= "Weight",
                            create_using=nx.DiGraph(),
                            edge_key=None)
#convert to matrix
matrix = nx.to_scipy_sparse_matrix(G,
                                    nodelist=G.nodes(),
                                    dtype=None,
                                    weight='Weight',
                                    format='csr')

#choose inlfation value: higher modularity the better
for inflation in [i / 10 for i in range(15, 51)]:
    result = mc.run_mcl(matrix, inflation=inflation)
    clusters = mc.get_clusters(result)
    Q = mc.modularity(matrix=result, clusters=clusters)
    print("inflation:", inflation, "modularity:", Q, "No. of clusters:", len(clusters))

parameter = input("Enter an inflation value.")

#create MCL clusters
result = mc.run_mcl(matrix, inflation=parameter)
clusters = mc.get_clusters(result)

#restore the company names
clusters_labeled = {}
companies = list(G.nodes())

for i in range(len(clusters)):
    clusters_labeled[i] = []
    nodes = list(clusters[i])
    for n in nodes:
        clusters_labeled[i].append(companies[n])

print(clusters_labeled)

