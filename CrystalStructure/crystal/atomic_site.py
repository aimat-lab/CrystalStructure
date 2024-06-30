from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Union, Optional
from pymatgen.core import Species, Element

from holytools.abstract import Serializable
from CrystalStructure.atomic_constants.atomic_constants import Void, UnknownSite, AtomicConstants

ScatteringParams = tuple[float, float, float, float, float, float, float, float]
#---------------------------------------------------------

@dataclass
class AtomicSite(Serializable):
    """x,y,z are the coordinates of the site given in the basis of the lattice"""
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
    occupancy : Optional[float]
    atom_type : Union[Element,Species, Void, UnknownSite]
    wyckoff_letter : Optional[str] = None

    def __post_init__(self):
        if isinstance(self.atom_type,Element):
            self.atom_type = Species(self.atom_type.symbol)
        self.atom_type : Union[Species, Void, UnknownSite]

    @classmethod
    def make_void(cls) -> AtomicSite:
        return cls(x=None, y=None, z=None, occupancy=0.0, atom_type=Void())

    @classmethod
    def make_placeholder(cls):
        return cls(x=None, y=None, z=None, occupancy=None, atom_type=UnknownSite())

    def is_nonstandard(self) -> bool:
        if isinstance(self.atom_type, Void) or isinstance(self.atom_type, UnknownSite):
            return True
        return False

    # ---------------------------------------------------------
    # properties

    def get_symbol(self) -> str:
        if isinstance(self.atom_type, Species):
            return self.atom_type.element.symbol
        elif isinstance(self.atom_type, Void):
            return Void.symbol
        elif isinstance(self.atom_type, UnknownSite):
            return UnknownSite.symbol
        else:
            raise ValueError(f'Unknown species type: {self.atom_type}')

    def as_list(self) -> list[float]:
        site_arr = [*self.get_scattering_params(), self.x, self.y, self.z, self.occupancy]
        return site_arr

    # TODO: These are currently the scattering factors in pymat gen atomic_scattering_parmas.json
    # These are *different* paramters from what you may commonly see e.g. here (https://lampz.tugraz.at/~hadley/ss1/crystaldiffraction/atomicformfactors/formfactors.php)
    # since pymatgen uses a different formula to compute the form factor
    def get_scattering_params(self) -> ScatteringParams:
        if isinstance(self.atom_type, Species):
            values = AtomicConstants.get_scattering_params(species=self.atom_type)
        elif isinstance(self.atom_type, Void):
            values = (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
        elif isinstance(self.atom_type, UnknownSite):
            fnan = float('nan')
            values = (fnan,fnan), (fnan,fnan), (fnan,fnan), (fnan,fnan)
        else:
            raise ValueError(f'Unknown species type: {self.atom_type}')

        (a1, b1), (a2, b2), (a3, b3), (a4, b4) = values
        return a1, b1, a2, b2, a3, b3, a4, b4

    # ---------------------------------------------------------
    # save/load

    def to_str(self) -> str:
        the_dict = {'x': self.x, 'y': self.y, 'z': self.z, 'occupancy': self.occupancy,
                    'species': str(self.atom_type),
                    'wyckoff_letter': self.wyckoff_letter}

        return json.dumps(the_dict)

    @classmethod
    def from_str(cls, s: str):
        the_dict = json.loads(s)
        species_symbol = the_dict['species']
        if species_symbol == Void.symbol:
            species = Void()
        elif species_symbol == UnknownSite.symbol:
            species = UnknownSite()
        else:
            species = Species.from_str(species_symbol)

        return cls(x=the_dict['x'], y=the_dict['y'], z=the_dict['z'],
                   occupancy=the_dict['occupancy'],
                   atom_type=species,
                   wyckoff_letter=the_dict['wyckoff_letter'])
