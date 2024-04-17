from collections import namedtuple
import numpy as np
from functools import partial
from .particle import Particle
from .elementary import Lepton, Strange, AntiStrange
from .composite import Baryon, Meson
from functools import partial


# a named tuple that returns if a decay is allowed or not and gives a reason
ConservationCheckResult = namedtuple('ConservationCheckResult', ['isPermited', 'reason'])


def _attributeConversation(parents: list[Particle], daughters: list[Particle], attribute: str, conversationName: str) -> ConservationCheckResult:
     # Convert parents to a list if it's not already
    if not isinstance(parents, list):
        parents = [parents]

    def sumAttribute(particles):
        return sum(getattr(p, attribute).value for p in particles if getattr(p, attribute).value is not None)

    before = sumAttribute(parents)
    after = sumAttribute(daughters)

    isPermited = (before == after)
    reason = f'{conversationName} is conserved (Total {conversationName} before: {before}, after: {after})' if isPermited else f'{conversationName} is not conserved (Total {conversationName} before: {before}, after: {after})'
    return ConservationCheckResult(isPermited=isPermited, reason=reason)


chargeConversation = partial(_attributeConversation, attribute='charge', conversationName='Charge')
isoSpinConservation = partial(_attributeConversation, attribute='isoSpin', conversationName='Isospin')


def _typeConservation(parents: list[Particle], daughters: list[Particle], pType: str, conversationName: str) -> ConservationCheckResult:
     # Convert parents to a list if it's not already
    if not isinstance(parents, list):
        parents = [parents]

    before = 0
    for p in parents:
        if isinstance(p, pType):
            before += 1 if not p.isAntiParticle else -1
    after = 0
    for p in daughters:
        if isinstance(p, pType):
            after += 1 if not p.isAntiParticle else -1

    isPermited = (before == after)
    reason = f'{conversationName} is conserved ({conversationName} before: {before}, after: {after})' if isPermited else f'{conversationName} is not conserved ({conversationName} before: {before}, after: {after})'
    return ConservationCheckResult(isPermited=isPermited, reason=reason)


baryonNumberConservation = partial(_typeConservation, pType=Baryon, conversationName='Baryon Number')
leptonNumberConservation = partial(_typeConservation, pType=Lepton, conversationName='Lepton Number')

"""
def calcEnergyMass(parents: list[Particle], daughters: list[Particle], kineticEnergies: list[float] = [0.0]) -> float:
    # Convert parents to a list if it's not already
   if not isinstance(parents, list):
       parents = [parents]
   if not isinstance(kineticEnergies, list):
       kineticEnergies = [kineticEnergies] * len(parents)

    def sumMass(particles):
        return sum(p.mass for p, ke in zip(particles, kineticEnergies) if p.mass is not None)

    before = sumMass(parents, kineticEnergies)
    after = sumMass(daughters, [0.0] * len(daughters))

    return before-after


def calcRelativisticEnergyMass(parents, daughters, kineticEnergies: list[float] = [0.0]):
    if not isinstance(parents, list):
        parents = [parents]
    if not isinstance(kineticEnergies, list):
        kineticEnergies = [kineticEnergies] * len(parents)

    def sumRelativisticEnergy(particles, kineticEnergies):
        c = 299792458  # Speed of light in meters per second
        return sum(p.mass * c**2 + ke for p, ke in zip(particles, kineticEnergies) if p.mass is not None)

    before = sumRelativisticEnergy(parents, kineticEnergies)
    after = sumRelativisticEnergy(daughters, [0.0] * len(daughters))

    return before - after
"""

def checkDecay(parents: list[Particle], daughters: list[Particle]) -> ConservationCheckResult:
    checks = {
        'Charge Conservation': chargeConversation(parents, daughters),
        'Isospin Conservation': isoSpinConservation(parents, daughters),
        'Baryon Number Conservation': baryonNumberConservation(parents, daughters),
        'Lepton Number Conservation': leptonNumberConservation(parents, daughters)
    }

    isPermited = all(result[0] for result in checks.values())
    reasons = [name for name, result in checks.items() if not result[0]]

    reason = ', '.join(reasons) + (' is/are violated.' if reasons else '')

    return ConservationCheckResult(isPermited=isPermited, reason=reason)
