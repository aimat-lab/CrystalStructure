import math

from holytools.devtools import Unittest
from pymatgen.core import Structure

from CrystalStructure.crystal import CrystalStructure
from CrystalStructure.examples import CrystalExamples

# ---------------------------------------------------------

class TestPymatgenStructure(Unittest):
    def setUp(self):
        self.cifs : list[str] =  [CrystalExamples.get_cif_content(), CrystalExamples.get_cif_content(secondary=True)]

        self.pymatgen_structures : list[Structure] = [Structure.from_str(cif, fmt='cif') for cif in self.cifs]
        self.crystal_structures : list[CrystalStructure] = [CrystalStructure.from_cif(cif_content=cif) for cif in self.cifs]
        self.spgs : list[int] = [self.extract_spg(cif) for cif in self.cifs]


    def test_spacegroup_calculation(self):
        for spg, crystal in zip(self.spgs,self.crystal_structures):
            crystal.calculate_properties()
            computed_sg = crystal.space_group
            print(f'Computed, actual spg = {computed_sg}, {spg}')

            if computed_sg != spg:
                raise ValueError(f'Computed spg {computed_sg} does not match actual spg {spg} given in cif files')

    def test_to_pymatgen_faithfulness(self):
        for struct, crystal in zip(self.pymatgen_structures, self.crystal_structures):
            actual = crystal.to_pymatgen()
            expected = struct

            self.assertEqual(actual.lattice, expected.lattice)

            print(f'Actual sites = {actual.sites}; Expected sites = {expected.sites}')
            self.assertEqual(len(actual.sites), len(expected.sites))

            actual_sites = sorted(actual.sites, key=self.euclidean_distance)
            expected_sites = sorted(expected.sites, key=self.euclidean_distance)
            for s1,s2 in zip(actual_sites, expected_sites):
                self.assertEqual(s1,s2)

            print(f'Composition = {actual.composition}')

    @staticmethod
    def extract_spg(cif : str) -> int:
        lines = cif.split('\n')
        spg = None
        for line in lines:
            if '_space_group_IT_number' in line:
                _, spg = line.split()
                spg = int(spg)
        # print(f'Parsed spg number = {spg}')
        return spg


    @staticmethod
    def euclidean_distance(site):
        return math.sqrt(site.x ** 2 + site.y ** 2 + site.z ** 2)


if __name__ == "__main__":
    TestPymatgenStructure.execute_all()
