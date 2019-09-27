# Paths of the tools to integrate.
BIOTOOLS_TOOLS =  False
BIOCONDA_TOOLS = False
BIOCONTUCTOR_TOOLS = False
GALAXY_TOOLS = False
GALAXY_XML_TOOLS = False

#if --skip_integration
TOOLS= "three_instances.json"

# Instances obtained from integration writen as json
INTEGRATION_OUT = True
# path where instances from integration will be saved if INTEGRATION_OUT == True.
INTEGRATED_TOOLS_PATH = "only.biotools/instances.json"

# Statistics and plots about metadata
STATS_CALC = False

# Metrics ans scores calculated
METRICS_CALC = True
METRICS_OUT = True
METRICS_OUT_PATH = 'only.biotools/metrics.json'

SCORES_CALC = True
SCORES_OUT = True
INSTANCES_SCORES_OUT_PATH = 'threeInstances/scores'
INSTANCES_SCORES_OUT_NAME = 'FAIRinst'
CANONICAL_SCORES_OUT_PATH = 'threeInstances/scores'
CANONICAL_SCORES_OUT_NAME = 'FAIRcanon'
