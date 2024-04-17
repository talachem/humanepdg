from difflib import get_close_matches
from .particle import Particle, Charge, SpinType, ParticleType, DecayList, Mass, AngularMomentum
from importlib_resources import files, as_file
from .data import *


# I do this in order to merge all particle dicts
data = {}
data.update(elementaryData)
data.update(compositeData)


def __findParticle__(particle: str | int | float) -> int:
    """
    An internal function for handling different types of particle identifiers
    it's important to keep in mind, the data is stored in dict, with pdg codes
    as identifiers, they are of type str, because of the way how json loads
    the dicts.
    """
    # Going through different possibilities
    if isinstance(particle, str):
        if len(particle) == 1 and not particle.isdigit():
            return str(pdgNamesData[particle[0]])
        elif (len(particle) == 6 and particle.lower().endswith('meson')) or (len(particle) == 6 and particle.lower().endswith('boson')):
            return str(pdgNamesData[particle[0]])

        # If identifier is a PDG Code, e.g., 11, -211
        elif (len(particle) < 2 and particle.isdigit()) or particle.isdigit():
            if int(particle) in namesData.values():
                return str(int(particle))
            else:
                raise ValueError(f"Particle ID {particle} not found.")

        # If the identifier is a PDG ID, e.g., S000
        elif particle[0].isalpha() and particle[1].isdigit():
            try:
                return str(codeData[particle])
            except KeyError:
                raise KeyError(f"Particle Code {particle} not found.")

        elif particle in pdgNamesData:
            return str(pdgNamesData[particle])

        # If the identifier is an MC ID, e.g., 211
        else:
            return __checkDicts__(particle)

    # Checking the float and turning it into an int
    elif isinstance(particle, float):
        # turning float into an int
        if particle.is_integer():
            if int(particle) in namesData.values():
                return str(int(particle))
            else:
                raise ValueError(f"Particle ID {particle} not found.")
        else:
            raise ValueError("Float particle identifiers must be integer-valued, e.g., 211.0")

    # Just return the identifier if it's already an integer
    elif isinstance(particle, int):
        if particle in namesData.values():
            return str(particle)
        else:
            raise ValueError(f"Particle ID {particle} not found.")
    else:
        raise TypeError('The particle identifier needs to be a name (str) or id (int, float)')


def __checkDicts__(keyWord: str | int | float) -> str:
    # Create a list of possible variations of the keyword
    keyword_variations = [
        keyWord,
        str(keyWord).lower(),
        str(keyWord).replace('_', ''),
        str(keyWord).replace(' ', ''),
        str(keyWord).replace('(', '_').replace(')', ''),
        str(keyWord).replace('~', 'bar'),
        str(keyWord).replace('~', '_bar'),
        str(keyWord).replace('bar', '~'),
        str(keyWord).replace('_bar', '~'),
        str(keyWord).capitalize()
    ]

    # Combine all dictionaries for easier lookup
    combined_data = {**pdgNamesData, **namesData, **programmNamesData, **symbolsData}

    # Check each variation against the combined dictionaries
    for variation in keyword_variations:
        if variation in combined_data:
            return str(combined_data[variation])

    raise ValueError(f"Particle Name {keyWord} not found.")


def getParticle(particle: str | int) -> int | str:
    """
    A function that returns the name of a particle when give an ID
    or it returns the ID under a given name of different conventions
    """
    identifier = __findParticle__(particle)
    name = data[identifier]['name']
    if isinstance(particle, (float, int)):
        return name
    elif isinstance(particle, str):
        return int(identifier)
    else:
        raise TypeError(f'the type {type(particle)} is not supported, only floats, ints and strs')


def getAntiParticle(particle: str | int, returnType: str = 'id') -> int | str:
    """
    A function that returns the name of the anti particle when give an ID
    or it returns the ID under a given name of different conventions
    one can choose of an ID or name will be returned
    """
    identifier = __findParticle__(particle)
    isSelfConjugate = data[identifier]['isSelfConjugate']

    antiParticle = identifier if isSelfConjugate else -identifier

    if returnType == 'id':
        return antiParticle
    return names.get(antiParticle)


