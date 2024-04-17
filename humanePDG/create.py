from .elementary import Lepton, Quark, Boson
from .composite import DiQuark, Baryon, Meson
from .humane import __findParticle__
from .particle import Particle
from .data import compositeData, elementaryData


def createParticle(identifier: str | int | float) -> Particle:
    particleID = __findParticle__(identifier)
    if particleID in compositeData:
        kwargs = compositeData[particleID]

        if kwargs['particleType'] == 'meson':
            baseClass = Meson
        elif kwargs['particleType'] == 'baryon':
            baseClass = Baryon
        elif kwargs['particleType'] == 'diquark':
            baseClass = DiQuark

        newClass = type(kwargs['name'], (baseClass,), {})
        return newClass(**kwargs)

    elif particleID in elementaryData:
        kwargs = elementaryData[particleID]

        if kwargs['particleType'] == 'boson':
            baseClass = Boson
        elif kwargs['particleType'] == 'lepton':
            baseClass = Lepton
        elif kwargs['particleType'] == 'quark':
            baseClass = Quark

        newClass = type(kwargs['name'], (baseClass,), {})
        return newClass(**kwargs)

    else:
        raise ValueError(f"Particle {identifier} not found.")
