from holytools.devtools import Unittest
from pymatgen.core import Species

from CrystalStructure.examples import CrystalExamples

# ---------------------------------------------------------

class TestCrystalBase(Unittest):
    def test_scattering_params(self):
        base = CrystalExamples.get_base()
        seen_species = set()

        for atomic_site in base:
            params = atomic_site.get_scattering_params()
            self.assertEqual(len(params), 8)
            for p in params:
                self.assertIsInstance(p, float)
            if not atomic_site.atom_type in seen_species:
                print(f'Scattering params for species \"{atomic_site.atom_type}\" a1, a2, a3, a4, b1, b2, b3, b4 = {params}')
            seen_species.add(atomic_site.atom_type)


    def test_site_dictionaries(self):
        base = CrystalExamples.get_base(mute=False)
        site_dictionaries = base.as_site_dictionaries()
        coordinates = list(site_dictionaries.keys())

        max_err = 10**(-2)
        target_coordinate = (0.931,0.25,0)
        def dist(coor1, coord2):
            return sum([(x-y)**2 for x,y in zip(coor1, coord2)])**(1/2)

        match = None
        for coord in coordinates:
            match_found = any([dist(coord, target_coordinate) < max_err])
            if match_found:
                match = coord

        self.assertIsNotNone(match)
        self.assertIn(Species(f'Al0+'), site_dictionaries[match])


if __name__ == '__main__':
    TestCrystalBase.execute_all()