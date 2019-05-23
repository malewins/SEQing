#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas

__author__ = "Yannik Bramkamp"

if __name__ == '__main__':
    print('Please start the program via validator.py')
    exit()

gtfHeader = ['chrom','chromStart','chromEnd','name','score','strand','thickStart','thickEnd','itemRGB','blockCount','blockSizes','blockStarts']
def convertGTFToBed(df):
    """ Convert a gtf dataframe to a bed12 dataframe for internal use. Only relevant
    lines will be taken into account, in this case exon and cds can be used 
    to reconstruct all needed information.
    
    Positional arguments:
    df -- gtf dataframe
    """

    bedFile = []
    current = ''
    chrom = ''
    strand = ''
    itemRGB = 0
    score = 0
    blockCount = 0
    blockStarts = []
    blockEnds = []
    blockSizes = []
    thickStart = -1
    thickEnd = -1
    
    rowIndex = 1
    percent = 10
    for i in df.iterrows():
        if rowIndex/len(df)*100 >= percent:
            print(str(percent) + '%')
            percent += 10
        rowIndex +=1
        # Split attributes for relevant lines and extract needed ones
        if i[1]['feature'] == 'exon' or i[1]['feature'] == 'CDS':
            attributes = i[1]['attribute'].split(';')
            geneID = [s for s in attributes if 'gene_id' in s]
            transID = [s for s in attributes if 'transcript_id' in s]
            # check if gene and transcript id are specified only once
            if len(geneID) == 1:
                geneID = geneID[0].split(' ')[-1]
                if geneID[0] == '"':
                    geneID = geneID[1:-1]
            else:
                geneID = ''
            if len(transID) == 1:
                transID = transID[0].split(' ')[-1]
                if transID[0] == '"':
                    transID = transID[1:-1]
            else:
                transID = ''
            # handle ids that consist of multiple, point seperated values
            geneParts = geneID.split('.')
            transParts = transID.split('.')
            finalID = '' # this will be the final id used for the gene
            if geneID != '':
                if transID != '':
                    if len(geneParts) == 1 and len(transParts) == 1:
                        finalID = geneParts[0] + '.' + transParts[0]
                    else:
                        if len(geneParts) == 1 and len(transParts) == 2:
                            if geneParts[0] == transParts[0]:
                                finalID = geneParts[0] + '.' + transParts[1]
                            else:
                                finalID = geneParts[0] + '.' + '_'.join(transParts)
                        else:
                            finalID = '_'.join(geneParts) + '.' + '_'.join(transParts)
                else:
                    finalID = geneID
            else:
                continue
            # convert the data into bed 12
            if current == '':
                current = finalID
                chrom = i[1]['seqname']
                strand = i[1]['strand']
                blockCount = 0
                blockStarts = []
                blockEnds = []
                blockSizes = []
                thickStart = -1
                thickEnd = -1
                if i[1]['feature'] == 'exon':
                    blockCount += 1
                    blockStarts.append(int(i[1]['start']))
                    blockEnds.append(int(i[1]['end']))
                    blockSizes.append(int(i[1]['end'])-int(i[1]['start'])+1)
                if i[1]['feature'] == 'CDS':
                    if thickStart == -1 or thickStart > i[1]['start']:
                        thickStart = int(i[1]['start'])-1
                    if thickEnd == -1 or thickEnd < i[1]['end']:
                        thickEnd = i[1]['end']
            else:
                if finalID == current: # line still belongs to the same gene
                    if i[1]['feature'] == 'exon':
                        blockCount += 1
                        blockStarts.append(int(i[1]['start']))
                        blockEnds.append(int(i[1]['end']))
                        blockSizes.append(int(i[1]['end'])-int(i[1]['start'])+1)
                    if i[1]['feature'] == 'CDS':
                        if thickStart == -1 or thickStart > i[1]['start']:
                            thickStart = int(i[1]['start'])-1
                        if thickEnd == -1 or thickEnd < i[1]['end']:
                            thickEnd = i[1]['end']
                else:   # line belongs to a new gene with a different final id
                    chromStart = min(blockStarts)
                    chromEnd = max(blockEnds)
                    if thickEnd == -1:
                        thickEnd = chromEnd
                    if thickStart == -1:
                        thickStart = chromStart-1
                    bBlockStarts = [int(i)-int(chromStart) for i in blockStarts]
                    # append data of previous gene before resetting values for
                    # the new one
                    bedFile.append([chrom, chromStart-1, chromEnd, current, score,
                                    strand, thickStart, thickEnd, itemRGB,
                                    blockCount, ','.join(map(str, blockSizes)), ','.join(map(str, bBlockStarts))])
                    current = finalID
                    chrom = i[1]['seqname']
                    strand = i[1]['strand']
                    blockCount = 0
                    blockStarts = []
                    blockEnds = []
                    blockSizes = []
                    thickStart = -1
                    thickEnd = -1    
                    if i[1]['feature'] == 'exon':
                        blockCount += 1
                        blockStarts.append(int(i[1]['start']))
                        blockEnds.append(int(i[1]['end']))
                        blockSizes.append(int(i[1]['end'])-int(i[1]['start'])+1)
                    if i[1]['feature'] == 'CDS':
                        if thickStart == -1 or thickStart > i[1]['start']:
                            thickStart = int(i[1]['start'])-1
                        if thickEnd == -1 or thickEnd < i[1]['end']:
                            thickEnd = i[1]['end']
    return pandas.DataFrame(data = bedFile, columns = gtfHeader)
