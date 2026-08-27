from molio.structure.atom import Atom
from molio.structure.structure import Structure


class StructrueFile:
    """
    Parent class of a structure file
    """
    structure: Structure

    def __init__(self) -> None:
        pass

    def update_coordinates(self, coordinates: list[Atom]|Structure) -> None:
        """
        Update the coordinates of the PDB file
        """
        atms = None
        if isinstance(coordinates, Structure):
            atms = coordinates.atoms
        elif isinstance(coordinates, list):
            atms = coordinates

        assert atms is not None

        self.structure.update_coordinates(atms)

    def from_structure(self, structure: Structure|list[Atom]) -> None:
        """Allows the generation of a file from a list of atoms/Structure object

        Args:
            structure (Structure): List of atoms to form the .xyz file
        """
        if isinstance(structure, Structure):
            self.structure = structure
        elif isinstance(structure, list):
            self.structure = Structure()
            self.structure.add_atoms(structure)

    def from_file(self, file: str) -> None:
        """
        Reads in a file and converts it into a structure object
        """
        raise NotImplementedError()

    def to_file(self, file: str) -> None:
        """
        Writes the structure to a file
        """
        raise NotImplementedError()