from molio.filetypes.filetypes import StructrueFile


class Mol2(StructrueFile):
    def from_file(self, file: str) -> None:
        with open(file, "r") as f:
            lines = f.readlines()

        #TODO