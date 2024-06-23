import tests.t_crystal.crystaltest as BaseTest

# ---------------------------------------------------------

class TestPropertyCalculation(BaseTest.CrystalTest):
    def test_pymatgen(self):
        for struct, crystal in zip(self.pymatgen_structures, self.crystals):
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


    def test_volumes(self):
        for crystal in self.crystals:
            crystal.calculate_properties()

        expected_volumes = [364.21601704000005, 67.96]
        for crystal, volume_exp in zip(self.crystals, expected_volumes):
            self.assertAlmostEqual(crystal.volume_uc, volume_exp, places=1)
        for crystal in self.crystals:
            print(f'self.crystal atomic volume fraction = {crystal.packing_density}')


    def test_symmetries(self):
        for crystal in self.crystals:
            crystal.calculate_properties()

        for crystal, space_group_exp in zip(self.crystals, self.spgs):
            self.assertEqual(crystal.space_group, space_group_exp)

        expected_systems = ['orthorhombic', 'trigonal']
        for crystal, system_exp in zip(self.crystals, expected_systems):
            self.assertEqual(crystal.crystal_system, system_exp)

        expected_symbols = [
            ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
            ['a','a','a','b','b','b']
        ]
        for crystal, symbols_exp in zip(self.crystals, expected_symbols):
            self.assertEqual(crystal.wyckoff_symbols, symbols_exp)



if __name__ == '__main__':
    TestPropertyCalculation.execute_all()
