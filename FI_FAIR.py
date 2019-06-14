import json

with open('bioconductor2000.json') as fp:
    raw2000 = json.load(fp)

class instance(object):

    def __init__(self, name, type_, version):
        self.name = name
        self.description = None # string
        self.version = version
        self.type = type_
        self.links =[]
        self.publication =  0 # number of related publications [by now, for simplicity]
        self.download = []  # list of lists: [[type, url], [], ...]
        self.inst_instr = False # boolean // FUTURE: uri or text
        self.test = False # boolean // FUTURE: uri or text
        self.src = [] # string
        self.os = [] # list of strings
        self.input = [] # list of dictionaries biotools-like {'format' : <format> , 'uri' : <uri> , 'data' : <data> , 'uri': <uri>}
        self.output = [] # list of dictionaries biotools-like {'format' : <format> , 'uri' : <uri> }
        self.dependencies = [] # list of strings
        self.documentation = [] # list of lists [[type, url], [type, rul], ...]
        self.license = False # string
        self.termsUse = False #
        self.contribPolicy = False
        self.authors = [] # list of strings
        self.repository = []
        self.description = False
        self.source = [] #string


    ##============ Findability metrics computation functions ================

    def compF1_2(self):
        '''
        a version of the form X.X is considered acceptable: True
        anything else is False
        '''
        if self.version != None:
            if len(self.version.split('.'))==2:
                return(True)
            else:
                return(False)
        return(False)

    global struct_meta

    struct_meta = ['biotools', 'bioconda', 'bioconductor', 'galaxyShed', 'galaxyConfig']
    def compF2_1(self):
        '''
        The sources in struct_meta are structured. If these sources are among self.source: True.
        Otherwise: False
        '''
        if True in [a in struct_meta for a in self.source]:
            return(True)
        else:
            return(False)

    global softReg
    softReg = ['biotools', 'bioconda', 'bioconductor']
    def compF3_1(self):
        '''
        If the source is among the software registries: True
        Otherwise: Falsecource
        '''
        if True in [a in softReg for a in self.source]:
            return(True)
        else:
            return(False)

    def compF3_2(self):
        '''
        If the instance has an associated repository uri: True
        Otherwise: False
        '''
        if len(self.repository)>0:
            return(True)
        else:
            return(False)

    def compF3_3(self):
        '''
        If the instance at least one associated publication: True
        Otherwise: False
        '''
        if self.publication>0:
            return(True)
        else:
            return(False)

    ##============== Accessibility metrics computation functions ================

    global webTypes
    webTypes = ['app', 'web', 'app', 'api', 'soap']
    def compA1_1(self):
        '''
        BY TYPE
        For web types this metrics is always True.
        For the rest, it is False.
        CHECK if url works!!!
        '''
        if self.type in webTypes:
            return(True)
        else:
            return(False)

    def compA1_2(self):
        '''
        BY TYPE
        If there is a download link: True ## we do not check if it is available
        or anything else.
        '''
        if self.type not in webTypes:
            if len(self.download)>0:
                return(True)
            else:
                return(False)
        else:
            return(False)

    def compA1_3(self):
        '''
        We check self.inst_instructions (already a boolean)
        '''
        if self.type not in webTypes:
            return(self.inst_instr)



    def compA1_4(self):
        '''
        We check self.test (already a boolean)
        '''
        return(self.test)

    def compA1_5(self):
        '''
        '''
        if len(self.src)>0:
            return(True)
        else:
            return(False)


    def compA3_1(self):
        '''
        '''
        import urllib.request
        status = []
        for url in self.download + self.links:

            if len(url)>0:
                if 'http:' in url[1]:
                    try:
                        re = urllib.request.urlopen(url[1])
                    except:
                        continue
                    else:
                        #print(re.status_code)
                        status.append(re.status)
                elif 'ftp:' in url[1]:
                    #print(url[1])
                    try:
                        a, b=urllib.request.urlretrieve(url[1], r'%s'%(url[1].split('/')[-1]))
                    except:
                        continue
                    else:
                        #print(re.status_code)
                        status.append(200)
        if 200 in status:
            #print('here')
            return(True)
        else:
            return(False)

    def compA3_2(self):
        if 'Linux' in self.os:
            return(True)
        else:
            return(False)

    def compA3_3(self):
        if len(self.os)>1:
            return(True)
        else:
            return(False)

    def compA3_4(self):
        '''
        We are only considering galaxy servers and vre
        '''
        eInfra = ['vre.multiscalegenomics.eu', 'galaxy.', 'usegalaxy.']
        for url in self.links:
            if True in  [a in url for a in eInfra]:
                return(True)
            else:
                return(False)
        return(False)


    def compA3_5(self):
        eInfra = ['vre.multiscalegenomics.eu', 'galaxy.', 'usegalaxy.']
        count = 0
        for url in self.links:
            if True in  [a in url for a in eInfra]:
                count += 1
        if count>1:
            return(True)

        return(False)

    ##============== Anteroperability metrics computation functions ================
    def compI1_1(self):
        for i in self.input:
            if 'format' in i.keys():
                if i['format']['term'] in stdFormats:
                    return(True)

        for i in self.output:
            if 'format' in i.keys():
                if i['format']['term'] in stdFormats:
                    return(True)

        return(False)

    def compI1_3(self):
        for i in self.input:
            if 'format' in i.keys():
                if 'biojason' in i['format']['term']:
                    return(True)

        for i in self.output:
            if 'format' in i.keys():
                if 'biojason' in i['format']['term']:
                    return(True)


        return(False)


    def compI1_4(self):
        ins = []
        for i in self.input:
            if 'format' in i.keys():
                ins.append(i['format']['term'])
        for i in self.output:
            if 'format' in i.keys():
                ins.append(i['format']['term'])

        if len(ins)>1:
            return(True)
        else:
            return(False)

    #def compI1_5(self):
    def compI2_1(self):
        interTypes = ['library', 'API']
        if self.type in interTypes:
            return(True)
        else:
            return(False)


    def compI2_2(self):
        if 'galaxyConfig' in self.source or 'galaxyShed' in self.source:
            return(True)

        elif len([a[1] for a in self.links if 'galaxy' in a]):
            return(True)

        else:
            return(False)

    def compI3_1(self):
        if len(self.dependencies)>0:
            return(True)
        else:
            return(False)

    def compI3_2(self):
        if 'galaxyShed' in self.source:
            return(True)
        elif 'bioconda' in self.source:
            return(True)
        elif 'bioconductor' in self.source:
            return(True)
        else:
            return(False)

    def compR1_1(self):
        noGuide = ['NEWS', 'LICENSE', 'Terms of use']
        for doc in self.documentation:
            if doc[0] not in noGuide:
                return(True)

        return(False)


    def compR2_1(self):
        for doc in self.documentation:
            if doc[0] == 'Terms of use':
                return(True)
        if len(self.license)>0:
            return(False)
        return(False)

    def compR2_2(self):
        for doc in self.documentation:
            if doc[0].lower() == 'conditions of use':
                return(True)
        return(False)

    #def compR3_1(self):
    def compR3_2(self):
        if len(self.authors)>0:
            return(True)
        else:
            return(False)

    def compR4_1(self):
        for repo in self.repository:
            if 'github' in repo or 'mercurial-scm' in repo:
                return(True)
        return(False)



    def FAIRscores(self):
        self.F = 0
        self.F += (0.8*self.metrics.F1_1 + 0.2*self.metrics.F1_2)*0.4
        self.F += self.metrics.F2_1*0.2

        acc = [self.metrics.F3_1, self.metrics.F3_2, self.metrics.F3_3].count(True)
        if acc == 1:
            self.F += 0.7*0.4
        elif acc == 2:
            self.F += 0.85*0.4
        elif acc == 3:
            self.F += 1*0.4

        self.A = 0
        if self.type in webTypes:
            self.A += (self.metrics.A1_1*0.6 + self.metrics.A1_4*0.4)*0.7
            self.A += self.metrics.A3_1*0.3
        else:
            self.A += (self.metrics.A1_2*0.5 + self.metrics.A1_3*0.2 + self.metrics.A1_4*0.1 + self.metrics.A1_5*0.2)*0.7
            self.A += (self.metrics.A3_1+self.metrics.A3_2+self.metrics.A3_3+self.metrics.A3_4+self.metrics.A3_5)*(1/5)*0.3
        #self.A += (self.metrics.A2_1*(1/3)+self.metrics.A2_2*(2/3))*0.15

        self.I = 0
        self.I += (self.metrics.I1_1*0.5+self.metrics.I1_2*0.3+self.metrics.I1_3*0.3+self.metrics.I1_4*0.2)*0.6
        self.I += (self.metrics.I2_1*0.5+self.metrics.I2_2*0.5)*0.5
        self.I += (self.metrics.I3_1+self.metrics.I3_2+self.metrics.I3_3)*(1/3)*(0.3)

        self.R = 0
        self.R += self.metrics.I1_1*0.3
        if self.metrics.R2_1:
            self.R += 0.3
        elif self.metrics.R2_2:
            self.R += 0.3
        self.R += self.metrics.R3_2*0.2
        self.R += self.metrics.R4_1*0.2



    def generateFAIRMetrics(self):
        # FINDABILITY
        self.metrics = FAIRmetrics()

        self.metrics.F1_1 = True # all have a name
        self.metrics.F1_2 = self.compF1_2() #
        self.metrics.F2_1 = self.compF2_1()
        self.metrics.F2_2 = True # by now, not accepted metadata standard known

        self.metrics.F3_1 = self.compF3_1()
        self.metrics.F3_2 = self.compF3_2()
        self.metrics.F3_3 = self.compF3_3()
        # ACCESIBILITY
        self.metrics.A1_1 = self.compA1_1()
        self.metrics.A1_2 = self.compA1_2()
        self.metrics.A1_3 = self.compA1_3()
        self.metrics.A1_4 = self.compA1_4()
        self.metrics.A1_5 = self.compA1_5()

        self.metrics.A2_1 = False
        self.metrics.A2_2 = False

        self.metrics.A3_1 = self.compA3_1()
        self.metrics.A3_2 = self.compA3_2()
        self.metrics.A3_3 = self.compA3_3()
        self.metrics.A3_4 = self.compA3_4()
        self.metrics.A3_5 = self.compA3_4()

        self.metrics.I1_1 = self.compI1_1()  # TO DO
        self.metrics.I1_2 = False # NOT FOR NOW
        self.metrics.I1_3 = self.compI1_3()
        self.metrics.I1_4 = self.compI1_4()
        self.metrics.I1_5 = False # NOT FOR NOW

        self.metrics.I2_1 = self.compI2_1()
        self.metrics.I2_2 = self.compI2_2()

        self.metrics.I3_1 = self.compI3_1()
        self.metrics.I3_2 = self.compI3_2()
        self.metrics.I3_3 = self.compI3_2() # Same as befor, BY NOW

        self.metrics.R1_1 = self.compR1_1()
        self.metrics.R1_2 = False #NOT FOR NOW

        self.metrics.R2_1 = self.compR2_1()
        self.metrics.R2_2 = self.compR2_2()

        self.metrics.R3_1 = False # Not for now
        self.metrics.R3_2 = self.compR3_2()

        self.metrics.R4_1 = self.compR4_1()
        self.metrics.R4_2 = False # By now
        self.metrics.R4_3 = False # By now


