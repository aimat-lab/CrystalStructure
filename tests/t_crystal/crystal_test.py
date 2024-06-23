import math

from holytools.devtools import Unittest
from pymatgen.core import Structure

from CrystalStructure.atomic_constants.atomic_constants import Void
from CrystalStructure.crystal import CrystalStructure, AtomicSite
from CrystalStructure.examples import CrystalExamples

# ---------------------------------------------------------

class CrystalTest(Unittest):
    def setUp(self):
        self.cifs : list[str] =  [CrystalExamples.get_cif_content(), CrystalExamples.get_cif_content(secondary=True)]

        self.pymatgen_structures : list[Structure] = [Structure.from_str(cif, fmt='cif') for cif in self.cifs]
        self.crystals : list[CrystalStructure] = [CrystalStructure.from_cif(cif_content=cif) for cif in self.cifs]
        self.spgs : list[int] = [self.extract_spg(cif) for cif in self.cifs]

    @staticmethod
    def extract_spg(cif : str) -> int:
        lines = cif.split('\n')
        spg = None
        for line in lines:
            if '_space_group_IT_number' in line:
                _, spg = line.split()
                spg = int(spg)
        return spg


if __name__ == "__main__":
    CrystalTest.execute_all()
