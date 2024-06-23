from pymatgen.core import Species

from holytools.devtools import Unittest

from CrystalStructure.crystal import CrystalStructure, Lengths, Angles, CrystalBase, AtomicSite
from CrystalStructure.atomic_constants.atomic_constants import Void

# ---------------------------------------------------------


class TestCrystalCalculations(Unittest):
    def setUp(self):
        self.primitives = Lengths(5, 3, 4)
        self.angles = Angles(90, 90, 90)
        self.base = CrystalBase([
            AtomicSite(x=0.5, y=0.5, z=0.5, occupancy=1.0, species=Species("Si")),
            AtomicSite(x=0.1, y=0.1, z=0.1, occupancy=1.0, species=Species("O")),
            AtomicSite(x=0.9, y=0.9, z=0.9, occupancy=1.0, species=Void())
        ])
        crystal = CrystalStructure(lengths=self.primitives, angles=self.angles, base=self.base)
        crystal.calculate_properties()
        crystal.standardize()
        self.crystal = crystal

    def test_standardization(self):
        self.crystal.standardize()
        expected_species_list = ['O', 'Si', Void.symbol]
        acrual_species_list = [self.get_site_symbol(site) for site in self.crystal.base]
        self.assertEqual(acrual_species_list, expected_species_list)

        actual_primitives = self.crystal.lengths.as_tuple()
        expected_primitives = (3,4,5)
        self.assertEqual(actual_primitives, expected_primitives)


    def test_atomic_volume(self):
        print(f'self.crystal atomic volume fraction = {self.crystal.packing_density}')

    def test_scaling(self):
        target_density = 0.5
        self.crystal.scale(target_density=target_density)
        print(f'Packing density, target density = {self.crystal.packing_density}, {target_density}')
        print(f'Volume scaling = {self.crystal.packing_density/target_density}')
        print(f'New primitives = {self.crystal.lengths.as_tuple()}')
        print(f'New packing density = {self.crystal.packing_density}')
        self.assertEqual(round(self.crystal.packing_density,2), round(target_density,2))

    @staticmethod
    def get_site_symbol(site : AtomicSite):
        if isinstance(site.species, Void):
            symbol = Void.symbol
        else:
            symbol = site.species.element.symbol
        return symbol


if __name__ == '__main__':
    TestCrystalCalculations.execute_all()

