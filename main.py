import FI_FAIR as FI
import FI_FAIR_stats as FI_stats
import json
import sys
import argparse


if __name__ == '__main__':

    conffile = sys.argv[1]
    import importlib
    config = importlib.import_module(conffile)

    ######----------- Data restructuring and integration ------------------------------------##########

    allSets = []
    
    ## Importation of data and generation of "tool" instances with it. 

    # Bioconductor
    if config.BIOCONTUCTOR_TOOLS:
        bioconductor2000raw = FI.loadJSON(config.BIOCONTUCTOR_TOOLS)
        bioconductInts = FI.bioconductorToolsGenerator(bioconductor2000raw).instSet
        allSets.append(FI.bioconductorToolsGenerator(bioconductor2000raw).instSet)

    # bioconda
    if config.BIOCONDA_TOOLS:
        bioconda2000raw = FI.loadJSON(config.BIOCONDA_TOOLS)
        biocondaInts = FI.biocondaToolsGenerator(bioconda2000raw).instSet
        allSets.append(FI.biocondaToolsGenerator(bioconda2000raw).instSet)

    # biotools
    if config.BIOTOOLS_TOOLS:
        biotools2000raw = FI.loadJSON(config.BIOTOOLS_TOOLS)
        biotoInts = FI.biotoolsToolsGenerator(biotools2000raw).instSet
        allSets.append(FI.biotoolsToolsGenerator(biotools2000raw).instSet)

    # galaxyConfig
    if config.GALAXY_XML_TOOLS:
        shedXML2000raw = FI.loadJSON(config.GALAXY_XML_TOOLS)
        shedXMLInts = FI.galaxyConfigToolsGenerator(shedXML2000raw).instSet
        allSets.append(FI.galaxyConfigToolsGenerator(shedXML2000raw).instSet)

    # galaxy
    if config.GALAXY_TOOLS:
        shed2000raw = FI.loadJSON(config.GALAXY_TOOLS)
        shedInts = FI.galaxyShedToolsGenerator(shed2000raw).instSet
        allSets.append(FI.galaxyShedToolsGenerator(shed2000raw).instSet)
     

    ## Integration of "tool" instances of same ID (name, version, type)

    mergedSet = FI.integrateInstances(allSets)
    canonicalMerged = FI.generateCanonicalSet(mergedSet)

    instances = [canon.instances for canon in canonicalMerged.canonicals] # [[],[],[]]
    instances = [item for sublist in instances for item in sublist]
    instToWrite = [ vars(item) for item in instances]

    ## Exportation of integrated tools to file
    ## TODO: exportation to DB. 
    if config.INTEGRATION_OUT == True:
        with open(config.INTEGRATED_TOOLS_PATH, 'w') as outfile:
            json.dump(instToWrite, outfile)



    ######-------------- Exploration of data: statistics and plots -------------------------------------------------########

    if config.STATS_CALC == True:

        # WRITTING REPORTS
        # Features per source
        S = [instances, biotoInts.instances, biocondaInts.instances, bioconductInts.instances,shedInts.instances, shedXMLInts.instances]
        FI_stats.repFeatsPerSource(instances, 'stats/features.txt', S)
        FI_stats.featuresBarPlot(FI_stats.dfFeatures('stats/features.txt'), 'images/featuresBarPlot.png')

        # Sources per instance
        FI_stats.repSourcesPerInstance(instances, 'stats/sources.txt')
        FI_stats.nSourcesBarPlot(FI_stats.dfNSources('stats/sources.txt'), 'images/sourcesBarPlot.png')
        FI_stats.pie( FI_stats.dfNSources('stats/sources.txt'), 'images/sourcesPerInstPie.png')

        #Types per canonical
        FI_stats.repTypesPerCanon(instances, 'stats/typesPerCanon.txt', canonicalMerged )

        #Frequency of types in instances
        FI_stats.typesInInstances(instances, 'stats/typesInInstances.txt')
        d = FI_stats.dfTypes('stats/typesInInstances.txt')
        FI_stats.pieF(d, 'images/typesInInstPie.png')
        FI_stats.typesBarPlot(d, 'images/typesBarPlot.png', (5, 7))

        #Features in canonicals
        FI_stats.featuresInCanonicals(instances, 'stats/featsCanon.txt', canonicalMerged)

        #Number of versions in canonicals
        FI_stats.versionsCanon(instances, 'stats/versionsCanon.txt', canonicalMerged)

        #Types of versions in instances
        FI_stats.typesVersions(instances, 'stats/typesVersions.txt')
        FI_stats.pieF(FI_stats.dfTypes('stats/typesVersions.txt'), 'images/typeVerSPie.png')

        #Types of licenses
        FI_stats.typesLicenses(instances, 'stats/typesLicenses.txt')
        d = FI_stats.dfTypes('stats/typesLicenses.txt')
        FI_stats.pieF(d, 'images/typeLicPie.png')
        FI_stats.typesBarPlot(d, 'images/typeLicBarPlot.pdf', (5, 6))

        # Different licenses per canon
        FI_stats.diffLicenses(instances, 'stats/diffLicenses.txt', canonicalMerged)

        # Operating systems
        FI_stats.repOSystems(instances, 'stats/OStypes.txt', 'stats/OSfreqs.txt')
        FI_stats.pieF(FI_stats.dfTypes('stats/OStypes.txt'), 'images/OStypes.png')
        FI_stats.nSourcesBarPlot(FI_stats.dfTypes('stats/OSfreqs.txt'), 'images/OSfreqs.pdf')

        # input/output data formats
        FI_stats.repDataformats(instances, 'stats/inputExistenceOfFormats.txt', 'stats/inputFreqsFormats.txt')
        FI_stats.pieF(FI_stats.dfTypes('stats/inputExistenceOfFormats.txt'), 'images/inputExistenceOfFormats.png')
        df = FI_stats.dfTypes('stats/inputFreqsFormats.txt')
        FI_stats.typesBarPlot(df, 'images/inputFreqsFormats.png', (6, 15))


 ##### ---------------- FAIRness calculation---------------------------------------------------#########################

    if config.METRICS_CALC == True:
        # instances FAIRness
        FI.prepFAIRcomp(instances)
        print("Preapared for FAIRsoft measurement")
        print("Calculating instances FAIRsoft metrics and scores ...")
        outnameInst = config.INSTANCES_SCORES_OUT_PATH + config.INSTANCES_SCORES_OUT_NAME + '.txt'
        FI_stats.computeFAIRinsts(canonicalMerged, outnameInst, config.METRICS_OUT, config.SCORES_CALC, config.METRICS_OUT_PATH)
        print("Instances FAIRsoft metrics and scores obtained")
        FI_stats.FAIRviolinPlot(outnameInst, config.INSTANCES_SCORES_OUT_PATH + '/FAIRinsts.png')

    if config.SCORES_CALC == True:
        # canonicals FAIRness
        print("Calculating canonical tools FAIRsoft metrics and scores ...")
        outnameCan = config.CANONICAL_SCORES_OUT_PATH + config.CANONICAL_SCORES_OUT_NAME + '.txt'
        FI_stats.computeFAIRcanon(canonicalMerged, outnameCan )
        print("Instances FAIRsoft metrics and scores obtained")
        FI_stats.FAIRviolinPlot(outnameCan, config.CANONICAL_SCORES_OUT_PATH + '/FAIRcanon.png')