class FAIRmetrics(object):

    def __init__(self):
        self.F1_1 = [] # uniqueness of name
        self.F1_2 = [] # idenfibiability of version

        self.F2_1 = [] # structured metadata
        self.F2_2 = [] # standarized metadata

        self.F3_1 = [] # searchability in registries
        self.F3_2 = [] # searchability in software repositories
        self.F3_3 = [] # searchability in literature

        self.A1_1 = []
        self.A1_2 = []
        self.A1_3 = []
        self.A1_4 = []
        self.A1_5 = []

        self.A2_1 = []
        self.A2_2 = []

        self.A3_1 = []
        self.A3_2 = []
        self.A3_3 = []
        self.A3_4 = []
        self.A3_5 = []

        self.I1_1 = []
        self.I1_2 = []
        self.I1_3 = []
        self.I1_4 = []
        self.I1_5 = []

        self.I2_1 = []
        self.I2_2 = []

        self.I3_1 = []
        self.I3_2 = []
        self.I3_3 = []

        self.R1_1 = []
        self.R1_2 = []

        self.R2_1 = []
        self.R2_2 = []

        self.R3_1 = []
        self.R3_2 = []

        self.R4_1 = []
        self.R4_2 = []
        self.R4_3 = []




class canonicalSet(object):

    def __init__(self):
        self.canonicals = []

    def addCanononical(self, canon):
        self.canonicals.append(canon)


