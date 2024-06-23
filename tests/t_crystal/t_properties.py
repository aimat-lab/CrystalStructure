import tests.t_crystal.crystaltest as BaseTest


# ---------------------------------------------------------

class TestPropertyCalculation(BaseTest.CrystalTest):
    def test_atomic_volume(self):
        for crystal in self.crystals:
            print(f'self.crystal atomic volume fraction = {crystal.packing_density}')

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

    def test_spacegroup_calculation(self):
        for spg, crystal in zip(self.spgs,self.crystals):
            crystal.calculate_properties()
            computed_sg = crystal.space_group
            print(f'Computed, actual spg = {computed_sg}, {spg}')

            if computed_sg != spg:
                raise ValueError(f'Computed spg {computed_sg} does not match actual spg {spg} given in cif file')


    def test_volume_uc(self):
        expected_volumes = [364.21601704000005, 1205.5]
        for crystal, volume_exp in zip(self.crystals, expected_volumes):
            self.assertAlmostEqual(crystal.volume_uc, volume_exp, places=5)


    def test_wyckoff_symbols(self):
        expected_symbols = [
            ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'c', 'c', 'c', 'c', 'd', 'd', 'd', 'd'],
            ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'O', 'O', 'O', 'O', 'O', 'O', 'N', 'N', 'H', 'H',
             'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        ]
        for crystal, symbols_exp in zip(self.crystals, expected_symbols):
            self.assertEqual(crystal.wyckoff_symbols, symbols_exp)

    def test_crystal_system(self):
        expected_systems = ['orthorhombic', 'monoclinic']
        for crystal, system_exp in zip(self.crystals, expected_systems):
            self.assertEqual(crystal.crystal_system, system_exp)

    def test_space_group(self):
        expected_space_groups = [57, 14]
        for crystal, space_group_exp in zip(self.crystals, expected_space_groups):
            self.assertEqual(crystal.space_group, space_group_exp)

if __name__ == '__main__':
    TestPropertyCalculation.execute_all()
