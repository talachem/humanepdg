import json
from importlib_resources import files, as_file


def loadData(fileName):
    source = files('humanePDG.data').joinpath(fileName)
    with as_file(source) as f:
        with open(f, 'r') as jsonFile:
            return json.load(jsonFile)


elementaryData = loadData('elementary.json')
compositeData = loadData('composite.json')
namesData = loadData('namesToIDs.json')
pdgNamesData = loadData('pdgNameToIDs.json')
programmNamesData = loadData('programmToIDs.json')
codeData = loadData('codesToIDs.json')
symbolsData = loadData('symbolsToIDs.json')


__all__ = ['elementaryData', 'compositeData', 'namesData', 'pdgNamesData', 'programmNamesData', 'codeData', 'symbolsData']