class canonicalTool(object):

    def __init__(self, name, instances, sources, types):
        self.name = name
        self.instances = instances
        self.sources = sources
        self.types = types

    def computeFAIRmetrics(self):
        self.F = max([ins.F for ins in self.instances])
        self.A = max([ins.A for ins in self.instances])
        self.I = max([ins.I for ins in self.instances])
        self.R = max([ins.R for ins in self.instances])



class setOfInstances(object):

    def __init__(self, source):
        self.source = source
        self.instances = []



class toolGenerator(object):
    def __init__(self, tools, source):
        self.tools = tools
        self.source = source

def cleanVersion(version):
    if version != None:
        if '.' in version:
            #print(version.split('.')[0]+'.'+ version.split('.')[1])
            return(version.split('.')[0]+'.'+ version.split('.')[1])
        else:
            return(version)
    else:
        return(version)

class biocondaToolsGenerator(toolGenerator):
    def __init__(self, tools, source = 'bioconda'):
        toolGenerator.__init__(self, tools, source)

        self.instSet = setOfInstances('bioconda')

        names = [a['name'].lower() for a in self.tools]
        #print('diferent names in bioconda tools: ' + str(len(set(names))))

        for tool in self.tools:
            vers = []
            name = tool['name'].lower()
            version = cleanVersion(tool['@version'])
            type_ = 'Command-line tool' # all biocondas are cmd

            newInst = instance(name, type_, version)
            if 'description' in tool.keys():
                newInst.description = tool['description'] # string
            if tool['web']['homepage']:
                newInst.links = [tool['web']['homepage']] #list
            else:
                newInst.links = []
            newInst.publication =  len(tool['publications']) # number of related publications [by now, for simplicity]
            newInst.download = [ [ down ,tool['distributions'][down] ] for down in tool['distributions'].keys()  ]  #

            newSrc = []
            for down in tool['distributions'].keys():
                if 'source' in down:
                    if len(tool['distributions'][down])>0:
                        for u in tool['distributions'][down]:
                            newSrc.append(u)
            newInst.src = newSrc # string

            if 'license' in tool.keys() and tool['license']!='':
                newInst.license = tool['license'] # string
            newInst.repository = tool['repositories']
            newInst.source = ['bioconda']

            self.instSet.instances.append(newInst)



