import random
import string
import PySimpleGUI as sg
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from uuid import uuid4
from matplotlib import patches
import networkx as nx
import scipy
from itertools import combinations,groupby

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
        
        #ensure nested locations are accounted for
        #if sun determine determine how many are planets (and their moons) and asteroid belts
        if self['type'] == 1:
            child_types = random.choices([2,4], weights=[5,1], k=num_children)
            for i in range(num_children):
                if child_types[i] == 2:
                    child = Location(random.randint(0,4), child_types[i], random.randint(1,3), self)
                    self["children"].append(child)
                elif child_types[i] == 4:
                        child = Location(0, child_types[i], None, self)
                        self["children"].append(child)
        
        #if a planet make moons
        elif self['type'] == 2:
            child_types = [3 for i in range(num_children)]
            for i in range(num_children):
                child = Location(0, child_types[i], None, self)
                self["children"].append(child)


        return

    def setImage(self):
        """
        draw an image of the location, including the locations children but not its grandchildren
        """

        #draw a larger image of the image itself
        c = plt.Circle((15,15), radius = 3, fill = False)
        self.figure = mpl.figure.Figure(figsize=(10,6), dpi=100)
        self.ax = self.figure.add_subplot()
        #set aspects of the axis
        self.ax.add_patch(c)
        self.ax.grid(False)
        self.ax.set_facecolor('#FAF9F6')
        self.ax.set_title(self['name'])
        self.ax.set_xticklabels([])
        self.ax.set_xlim([0,30])
        self.ax.set_ylim([0,30])
        self.ax.axis('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_yticklabels([])
        #draw children
        #for child n children draw diagonally up or down from self
        self["image"] = self.figure


    def __init__(self, num_children, loc_type, loc_subtype, parent):
        """
        location types: 
        1: Sun
        2: Planet
        3: Moon
        4: Asteroid Belt

        location subtypes:
        Suns:
        1: Giant
        2: Main Sequence
        3: Dwarf
        4: Neutron
        5: Black Hole

        Planets:
        1: Terrestial
        2: Gas Giant
        3: Dwarf
        
        No types for Moons or Asteroid Belts
        """

        #constructor needs to also construct children also exist?
        #base case: location is either 3 or 4
        #otherwise also need to construct children

        self.setName()
        self.setImage()
        self["type"] = loc_type
        self["subtype"] = loc_subtype
        self["parent"] = parent

        if num_children == 0:
            return

        self.setChildren(num_children)

        return

class gameGraph:
    """
    class to manage the logic of the game's nested location graph
    at the top level solar systems -> planets and asteroid belts -> moons
    """
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

    def setGraphImage(self):
        print("initalizing map image...")
        fig = mpl.figure.Figure()
        ax = fig.add_subplot()
        nx.draw(self.graph, node_color = 'lightblue', with_labels = False, node_size = 20, ax=ax)
        self.image = fig
        return

    def setNodeIds(self):
        #
        for node in self.graph.nodes:
            node_id = id(node)
            if 'id' not in self.graph.nodes[node]:
                self.graph.nodes[node]['id'] = node_id
        return

    def setNodeLocations(self):
        """
        sets node locations
        note: node IDS must be initialized
        """

        print("defining map locations...")
        for node in self.graph.nodes:
            if 'location' not in self.graph.nodes[node]:
                self.graph.nodes[node]['location'] = Location(random.randint(1,12), 1, random.choices([1,2,3,4,5], weights =[10,10,10,1,1]), None)


    def __init__(self, n, p):
        self.graph = self.gnp_random_connected_graph(n,p)
        self.setGraphImage()
        self.setNodeIds()
        self.setNodeIds()
        self.setNodeLocations()



class Resource:
    '''
    a resource object refers to an in game resource that exists as a member of any location
    resources need to be modifiable, and referrable both the locations they are in and for the player when they are extracted
    
    '''
    pass

class Interface:
    '''
    a class to encaspulate all game GUI methods and members
    '''
    __init__(self):
        pass

    def start(self):
        '''
        define a start function that
        either opens a save file or starts a new game
        '''

        #init a start window that either starts a new game or loads an existing game
        sg.theme('Topanga')
        layout =[
            [sg.Text("Welcome to Universal Assemblers")],
            [sg.Text("Select a save file"), sg.Input(), sg.FileBrowse(), sg.Button("Ok")],
            [sg.Button("New Game")]
        ]

        window = sg.Window('Welcome to Universal Assemblers', layout)
        #open the window and loop to handle events
        while True:
            #close window if closed event
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            #if user selects new game make a game graph
            if event == "New Game":
                self.G = ua.gameGraph(100, 0.01)
                window.close()
            #if user selects ok event try to open save file
            if event == "Ok":
                selected_file = values[0]
                if selected_file is None:
                    sg.Popup('Oops! No save file was selected, please select a \'*.pickle\' file')
                else:
                    try: 
                        with open('{selec}'.format(selec=selected_file), 'rb') as f:
                            #load game map --> this may be updated to be a broader game object
                            self.G =pkl.load(f)
                        sg.Popup('Game Loaded!')
                        window.close()
                    except:
                        sg.Popup('Oops! Please select a \'*.pickle\' file')

        window.close()
        return self.G

    def setMainWindow(self, G, node):
        '''
        takes a game graph object and a current node and sets the main window
        to that node for display,
        sets the buttons and text elements as well (defined separately)
        '''
        pass

