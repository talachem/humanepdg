# Introduction

CERN mostly certainly had its impact on high energy physics. While much of this has been regrettable.
This library tries to fix one of those, by translating PDG codes into a human readable format.
And it can convert it backwards, with fuzzy terms and alternative names.


## Alternatives

There is the pdg Python library build by the pdg group. I will not link to it.
I whole heartedly recommend [Particle](https://pypi.org/project/particle/) and [ParticleTools](https://pypi.org/project/particletools/).
They nearly do every thing one could wish for, also both are more user friendly
than pdgs in-house ... I don't wanna call it a solution.


## Why this tool then?

I wanted something simpler and rather specific, that I can use directly inside my work.
Still I highly recommend [Particle](https://pypi.org/project/particle/) and [ParticleTools](https://pypi.org/project/particletools/).
I used these to build my own database. Additionally I found three sources from the PDG group.
Additionally I supplemented this data then with data from Wikipedia.
After sifting through everything, I bundled it together into one database.


## How to use this tool?

I had a bit of different approach.
One can use a slew of functions to look up different properties of particles.
For that one can use either the Monte Carlo ID or the name written in several ways.
Then one gets back just the property, nothing else.
As I said, it is a simpler tool.
These functions are:
- getParticle: returns name or ID of a given particle
- getAntiParticle: returns the name or ID of the anti particle
- getDecayMode: returns the decay modes of a given particle
- getDecayWidth: returns the decay width of a given particle, optionally the error
- getMass: returns the mass of a given particle, optionally the error
- getLifetime: returns the life time of a given particle
- getCharge: returns the charge of a given particle
- getQuarks: returns the quark content of a given particle
- getSpin: returns the spin direction of a given particle
- getIsospin: returns the iso-spin of a given particle
- getParticleType: returns the type of a given particle (lepton, meson, ...)
- isLepton: wether a given particle is a lepton
- isBoson: wether a given particle is a boson
- isMeson: wether a given particle is a meson
- isBaryon: wether a given particle is a baryon
- getParity: returns the parity of a given particle
- getChargeConjungation: returns the charge conjugate of a given particle
- getTimeReversal: returns the time reversal of a given particle


These two very important functions can give you the whole list of all IDs and Names:
- listNames
- listIDs

All of these can be imported like:

```python
from humanePDG import getParticle
```


Additionally there is one class that can create a particle class:

```python
createParticle(particle)
```

Will create a class, containing all information.
The argument can be a variation of names or Monte Carlo IDs.


## Importing Classes

This is still iffy, but one can import particles directly from the library:

```python
from humanePDG.composite import PionPlus, Klong, Beauty, Duty
from humanePDG.elementary import Electron, ElectronNeutrino
```

or

```python
from humanePDG.composite import PionPlus, Klong, BMeson, DMeson
from humanePDG.elementary import Electron, ElectronNeutrino
```

Iffy here means, one has to look-up the names I used for implementing,
which is not ideal. I am looking into ways of broadening the range of
possible names.


## Sources

As for sources, I've used the already mentioned [Particle](https://pypi.org/project/particle/) and [ParticleTools](https://pypi.org/project/particletools/),
I used some json and some SQLite file from the PDG Group. Finally I supplemented
it all with Wikipedia:
- [Quarks](https://en.wikipedia.org/wiki/List_of_particles)
- [Quarks](https://en.wikipedia.org/wiki/Quark)
- [Leptons](https://en.wikipedia.org/wiki/List_of_particles)
- [Leptons](https://en.wikipedia.org/wiki/Lepton)
- [Bosons](https://en.wikipedia.org/wiki/List_of_particles)
- [Mesons](https://en.wikipedia.org/wiki/List_of_mesons)
- [Baryons](https://en.wikipedia.org/wiki/List_of_baryons)


## Installation

You will need to the [wheel](https://pypi.org/project/wheel/) and [setuptools](https://pypi.org/project/setuptools/) packages of python in order to install
Download the repo, navigate in the terminal to the folder and run the following script:

```bash
python3 setup.py sdist
```

and then:

```bash
pip3 install .
```
