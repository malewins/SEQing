#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Interactive visualizaton for binding site data"""
import runpy
from argparse import ArgumentParser
from pathlib import Path
from xml.dom import minidom
import pickle
import hashlib
import itertools
import pandas
from Bio import SeqIO
from Bio.Alphabet import generic_dna
import converter


__author__ = "Yannik Bramkamp"

def validateGTF(df):
    """Validates gtf files. Returns True and an empty String if dataframe is valid,
    else returns false and an error message.
    
    Positional arguments:
    df -- dataframe to be validated
    """
    
    msg = ''
    if df.isnull().values.any() == True:
        msg = 'Missing values' + '\n' + str(df.isnull().sum())
        return [False, msg]
    if df['start'].map(lambda x: type(x)).values.any() != int:
        msg = 'column start contains non int values'
        return [False, msg]
    if df['end'].map(lambda x: type(x)).values.any() != int:
        msg = 'column end contains non int values'
        return [False, msg]
    if df['strand'].map(lambda x: x in ['+', '-']).values.all() != True:
        msg = 'bad strand symbol(has to be + or -'
        return [False, msg]
    return [True, msg] 

def validateBed12(df):
    """Validates 12 column bed files. Returns True and an empty String if dataframe is valid,
    else returns false and an error message.
    
    Positional arguments:
    df -- dataframe to be validated
    """
    
    msg = ''
    if df.isnull().values.any() == True:        
        msg = 'Missing values' + '\n' + str(df.isnull().sum())
        return [False, msg]
    if df['strand'].map(lambda x: x in ['+', '-']).values.all() != True:
        msg = 'bad strand symbol(has to be + or -'
        return [False, msg]
    if df['chromStart'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromStart contains non int values'
        return [False, msg]
    if df['chromEnd'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromEnd contains non int values'
        return [False, msg]    
    if df['thickStart'].map(lambda x: type(x)).values.any() != int:
        msg = 'column thickStart contains non int values'
        return [False, msg]
    if df['thickEnd'].map(lambda x: type(x)).values.any() != int:
        msg = 'column thickEnd contains non int values'
        return [False, msg]
    if df['blockCount'].map(lambda x: type(x)).values.any() != int:
        msg = 'column blockCount contains non int values'
        return [False, msg]
    if all(y.isdigit() for z in df['blockSizes'].map(lambda x: x.split(',')[:-1]).tolist()[0] for y in z ) == False:
        msg = 'column blockSizes contains non int values'
        return [False, msg]    
    if all(y.isdigit() for z in df['blockStarts'].map(lambda x: x.split(',')[:-1]).tolist()[0] for y in z ) == False:
        msg = 'column blockStarts contains non int values'
        return [False, msg]
    return [True, msg]

def validateBedGraph(df):
    """Validates 4 column bedgraph files. Returns True and an empty String if dataframe is valid,
    else returns false and an error message.
    
    Positional arguments:
    df -- dataframe to be validated
    """
    
    msg = ''
    if df.isnull().values.any() == True:        
        msg = 'Missing values' + '\n' + str(df.isnull().sum())
        return [False, msg]
    if df['chromStart'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromStart contains non int values'
        return [False, msg]
    if df['chromEnd'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromEnd contains non int values'
        return [False, msg]    
    if df['count'].map(lambda x: type(x)).values.any() != int:
        msg = 'column count contains non int values'
        return [False, msg]
    return [True, msg]

def validateBed(df):
    """Validates 6 column bed files. Returns True and an empty String if dataframe is valid,
    else returns false and an error message.
    
    Positional arguments:
    df -- dataframe to be validated
    """
    
    msg = ''
    if df.isnull().values.any() == True:        
        msg = 'Missing values' + '\n' + str(df.isnull().sum())
        return [False, msg]
    if df['strand'].map(lambda x: x in ['+', '-']).values.all() != True:
        msg = 'bad strand symbol(has to be + or -'
        return [False, msg]
    if df['chromStart'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromStart contains non int values'
        return [False, msg]
    if df['chromEnd'].map(lambda x: type(x)).values.any() != int:
        msg = 'column chromEnd contains non int values'
        return [False, msg]    
    if df['score'].map(lambda x: type(x)).values.any() != float:
        msg = 'column score contains non float values'
        return [False, msg]    
    return [True, msg]

def isRGB(color):
    """ Check if the provided strings match the required rgb format

    Positional arguments:
    color -- a single color string
    """
    if color[0:4] != 'rgb(':
        return False
    if color[-1:] != ')':
        return False
    if len(color[4:-1].split(',')) != 3:
        return False
    for i in color[4:-1].split(','):
        if i.replace(' ', '').isdigit() == False:
            return False
        if int(i.replace(' ', '')) < 0 or int(i.replace(' ', '')) > 255:
            return False
    return True

parser = ArgumentParser(description = '''Interactive, web based visualization for iCLIP data.
                        Atleast one gene annotaiton file in bed12 or gtf format is required for execution.
                        These files need to be unzipped and have the proper file extension.
                        The -bsraw and -bsdata options can be used to provide iCLIP and binding site data
                        to be shown in the visualization. The program will use prefixes to match files 
                        from both options in a one to one relationship. 
                        If multiple files from the same category share a prefix,
                        only the first will be taken into account.
                        For more details on the prefixes consult the help text for the two options.
                        An optional file containing gene descriptions can be provided with -desc,
                        this file should be a tab seperated 4 column csv.
                        The -seqs option can be used to provide fasta files containing dna sequence information.''')
parser.add_argument(dest='geneAnno', help = '''files containing gene annotations in bed12 or gtf format,
                    atleast one such file is required for execution. These files should not include a header.''',
                    nargs = '+', type = Path,metavar = 'GENE ANNOTATION FILE')
#parser.add_argument(dest='nonCoding', help = 'file containing information on non protein coding genes')
parser.add_argument('-bsdata', dest = 'bsdata', help = '''files containing binding site data in 6 column bed format. 
                    Everything before the first underscore _ in the file name will be treated as prefix 
                    and used to match iCLIP files to files containing binding sites.
                    These files should not include a header.''',
                    nargs = '+', type = Path, default = [], metavar = 'FILE')
parser.add_argument('-bsraw', dest = 'bsraw', help = '''files containing iCLIP data, 
                    in .bedgraph format. Everything before the first underscore _ 
                    in the file name will be treated as prefix and used to match 
                    iCLIP files to files containing binding sites. These files should not include a header.''',
                    nargs = '+', type = Path, default = [], metavar = 'FILE')
parser.add_argument('-port', dest = 'port', help = 'port for the dashboard to run on, defaults to 8060',
                    default = 8060, metavar = 'INTEGER', type = int)
parser.add_argument('-desc', dest = 'desc', help = '''file containing gene descriptions,
                    tab seperated csv with 4 columns. This file should include a header line matching:
                        ensembl_gene_id description external_gene_name gene_biotype''',
                    type = Path, metavar = 'FILE')
parser.add_argument('-seqs', dest = 'fastas', help = '''Fasta files containing genomic sequences,
                    please consult readme for important details''',
                    type = Path, nargs = '+', metavar = 'FILE')
parser.add_argument('-colors', dest = 'colors', 
                    help = '''Colors for the different data sets. Default is a set of 4 colors. 
                    Format(in quotes): rgb(111, 111, 111) Multiple color strings have to be seperated by a sapce.''',
                    nargs = '+', type = str, 
                    default = ['rgb( 88, 24, 69 )', 'rgb( 199, 0, 57 )', 'rgb(46, 214, 26)', 'rgb(255, 87, 51)' ],
                    metavar = 'STRING')
parser.add_argument('-k', dest = 'keys',
                    help = '''Enables you to provide the \'key\' and \'reverse\' arguments
                    for the python standard sort() function. You can use this argment multiple times. 
                    Each key should be provided like this example: -k \'lambda x : x[1:]\' \'False\' ''',
                    nargs = '+',
                    action = 'append')
parser.add_argument('-config' , dest = 'cfg',
                    help = 'An xml config file can be used instead of command lin arguments to specify parameters',
                    type = Path, metavar = 'FILE')
parser.add_argument('-splice_data',
                    dest='splice_data',
                    help = 'files containing splice site data in 6 column bed format.',
                    nargs = '+',
                    default = [],
                    type = Path,
                    metavar = 'FILE')


args=parser.parse_args()

useCfg = False
if args.cfg != None:
    try:
        configFile = minidom.parse(str(args.cfg))
        useCfg = True
    except FileNotFoundError:
        print('Could not open config file, aborting.')
        exit()

# Dict containing checksums for gene annotation files, files loaded once will
# be serialized to speed up future loading
try:
    sums = pickle.load(open('checksums', 'rb'))
except IOError:
    sums = []
checksums = dict(sums)

plotColors = []


     
if useCfg == False: #use command line arguments for setup  
    port = args.port
    geneAnnotationPaths = args.geneAnno
    bindingSitePaths = args.bsdata
    bindingSiteRawPaths = args.bsraw
    fastaPaths = args.fastas
    sortKeys = args.keys
    spliceSitePaths = args.splice_data
    try:
        descriptionPath = Path(args.desc)
    except TypeError:
        descriptionPath = None
    colors = args.colors
    for i in colors:
        if isRGB(i) == True:
            plotColors.append(i)
        else:
            print('Color string ' + str(i) + ' is not valid')
else: #use xml document for setup
    try:
        port = configFile.getElementsByTagName('port')[0].firstChild.data
        print(port)
    except:
        print('No port specified, using 8060')
        port = 8060
    try:
        geneAnnotationPaths = [Path(i.firstChild.data) for i in configFile.getElementsByTagName('anno')]
        print(geneAnnotationPaths)
    except:
        print('Unable to load annotation files, please check your config. Exiting.')
    try:
        fastaPaths = [Path(i.firstChild.data) for i in configFile.getElementsByTagName('seq')]
    except:
        fastaPaths = None
    try:
        descriptionPath = [Path(i.firstChild.data) for i in configFile.getElementsByTagName('desc')][0]
        print(descriptionPath)
    except:
        descriptionPath = None
    try:
        sortKeys = []
        keyList = [i for i in configFile.getElementsByTagName('key')]
        for  i in keyList:
            sortKeys.append([i.getElementsByTagName('lambda')[0].firstChild.data,
                             i.getElementsByTagName('reverse')[0].firstChild.data])
        print(sortKeys)
    except:
        sortKeys = None
    try:
        dataSetList = [i for i in configFile.getElementsByTagName('set')]
    except:
        dataSetList = []
    bindingSitePaths = []
    bindingSiteRawPaths = []
    if len(dataSetList) >= 1:
        for  i in dataSetList:
            try:
                bindingSiteRawPaths.append(Path(i.getElementsByTagName('clip')[0].firstChild.data))
            except:
                pass
            try:
                bindingSitePaths.append(Path(i.getElementsByTagName('binding')[0].firstChild.data))
            except:
                pass
            try:
                color = i.getElementsByTagName('color')[0].firstChild.data
                if isRGB(color) == True:
                    plotColors.append(color)
            except:
                pass

if len(plotColors) == 0:
    print('No valid color strings provided, using defaults')
    plotColors = ['rgb( 88, 24, 69 )', 'rgb( 199, 0, 57 )', 'rgb(46, 214, 26)', 'rgb(255, 87, 51)']


# headers for the datafiles, files obviously need to conform to these headers for the visualization to work
bedHeader = ['chrom','chromStart','chromEnd','name','score','strand','thickStart',
             'thickEnd','itemRGB','blockCount','blockSizes','blockStarts']
bsHeader = ['chrom', 'chromStart','chromEnd','type', 'score', 'strand']
rawHeader = ['chrom','chromStart','chromEnd','count']
gtfheader = ['seqname', 'source', 'feature', 'start', 'end', 'score',
               'strand', 'frame', 'attribute']

descAvail = True
print('Loading gene annotation files.')
geneAnnotations = []

counter = 0
for idx, i in enumerate(geneAnnotationPaths):
    print('Loading file ' + str(idx+1) )
    try:
        if i.suffix.lower() =='.bed':
            checksum = hashlib.md5(open(str(i)).read().encode('utf-8'))
            if checksums.get(str(i.stem), None) != checksum.hexdigest():
                checksums[str(i.stem)] = checksum.hexdigest()
                df = pandas.read_csv(i, sep = '\t', comment = '#', names = bedHeader)
                validation = validateBed12(df)
                if validation[0] == True:
                    geneAnnotations.append(df)
                    out = open(str(i.stem)+'.bin', 'wb')
                    pickle.dump(df, out)
                    out.close()
                else:
                    print('Error in file ' + str(i) + ':')
                    print(validation[1])
            else:
                try:
                    df = pickle.load(open(str(i.stem)+'.bin', 'rb'))
                    geneAnnotations.append(df)
                    print('Loaded from pickle')
                except IOError:
                    print('pickle not  found, loading from raw file')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = bedHeader)                    
                    validation = validateBed12(df)
                    if validation[0] == True:
                        geneAnnotations.append(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
                except UnicodeDecodeError:
                    print('Error decoding pickle binary file, will load from raw file instead')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = bedHeader)                    
                    validation = validateBed12(df)
                    if validation[0] == True:
                        geneAnnotations.append(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
                except ModuleNotFoundError:
                    print('Pickle was created using different package versions, will load from raw file instead')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = bedHeader)                    
                    validation = validateBed12(df)
                    if validation[0] == True:
                        geneAnnotations.append(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
        if i.suffix.lower() == '.gtf':
            checksum = hashlib.md5(open(str(i)).read().encode('utf-8'))
            if checksums.get(str(i.stem), None) != checksum.hexdigest():
                checksums[str(i.stem)] = checksum.hexdigest()
                df = pandas.read_csv(i, sep = '\t', comment = '#', names = gtfheader)
                validation = validateGTF(df)
                if validation[0] == True:
                    df = converter.convertGTFToBed(df)
                    out = open(str(i.stem)+'.bin', 'wb')
                    pickle.dump(df, out)
                    out.close()
                    geneAnnotations.append(df)
                else:
                    print('Error in file ' + str(i) + ':')
                    print(validation[1])
            else:
                try:
                    df = pickle.load(open(str(i.stem)+'.bin', 'rb'))
                    geneAnnotations.append(df)
                    print('Loaded from pickle')
                except IOError:
                    print('pickle not  found, loading from raw file')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = gtfheader)
                    validation = validateGTF(df)
                    if validation[0] == True:
                        df = converter.convertGTFToBed(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                        geneAnnotations.append(df)
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
                except UnicodeDecodeError:
                    print('Error decoding pickle binary file, will load from raw file instead')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = gtfheader)
                    validation = validateGTF(df)
                    if validation[0] == True:
                        df = converter.convertGTFToBed(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                        geneAnnotations.append(df)
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
                except ModuleNotFoundError:
                    print('Pickle was created using different package versions, will load from raw file instead')
                    df = pandas.read_csv(i, sep = '\t', comment = '#', names = gtfheader)
                    validation = validateGTF(df)
                    if validation[0] == True:
                        df = converter.convertGTFToBed(df)
                        out = open(str(i.stem)+'.bin', 'wb')
                        pickle.dump(df, out)
                        out.close()
                        geneAnnotations.append(df)
                    else:
                        print('Error in file ' + str(i) + ':')
                        print(validation[1])
        if i.suffix.lower() != '.gtf' and i.suffix.lower() != '.bed':
            print('Invalid file format, please use only .bed or .gtf files')              
    except FileNotFoundError:
        print('File ' + str(i.stem) + ' not found, skipping')
if len(geneAnnotations) == 0:
    print('No valid gene annotation files found, terminating.')
    exit()

out = open('checksums', 'wb')
pickle.dump(checksums, out)
out.close()

geneNames = list(set().union([x[0] for y in [i['name'].str.split('.') for i in geneAnnotations] for x in y]))
print('Done.')
print('Loading description and sequence data if provided.')
sequences = []
ensembl = False
try:
    for i in fastaPaths:
        try:

            seq = SeqIO.parse(str(i), 'fasta', alphabet = generic_dna)
            for record in seq:
                if record.description == record.name:
                    ensembl = False
                else:
                    ensembl = True
                seq = itertools.chain([record], seq)
                break
            if ensembl != True:
                sequences.append(SeqIO.to_dict(seq, 
                    key_function = lambda rec : rec.description.split(':')[0]
                    )
                )
            else:
                sequences.append(SeqIO.to_dict(seq, 
                    key_function = lambda rec : rec.name
                    )
                )
        except FileNotFoundError:
            print('Sequence annotations for coding genes not found, proceeding without')
except TypeError:
    pass

geneDescriptions = pandas.DataFrame()
try:
    geneDescriptions = pandas.read_csv(descriptionPath, sep = '\t')
    if list(geneDescriptions.columns.values)	 == ['ensembl_gene_id', 'description', 'external_gene_name', 'gene_biotype']:
        geneDescriptions = geneDescriptions[geneDescriptions['ensembl_gene_id'].isin(geneNames)]
        geneDescriptions.fillna(':',inplace = True)
    else:
        print('Header for descriptions does not match specifications, ignoring description file')
        descAvail = False
except FileNotFoundError:
    print('description file not found, proceeding without')
    descAvail = False
except ValueError:
    descAvail = False

#setup dropdown with gene descriptions if available
dropList = []
if descAvail == True:
    geneDict = geneDescriptions.to_dict(orient = 'records')
    # Builds list of gene names and descriptions.
    # Note, in order to be added to the dashboard a gene has to have an entry in the descriptions file
    for i in geneDict:
        dropList.append(
            [i['ensembl_gene_id'] + ' - ' + i['description'][:30] + ' - ' + i['external_gene_name'],
            i['ensembl_gene_id']]
        )
if descAvail == False or len(dropList) == 0:
    dropList = [[i,i] for i in geneNames]

dropList.sort(key = lambda x : x[1])

# Setup all needed data frames
print('Done.')
dsElements = 0 # number of traces per dataset, i.e Rawdata+ bindingsites = 2
rawAvail = False # Raw data available
procAvail = False # proc data available
spliceAvail = False # splice data available

#setup iCLIP data
bsRawDFs = {}
dataSetNames = []
if len(bindingSiteRawPaths) > 0:
    print('Loading iCLIP data.')
    for i in bindingSiteRawPaths:
        try:

            df = pandas.read_csv(i, sep = '\t', names = rawHeader)
            validation = validateBedGraph(df)
            if validation[0] == True:
                if i.stem.split('_')[0] not in dataSetNames:
                    dataSetNames.append(i.stem.split('_')[0])
                    bsRawDFs.update({str(dataSetNames[-1]) : df})
                else:
                    print('Warning, you are using the same prefix for multiple iCLIP files, file ' + str(i) + ' will be ignored')
            else:
                print('Error in file ' + str(i) + ':')
                print(validation[1])
        except FileNotFoundError:
            print('File '+str(i) + ' was not found')
    print('Done.')
if len(bsRawDFs) > 0:
    rawAvail = True
    dsElements += 1


#setup data for binding sites
bsProcDFs = {}
if len(bindingSitePaths) > 0:
    print('Loading bindings site data.')
for i in bindingSitePaths:
    if i.stem.split('_')[0] in dataSetNames:
        try:
            df = pandas.read_csv(i, sep = '\t', names = bsHeader)
            validation = validateBed(df)
            if validation[0] == True:
                if i.stem.split('_')[0] in bsProcDFs:
                    print('Warning, you are using the same prefix for multiple bedgraph files, file ' + str(i) + ' will be ignored')
                else:
                    bsProcDFs.update({i.stem.split('_')[0] : df})
            else:
                print('Error in file ' + str(i) + ':')
                print(validation[1])                   
        except FileNotFoundError:
            print('File '+str(i) + ' was not found')  
    else:
        print('No corresponding raw data found for data set ' + i.stem.split('_')[0])
if len(bindingSitePaths) > 0:
    print('Done.')
if len(bsProcDFs) > 0:
    dsElements +=1
    procAvail = True


#setup data for splice sites
spliceProcDFs = {}
spliceSetNames = [[],[]]
spliceElements = 0
if len(spliceSitePaths) > 0:
    print('Loading splice site data')
for i in spliceSitePaths:
        try:
            df = pandas.read_csv(i, sep= '\t', names= bsHeader)
            validation = validateBed(df)
            file_name = i.stem.split('_')[0]+'_'+i.stem.split('_')[1]
            if validation[0]:
                if file_name in spliceProcDFs:
                    print('Warning, you are using the same prefix for multiple bedgraph files, file ' + str(i) + ' will be ignored')
                else:
                    spliceProcDFs.update({file_name : df})
                if i.stem.split('_')[0] not in spliceSetNames[1]:
                    spliceSetNames[0].append(i.stem.split('_')[1])
                    spliceSetNames[1].append(i.stem.split('_')[0])
            else:
                print('Error in file ' + str(i) + ':')
                print(validation[1])
        except FileNotFoundError:
            print('File ' + str(i) + ' was not found')
if len(spliceSitePaths) > 0:
    print('Done.')
if len(spliceProcDFs) > 0:
        spliceElements += 1
        spliceAvail = True

colorA = 'rgb(0, 150, 0)'
colorC = 'rgb(15,15,255)'
colorG = 'rgb(209, 113, 5)'
colorT = 'rgb(255, 9, 9)'

if sortKeys == None:
    sortKeys = [['lambda x : x[:1]', 'False']]
else:
    if len(sortKeys) == 0:
        sortKeys.append(['lambda x : x[:1]', 'False'])

# map for data track colors
colorMap = {}
for i in range(len(dataSetNames)):
    colorMap.update({dataSetNames[i] : plotColors[i%len(plotColors)]})
    
print('preparing to start dashboard on port ' + str(port) + '.')


globalDict = {
    'colorMap' : colorMap, #Contains colors for the data traces
    'descAvail' : descAvail, #description file present yes/no
    'colorA' : colorA, #colors for sequence display
    'colorC' : colorC,
    'colorG' : colorG,
    'colorT' : colorT,
    'port' : port, # port the dashboard runs on
    'procAvail' : procAvail, # binding site data available True/False
    'dsElements' : dsElements, # Number of elements per dataset, can be 0,1,2
    'spliceElements': spliceElements, # Number of elements per rna dataset, can be 0, 1
    'bsProcDFs' : bsProcDFs, # dataframes with binding site data
    'bsRawDFs' : bsRawDFs, # dataframes with iCLIP data
    'spliceProcDFs' : spliceProcDFs, # dataframes with rnaSeq data
    'dataSetNames' : dataSetNames, # names for the data sets
    'spliceSetNames' : spliceSetNames, # names for the rnaSeq data sets
    'rawAvail' : rawAvail, # iCLIP data available True/False
    'spliceAvail' : spliceAvail, # rnaSeq data available True/False
    'dropList' : dropList, # list of entries for the gene selection dropdown
    'geneDescriptions' : geneDescriptions, # dataframe with gene descriptions
    'sequences' : sequences, # list containing sequence files
    'geneAnnotations' : geneAnnotations, # dataframes containing gene annotation data
    'ensembl' : ensembl, # ensembl style fasta format True/False
    'sortKeys' : sortKeys } # arguments for the list.sort function

runpy.run_module('dashboard_binding_sites', init_globals = globalDict, run_name = '__main__')
