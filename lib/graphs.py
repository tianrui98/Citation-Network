"""
Generate and save heat maps and network diagrams.
"""
from lib.default import *

def GenerateHeatMap(CF_df, save_path, input_analysis):
    name = InputToName(input_analysis)
    path = str(save_path) + '/' + 'heatmap_'+name + '_' + date +'.png'
    plt.figure(figsize=(30, 30))
    heatmap = sns.heatmap(CF_df, annot=False,cmap='BrBG')
    title = 'Citeflow Heatmap #' + input_analysis
    heatmap.set_title(title,fontdict={'fontsize':25})
    if "cited" in name:
        plt.xlabel('Cited')
        plt.ylabel('Citing')
    else:
        plt.xlabel('Citing')
        plt.ylabel('Cited')
    plt.savefig(path)
    return heatmap


#%% Network Diagram

def GenerateNetwork (CF_df, save_path, input_analysis):
    name = InputToName(input_analysis) 
    path = str(save_path) + '/' + 'network_'+name + '_' + date +'.png'
    matrix_np = CF_df.to_numpy()
    G = nx.from_numpy_matrix(matrix_np)
    labels = CF_df.columns
    lab_node = dict(zip(G.nodes, labels))

    random_pos = nx.random_layout(G, seed=42)
    pos = nx.spring_layout(G, pos=random_pos)

    plt.figure(figsize=(30, 30))

    options = {"node_size": 1000, "alpha": 0.8}
    nx.draw_networkx_nodes(G, pos, node_color="c", **options)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.4)
    nx.draw_networkx_labels(G, pos, labels=lab_node, font_size=50, font_family='sans-serif')
    plt.savefig(path)
    return None