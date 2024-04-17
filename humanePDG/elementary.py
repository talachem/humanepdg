from .particle import Particle, Charge, SpinType, ParticleType
from importlib_resources import files, as_file
from .data import elementaryData


__all__ = []


class Quark(Particle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.QUARK
        self.spinType = SpinType.HALF

    @property
    def quarks(self):
        return self

class Lepton(Particle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.LEPTON
        self.spinType = SpinType.HALF


class Boson(Particle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.particleType = ParticleType.BOSON
        self.spinType = SpinType.FULL


# Dynamically create classes and instances based on the data
for key in elementaryData:
    name = elementaryData[key]['name']
    kwargs = elementaryData[key]

    if elementaryData[key]['particleType'] == 'boson':
        baseClass = Boson
    elif elementaryData[key]['particleType'] == 'lepton':
        baseClass = Lepton
    elif elementaryData[key]['particleType'] == 'quark':
        baseClass = Quark

    # Create the new class
    newClass = type(name, (baseClass,), {})

    # Check for name collisions
    if name in globals():
        print(f"Warning: A class named {name} already exists.")

    globals()[name] = newClass(**kwargs)  # Create an instance and store it in globals
    __all__.append(name)
