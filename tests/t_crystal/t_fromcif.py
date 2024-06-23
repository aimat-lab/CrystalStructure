import tests.t_crystal.crystaltest as BaseTest

# ---------------------------------------------------------

class TestCifParsing(BaseTest.CrystalTest):
    def test_lattice_parameters(self):
        expected_lengths = [(5.801, 11.272, 5.57), (26.371, 5.2029, 8.904)]
        for crystal, (a_exp, b_exp, c_exp) in zip(self.crystals, expected_lengths):
            a, b, c = crystal.lengths
            self.assertAlmostEqual(a, a_exp, places=3)
            self.assertAlmostEqual(b, b_exp, places=4)
            self.assertAlmostEqual(c, c_exp, places=3)

    def test_angles(self):
        expected_angles = [(90, 90, 90), (90, 99.325, 90)]
        for crystal, (alpha_exp, beta_exp, gamma_exp) in zip(self.crystals, expected_angles):
            alpha, beta, gamma = crystal.angles
            self.assertEqual(alpha, alpha_exp)
            self.assertAlmostEqual(beta, beta_exp, places=3)
            self.assertEqual(gamma, gamma_exp)

    def test_volume_uc(self):
        expected_volumes = [364.21601704000005, 1205.5]
        for crystal, volume_exp in zip(self.crystals, expected_volumes):
            self.assertAlmostEqual(crystal.volume_uc, volume_exp, places=5)

    def test_num_atoms(self):
        expected_atom_counts = [16, 44]
        for crystal, num_atoms_exp in zip(self.crystals, expected_atom_counts):
            self.assertEqual(crystal.num_atoms, num_atoms_exp)

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


if __name__ == "__main__":
    TestCifParsing.execute_all()