from molio.utils.print_tools import print_center
from molio.structure.structure import Structure
from molio.structure.atom import Atom
from molio.filetypes.filetypes import StructrueFile

import datetime
import os

class PDB(StructrueFile):
    """
    PDB structure parser
    """
    def from_file(self, file: str) -> None:
        """
        Reads in a PDB file

        Args:
            file (str): Path to PDB file
        """
        assert os.path.isfile(file), f"File {file} does not exist"

        with open(file, "r") as f:
            lines = f.readlines()
        nat = None
        for line in reversed(lines):
            if line.startswith("ATOM") or line.startswith("HETATM"):
                nat = int(line[6:11])

                break

        assert nat is not None

        tmp = [Atom]*(nat-1)
        index = 0

        print_center(f"Starting to parse the PDB file {file}", emph = True)
        print_center(f"Number of atoms: {nat}")

        res_chain: dict = dict()
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                if line.startswith("HETATM"):
                    prefix = "HETATM"
                else:
                    prefix = "ATOM"
                
                elem = line[76:78].strip()
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                resn = line[17:20].strip()
                resi = int(line[22:26].strip())
                chain = line[21]
                if chain not in res_chain:
                    res_chain[chain] = dict()
                if resi not in res_chain[chain]:
                    res_chain[chain][resi] = resn
                if chain == " ":
                    chain = None
                at = Atom()
                at.set_atom(elem, x, y, z)
                at.add_index(int(line[6:11]))
                at.change_prefix(prefix)
                at.add_atom_type(line[12:16].strip())
                at.add_residue_information(resname=resn, resid=resi, chain=chain)

                tmp[index]  = at
                index += 1
        total = 0
        for chain in res_chain.keys():
            total += len(res_chain[chain].keys())
        print_center(f"Total number of residues: {total}")
        print_center(f"Chains in file: {list(res_chain.keys())}")

        print_center("PDB file parsed", emph=True)

        self.structure = Structure()
        self.structure.add_atoms(tmp)


    def _format_atom(self, atom: Atom) -> str:
        """
        Formats an atom into PDB format.

        Args:
            atom (Atom): Atom object to format.
        """
        if atom.atom_type is None:
            atom.atom_type = atom.element
        if atom.chain is None:
            atom.chain = " "
        string = ("{0:6}{1:5} {2:4}{3:1}{4:3} {5:1}{6:4}{7:1}   "
                  "{8:8}{9:8}{10:8}{11:6}{12:6}      {13:4}{14:2}{15:2}").format(atom.pdb_prefix,
                                                    atom.index,
                                                    atom.atom_type.ljust(4),
                                                    " ", #Alternate location indicator
                                                    atom.resname.rjust(3),
                                                    atom.chain,
                                                    str(atom.resid).rjust(4),
                                                    " ", #Code for insertions of residues
                                                    str(round(atom.x,3)).rjust(8),
                                                    str(round(atom.y,3)).rjust(8),
                                                    str(round(atom.z,3)).rjust(8),
                                                    str(atom.occ).rjust(6),
                                                    str(atom.beta).rjust(6),
                                                    " ".ljust(4),
                                                    atom.element.rjust(2),
                                                    str(round(atom.charge)).rjust(2)
                                                    )
        return string


    def to_file(self, file: str) -> None:
        """
        Writes the structure to a file

        Args:
            file (str): Path to file
        """
        with open(file, "w") as f:
            print("TITLE   {0:2} {1:79}".format(" ", # Continuation
                f"PDB file created by Ross Amory on {datetime.datetime.now().strftime('%x at %X')}",),
                file=f)
            print("REMARK {0:3} {1:68}".format("1".ljust(3),
                f"PDB file generated according to PDB v3.3"), file=f)
            print("REMARK {0:3} {1:68}".format("2".ljust(3),
                f"PDB file generated using a script made by Dr. Ross Amory"),
                file=f)
            print("REMARK {0:3} {1:68}".format("3".ljust(3),
                f"This script is in its BETA stage and so should be used with caution."),
                file=f)
            for at in self.structure.atoms:
                print(self._format_atom(at), file=f)
