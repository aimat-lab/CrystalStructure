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
                print(f'Scattering params for species \"{atomic_site.species_str}:\n a1, a2, a3, a4, b1, b2, b3, b4 = {params}')
            seen_species.add(atomic_site.atom_type)


if __name__ == '__main__':
    TestCrystalBase.execute_all()