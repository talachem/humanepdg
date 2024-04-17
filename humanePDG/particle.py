from abc import ABC
from enum import Enum
from fractions import Fraction
from typing import Any


class ParticleType(Enum):
    QUARK = 'quark'
    DIQUARK = 'diquark'
    BARYON = 'baryon'
    MESON = 'meson'
    LEPTON = 'lepton'
    BOSON = 'boson'
    UNKNOWN = 'unknown'

    def __repr__(self) -> str:
        return 'particle type: ' + self.value

class Parity(Enum):
    POSITIVE = 1
    NEGATIVE = -1
    UNDIFINED = None
    NONE = None

    def __repr__(self) -> str:
        return 'parity: ' + self.value


class Charge(Enum):
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    UNKNOWN = None

    PLUSONETHIRD = Fraction(1,3)
    PLUSTWOTHIRDS = Fraction(2,3)
    MINUSONETHIRD = Fraction(-1,3)
    MINUSTWOTHIRDS = Fraction(-2,3)

    @classmethod
    def set(cls, value: Any):
        if isinstance(value, str):
            return cls.__members__.get(value.upper(), cls.UNKNOWN)
        else:
            if value is None:
                return cls.NEUTRAL
            elif value == -1:
                return cls.NEGATIVE
            elif value == 1:
                return cls.POSITIVE
            elif value == 0:
                return cls.NEUTRAL
            elif value > 0.3 and value < 0.4:
                return cls.PLUSONETHIRD
            elif value > 0.5 and value < 0.7:
                return cls.PLUSTWOTHIRDS
            elif value < -0.3 and value > -0.4:
                return cls.MINUSONETHIRD
            elif value < -0.5 and value > -0.7:
                return cls.MINUSTWOTHIRDS
            else:
                return cls.UNKNOWN

    def __repr__(self) -> str:
        if self.value == -1:
            return '-1e'
        elif self.value == 1:
            return '+1e'
        elif self.value == 0:
            return '±0e'
        elif self.value == Fraction(1,3):
            return '+1∕3e'
        elif self.value == Fraction(2,3):
            return '+2∕3e'
        elif self.value == Fraction(-1,3):
            return '-1∕3e'
        elif self.value == Fraction(-2,3):
            return '-2∕3e'
        else:
            return 'unknown charge'

    def __str__(self) -> str:
        if self.value == -1:
            return '-1e'
        elif self.value == 1:
            return '+1e'
        elif self.value == 0:
            return '±0e'
        elif self.value == Fraction(1,3):
            return '+1∕3e'
        elif self.value == Fraction(2,3):
            return '+2∕3e'
        elif self.value == Fraction(-1,3):
            return '-1∕3e'
        elif self.value == Fraction(-2,3):
            return '-2∕3e'
        else:
            return 'unknown charge'


class SpinType(Enum):
    FULL = 'full'
    HALF = 'half'
    UNKNOWN = 'unknown'

    def __repr__(self) -> str:
        return 'spin type: ' + self.value


class AngularMomentum(Enum):
    FOUR = 4.0
    SEVENHALFS = 3.5
    THREE = 3.0
    FIVEHALFS = 2.5
    TWO = 2.0
    THREEHALFS = 1.5
    ONE = 1.0
    ONEHALF = 0.5
    ZERO = 0.0
    UNKNOWN = None

    def __repr__(self) -> str:
        if self.value == 0.0:
            return 'angular momentum: 0'
        elif self.value == 0.5:
            return 'angular momentum: 1/2'
        elif self.value == 1.0:
            return 'angular momentum: 1'
        elif self.value == 1.5:
            return 'angular momentum: 3/2'
        elif self.value == 2.0:
            return 'angular momentum: 2'
        elif self.value == 2.5:
            return 'angular momentum: 5/2'
        elif self.value == 3.0:
            return 'angular momentum: 3'
        elif self.value == 3.5:
            return 'angular momentum: 7/2'
        elif self.value == 4.0:
            return 'angular momentum: 4'
        else:
            return 'unknown angular momentum'


