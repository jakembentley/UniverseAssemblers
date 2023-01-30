import random
import string
import PySimpleGUI as sg
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from uuid import uuid4
from matplotlib import patches
import networkx as nx

class Location(dict):

    def setName(self):
        """
        set locations name
        """
        name_len = random.randint(5, 15)
        self["name"] = ''.join(random.choice(string.ascii_letters) for i in range(name_len))
        return

    def setChildren(self, num_children):
        """
        create a kvp of locations children and unique ids
        """
        self["children"] = []
        
        for i in range(num_children):
            self["children"].append(str(uuid4()))
        return

    def setImage(self):
        """
        draw an image of the location, including the locations children but not its grandchildren
        """

        #draw a larger image of the image itself
        c = plt.Circle((15,15), radius = 3, fill = False)
        fig, ax = plt.subplots(figsize = (10,6),  dpi = 100, frameon = False)
        #set aspects of the axis
        ax.add_patch(c)
        ax.grid(False)
        ax.set_facecolor('#FAF9F6')
        ax.set_title(self['name'])
        ax.set_xticklabels([])
        ax.set_xlim([0,30])
        ax.set_ylim([0,30])
        ax.axis('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_yticklabels([])
        #draw children
        #for child n children draw diagonally up or down from self
        ax.add_patch(c)
        self["image"] = (fig, ax)

    def getSelfie(self, figpath):
        self["image"][0].savefig(figpath)
        return

    def __init__(self, num_children, loc_type, loc_subtype, parent_ref, ref):
        self.setName()
        self.setImage()
        self.setChildren(num_children)
        self["type"] = loc_type
        self["subtype"] = loc_subtype
        self["parent"] = parent_ref
        self["ref"] = 


class gameGraph:
    def gnp_random_connected_graph(self, n, p):
        """
        Generates a random undirected graph, similarly to an Erdős-Rényi 
        graph, but enforcing that the resulting graph is conneted
        """
        edges = combinations(range(n), 2)
        G = nx.Graph()
        G.add_nodes_from(range(n))
        if p <= 0:
            return G
        if p >= 1:
            return nx.complete_graph(n, create_using=G)
        for _, node_edges in groupby(edges, key=lambda x: x[0]):
            node_edges = list(node_edges)
            random_edge = random.choice(node_edges)
            G.add_edge(*random_edge)
            for e in node_edges:
                if random.random() < p:
                    G.add_edge(*e)
        return G

    def __init__(self, n, p):
        self.graph = self.gnp_random_connected_graph(n,p)

       
        
