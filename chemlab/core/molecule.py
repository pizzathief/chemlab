#! /usr/bin/env python -tt

import re
import numpy as np
import os
import sys


from numpy import linalg as LA
from .. import data
from ..data import symbols


class Molecule:

    '''Building the molecule with atoms and bonds'''
    
    def __init__(self,atoms,bonds):
    
        self.atoms=atoms
        
        if bonds:
            self.bonds=bonds
        else:
            self.guess_bonds()    
    
    
    def guess_bonds(self, threshold=0.1):
        d = os.path.dirname(sys.modules['chemlab.data'].__file__)
        
        radiifile = os.path.join(d, "covalent_radii.dat")
        radii = np.genfromtxt(radiifile,
                              delimiter=",",
                              dtype=[("type", "a3"),
                                     ("single", "f"),
                                     ("double", "f"),
                                     ("triple","f")])
        
        #initializing bonds
        self.bonds = []
        #copy to pop elements without damage
        atoms=self.atoms[:]
    
        #guessing bonds
        while atoms:
            atom1 = atoms.pop(0)
            for atom in atoms:
            
                cov_dist = (radii[atom1.atno-1][1] +
                            radii[atom.atno-1][1])

                cov_dist_inf = cov_dist - cov_dist * threshold
                cov_dist_sup = cov_dist + cov_dist * threshold
                
                if  (cov_dist_inf <
                     LA.norm(atom1.coords - atom.coords) <
                     cov_dist_sup):
                     self.bonds.append(Bond(atom1, atom))
    
    
    
class Atom:
    '''Takes a line of the formatted input file.
    
    Build an atom with: 
    - id -> number in the input file (if id is actually passed)
    - type -> type of atom we are dealing with for example C
    - coordinates -> a vector with the coordinates of the atom
    '''
    
    def __init__(self,id,type,coords):
        
        self.id = id
        self.type = type
        self.coords = np.array(coords)

        self.atno = symbols.symbol_list.index(type) + 1
        


class Bond:

    '''Generate bond and bond properties '''
    
    def __init__(self,atom1,atom2):
    
        self.start = atom1
        self.end = atom2
        
        self.atom_bonded = [atom1.type,atom2.type]
        self.id_bonded = [atom1.id,atom2.id]
        self.lenght = LA.norm(atom1.coords - atom2.coords)
        