class IsoSpin(Enum):
    FOUR = 4.0
    SEVENHALFS = 3.5
    THREE = 3.0
    FIVEHALFS = 2.5
    TWO = 2.0
    THREEHALFS = 1.5
    ONE = 1.0
    ONEHALF = 0.5
    ZERO = 0.0
    UNKNOWN = None

    def __repr__(self) -> str:
        if self.value == 0.0:
            return 'isospin: 0'
        elif self.value == 0.5:
            return 'isospin: 1/2'
        elif self.value == 1.0:
            return 'isospin: 1'
        elif self.value == 1.5:
            return 'isospin: 3/2'
        elif self.value == 2.0:
            return 'isospin: 2'
        elif self.value == 2.5:
            return 'isospin: 5/2'
        elif self.value == 3.0:
            return 'isospin: 3'
        elif self.value == 3.5:
            return 'isospin: 7/2'
        elif self.value == 4.0:
            return 'isospin: 4'
        else:
            return 'unknown isospin'


class Excited(Enum):
    EXCITED = 'excited'
    GROUND = 'ground'
    UNKNOWN = 'unknown'


class DecayList:
    probability: float
    daughters: []


class Mass:
    def __init__(self, mass: float, *, upperError: float = None, lowerError: float = None, unit: str = 'MeV'):
        self.mass = mass
        self.upperError = upperError
        self.lowerError = lowerError
        self.error = None
        if upperError == lowerError:
            self.error = upperError
        self.unit = unit

    def __repr__(self) -> str:
        if not self.error == None:
            return f'({self.mass} ± {self.error}) {self.unit}'
        return f'({self.mass} + {self.upperError} - {self.lowerError}) {self.unit}'


class DecayWidth:
    def __init__(self, decayWidth: float, *, upperError: float = None, lowerError: float = None, unit: str = 'MeV'):
        self.decayWidth = decayWidth
        self.upperError = upperError
        self.lowerError = lowerError
        self.error = None
        if upperError == lowerError:
            self.error = upperError
        self.unit = unit

    def __repr__(self) -> str:
        if not self.error == None:
            return f'({self.decayWidth} ± {self.error}) {self.unit}'
        return f'({self.decayWidth} + {self.upperError} - {self.lowerError}) {self.unit}'


class Particle(ABC):
    def __init__(self,
            pdgName: str,
            pdgID: int,
            symbol: str = '',
            unicode: str = '',
            charge: Charge = Charge.UNKNOWN,
            angularMomentum: AngularMomentum = AngularMomentum.ZERO,
            isoSpin: IsoSpin = IsoSpin.ZERO,
            mass: float = 0,
            massUpper: float = 0,
            massLower: float = 0,
            selfConjugated: bool = False,
            lifetime: float = 0,
            chargeConjugate: Parity = Parity.UNDIFINED,
            paritySymmetry: Parity = Parity.UNDIFINED,
            decayWidth: float = 0,
            decayWidthUpper: float = 0,
            decayWidthLower: float = 0,
            decayModes: list[DecayList] = [],
            **kwargs
        ):
        self.name = self.__class__.__name__
        self.pdgName = pdgName
        self.pdgID = pdgID
        self.symbol = symbol
        self.unicode = unicode
        if selfConjugated:
            self.antiParticle = pdgID
        else:
            self.antiParticle = -pdgID
        self.particleType = ParticleType.UNKNOWN
        self.isElementary = True

        self._charge = Charge.set(charge)
        self.spinType = SpinType.UNKNOWN
        self.angularMomentum = AngularMomentum(angularMomentum)
        self.isoSpin = IsoSpin(isoSpin)

        self.mass = Mass(mass, upperError=massUpper, lowerError=massLower)
        self.massValue = mass

        self.lifetime = lifetime
        self.chargeConjugate = chargeConjugate
        self.paritySymmetry = paritySymmetry
        self.decayWidth = DecayWidth(decayWidth, upperError=decayWidthUpper, lowerError=decayWidthLower)
        self.decayWidthValue = decayWidth
        self._decayModes = decayModes

    @property
    def isSelfConjugated(self) -> bool:
        return self.pdgID == self.antiParticle

    @property
    def charge(self) -> Charge:
        return self._charge

    def __repr__(self) -> str:
        return f'{self.unicode}, {self._charge}, {self.mass}, {self.pdgID}'

    @property
    def isAntiParticle(self) -> bool:
        return self.pdgID < 0

    @property
    def decayModes(self) -> DecayList:
        return self._decayModes
