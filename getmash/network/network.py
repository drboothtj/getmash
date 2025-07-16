'''
network module for getmash
    functions:
        XXX
'''
import os
from typing import Dict

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

from getmash.utils import io

def draw_network_graphic(graph: nx.Graph, outdir: str, svg: bool, png: bool) -> None:
    '''
    draw the network x graph to a png or svg
        arguments:
            graph: graph from networkx
            outdir: directory to write to
            svg: bool TRUE to write a .svg
            png: bool TRUE to write a .png
    '''
    plt.figure(figsize=(8, 6), facecolor='#eede7b')
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="#e64110")
    nx.draw_networkx_edges(graph, pos, width=1.5, edge_color='#207394')
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="white")

    plt.axis("off")
    plt.tight_layout()

    if svg:
        plt.savefig(os.path.join(outdir, "network.svg"), format="svg")
    if png:
        plt.savefig(os.path.join(outdir, "network.png"), format="png") # add arg
    plt.close()

def draw_networkx(
        mash: Dict, outdir:str, threshold: float, nodes: set,
        svg: bool, png: bool) -> None:
    '''
    write the networkx graph as an .svg
        arguments:
            mash: mash dictionary
            outdir: directory to write to
            threshold: mash distance below which to draw edges
            nodes: a set of unique values in the mash dict to use as nodes
            svg: bool TRUE to write a .svg
            png: bool TRUE to write a .png
        returns:
            None
    '''
    graph = nx.Graph()
    for label in nodes:
        graph.add_node(label)

    for i, source in enumerate(mash['Source']):
        target = mash['Hit'][i]
        value = mash['Value'][i]
        if source == target: #remove self hits
            continue
        if value < threshold: #value is distance!
            graph.add_edge(source, target, weight=value)

    subnetworks = list(nx.connected_components(graph))
    for i, sub_nodes in enumerate(subnetworks):
        nodes_list = sorted(sub_nodes)
        io.write_list_to_file(nodes_list, f"{outdir}/subnetwork_{i}.txt")

    nx.write_graphml(graph, os.path.join(outdir, "network.graphml")) # maybe add arg

    if svg or png:
        draw_network_graphic(graph, outdir, svg, png)


def draw_pyvis_network(
        mash: Dict, outdir: str, threshold: float, nodes: set
        ):
    '''
    draw a pyvis network and create the networkx graph simultaneously
        arguments:
            mash: mash dictionary
            outdir: directory to write to
            threshold: mash distance below which to draw edges
            nodes: a set of unique values in the mash dict to use as nodes
    '''
    net = Network(height='800px', width='100%', bgcolor='#eede7b', font_color='white')
    #add nodes
    for label in nodes:
        net.add_node(label, color='#e64110')
    #add edges
    for i, source in enumerate(mash['Source']):
        target = mash['Hit'][i]
        value = mash['Value'][i]
        if source == target: #remove self hits
            continue
        if value < threshold: #value is distance... (rename)
            net.add_edge(
                source,
                target,
                width = value * 7,
                title = str(value),
                color='#207394'
            )
    net.write_html(outdir + "network.html")

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
    nodes = set(mash['Source']).union(set(mash['Hit']))
    if args.html:
        draw_pyvis_network(mash, outdir, threshold, nodes)
    draw_networkx(mash, outdir, threshold, nodes, args.svg, args.png)
