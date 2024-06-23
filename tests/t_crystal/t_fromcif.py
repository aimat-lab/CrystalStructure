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


    def test_num_atoms(self):
        expected_atom_counts = [4*4, (11+14+2+5)*4]
        for crystal, num_atoms_exp in zip(self.crystals, expected_atom_counts):
            self.assertEqual(len(crystal.base), num_atoms_exp)


if __name__ == "__main__":
    TestCifParsing.execute_all()