class bioconductorToolsGenerator(toolGenerator):
    def __init__(self, tools, source='bioconductor'):
        toolGenerator.__init__(self, tools, source)

        self.instSet = setOfInstances('bioconductor')

        for tool in self.tools:
            type= 'Library'
            version = cleanVersion(tool['Version'])
            name = tool['name'].lower()
            newInst = instance(name, type, version)
            newInst.description = tool['description'] # string
            if tool['URL']:
                newInst.links = [tool['URL']]
            else:
                newInst.links = []
            newInst.publication =  int(tool['citation']) # number of related publications [by now, for simplicity]
            download = []
            for a in ["Windows Binary", "Source Package", "Mac OS X 10 10.11 (El Capitan)"]:
                if a in tool.keys() and tool[a]:
                    download.append([a, tool['Package Short Url'] + tool[a]])

            newInst.download = download
            newInst.inst_instr = tool['Installation instructions'] #
            newInst.src = [ a for a in newInst.download if a[0] == "Source Package"[0] ]# string
            newInst.os = ['Linux', 'Mac', 'Windows'] # list of strings
            if tool['Depends']:
                deps = tool['Depends'].split(',')
            else:
                deps = []
            if tool['Imports']:
                impo = tool['Imports'].split(',')
            else:
                impo = []

            newInst.dependencies = [item for sublist in [deps+impo] for item in sublist] # list of strings

            newInst.documentation = [[ a, a[0] ] for a in tool['documentation']] # list of lists [[type, url], [type, rul], ...]
            if tool['License']!='':
                newInst.license = tool['License'] # string
            else:
                newInst.license = False
            newInst.authors = [a.lstrip() for a in tool['authors']] # list of strings
            newInst.repository = [tool['Source Repository'].split('gitclone')[1]]
            newInst.description = tool['description']
            newInst.source = ['bioconductor'] #string

            self.instSet.instances.append(newInst)


