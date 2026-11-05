# Standard atomic weights (g/mol), keyed by element symbol.
# Radioactive elements without a standard weight use the mass number of their most stable isotope.
ATOMIC_MASSES: dict[str, float] = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98.0, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91,
    "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145.0, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93,
    "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21,
    "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209.0, "At": 210.0,
    "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0, "Th": 232.04,
    "Pa": 231.04, "U": 238.03, "Np": 237.0, "Pu": 244.0, "Am": 243.0,
    "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0,
    "Md": 258.0, "No": 259.0, "Lr": 266.0, "Rf": 267.0, "Db": 268.0,
    "Sg": 269.0, "Bh": 270.0, "Hs": 269.0, "Mt": 278.0, "Ds": 281.0,
    "Rg": 282.0, "Cn": 285.0, "Nh": 286.0, "Fl": 289.0, "Mc": 290.0,
    "Lv": 293.0, "Ts": 294.0, "Og": 294.0,
}





class Atom:
    """Class containing atom information
    
    Attributes:
        element (str): Element symbol from the periodic table
        x (float): X-coordinate of the atom in Angstrom
        y (float): Y-coordinate of the atom in Angstrom
        Z (float): Z-coordinate of the atom in Angstrom
        chain (str|None): The chain identifier for the atom. Defaults to None
        atom_type (str|None): Atom type for the respective forcefield. Defaults to None
        resname (str|None): Residue Name. Defaults to None
        resid (int|None): Residue index. Defaults to None
        occ (float|None): Occupancy column value in the PDB file. Defaults to None
        beta (float|None): Beta column value in the PDB file. Defaults to None
        pdb_prefix (str): The start str for a PDB file. Defaults to `ATOM`
    """
    element: str
    x: float
    y: float
    z: float
    charge: float = 0.0
    chain: str|None = None
    atom_type: str|None = None
    resname: str|None = None
    resid: int|None = None
    occ: float = 1.00
    beta: float = 0.00
    pdb_prefix: str = "ATOM"
    index: int|None = None

    def __init__(self):
        pass

    def coords(self) -> (float, float, float):
        """
        Creates the atomic coordinates as a tuple
        Returns:
            coordinates (float,float,float): The x,y,z coordinates of the atom.
        """
        return (self.x, self.y, self.z)

    def set_atom(self, element: str, x: float, y: float, z: float) -> None:
        """Initialises the atom object
        
        Args:
            element (str): element key
            x (float): X coordinate of the atom in Angstrom
            y (float): Y coordinate of the atom in Angstrom
            z (float): Z coordinate of the atom in Angstrom
        """
        if element not in ATOMIC_MASSES:
            print(f"Warning: {element} is not a valid element. Do not try to calculate the center of mass.")


        self.element = element
        self.x = x
        self.y = y
        self.z = z


    def echo(self) -> str:
        """Prints the coordinates of the atom in .xyz format."""
        return f"{self.element} {self.x} {self.y} {self.z}"


    def translate_x(self, distance: float) -> None:
        """Translates the atom in the x-direction by the given distance
        
        Args:
            distance (float): Distance to move in Angstrom
        """
        self.x += distance


    def translate_y(self, distance: float) -> None:
        """Translates the atom in the y-direction by the given distance
        
        Args:
            distance (float): Distance to move in Angstrom
        """
        self.y += distance


    def translate_z(self, distance: float) -> None:
        """Translates the atom in the z-direction by the given distance
        
        Args:
            distance (float): Distance to move in Angstrom
        """
        self.z += distance


    def add_atom_type(self, atom_type: str) -> None:
        """Allows for allocating atom types to an atom for use in a forcefield.
        
        Args:
            atom_type (str): Atom type to be allocated to this atom
        """
        self.atom_type = atom_type
    
    
    def add_residue_information(self, resname: str, resid: int, chain: str|None = None) -> None:
        """Adds residue informaiton to allow for PDB compatibility

        ArgS:
            resname (str): Name of residue
            resid (int): Index of residue
            chain (str): Chain that the residue is in
        """
        self.resname = resname
        self.resid = resid
        self.chain = chain
    

    def add_occ_beta(self, occupancy: float = 1.00, beta: float = 0.00) -> None:
        """Adds the occupancy and beta information into the atom. Useful when creating PDB files. 
        """
        self.occ = occupancy
        self.beta = beta


    def change_prefix(self, prefix: str) -> None:
        """Allows for the adjustment of prefix in a pdb file. 

        Args:
            prefix (str): The prefix in a pdb file.
                Default is ATOM. But can also be HETATM.
        """
        self.pdb_prefix = prefix


    def add_index(self, index: int) -> None:
        """Adds an index to the atom

        Args:
            index (int): The index of the atom
        """
        self.index = index


    def add_charge(self, charge: float, pdb_col: str = "end") -> None:
        """Allows for the addition of a partial charge to the atom

        Args:
            charge (float): The charge of the atom
            pdb_col (str): Where to add it in the pdb file. Options are either `end`, `occ` or `beta`.
                Defaults to `end`.
        """
        self.charge = charge
        if pdb_col == "occ":
            self.occ = charge
        if pdb_col == "beta":
            self.beta = charge


    def update_coordinates(self, x: float, y: float, z: float) -> None:
        """Allows for direct manipulation of coordinates"""
        self.x = x
        self.y = y
        self.z = z

    def _get_atomic_mass(self) -> float:
        """Looks up the standard atomic weight of an element.

        Masses are not stored on Atom objects; use this function where needed.

        Args:
            element (str): Element symbol, e.g. "C" or "Cl". Case-insensitive.

        Returns:
            mass (float): Atomic weight in g/mol.

        Raises:
            ValueError: If the element is not in the periodic table.
        """
        if self.element not in ATOMIC_MASSES:
            raise ValueError(f"Unknown element {self.element!r}. Cannot look up atomic mass.")
        return ATOMIC_MASSES[self.element]