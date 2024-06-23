from holytools.devtools import Unittest
from pymatgen.core import Species

from CrystalStructure.atomic_constants.atomic_constants import Void
from CrystalStructure.crystal import CrystalStructure, AtomicSite, Lengths, Angles, CrystalBase


# ---------------------------------------------------------

class TestCrystalStandardization(Unittest):
    def setUp(self):
        primitives = Lengths(5, 3, 4)
        mock_angles = Angles(90, 90, 90)
        mock_base = CrystalBase([
            AtomicSite(x=0.5, y=0.5, z=0.5, occupancy=1.0, species=Species("Si")),
            AtomicSite(x=0.1, y=0.1, z=0.1, occupancy=1.0, species=Species("O")),
            AtomicSite(x=0.9, y=0.9, z=0.9, occupancy=1.0, species=Void())
        ])
        crystal = CrystalStructure(lengths=primitives, angles=mock_angles, base=mock_base)
        crystal.calculate_properties()
        crystal.standardize()

        self.mock_crystal = crystal


    def test_standardization(self):
        self.mock_crystal.standardize()
        expected_species_list = ['O', 'Si', Void.symbol]
        acrual_species_list = [self.get_site_symbol(site) for site in self.mock_crystal.base]
        self.assertEqual(acrual_species_list, expected_species_list)

        actual_primitives = self.mock_crystal.lengths.as_tuple()
        expected_primitives = (3, 4, 5)
        self.assertEqual(actual_primitives, expected_primitives)



    @staticmethod
    def get_site_symbol(site : AtomicSite):
        if isinstance(site.species, Void):
            symbol = Void.symbol
        else:
            symbol = site.species.element.symbol
        return symbol