def constrFormatsConfig(formatList):
    '''
    From an input that is a str to a biotools kind of format
    '''
    notFormats = ['data']
    newFormats = []
    seenForms = []
    for formt in formatList:
        if formt not in seenForms:
            if ',' in formt:
                formats = formt.split(',')
                for f in formats:
                    if f not in notFormats:
                        newFormats.append({ 'format' : {'term' : f , 'uri' :  None }})
                        seenForms.append(formt)
            else:
                if formt not in notFormats:
                    newFormats.append({ 'format' :  {'term' : formt , 'uri' :  None }})
                    seenForms.append(formt)
        else:
            continue
    return(newFormats)


class galaxyConfigToolsGenerator(toolGenerator):
    def __init__(self, tools, source = 'galaxyConfig'):
        toolGenerator.__init__(self, tools, source)

        self.instSet = setOfInstances('galaxyConfig')

        for tool in self.tools:
            name = tool['name'].lower()

            type_ = 'Command-line tool'

            version = cleanVersion(tool['version'])

            newInst = instance(name, type_, version)

            newInst.description = tool['description'] # string

            if tool['ciation']:
                newInst.publication =  len(tool['ciation']) # number of related publications [by now, for simplicity]

            newInst.test = tool['tests'] # boolean

            if len(tool['dataFormats']['inputs'])>0:
                newInst.input = constrFormatsConfig(tool['dataFormats']['inputs']) # list of strings

            if len(tool['dataFormats']['outputs'])>0:
                newInst.output = constrFormatsConfig(tool['dataFormats']['outputs']) # list of strings

            docu = []
            if tool['readme'] == True:
                docu.append(['readme', None])
            if tool['help']:
                docu.append(['help', tool['help'].lstrip()])

            newInst.documentation = docu # list of lists [[type, url], [type, rul], ...]

            newInst.source = ['galaxyConfig'] #string

            self.instSet.instances.append(newInst)



class galaxyShedToolsGenerator(toolGenerator):
    def __init__(self, tools, source = 'galaxyShed'):
        toolGenerator.__init__(self, tools, source)

        self.instSet = setOfInstances('galaxyShed')

        for tool in self.tools:
            name = tool['name'].lower()
            type = 'Command-line tool'
            version = cleanVersion(tool['version'])

            newInst = instance(name, type, version)

            newInst.description = tool['description'] # string
            newInst.inst_instr = True # Since this is installable through ToolShed
            if len(tool['tests'])>0:
                newInst.test = True # boolean
            else:
                newInst.test = False

            newInst.dependencies = [a['name'] for a in tool['requirements']] # list of strings
            newInst.repository = [] ### FILL!!!!!!!!!!!
            newInst.links = [] ### FILL!!!!!!!!!!!!
            newInst.source = ['galaxyShed']#string

            self.instSet.instances.append(newInst)


def lowerInputs(listInputs):
    newList = []
    if len(listInputs)>0:
        for format in listInputs:
            newFormat = {}
            for a in format.keys():
                newInner = {}
                if format[a] != []:
                    #print(format[a])
                    if type(format[a]) == list:
                        for eachdict in format[a]:
                            for e in eachdict.keys():
                                newInner[e] = eachdict[e].lower()
                            newFormat[a] = newInner
                    else:
                        for e in format[a].keys():
                            newInner[e] = format[a][e].lower()
                        newFormat[a] = newInner
        newList.append(newFormat)
    else:
        return([])
    return(newList)



