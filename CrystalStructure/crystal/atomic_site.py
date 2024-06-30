from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from holytools.abstract import Serializable
from pymatgen.core import Species, DummySpecies
from pymatgen.util.typing import SpeciesLike

from CrystalStructure.atomic_constants.atomic_constants import AtomicConstants

ScatteringParams = tuple[float, float, float, float, float, float, float, float]
#---------------------------------------------------------

# Conditions:
# - AtomicSite should be initializable with only a pymatgen species
# - The make_void and make_placeholder classmethods should continue to work as before

# ->

@dataclass
class AtomicSite(Serializable):
    """x,y,z are the coordinates of the site given in the basis of the lattice"""
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
    occupancy : Optional[float]
    species_symbol : str
    wyckoff_letter : Optional[str] = None

    def __post_init__(self):
        self.atom_type : AtomType = AtomType(symbol=self.species_symbol)

    @classmethod
    def make_void(cls) -> AtomicSite:
        return cls(x=None, y=None, z=None, occupancy=0.0, species_symbol=AtomType.void_symbol)

    @classmethod
    def make_placeholder(cls):
        return cls(x=None, y=None, z=None, occupancy=None, species_symbol=AtomType.placeholder_symbol)

    def is_nonstandard(self) -> bool:
        if self.species_symbol == AtomType.void_symbol or self.species_symbol == AtomType.placeholder_symbol:
            return True
        return False

    # ---------------------------------------------------------
    # properties

    def as_list(self) -> list[float]:
        site_arr = [*self.get_scattering_params(), self.x, self.y, self.z, self.occupancy]
        return site_arr

    # TODO: These are currently the scattering factors in pymat gen atomic_scattering_parmas.json
    # These are *different* paramters from what you may commonly see e.g. here (https://lampz.tugraz.at/~hadley/ss1/crystaldiffraction/atomicformfactors/formfactors.php)
    # since pymatgen uses a different formula to compute the form factor
    def get_scattering_params(self) -> ScatteringParams:
        return self.atom_type.scattering_params

    # ---------------------------------------------------------
    # save/load

    def to_str(self) -> str:
        the_dict = {'x': self.x, 'y': self.y, 'z': self.z, 'occupancy': self.occupancy,
                    'symbol': self.species_symbol,
                    'wyckoff_letter': self.wyckoff_letter}

        return json.dumps(the_dict)

    @classmethod
    def from_str(cls, s: str):
        the_dict = json.loads(s)

        return cls(x=the_dict['x'], y=the_dict['y'], z=the_dict['z'],
                   occupancy=the_dict['occupancy'],
                   species_symbol=the_dict['symbol'],
                   wyckoff_letter=the_dict['wyckoff_letter'])


class AtomType:
    void_symbol = '⊥'
    placeholder_symbol = 'NaN'

    def __init__(self, symbol : str):
        if symbol == self.void_symbol:
            self.specifier : SpeciesLike = DummySpecies(symbol=self.void_symbol)
        if symbol == self.placeholder_symbol:
            self.specifier : SpeciesLike = DummySpecies(symbol=self.placeholder_symbol)
        else:
            self.specifier : SpeciesLike = Species.from_str(species_string=symbol)

    def get_symbol(self):
        return str(self.specifier)

    @property
    def scattering_params(self) -> ScatteringParams:
        if self.get_symbol() == self.void_symbol:
            values = (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
        elif self.get_symbol() == self.placeholder_symbol:
            fnan = float('nan')
            values = (fnan, fnan), (fnan, fnan), (fnan, fnan), (fnan, fnan)
        else:
            # TODO: This casting only currently exists beacuse the scattering param table only has values for (unoxidized) elements, not ions
            # TODO: Normally would simply be species_symbol=str(self.species_like)
            species_symbol = self.specifier.element.symbol
            values = AtomicConstants.get_scattering_params(species_symbol=species_symbol)

        (a1, b1), (a2, b2), (a3, b3), (a4, b4) = values
        return a1, b1, a2, b2, a3, b3, a4, b4
