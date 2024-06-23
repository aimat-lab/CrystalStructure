from holytools.devtools import Unittest
from CrystalStructure.crystal import CrystalStructure
from CrystalStructure.examples import CrystalExamples


class TestCifParsing(Unittest):
    def test_c1(self):
        c1 = CrystalStructure.from_cif(cif_content=CrystalExamples.get_cif_content())
        c1.calculate_properties()
        
        a, b, c = c1.lengths
        self.assertAlmostEqual(a, 5.801, places=3)
        self.assertAlmostEqual(b, 11.272, places=3)
        self.assertAlmostEqual(c, 5.57, places=3)

        # Unpack angles into alpha, beta, gamma
        alpha, beta, gamma = c1.angles
        self.assertEqual(alpha, 90)
        self.assertEqual(beta, 90)
        self.assertEqual(gamma, 90)

        self.assertAlmostEqual(c1.volume_uc, 364.21601704000005, places=5)
        self.assertEqual(c1.num_atoms, 16)

        expected_symbols = ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'c', 'c', 'c', 'c', 'd', 'd', 'd', 'd']
        self.assertEqual(c1.wyckoff_symbols, expected_symbols)
        self.assertEqual(c1.crystal_system, 'orthorhombic')
        self.assertEqual(c1.space_group, 57)


    def test_c2(self):
        c2 = CrystalStructure.from_cif(cif_content=CrystalExamples.get_cif_content(secondary=True))
        c2.calculate_properties()

        a, b, c = c2.lengths
        self.assertAlmostEqual(a, 26.371, places=3)
        self.assertAlmostEqual(b, 5.2029, places=4)
        self.assertAlmostEqual(c, 8.904, places=3)

        alpha, beta, gamma = c2.angles
        self.assertEqual(alpha, 90)
        self.assertAlmostEqual(beta, 99.325, places=3)
        self.assertEqual(gamma, 90)

        self.assertAlmostEqual(c2.volume_uc, 1205.5, places=1)
        self.assertEqual(c2.num_atoms, 44)

        expected_symbols = ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O', 'N',
                            'N', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        self.assertEqual(c2.wyckoff_symbols, expected_symbols)
        self.assertEqual(c2.crystal_system, 'monoclinic')
        self.assertEqual(c2.space_group, 14)


if __name__ == "__main__":
    TestCifParsing.execute_all()