class biotoolsToolsGenerator(toolGenerator):

    def __init__(self, tools, source = 'biotools'):

        toolGenerator.__init__(self, tools, source)

        self.splitInstances()


    def splitInstances(self):
        '''
        newInst.splitInstances returns the set of instances
        '''
        self.instSet = setOfInstances('biotools')
        names = [a['biotoolsID'].lower for a in self.tools]
        #print('diferent names in biotools tools: ' + str(len(set(names))))
        #print('diferent insatances in biotools tools: ' + len(names))
        for tool in self.tools:
            if len(tool['toolType']) > 0:
                for type_ in tool['toolType']:
                    vers = []
                    if len(tool['version']) > 0:
                        for version in tool['version']:

                            name = tool['biotoolsID'].lower()

                            newInst = instance(name, type_, cleanVersion(version))

                            newInst.description = tool['description']

                            newInst.homepage = tool['homepage']

                            newInst.publication = len(tool['publication'])

                            newInst.download = [ [tol['type'], tol['url']] for tol in tool['download'] ]

                            src = []
                            for down in [a for a in tool['download'] if a['type'] == 'Source package']:
                                src.append(down['url'])
                            newInst.src =src

                            newInst.os = tool['operatingSystem']

                            inputs = []
                            if len(tool['function'])>0:
                                inputs = [f['input'] for f in tool['function']]
                                newInst.input = lowerInputs(inputs[0])
                            else:
                                newInst.input = []

                            outputs = []
                            if len(tool['function'])>0:
                                outputs = [f['input'] for f in tool['function']]
                                newInst.output = lowerInputs(outputs[0])
                            else:
                                newInst.output = []



                            newInst.documentation = [ [doc['type'], doc['url']] for doc in tool['documentation']]

                            if 'Manual' in [ doc[0] for doc in newInst.documentation ]:
                                newInst.inst_instr = True

                            newInst.license = tool['license']

                            newAuth = []
                            for dic in tool['credit']:
                                if dic['name'] not in newAuth and dic['name']!=None:
                                    newAuth.append(dic['name'])
                            newInst.authors = newAuth

                            repos = []
                            for link in tool['link']:
                                if link['type'] == "Repository":
                                    repos.append(link['url'])
                            newInst.repository = repos

                            newInst.description = tool['description']

                            newInst.source = ['biotools']

                            self.instSet.instances.append(newInst)


                    else:
                        version = None
                        name = tool['biotoolsID'].lower()
                        newInst = instance(name, type_, cleanVersion(version))

                        newInst.description = tool['description']

                        newInst.homepage = tool['homepage']

                        newInst.publication = len(tool['publication'])

                        newInst.download = [ [tol['type'], tol['url']] for tol in tool['download'] ]

                        src = []
                        for down in [a for a in tool['download'] if a['type'] == 'Source package']:
                            src.append(down['url'])
                        newInst.src =src

                        newInst.os = tool['operatingSystem']

                        inputs = []
                        inputs = [f['input'] for f in tool['function']]
                        if len(tool['function'])>0:
                            inputs = [f['input'] for f in tool['function']]
                            newInst.input = lowerInputs(inputs[0])
                        else:
                            newInst.input = []

                        outputs = []
                        if len(tool['function'])>0:
                            outputs = [f['input'] for f in tool['function']]
                            newInst.output = lowerInputs(outputs[0])
                        else:
                            newInst.output = []

                        newInst.documentation = [ [doc['type'], doc['url']] for doc in tool['documentation']]

                        if 'Manual' in [ doc[0] for doc in newInst.documentation ]:
                            newInst.inst_instr = True

                        newInst.license = tool['license']

                        newAuth = []
                        for dic in tool['credit']:
                            if dic['name'] not in newAuth and dic['name']!=None:
                                newAuth.append(dic['name'])
                        newInst.authors = newAuth

                        repos = []
                        for link in tool['link']:
                            if link['type'] == "Repository":
                                repos.append(link['url'])
                        newInst.repository = repos

                        newInst.description = tool['description']

                        newInst.source = ['biotools']

                        self.instSet.instances.append(newInst)

            else:
                type_ = None
                if len(tool['version']) > 0:
                    for version in tool['version']:

                        name = tool['biotoolsID'].lower()
                        newInst = instance(name, type_, cleanVersion(version))

                        newInst.description = tool['description']

                        newInst.homepage = tool['homepage']

                        newInst.publication = len(tool['publication'])

                        newInst.download = [ [tol['type'], tol['url']] for tol in tool['download'] ]

                        src = []
                        for down in [a for a in tool['download'] if a['type'] == 'Source package']:
                            src.append(down['url'])
                        newInst.src =src

                        newInst.os = tool['operatingSystem']

                        inputs = []
                        if len(tool['function'])>0:
                            inputs = [f['input'] for f in tool['function']]
                            newInst.input = lowerInputs(inputs[0])
                        else:
                            newInst.input = []

                        outputs = []
                        if len(tool['function'])>0:
                            outputs = [f['input'] for f in tool['function']]
                            newInst.output = lowerInputs(outputs[0])
                        else:
                            newInst.output = []

                        newInst.documentation = [ [doc['type'], doc['url']] for doc in tool['documentation']]

                        if 'Manual' in [ doc[0] for doc in newInst.documentation ]:
                            newInst.inst_instr = True

                        newInst.license = tool['license']

                        newAuth = []
                        for dic in tool['credit']:
                            if dic['name'] not in newAuth and dic['name']!=None:
                                newAuth.append(dic['name'])
                        newInst.authors = newAuth

                        repos = []
                        for link in tool['link']:
                            if link['type'] == "Repository":
                                repos.append(link['url'])
                        newInst.repository = repos

                        newInst.source = ['biotools']

                        self.instSet.instances.append(newInst)

                else:
                    version = None
                    name = tool['biotoolsID'].lower()
                    newInst = instance(name, type_, cleanVersion(version))

                    newInst.description = tool['description']

                    newInst.homepage = tool['homepage']

                    newInst.publication = len(tool['publication'])

                    newInst.download = [ [tol['type'], tol['url']] for tol in tool['download'] ]

                    src = []
                    for down in [a for a in tool['download'] if a['type'] == 'Source package']:
                        src.append(down['url'])

                    newInst.src =src

                    newInst.os = tool['operatingSystem']

                    inputs = []
                    if len(tool['function'])>0:
                        inputs = [f['input'] for f in tool['function']]
                        newInst.input = lowerInputs(inputs[0])
                    else:
                        newInst.input = []

                    outputs = []
                    if len(tool['function'])>0:
                        outputs = [f['input'] for f in tool['function']]
                        newInst.output = lowerInputs(outputs[0])
                    else:
                        newInst.output = []

                    newInst.documentation = [ [doc['type'], doc['url']] for doc in tool['documentation']]

                    if 'Manual' in [ doc[0] for doc in newInst.documentation ]:
                        newInst.inst_instr = True

                    newInst.license = tool['license']

                    newAuth = []
                    for dic in tool['credit']:
                        if dic['name'] not in newAuth and dic['name']!=None:
                            newAuth.append(dic['name'])
                    newInst.authors = newAuth

                    repos = []
                    for link in tool['link']:
                        if link['type'] == "Repository":
                            repos.append(link['url'])
                    newInst.repository = repos

                    newInst.source = ['biotools']

                    self.instSet.instances.append(newInst)