def isSelfConjugate(particle: str | int) -> bool:
    """
    A function that returns if a particle is self conjugated
    """
    identifier = __findParticle__(particle)
    return data[identifier]['pdgCode'] == data[identifier]['antiParticle']


def getDecayMode(particle: str | int) -> list[str]:
    """
    A function that returns the decay modes of any given particle
    """
    identifier = __findParticle__(particle)
    return data[identifier]['decayModes']


def getDecayWidth(particle: str | int, returnError: bool = False) -> tuple[float]:
    """
    A function that returns the decay with of any given particle
    optionally it can return the error as well
    """
    identifier = __findParticle__(particle)
    if returnError is True:
        (data[identifier]['decayWidth'], data[identifier]['decayWidthUpper'], data[identifier]['decayWidthLower'])
    return (data[identifier]['decayWidth'])


def getMass(particle: str | int, returnError: bool = False) -> tuple[float]:
    """
    A function that returns the mass of any given particle
    optionally it can return the error as well
    """
    identifier = __findParticle__(particle)
    if returnError is True:
        (data[identifier]['mass'], data[identifier]['massLower'], data[identifier]['massUpper'])
    return (data[identifier]['mass'])


def getLifetime(particle: str | int) -> float:
    """
    A function that returns the lifetime of any given particle
    """
    identifier = __findParticle__(particle)
    return data[identifier]['lifetime']


def getCharge(particle: str | int) -> Charge:
    """
    A function that returns the charge of any given particle
    """
    identifier = __findParticle__(particle)
    charge = Charge.set(data[identifier]['charge'])
    return charge


def getQuarks(particle: str | int) -> list[str]:
    """
    A function that returns the quark content of any given particle
    """
    identifier = __findParticle__(particle)
    if data[identifier]['particleType'] == 'boson' | data[identifier]['particleType'] == 'lepton':
        raise Warning(f'{particle} does not contain quarks')
    elif data[identifier]['particleType'] == 'quark':
        return [data[identifier]['symbol']]
    return data[identifier]['quarks']


def getSpinType(particle: str | int) -> SpinType:
    """
    A function that returns the spin type of any given particle
    """
    identifier = __findParticle__(particle)
    return SpinType.set(data[identifier]['spin'])


def getParticleType(particle: str | int) -> ParticleType:
    """
    A function that returns the particle type of any given particle
    """
    identifier = __findParticle__(particle)
    return ParticleType(data[identifier]['particleType'])


def isQuark(particle: str | int) -> bool:
    """
    A function that returns if any given particle is a lepton
    """
    identifier = __findParticle__(particle)
    return data['particleType'] == 'quark'


def isLepton(particle: str | int) -> bool:
    """
    A function that returns if any given particle is a lepton
    """
    identifier = __findParticle__(particle)
    return data['particleType'] == 'lepton'


def isBoson(particle: str | int) -> bool:
    """
    A function that returns if any given particle is a gauge boson
    """
    identifier = __findParticle__(particle)
    return data['particleType'] == 'boson'


def isMeson(particle: str | int) -> bool:
    """
    A function that returns if any given particle is a meson
    """
    identifier = __findParticle__(particle)
    return data['particleType'] == 'meson'


def isBaryon(particle: str | int) -> bool:
    """
    A function that returns if any given particle is a baryon
    """
    identifier = __findParticle__(particle)
    return data['particleType'] == 'baryon'


def listNames() -> list[str]:
    """
    Lists all names that can be imported
    """
    return [data[id]['name'] for id in data]


def listIDs() -> list[int]:
    """
    Lists all particle Monte Carlo IDs
    """
    return list(data.keys())


def listPDGNames() -> list[str]:
    """
    Lists all pdg names that can be imported
    """
    return [data[id]['pdgName'] for id in data]
