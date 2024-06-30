import os

from CrystalStructure.crystal import CrystalStructure, CrystalBase


# ---------------------------------------------------------

class CrystalExamples:
    @staticmethod
    def get_crystal(num: int, mute: bool = False):
        cif_content = CrystalExamples.get_cif_content(num=num)
        crystal_structure = CrystalStructure.from_cif(cif_content=cif_content)
        if not mute:
            print(f'--> Cif content:\n {cif_content}')
            print(f'--> Crystal structure:\n {crystal_structure}')
        return crystal_structure

    @staticmethod
    def get_base(num : int = 1, mute : bool = True) -> CrystalBase:
        crystal_stucture = CrystalExamples.get_crystal(num=num, mute=mute)
        return crystal_stucture.base

    @staticmethod
    def get_cif_content(num : int = 1) -> str:
        cif_fpath = os.path.join(os.path.dirname(__file__), 'cifs', f"test{num}.cif")
        with open(cif_fpath, 'r') as f:
            cif_content = f.read()
        return cif_content