def integrateInstances(setsOfInsts):
    '''
    setsOfInstances is a list of sets of instances
    by name and type
    also by version?
    '''
    totalNames = []
    names = []
    for s in setsOfInsts:
        print('instances from ' + s.source + ': '+ str(len(s.instances)))
        print('names from ' + s.source + ': ' + str(len(set([a.name for a in s.instances]))))

        names.append(set([a.name for a in s.instances]))
        totalNames = totalNames + [ a.name for a in s.instances ]

    groupInst = {}

    totalNames = set(totalNames)
    #print('There are %d tool names'%len(totalNames))

    # Grouping the instances by name and type in a dictionary
    count = 0
    Count = 0
    for name in totalNames: # iterating tool names
        Count += 1
        for set_ in setsOfInsts: # iterating sources
            for inst in set_.instances: # iterating instances in a given set
                if inst.name == name:
                    count += 1
                    if name not in groupInst.keys():
                        groupInst[name] = { inst.version : { inst.type : [inst] } }

                    else:
                        if inst.version in groupInst[name].keys():
                            if inst.type in groupInst[name][inst.version].keys():
                               newTlist = groupInst[name][inst.version][inst.type] + [inst]
                               groupInst[name][inst.version][inst.type] = newTlist
                            else:
                               groupInst[name][inst.version][inst.type] = [inst]

                        else:
                            groupInst[name][inst.version] = { inst.type : [inst] }
    #print('count =' + str(count))
    #print('Count =' + str(Count))
    #print(len(groupInst))
    # Creating the integrated instances
    finalSet = {}
    print('\nIntegrating metadata from different sources ... \n')
    for name in totalNames:
        finalSet[name] = []
        for version in groupInst[name].keys():

            for type_ in groupInst[name][version].keys():

                newInst = instance(name, type_, version)

                instaList = groupInst[name][version][type_]

                newInst.description = [a.description for a in instaList if a.description] # constructing_consensus
                if None in newInst.description:
                    newInst.description.remove(None)

                newLinks = []
                for inst in instaList:
                    for link in inst.links:
                        if link not in newLinks and link:
                            newLinks.append(link)
                newInst.links = newLinks

                newInst.publication =  sum([a.publication for a in instaList]) # number of related publications [by now, for simplicity]

                newInst.download = [item for sublist in instaList for item in sublist.download]  # list of lists: [[type, url], [], ...]
                if None in newInst.download:
                    newInst.download.remove([])

                inst_instr = [a.inst_instr for a in instaList]
                if True in inst_instr:
                    newInst.inst_instr = True #
                else:
                    newInst.inst_instr = False

                tests = [a.test for a in instaList]
                if True in tests:
                    newInst.test = True #
                else:
                    newInst.test = False

                newSrc = []
                for a in instaList:
                    for s in a.src:
                        if s!=None:
                            #print(s)
                            newSrc.append(s)

                newInst.src = newSrc

                newOs = []
                for inst in instaList:
                    for os in inst.os:
                        if os not in newOs:
                            newOs.append(os)

                newInst.os = newOs


                newInputs = []
                for insta in instaList:
                    for Dict in insta.input:
                        if Dict not in newInputs:
                            newInputs.append(Dict)
                        else:
                            continue

                newInst.input = newInputs # list of strings

                newOutputs = []
                for insta in instaList:
                    for Dict in insta.output:
                        if Dict not in newOutputs:
                            newOutputs.append(Dict)
                        else:
                            continue

                newInst.output = newOutputs # list of strings

                newDep = []
                for inst in instaList:
                    for dep in inst.dependencies:
                        if dep not in newDep:
                            newDep.append(dep)
                newInst.dependencies = newDep # list of strings

                newDocs = []
                for inst in instaList:
                    for doc in inst.documentation:
                        if doc not in newDocs:
                            newDocs.append(doc)
                        else:
                            continue

                newInst.documentation = newDocs # list of lists [[type, url], [type, rul], ...]

                newLicense = []
                for a in instaList:
                    if a.license not in newLicense and a.license != None and a.license != [] and a.license != False:
                        newLicense.append(a.license)
                    else:
                        continue
                #print(newLicense)
                newInst.license = newLicense

                newInst.termsUse = False #
                newInst.contribPolicy = False

                newAuth  = []
                for l in instaList:
                    for a in l.authors:
                        if a != None and a.lstrip() not in newAuth:
                            newAuth.append(a.lstrip())
                        else:
                            continue

                newInst.authors = newAuth # list of strings

                newRepos = []
                for t in instaList:
                    for rep in t.repository:
                        if rep not in newRepos:
                            newRepos.append(rep)
                newInst.repository = newRepos

                newSource = []
                for ints in instaList:
                    for s in ints.source:
                        if s not in newSource:
                            newSource.append(s)

                newInst.source = newSource


                finalSet[name].append(newInst)


    return(finalSet)



