import tests.t_crystal.crystaltest as BaseTest


# ---------------------------------------------------------

class TestPropertyCalculation(BaseTest.CrystalTest):
    def test_atomic_volume(self):
        for crystal in self.crystals:
            print(f'self.crystal atomic volume fraction = {crystal.packing_density}')

    def test_scaling(self):
        for crystal in self.crystals:
            target_density = 0.5
            crystal.scale(target_density=target_density)
            print(f'Packing density, target density = {crystal.packing_density}, {target_density}')
            print(f'Volume scaling = {crystal.packing_density / target_density}')
            print(f'New primitives = {crystal.lengths.as_tuple()}')
            print(f'New packing density = {crystal.packing_density}')
            self.assertEqual(round(crystal.packing_density, 2), round(target_density, 2))


    def test_spacegroup_calculation(self):
        for spg, crystal in zip(self.spgs,self.crystals):
            crystal.calculate_properties()
            computed_sg = crystal.space_group
            print(f'Computed, actual spg = {computed_sg}, {spg}')

            if computed_sg != spg:
                raise ValueError(f'Computed spg {computed_sg} does not match actual spg {spg} given in cif file')


    def test_to_pymatgen_faithfulness(self):
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


if __name__ == '__main__':
    TestPropertyCalculation.execute_all()

