import random
import string
import PySimpleGUI as sg
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from uuid import uuid4

class Location:
    def __init__(self, cel_type, cel_subtype, parent, num_child, self.ref):
        
        #set the type of the celestial
        #categories of cel are mapped to int:
        # {1: solar system, 2: planet, 3: moon, 4:Asteroid Belt, 5:Satilite}
        #only large enough satilites will qualify as celestials
        self.cel_type = cel_type
        
        #celestial subtypes are dependent on celestial type, 
        #suns can be 1: Giant, 2: Standard, 3:Dwarf, 4:Neutron, 5:Black Hole
        #planets can be 1:Terra 2:Gas 3:Dwarf 4:Exo 
        self.cel_subtype = cel_subtype
        
        #reference id for celestial's parent
        self.parent = parent_ref
        
        #reference id for self
        self.ref = ref
        
        self.children = []
        #initalize child list
        for i in range(num_child):
            self.children.append(str(uuid4())) 
            
        #since a celestial is a location it will have a name and an image
        self.name = ''.join(random.choice(string.ascii_letters) for i in range(name_len))
        
        #define an image of the celestial
        self.image = ''

    def setName(self):
        name_len = random.randint(5, 15)
        return ''.join(random.choice(string.ascii_letters) for i in range(name_len))

    def setImage(self):
        pass
    

    