def generateCanonicalSet(instsctDist):
    '''
    groups instances by name into canonicals
    input: {
             name1: [instance1, instance2],
             name2: [instance3],
             ...
             }
    output: canonicalSet
    '''
    newCanonSet  = canonicalSet()
    for name in instsctDist.keys():
        instances = instsctDist[name]
        sources = list(set([item for sublist in instances for item in sublist.source]))
        types = list(set([inst.type for inst in instances if inst.type != None ]))
        newCanon = canonicalTool(name, instances, sources, types)
        newCanonSet.addCanononical(newCanon)
    return(newCanonSet)



def loadJSON(path):
    with open(path) as fil:
        return(json.load(fil))

def prepFAIRcomp(instances):
    global stdFormats
    stdFormats= getFormats(instances)


def getFormats(instances):
    inputs = [a.input for a in instances]
    inputs_ = [a for a in inputs]
    inputsNames = []

    nonSFormats = ['txt', 'text', 'csv', 'tsv', 'tabular', 'xml', 'json', 'nucleotide', 'pdf', 'interval' ]
    for List in inputs_:
        for eachD in List:
            if 'format' in eachD.keys():
                if ' format' not in eachD['format']['term'] and eachD['format']['term'].lstrip() not in nonSFormats:
                    if '(text)' not in eachD['format']['term']:
                        if eachD['format']['term'].lstrip() not in inputsNames:
                            inputsNames.append(eachD['format']['term'].lstrip())
    return(inputsNames)
