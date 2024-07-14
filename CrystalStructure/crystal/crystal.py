from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Optional, Literal

import numpy as np
from holytools.abstract import JsonDataclass
from pymatgen.core import Structure, Lattice, Species, Element
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.groups import SpaceGroup

from holytools.logging import LoggerFactory
from .atomic_site import AtomicSite
from .base import CrystalBase
from .lattice import Angles, Lengths

logger = LoggerFactory.get_logger(name=__name__)
CrystalSystem = Literal["cubic", "hexagonal", "monoclinic", "orthorhombic", "tetragonal", "triclinic", "trigonal"]
# ---------------------------------------------------------

@dataclass
class CrystalStructure(JsonDataclass):
    lengths : Lengths
    angles : Angles
    base : CrystalBase
    spacegroup : Optional[int] = None
    volume_uc : Optional[float] = None
    atomic_volume: Optional[float] = None
    num_atoms : Optional[int] = None
    wyckoff_symbols : Optional[list[str]] = None
    crystal_system : Optional[str] = None

    @classmethod
    def from_cif(cls, cif_content : str) -> CrystalStructure:
        pymatgen_structure = Structure.from_str(cif_content, fmt='cif')
        crystal_structure = cls.from_pymatgen(pymatgen_structure)
        return crystal_structure

    @classmethod
    def from_pymatgen(cls, pymatgen_structure: Structure) -> CrystalStructure:
        lattice = pymatgen_structure.lattice
        base : CrystalBase = CrystalBase()

        for index, site in enumerate(pymatgen_structure.sites):
            site_composition = site.species
            for species, occupancy in site_composition.items():
                if isinstance(species, Element):
                    species = Species(symbol=species.symbol, oxidation_state=0)
                x,y,z = lattice.get_fractional_coords(site.coords)
                atomic_site = AtomicSite(x, y, z, occupancy=occupancy, species_str=str(species))
                base.append(atomic_site)

        crystal_str = cls(lengths=Lengths(a=lattice.a, b=lattice.b, c=lattice.c),
                          angles=Angles(alpha=lattice.alpha, beta=lattice.beta, gamma=lattice.gamma),
                          base=base)

        return crystal_str

    # ---------------------------------------------------------
    # properties

    def calculate_properties(self):
        if len(self.base) == 0:
            logger.error(msg=f'Base is empty! Cannot calculate properties of empty crystal. Aborting ...')
            return

        pymatgen_structure = self.to_pymatgen()
        self.volume_uc = pymatgen_structure.volume
        analyzer = SpacegroupAnalyzer(structure=pymatgen_structure, symprec=0.1, angle_tolerance=10)
        self.spacegroup = analyzer.get_space_group_number()
        self.num_atoms = len(self.base)

        symmetry_dataset = analyzer.get_symmetry_dataset()
        self.wyckoff_symbols = symmetry_dataset['wyckoffs']

        pymatgen_spacegroup = SpaceGroup.from_int_number(self.spacegroup)
        self.crystal_system = pymatgen_spacegroup.crystal_system

    def standardize(self):
        """Permutes lattice primitives such that a <= b <=c and permutes lattice sites such that i > j => d(i) > d(j) with d(i) = (x_i**2+y_i**2+z_i**2)"""
        a,b,c = self.lengths
        alpha, beta, gamma = self.angles
        sort_permutation = get_sorting_permutation(a,b,c)

        lattice = Lattice.from_parameters(a,b,c, alpha, beta, gamma).matrix
        new_lattice = Lattice(apply_permutation(lattice, permutation=sort_permutation))

        self.lengths = Lengths(new_lattice.a, new_lattice.b, new_lattice.c)
        self.angles = Angles(new_lattice.alpha, new_lattice.beta, new_lattice.gamma)

        new_base = CrystalBase()
        for site in self.base:
            x,y,z = apply_permutation([site.x, site.y, site.z], sort_permutation)
            new_site = AtomicSite(x=x, y=y, z=z, occupancy=site.occupancy, species_str=site.species_str, wyckoff_letter=site.wyckoff_letter)
            new_base.append(new_site)


        def distance_from_origin(atomic_site : AtomicSite):
            coords = np.array([atomic_site.x, atomic_site.y, atomic_site.z])
            cartesian_coords = new_lattice.get_fractional_coords(coords)
            return np.sum(cartesian_coords**2)

        new_base = sorted(new_base.atomic_sites, key=distance_from_origin)
        self.base = CrystalBase(new_base)

    def scale(self, target_density: float):
        volume_scaling = self.packing_density / target_density
        cbrt_scaling = volume_scaling ** (1 / 3)
        self.lengths = self.lengths * cbrt_scaling
        self.volume_uc = self.volume_uc * volume_scaling

    @property
    def packing_density(self) -> float:
        volume_uc = self.volume_uc
        atomic_volume = self.base.calculate_atomic_volume()
        return atomic_volume/volume_uc

    # ---------------------------------------------------------
    # conversion

    def to_cif(self) -> str:
        pymatgen_structure = self.to_pymatgen()
        return pymatgen_structure.to(filename='', fmt='cif')

    def to_pymatgen(self) -> Structure:
        a, b, c = self.lengths.as_tuple()
        alpha, beta, gamma = self.angles.as_tuple()
        lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma)

        non_void_sites = self.base.get_non_void_sites()
        atoms = [site.atom_type.pymatgen_type for site in non_void_sites]
        positions = [(site.x, site.y, site.z) for site in non_void_sites]

        if len(atoms) == 0:
            logger.warning('Structure has no atoms!')

        return Structure(lattice, atoms, positions)

    def as_str(self) -> str:
        the_dict = asdict(self)
        the_dict = {str(key) : str(value) for key, value in the_dict.items() if not isinstance(value, Structure)}
        the_dict['base'] = f'{self.base[0]}, ...'
        return json.dumps(the_dict, indent='-')

    def __str__(self):
        return self.as_str()



def get_sorting_permutation(a, b, c):
    original = [a, b, c]
    sorted_with_indices = sorted(enumerate(original), key=lambda x: x[1])
    permutation = [x[0] for x in sorted_with_indices]
    return permutation


def apply_permutation(original_list, permutation):
    return [original_list[i] for i in permutation]

