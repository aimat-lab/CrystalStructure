import json
import os.path
from typing import Literal, Union
from pymatgen.core import Species, Element


SCATTERING_PARAMS_FILENAME = 'atomic_scattering_params.json'
COVALENT_RADI_FILENAME = 'covalent_radius.json'
VDW_FILENAME = 'vdw_radius.json'

ElementSymbol = Literal['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db']

def load_constants_json(fname: str) -> dict:
    dirpath = os.path.dirname(__file__)
    fpath = os.path.join(dirpath, fname)
    with open(fpath) as file:
        return json.load(file)

# ---------------------------------------------------------

class UnknownSite:
    symbol = 'NaN'

class Void:
    symbol = '⊥'


class AtomicConstants:
    _vdw : dict[str, float] = load_constants_json(fname=VDW_FILENAME)
    _covalent : dict[str, float] = load_constants_json(fname=COVALENT_RADI_FILENAME)
    _scattering_params : dict[str, tuple] = load_constants_json(fname=SCATTERING_PARAMS_FILENAME)

    # ---------------------------------------------------------
    # get

    @classmethod
    def get_vdw_radius(cls, element_symbol: ElementSymbol) -> float:
        return cls._vdw[element_symbol]

    @classmethod
    def get_covalent(cls, element_symbol: ElementSymbol) -> float:
        return cls._covalent[element_symbol]

    @classmethod
    def get_scattering_params(cls, species: Union[Element,Species]) -> tuple:
        if isinstance(species, Species):
            symbol = str(species.element.symbol)
        else:
            symbol = species.symbol

        return cls._scattering_params[symbol]

    @classmethod
    def print_all(cls):
        print("Van der Waals radii:", cls._vdw)
        print("Covalent radii:", cls._covalent)
        print("Scattering parameters:", cls._scattering_params)



if __name__ == "__main__":
    provider = AtomicConstants()
    provider.print_all()