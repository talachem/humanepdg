import numpy as np
from .particle import Particle, Charge, SpinType, ParticleType
from .elementary import Quark
from .humane import getParticle
from .data import elementaryData, compositeData
import re
from importlib_resources import files, as_file


__all__ = []


class Composite(Particle):
    def __init__(self, quarks: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isElementary = False
        if not '/' in quarks and not '+' in quarks and not '-' in quarks:
            self.quarks = QuarkTuple(quarks)
        else:
            self.quarks = QuarkSuperposition(quarks)

    @property
    def charge(self) -> Charge:
        if isinstance(self.quarks, QuarkTuple):
            return Charge(sum([q.charge.value for q in self.quarks]))
        else:
            return Charge(sum([q.charge.value for q in self.quarks[0]]))


class QuarkTuple():
    def __init__(self, quarks: str) -> None:
        self._quarks = []
        for quark in quarks:
            x = quark.lower()+'~' if quark == quark.upper() else quark
            id = getParticle(x)
            q = Quark(**elementaryData[str(id)])
            self._quarks.append(q)

    def __iter__(self):
        return iter(self._quarks)

    def __repr__(self) -> str:
        printString = ''
        for quark in self._quarks:
            printString += str(quark.unicode)
        return printString


class QuarkSuperposition():
    quarkPattern1 = re.compile(r'([udscbt][UDSCTB])')
    quarkPattern2 = re.compile(r'([UDSCTB][udscbt])')
    coefficientPattern = re.compile(r'([a-zA-Z])(\([a-zA-Z\+\-]*\))')

    def __init__(self, quarks: str) -> None:
        self._quarkTuples = []
        self._coefficients = []
        if '/' in quarks:
            quarkTuples = np.concatenate((self.quarkPattern1.findall(quarks), self.quarkPattern2.findall(quarks)))
            for quarkPair in quarkTuples:
                self._quarkTuples.append(QuarkTuple(quarkPair))
                self._coefficients.append('√2')
            if '-' in quarks:
                self._coefficients[-1] = '-√2'
        else:
            matches = self.coefficientPattern.findall(quarks)
            for coefficient, content in matches:
                patternMatches = np.concatenate((self.quarkPattern1.findall(content), self.quarkPattern2.findall(content)))
                for pair in patternMatches:
                    self._quarkTuples.append(QuarkTuple(pair))
                    self._coefficients.append(coefficient)

    def __iter__(self):
        for pair in self._quarkTuples:
            for quark in pair:
                yield quark

    def __getitem__(self, index):
        return self._quarkTuples[index]

    def __repr__(self) -> str:
        terms = []
        joiner = ' + '
        for quark_tuple, coefficient in zip(self._quarkTuples, self._coefficients):
            if coefficient.startswith('-'):
                joiner = ' - '
                coefficient = coefficient[1:]
            terms.append(f"{coefficient}({quark_tuple})")
        return joiner.join(terms)


class Meson(Composite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.MESON
        self.spinType = SpinType.FULL


class Baryon(Composite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.BARYON
        self.spinType = SpinType.HALF


class DiQuark(Composite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.DIQUARK
        self.spinType = SpinType.FULL


# Dynamically create classes and instances based on the data
for key in compositeData:
    name = compositeData[key]['name']
    kwargs = compositeData[key]

    if compositeData[key]['particleType'] == 'meson':
        baseClass = Meson
    elif compositeData[key]['particleType'] == 'baryon':
        baseClass = Baryon
    elif compositeData[key]['particleType'] == 'diquark':
        baseClass = DiQuark

    # Create the new class
    newClass = type(name, (baseClass,), {})

    # Check for name collisions
    if name in globals():
        print(f"Warning: A class named {name} already exists.")

    globals()[name] = newClass(**kwargs)  # Create an instance and store it in globals
    __all__.append(name)

    if 'Beauty' in name:
        secondName = name.replace('Beauty', 'BMeson')
        secondClass = type(secondName, (baseClass,), {})
        globals()[secondName] = secondClass(**kwargs)  # Create an instance and store it in globals
        __all__.append(secondName)
    if 'Duty' in name:
        thirdName = name.replace('Duty', 'DMeson')
        thirdClass = type(thirdName, (baseClass,), {})
        globals()[thirdName] = thirdClass(**kwargs)  # Create an instance and store it in globals
        __all__.append(thirdName)
