import argparse
import requests
import re
from bs4 import BeautifulSoup
import json

# initializing session
session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"

# the html retriever
def getHTML(url, verb=False):
    '''
    This function takes and url as an input and returns the corresponding
    bs4 object
    '''

    from bs4.dammit import EncodingDetector

    try:
        re = session.get(url, headers=headers, timeout=(10, 30))

    except:
        print(r'problem here')
        return(None)

    else:
        if re.status_code == 200:
            # dealing with encoding
            http_encoding = re.encoding if 'charset' in re.headers.get('content-type', '').lower() else None
            html_encoding = EncodingDetector.find_declared_encoding(re.content, is_html=True)
            encoding = html_encoding or http_encoding

            # generating BeautifulSoup object
            bsObj = BeautifulSoup(re.content, 'html5lib', from_encoding=encoding)

            if verb == True:
                print("The title of html is %s"%bsObj.title.getText())
            return(bsObj)
        else:
            return(None)


def preParsing(bs):
    '''
    This function return to parts of the bsObject.
    part 1: extended name, description, authors, maintainers and citation
    part 2: a dictionary with all fragments under a <h3>.
    '''
    Name = bs.find('h1').get_text()
    html1 = []
    html2 = {}
    htmlsub2 = []
    for tag in bs.find('h2').next_siblings:
        if tag.name == 'h3':
            name = tag.contents[0]
            break
        else:
            html1.append(tag)

    if bs.find('div', attrs={"class":"bioc_citation"}):
        citation = 1
    else:
        citation = 0

    # Getting second part
    for tag in bs.find('h3').next_siblings:
        if tag.name == 'h3':
            html2[name] = htmlsub2
            htmlsub2 = []
            name = tag.contents[0]
        else:
            htmlsub2.append(tag)
    html2[name] = htmlsub2
    return(Name, citation, html1, html2)

def getInsDocDetArch(part2):
    if 'Installation' in part2.keys():
        instRaw = part2['Installation']
    else:
        print('%s lacks Installation'%testUrl)

    if 'Documentation' in part2.keys():
        docRaw = part2['Documentation']
    else:
        print('%s lacks Documentation'%testUrl)

    if 'Details' in part2.keys():
        detailsRaw = part2['Details']
    else:
        print('%s lacks Details'%testUrl)

    if 'Package Archives' in part2.keys():
        packRaw = part2['Package Archives']
    else:
        print('%s lacks Package archives'%testUrl)
    return(instRaw, docRaw, detailsRaw, packRaw)


def parsePart1(bs, items):
    ps = [p for p in bs if p.name == 'p' ]
    if 'Bioconductor version' in ps[0].contents[0]:
        items['description'] = ps[1].contents[0]
        Auth = [a for a in ps[2].contents[0].split(':')[1].split(',') ]
        if ' and ' in Auth[-1]:
            last_auth = Auth[-1].split('and')
            items['authors'] = Auth[:-1] + last_auth
        else:
            items['authors'] = Auth

        Mant = [a for a in ps[3].contents[0].split(':')[1].split(',') ]
        if ' and ' in Mant[-1]:
            last_mant = Mant[-1].split('and')
            items['mantainers'] = Mant[:-1] + last_mant
        else:
            items['mantainers'] = Mant

    else:
        print('Unknown structure of part1. Aborting the parsin...')
    return(items)


def existInstallation(bs, items):
    instr = [a for a in bs if a.name == 'pre']
    if len(instr)>0:
        items['Installation instructions'] = True
    else:
        items['Installation instructions'] = False

    return(items)



def parseDocumentation(bs, items):
    table = [a for a in bs if a.name == 'table']
    if len(table) > 1:
        print('error in documentation parsing, aborting...')
    else:
        table = table[0]

    items['documentation'] = {}

    for row in table.findAll('tr'):
        cells = [cell for cell in row.findAll('td')]
        if cells[0].find('a') or cells[1].find('a'):
            doc = str(cells[0].find('a'))
            script = str(cells[1].find('a'))
            items['documentation'][cells[2].get_text()] = [doc, script]

    return(items)


