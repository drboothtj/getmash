'''
network module for getmash
    functions:
        XXX
'''
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

from getmash.utils import io

def draw_networkx(graph: nx.Graph, outdir:str) -> None:
    '''
    write the networkx graph as an .svg
        arguments:
            graph: networkx graph object
            outdir: the dir to write to
        returns:
            None
    '''
    plt.figure(figsize=(8, 6), facecolor='#eede7b')
    pos = nx.spring_layout(graph)  # or kamada_kawai_layout, shell_layout, etc.
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="#e64110")
    nx.draw_networkx_edges(graph, pos, width=1.5, edge_color='#207394')
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="white")

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(outdir +"network.svg", format="svg")
    plt.close()

def draw_pyvis_network(mash, outdir, threshold):
    '''
    draw a pyvis network and create the networkx graph simultaneously
        arguments:
            mash: the mash dictionary
            ourdir: the output directory
            threshold: 
                the mash score threshold, over which to draw an edge
    '''
    net = Network(height='800px', width='100%', bgcolor='#eede7b', font_color='white')
    graph = nx.Graph()

    nodes = set(mash['Source']).union(set(mash['Hit']))
    #add nodes
    for label in nodes:
        net.add_node(label, color='#e64110')
        graph.add_node(label)
    #add edges
    for i, source in enumerate(mash['Source']):
        target = mash['Hit'][i]
        value = mash['Value'][i]
        if value > threshold:
            net.add_edge(
                source,
                target,
                width = value * 7,
                title = str(value),
                color='#207394'
            )
        graph.add_edge(source, target, weight=value)
    net.write_html(outdir + "network.html")

    subnetworks = list(nx.connected_components(graph))
    for i, nodes in enumerate(subnetworks):
        nodes_list = sorted(nodes)
        io.write_list_to_file(nodes_list, f"{outdir}/subnetwork_{i}.txt")

    draw_networkx(graph, outdir)

def draw_network(args):
    '''
    draw a network from a mash table
        arguments:
            args: args from the argparser
        returns:
            None
    '''
    infile = args.mash_table
    outdir = args.output_directory
    threshold = args.threshold
    mash = io.get_mash_dict(infile)
    draw_pyvis_network(mash, outdir, threshold)
