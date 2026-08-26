from pickletools import read_unicodestringnl


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

    def coords(self):
        return (self.x, self.y, self.z)

    def set_atom(self, element: str, x: float, y: float, z: float) -> None:
        """Initialises the atom object
        
        Args:
            element (str): element key
            x (float): X coordinate of the atom in Angstrom
            y (float): Y coordinate of the atom in Angstrom
            z (float): Z coordinate of the atom in Angstrom
        """
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