def parseDetails(bs, items):
    table = [a for a in bs if a.name == 'table']
    if len(table) > 1:
        print('error in details parsing, aborting...')
    else:
        table = table[0]

    for row in table.findAll('tr'):
        cells = [cell for cell in row.findAll('td')]
        if re.sub('\s+', '', cells[1].get_text() ) in ['', ' ']:
            items[cells[0].get_text()] = None
        else:
            items[cells[0].get_text()] = re.sub('\s+', '', cells[1].get_text() )

    return(items)

import re
def parseArchives(bs, items):
    table = [a for a in bs if a.name == 'table']
    if len(table) > 1:
        print('error in archives parsing, aborting...')
    else:
        table = table[0]

    for row in table.findAll('tr'):
        cells = [cell for cell in row.findAll('td')]
        if re.sub('\s+', '', cells[1].get_text() ) in ['', ' ']:
            items[cells[0].get_text()] = None
        else:
            items[cells[0].get_text()] = re.sub('\s+', '', cells[1].get_text() )

    return(items)

def parseInput(InputPath):
    '''
    This function takes the input file and builds a list of urls
    required: the input path. Line format in input file: <url>\t<name>\n
    returns: a lis of urls in the file
    '''
    urls_file = open(InputPath, 'r')
    urls = []
    counter = 1
    counter_valid = 0
    for line in urls_file:
        if len(line.split('\t')) != 2:
            print("Input file line %s skipped: impossible to parse, number of columns != 2."%(counter))
        else:
            url = line.split('\t')[0]
            if "galaxy" not in url and "github" not in url:
                urls.append(check_protocol(url))
                counter_valid += 1
        counter += 1
    print("Number of URLs to be analyzed: %s"%(counter_valid))
    if urls == []:
        print("No URLs to analyze")
        return(None)
    else:
        return(urls)


def parseInput(InputPath):
    '''
    This function takes the input file and builds a list of urls
    required: the input path. Line format in input file: <url>\t<name>\n
    returns: a lis of urls in the file
    '''
    urls_file = open(InputPath, 'r')
    urls = []
    counter = 1
    counter_valid = 0
    for line in urls_file:
        if len(line.split('\t')) != 2:
            print("Input file line %s skipped: impossible to parse, number of columns != 2."%(counter))
        else:
            url = line.split('\t')[0]
            if "bioconductor.org/packages/release/bioc/html" in url:
                urls.append(check_protocol(url))
                counter_valid += 1
        counter += 1
    print("Number of URLs to be analyzed: %s"%(counter_valid))
    if urls == []:
        print("No URLs to analyze")
        return(None)
    else:
        return(urls)


def check_protocol(url):
    '''
    '''
    if re.match('^http', url) != None: # To be changed for proper regex (beginning of line)
        return(url)

    else:
        return('https://' + url)


if __name__ == '__main__':

    outpath = 'bioconductor2000.json' ########
    all_ = []
    urls = "/home/eva/BSC/galaxy/2000urls.txt"
    URLs = parseInput(urls)
    if URLs != None:
        for url in URLs:
            bsO = getHTML(url, verb=True)
            if bsO != None:
                items = {}
                name, citation, part1, part2 = preParsing(bsO)
                items['name'] = name
                items['citation'] = citation
                instRaw, docRaw, detailsRaw, packRaw = getInsDocDetArch(part2)
                items = parsePart1(part1, items)
                #print(instRaw)
                #print(docRaw)
                items = existInstallation(instRaw, items)
                items = parseDocumentation(docRaw, items)
                items = parseDetails(detailsRaw, items)
                items = parseArchives(packRaw, items)
                if items['URL'] != None:
                    items['links'] = [url] + [items['URL']]
                else:
                    items['links'] = [url]


                all_.append(items)

        with open(outpath, 'w') as fp:
            json.dump(all_, fp, sort_keys=True, indent=4)
