import FI_FAIR as FI
import FI_FAIR_stats as FI_stats
import json



if __name__ == '__main__':

    # Bioconductor
    bioconductor2000raw = FI.loadJSON('bioconductor2000.json')
    bioconductInts = FI.bioconductorToolsGenerator(bioconductor2000raw).instSet
    # bioconda
    bioconda2000raw = FI.loadJSON('bioconda2000.json')
    biocondaInts = FI.biocondaToolsGenerator(bioconda2000raw).instSet
    # biotools
    biotools2000raw = FI.loadJSON('biotools2000.json')
    biotoInts = FI.biotoolsToolsGenerator(biotools2000raw).instSet
    # galaxyConfig
    shedXML2000raw = FI.loadJSON('shedXML2000.json')
    shedXMLInts = FI.galaxyConfigToolsGenerator(shedXML2000raw).instSet
    # galaxyConfig
    shed2000raw = FI.loadJSON('shed2000.json')
    shedInts = FI.galaxyShedToolsGenerator(shed2000raw).instSet

    allSets = [bioconductInts, biocondaInts, biotoInts, shedXMLInts, shedInts]
    mergedSet = FI.integrateInstances(allSets)
    canonicalMerged = FI.generateCanonicalSet(mergedSet)

    instances = [canon.instances for canon in canonicalMerged.canonicals] # [[],[],[]]
    instances = [item for sublist in instances for item in sublist]

    #print([inst.input for inst in instances])


##################---------------------------- STATISTICS --------------------------------------###########################

# WRITTING REPORTS
# Features per source
S = [instances, biotoInts.instances, biocondaInts.instances, bioconductInts.instances,shedInts.instances, shedXMLInts.instances]
FI_stats.repFeatsPerSource(instances, 'stats/features.txt', S)
FI_stats.featuresBarPlot(FI_stats.dfFeatures('stats/features.txt'), 'images/featuresBarPlot.pdf')

# Sources per instance
FI_stats.repSourcesPerInstance(instances, 'stats/sources.txt')
FI_stats.nSourcesBarPlot(FI_stats.dfNSources('stats/sources.txt'), 'images/sourcesBarPlot.pdf')
FI_stats.pie( FI_stats.dfNSources('stats/sources.txt'), 'images/sourcesPerInstPie.pdf')

#Types per canonical
FI_stats.repTypesPerCanon(instances, 'stats/typesPerCanon.txt', canonicalMerged )

#Frequency of types in instances
FI_stats.typesInInstances(instances, 'stats/typesInInstances.txt')
d = FI_stats.dfTypes('stats/typesInInstances.txt')
FI_stats.pie(d, 'images/typesInInstPie.pdf')
FI_stats.typesBarPlot(d, 'images/typesBarPlot.pdf')

#Features in canonicals
FI_stats.featuresInCanonicals(instances, 'stats/featsCanon.txt', canonicalMerged)

#Number of versions in canonicals
FI_stats.versionsCanon(instances, 'stats/versionsCanon.txt', canonicalMerged)

#Types of versions in instances
FI_stats.typesVersions(instances, 'stats/typesVersions.txt')
FI_stats.pie(FI_stats.dfTypes('stats/typesVersions.txt'), 'images/typeVerSPie.pdf')

#Types of licenses
FI_stats.typesLicenses(instances, 'stats/typesLicenses.txt')
d = FI_stats.dfTypes('stats/typesLicenses.txt')
FI_stats.pie(d, 'images/typeLicPie.pdf')
FI_stats.typesBarPlot(d, 'images/typeLicBarPlot.pdf')

# Different licenses per canon
FI_stats.diffLicenses(instances, 'stats/diffLicenses.txt', canonicalMerged)

# Operating systems



# -------------------------------------------------- FAIRness ---------------------------------------#########################
# instances FAIRness
FI.prepFAIRcomp(instances)
FI_stats.computeFAIRinsts(instances, 'scores/FAIRinsts.txt')
FI_stats.FAIRviolinPlot('scores/FAIRinsts.txt', 'images/FAIRinsts.pdf')

# canonicals FAIRness
FI_stats.computeFAIRcanon(canonicalMerged, 'scores/FAIRcanon.txt')
FI_stats.FAIRviolinPlot('scores/FAIRcanon.txt', 'images/FAIRcanon.pdf')
