from molio.filetypes.pdb import PDB
from molio.structure.structure import Structure
from molio.structure.atom import Atom


WATER = Structure()
WATER.add_atoms([Atom().set_atom("O", 0, 0, 0),
                 Atom().set_atom("H", 0, 1, 0),
                 Atom().set_atom("H", 1, 0, 0)])

EXAMPLE_PDB = ""

def test_pdb_read():
    pdb = PDB()
    pdb.from_file(EXAMPLE_PDB)
    pass

def test_pdb_write():
    pass

