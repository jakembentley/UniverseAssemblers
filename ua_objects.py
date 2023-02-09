from genericpath import exists
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

class GameGUI:
    '''
    the base inteface will need to handle the generation of pop up windows triggered by buttons, 
    a base window that features a plot display, buttons and a counter text that tracks stats
    buttons in the interface will be of two kinds
    buttons that create pop up windows (static)
    buttons whose values are conditional off game elements (dynamic)
    '''
    def __init__(self, graph):
        self.graph = graph
        self.theme = sg.Theme("Topanga")
        #col 1
        self.display_row = [sg.Image(key = 'MAP IMAGE', background_color = '#F9EFE8', size = (1000, 600))]
        self.obj_row = [sg.Text('This will be game object descriptors')]
        self.list_box = [sg.Listbox(values = [], enable_events = True, key = 'OBJECT LIST', size = (900, 400))] 
        self.local_col = [self.display_row, self.obj_row, [sg.Text("Location Descriptions:")], self.list_box]

        
        #these resource counters represent the innate resources of a location
        self.metals_counter = 0 
        self.energy_counter = 0
        self.silicates_counter = 0

        #these resource counters map to processed resource counters reflected by user allocations
        self.ecology_counter = 0
        self.military_counter = 0
        self.information_counter = 0

        #this construction counter reflects the number of constructions generated by a user from a combination of innate and processed resources
        self.construction_counter = 0

        self.counters_dict = {
            "metals": self.metals_counter,
            "energy": self.energy_counter,
            "silicates": self.silicates_counter,
            "ecology": self.ecology_counter,
            "military": self.military_counter,
            "information": self.information_counter
            }

        #col 2
        #col 2 buttons
        self.navButton = sg.Button("Travel")
        self.allocateButton = sg.Button("Allocate")
        self.constructButton = sg.Button("Constructions")
        self.saveButton = sg.Button("Save")
        #col 2 resource list
        self.resource_list = [key+":"+value for key,value in self.counters_dict.items()]
        
        #group resource list into listbox
        self.resourceListbox = sg.Listbox(self.resource_list, size=(600,1000), key='resourceListbox')
        #group buttons
        self.buttonRow = [self.navButton, self.allocateButton, self.constructButton, self.saveButton]
        #combine both elements into two rows
        self.action_col = [self.buttonRow,
                           self.resourceListbox]
        #overall game layogut
        self.mainLayout = [[sg.Frame('Universe Assembler Frame', [[sg.Text('Universe Assembler')]], size = (1920, 50))],
                           sg.Column(self.local_col, size = (1000,1030)), sg.VerticalSeparator(), sg.Column(self.action_col, size = (920, 1030))]
        

        self.mainWindow = sg.Window("Universe Assembler", layout = self.mainLayout, size=(1920,1080))


    def start(self):
        '''
        define a start function that
        either opens a save file or starts a new game
        '''

        #init a start window that either starts a new game or loads an existing game
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
                self.graph = ua.gameGraph(100, 0.01)
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
                            self.graph =pkl.load(f)
                        sg.Popup('Game Loaded!')
                        window.close()
                    except:
                        sg.Popup('Oops! Please select a \'*.pickle\' file')

        window.close()
        return self.graph

    def updateResourceCount(self, resource_key, incre_add):
        self.counters_dict[resource_key] += incre_add
        self.resource_list = [key+":"+value for key,value in self.counters_dict.items()]
        return

    def multiUpdateResourceCount(self, resource_keys, incre_adds):
        #update multiple resources with a resource key list and number to increment lsit, the resource key list and incre_adds list must be the same size and must be aligned
        for i in range(len(resource_keys)):
            key = resource_keys[i]
            incre_add = incre_adds[i]
            #increment
            self.counters_dict[key] += incre_add
        #update the resource list to reflect dict changge
        self.resource_list = [key+":"+value for key,value in self.counters_dict.items()]
        return

    def updateResourceCount(self, resource_list):
        self.resource_list = resource_list
        self.resourceListbox.Update(self.resource_list)
        return

    def setWindow(self, layout, name):
        '''
        add a button with a str for its name, which will be the event trigger.
        add that button to a window element (a list)
        '''
        window  = sg.Window(name, layout)
        return window

    def setElement(self, name, ele_type):
        '''
        set an element to be included in a window of any pysimplegui type
        '''

        return ele_type(name)
    


    