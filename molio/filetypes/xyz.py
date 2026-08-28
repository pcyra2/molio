from molio.utils.variables import TERM_SIZE
from molio.structure.atom import Atom
from molio.structure.structure import Structure
from molio.utils.print_tools import print_center
from molio.filetypes.filetypes import StructrueFile

from tqdm import tqdm
import os

class XYZ(StructrueFile):
    """
    A class for parsing .xyz files. This can be either single structures or trajectories. 
    """

    trajectory: list[Structure]
    traj_length: int = 0


    def from_file(self, file: str) -> None:
        """
        Reads a .xyz file.

        Args:
            file (str): Path to the .xyz file.
        """
        assert os.path.isfile(file), f"File {file} does not exist"

        with open(file, "r") as f:
            lines = f.readlines()
     
        print_center(text="Starting the parse of the XYZ file", emph = True)

        nat = int(lines[0])

        print_center(text=f"Number of atoms: {nat}".center(TERM_SIZE))

        atoms: list[Atom] = [Atom()]*nat

        for i, line in enumerate(lines[2:nat+2]):
            words = line.split()
            atoms[i].set_atom(str(words[0]), float(words[1]), float(words[2]), float(words[3]))
            atoms[i].add_index(i) # Allows for bonds and angles to work.

        self.structure.add_atoms(atoms)
        
        print_center(text="XYZ file parsed".center(TERM_SIZE), emph=True)
        

    def to_file(self, file: str) -> None:
        """
        Writes the structure to a .xyz file.

        Args:
            file (str): Path to the .xyz file.
        """
        with open(file, "w") as f:
            print(str(self.structure.nat), file=f)
            print("\n", file=f)
            for at in self.structure.atoms:
                print(self._format_atom(at), file=f)

    def _format_atom(self, atom: Atom) -> str:
        string = f"{atom.element}\t{atom.x}\t{atom.y}\t{atom.z}"
        return string


    def from_trajectory(self, file: str) -> None:
        """Allows for the parsing of a trajectory file in .xyz format.
        
        Args:
            file (str): Path to the trajectory file.
        """
        print_center(text=f"Starting to parse the XYZ trajectory file {file}", emph=True)

        assert os.path.isfile(file), f"File {file} does not exist"

        with open(file, "r") as f:
            lines = f.readlines()
        nat = int(lines[0])
        n_structures = 0
        index = -1000
        trajectories = []

        struct = None


        print_center(f"Number of atoms: {nat}")

        mol = [Atom] * nat

        for line in tqdm(lines, "Reading file: "):
            
            if line.strip() == str(nat) and index < 0: # The gap between .xyz structures. 
                # Allows for structure delimiters rather than .xyz structures in rapid succession.
                index = -2 # Assuming nat definition is 2 lines before the start of the structure. 
            if index >= 0: # Where the atoms start
                words = line.split()
                at = Atom()
                at.set_atom(str(words[0]), float(words[1]), float(words[2]), float(words[3]))
                at.add_index(index)
                mol[index] = at
            if index == nat-1:
                struct = Structure()
                struct.add_atoms(mol)
                trajectories.append(struct) # Update the trajectory
                n_structures += 1
                index = -1000 # Reset the index counter
                # print(n_structures)
                # print(mol[0].echo())
                # print(mol[-1].echo())
                mol = [Atom] * nat

            index += 1 # Add to the index. 

        assert struct is not None # Ensures that at least one structure is found.

        self.structure = struct
        self.trajectory = trajectories
        self.traj_length = n_structures
        print_center(text = f"Number of structures in the trajectory: {n_structures}")

        print_center(text = "XYZ trajectory file parsed", emph = True)

