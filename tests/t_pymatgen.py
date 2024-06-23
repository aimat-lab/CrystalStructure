import math

from holytools.devtools import Unittest
from pymatgen.core import Structure

from CrystalStructure.crystal import CrystalStructure
from CrystalStructure.examples import CrystalExamples


class TestPymatgenSpacegroup(Unittest):
    def setUp(self):
        self.cifs : list[str] =  [CrystalExamples.get_cif_content(), CrystalExamples.get_cif_content(secondary=True)]

    def test_spacegroup_calculation(self):
        for cif in self.cifs:
            structure = CrystalStructure.from_cif(cif_content=cif)
            structure.calculate_properties()
            computed_sg = structure.space_group
            print(f'Computed space group = {computed_sg}')
            original_sg = self.extract_spg(cif)

            if computed_sg != original_sg:
                raise ValueError(f'Computed spg {computed_sg} does not match actual spg {original_sg} given in cif files')

    @staticmethod
    def extract_spg(cif : str) -> int:
        lines = cif.split('\n')
        spg = None
        for line in lines:
            if '_space_group_IT_number' in line:
                _, spg = line.split()
                spg = int(spg)
        print(f'Parsed spg number = {spg}')
        return spg



class TestPymatgenCompatibility(Unittest):
    @classmethod
    def setUpClass(cls):
        pymatgen_structure = Structure.from_str(CrystalExamples.get_cif_content(), fmt='cif')
        cls.crystal = CrystalStructure.from_pymatgen(pymatgen_structure=pymatgen_structure)
        cls.pymatgen_structure = pymatgen_structure

    def test_pymatgen_roundtrip(self):
        actual = self.crystal.to_pymatgen()
        expected = self.pymatgen_structure

        self.assertEqual(len(actual.sites), len(expected.sites))
        print(f'Actual sites = {actual.sites}; Expected sites = {expected.sites}')

        actual_sites = sorted(actual.sites, key=self.euclidean_distance)
        expected_sites = sorted(expected.sites, key=self.euclidean_distance)
        for s1,s2 in zip(actual_sites, expected_sites):
            self.assertEqual(s1,s2)

        print(f'Composition = {actual.composition}')


    @staticmethod
    def euclidean_distance(site):
        return math.sqrt(site.x ** 2 + site.y ** 2 + site.z ** 2)


if __name__ == "__main__":
    TestPymatgenCompatibility.execute_all()
    TestPymatgenSpacegroup.execute_all()
