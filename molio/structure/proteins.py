
class AminoAcid:
    resname: str
    parent: str
    polar: bool
    charge: int # charge at pH 7.0
    backbone_atoms: list[str] = ["CA", "C", "N", "O"]


    def __init__(self, resname: str,
                 parent: str,
                 polar: bool,
                 charge: int,):
        self.resname = resname
        self.parent = parent
        self.polar = polar
        self.charge = charge




AMINO_ACIDS = dict[str, AminoAcid](
    ARG = AminoAcid(resname="ARG",
                    parent="arginine",
                    polar=True,
                    charge=1),

    HIS = AminoAcid(resname="HIS",
                    parent="histidine",
                    polar=False,
                    charge=0),
    HID = AminoAcid(resname="HID",
                    parent="histidine",
                    polar=False,
                    charge=0),
    HIE = AminoAcid(resname="HIE",
                    parent="histidine",
                    polar=False,
                    charge=0
                    ),
    HIP = AminoAcid(resname="HIP",
                    parent="histidine",
                    polar=False,
                    charge=1),

    LYS = AminoAcid(resname="LYS",
                    parent="lysine",
                    polar=False,
                    charge=1),
    LYN = AminoAcid(resname="LYN",
                    parent="lysine",
                    polar=False,
                    charge=0),

    ASP = AminoAcid(resname="ASP",
                    parent = "aspartic_acid",
                    polar=True,
                    charge=-1),
    ASH = AminoAcid(resname="ASH",
                    parent="aspartic_acid",
                    polar=False,
                    charge=0),

    GLU = AminoAcid(resname="GLU",
                    parent="glutamic_acid",
                    polar=True,
                    charge=-1),
    GLH = AminoAcid(resname="GLH",
                    parent="glutamic_acid",
                    polar=False,
                    charge=0),

    SER = AminoAcid(resname="SER",
                    parent="serine",
                    polar=True,
                    charge=0),

    THR = AminoAcid(resname="THR",
                    parent="threonine",
                    polar=True,
                    charge=0),

    ASN = AminoAcid(resname="ASN",
                    parent="asparagine",
                    polar=True,
                    charge=0),

    GLN = AminoAcid(resname="GLN",
                    parent="glutamine",
                    polar=True,
                    charge=0),

    CYS = AminoAcid(resname="CYS",
                    parent="cysteine",
                    polar=False,
                    charge=0),
    CYM = AminoAcid(resname="CYM",
                    parent="cysteine",
                    polar=False,
                    charge=-1),
    CYX = AminoAcid(resname="CYX",
                    parent="cysteine",
                    polar=False,
                    charge=0),

    GLY = AminoAcid(resname="GLY",
                    parent="glycine",
                    polar=False,
                    charge=0),

    PRO = AminoAcid(resname="PRO",
                    parent="proline",
                    polar=False,
                    charge=0),

    ALA = AminoAcid(resname="ALA",
                    parent="alanine",
                    polar=False,
                    charge=0),

    VAL = AminoAcid(resname="VAL",
                    parent="valine",
                    polar=False,
                    charge=0),

    ILE = AminoAcid(resname="ILE",
                    parent="isoleucine",
                    polar=False,
                    charge=0),

    LEU = AminoAcid(resname="LEU",
                    parent="leucine",
                    polar=False,
                    charge=0),

    MET = AminoAcid(resname="MET",
                    parent="methionine",
                    polar=False,
                    charge=0),

    PHE = AminoAcid(resname="PHE",
                    parent="phenyl_alanine",
                    polar=False,
                    charge=0),

    TYR = AminoAcid(resname="TYR",
                    parent="tyrosine",
                    polar=False,
                    charge=0),

    TRP = AminoAcid(resname="TRP",
                    parent="tryptophan",
                    polar=False,
                    charge=0),

    ACE = AminoAcid(resname="ACE",
                    parent="acetyl",
                    polar=False,
                    charge=0),

    NME = AminoAcid(resname="NME",
                    parent="n_methyl",
                    polar=False,
                    charge=0),

    HYP = AminoAcid(resname="HYP",
                    parent="hydroxyproline",
                    polar=False,
                    charge=0),
    )