#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Interactive visualizaton for binding site data"""
import json
import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools
import pprint

__author__ = "Yannik Bramkamp"

if 'dropList' not in globals():
    print('Please start the program via validator.py')
    exit()

if len(sequences) == 0:
    seqDispStyle = {'display' : 'none'}
else:
    seqDispStyle = {'width':'20vw','display':'table-cell'}
    
try:
    initialColor = dataSetNames[0]
    disableSettings = False
except:
    initialColor = None
    disableSettings = True
    
print(disableSettings)

app = dash.Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1(id = 'headline', children = 'Report'),
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                dcc.Dropdown(
                                    id = 'geneDrop',
                                    options = [{'label':i[0], 'value' : i[1]} for i in dropList],
                                    value = dropList[0][1]
                                )
                            ],
                            style = {'width' : '70vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                        ),
                        html.Div(
                            style = {'width' : '1vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                        ),
                        html.Div(
                            children = [
                                html.Button(id = 'submit', n_clicks = 0, n_clicks_timestamp = 0, children = 'Submit' )
                            ],
                            style = {'width' : '8vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                        )
                    ]
                ),
                dcc.Tabs(
                    id = 'tabs',
                    children = [
                        dcc.Tab(
                            label = 'iCLIP data',
                            id = 'clipTab',
                            children = [
                                html.Div(
                                    children = [
                                        html.Div(
                                            children = [
                                                dcc.Checklist(
                                                    id = 'paramList',
                                                    options = [{'label':i, 'value' : i} for i in dataSetNames],
                                                    values = []
                                                )
                                            ],
                                            style = {'width':'10vw','display':'table-cell'}
                                        ),
                                        html.Div(
                                            children = html.P(html.B('Gene description: ')), 
                                            id = 'descDiv',
                                            style = {'width':'58vw','display':'table-cell'}
                                        ),
                                        html.Div(
                                            children = [
                                                dcc.RadioItems(
                                                    id = 'sequenceRadio',
                                                    options = [
                                                        {'label' : 'Do not show dna sequence', 'value' : 'noSeq'},
                                                        {'label' : 'Show dna sequence as letters', 'value' : 'letterSeq'},
                                                        {'label' : 'Show dna sequence as heatmap', 'value' : 'heatSeq'}
                                                    ],
                                                    value = 'heatSeq'
                                                )
                                            ],
                                            style = seqDispStyle
                                        )
                                    ]
                                ),
                                dcc.Graph(id = 'bsGraph')
                            ]
                        ),
                        dcc.Tab(
                            label = 'RNASeq',
                            id = 'rnaTab',
                            children = [
                                html.Div(
                                    children=[
                                        html.H2("RNA Seq data to identify splice events", style={"text-align": "center"}),
                                        html.P("The width shows how often"
                                               " this position turned out as exon in this "
                                               "specific experiment line.", style={"text-align": "center"})
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.B('Data set: '),
                                        dcc.Checklist(
                                            id='check_id_',
                                            options=[{'label': spliceSetNames[1][i], 'value': 'check'+str(i)} for i in range(len(spliceSetNames[1]))],
                                            values=['check'+str(i) for i in range(len(spliceSetNames[1]))],
                                        ),
                                    ],
                                    style = {'width':'20vw','display':'table-cell'}
                                ),

                                html.Div(
                                    children = html.P(html.B('Gene description: ')),
                                    id = 'rnaDescDiv',
                                    style = {'width':'58vw','display':'table-cell'}
                                ),

                                html.Div(
                                    children = [
                                        html.B('Display type: '),
                                        dcc.RadioItems(
                                            id = 'rnaRadio',
                                            options = [
                                                {'label': 'Display type 1', 'value': 'one'},
                                                {'label': 'Display type 2', 'value': 'two'},
                                                {'label': 'Display type 3', 'value': 'three'}
                                            ],
                                            value = 'one'
                                        )
                                    ],
                                    style = {'width':'20vw','display':'table-cell'}
                                ),
                                dcc.Graph(id='spliceGraph')
                            ]
                        ),
                        dcc.Tab(
                            label = 'Settings',
                            id = 'settings',
                            disabled = disableSettings,
                            children = [
                                html.Div(
                                    children = [
                                        html.Div(
                                            style = {'display' : 'none'},
                                            id = 'colorDiv',
                                            children = json.dumps(colorMap)
                                        ),
                                        html.Div(
                                            style = {'display' : 'none'},
                                            id = 'colorFinal',
                                            children = json.dumps(colorMap)
                                        ),
                                        dcc.Dropdown(
                                            id = 'colorDrop',
                                            options =  [{'label':i, 'value' : i} for i in dataSetNames],
                                            value = initialColor
                                        ),
                                        html.Div(
                                            id = 'rDisp',
                                            children = html.P(html.B('R: ')), 
                                            style = {'width':'10vw','display':'table-cell'}
                                        ),
                                        dcc.Slider(
                                            id = 'rInput',
                                            min = 0,
                                            max = 255,
                                            step = 1,
                                            updatemode = 'drag'
                                        ),
                                        html.Div(
                                            id = 'gDisp',
                                            children = html.P(html.B('G: ')), 
                                            style = {'width':'10vw','display':'table-cell'}
                                        ),
                                        dcc.Slider(
                                            id = 'gInput',
                                            min = 0,
                                            max = 255,
                                            step = 1,
                                            updatemode = 'drag'
                                        ),
                                        html.Div(
                                            id = 'bDisp',
                                            children = html.P(html.B('B: ')), 
                                            style = {'width':'10vw','display':'table-cell'}
                                        ),
                                        dcc.Slider(
                                            id = 'bInput',
                                            min = 0,
                                            max = 255,
                                            step = 1,
                                            updatemode = 'drag'
                                        ),
                                        html.Div(
                                            children = [
                                                html.Div(id = 'preview',
                                                    children = html.P(html.B('Preview')),
                                                    style = {'width' : '30vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                                                ),
                                                html.Div(
                                                    children = [
                                                        html.Button(id = 'colorConfirm', n_clicks_timestamp = 0, children = 'confirm' )
                                                    ],
                                                    style = {'width' : '10vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                                                )
                                            ],
                                            style = {'width':'10vw','display':'table-cell'}
                                        )                                                                              
                                    ],
                                    style = {'width' : '30vw','display' : 'table-cell', 'verticalalign' : 'middle'}
                                ),
                            ]
                        )
                    ]
                )

            ]
        )
    ]
)

@app.callback(
    dash.dependencies.Output('rDisp', component_property = 'children'),
    [dash.dependencies.Input('rInput', component_property = 'value')]
)
def showR(r):
    """Callback to display current value for red

    Positional arguments:
    r -- value for red
    """
    
    return html.P(html.B('R: ' + str(r)))

@app.callback(
    dash.dependencies.Output('gDisp', component_property = 'children'),
    [dash.dependencies.Input('gInput', component_property = 'value')]
)
def showG(g):
    """Callback to display current value for green

    Positional arguments:
    g -- value for green
    """
    
    return html.P(html.B('G: ' + str(g)))

@app.callback(
    dash.dependencies.Output('bDisp', component_property = 'children'),
    [dash.dependencies.Input('bInput', component_property = 'value')]
)
def showB(b):
    """Callback to display current value for blue

    Positional arguments:
    b -- value for blue
    """
    
    return html.P(html.B('B: ' + str(b)))

@app.callback(
    dash.dependencies.Output('preview', component_property = 'style'),
    [dash.dependencies.Input('rInput', 'value'),
     dash.dependencies.Input('gInput', 'value'),
     dash.dependencies.Input('bInput', 'value')]
)
def previewColor(r,g,b):
    """Callback for rgb color preview

    Positional arguments:
    r -- value for red
    g -- value for green
    b -- value for blue
    """
    
    if r == None or b == None or g == None:
        return {'backgroundColor' : 'rgb(255, 255, 255)', 'color' :  'rgb(255, 255, 255)'}
    else:
        return {'backgroundColor' : 'rgb(' + str(r) + ',' + str(g) + ',' 
                                         + str(b) + ')', 'color' : 'rgb(' + str(r) 
                                         + ',' + str(g) + ',' + str(b) + ')' }  

@app.callback(
    dash.dependencies.Output('rInput', component_property = 'value'),
    [dash.dependencies.Input('colorDrop', 'value')],
    [dash.dependencies.State('colorFinal', 'children')]
)
def rCallback(dataset, colors):
    """Callback to set initial value of red slider from dict

    Positional arguments:
    dataset -- currently selected dataset
    colors -- dictionary containing the color values(json string)
    """
    
    colorsDict = json.loads(colors)
    try:
        colorVal = colorsDict[dataset][4:-1].split(',')[0]
        return int(colorVal)
    except KeyError:
        return 0

@app.callback(
    dash.dependencies.Output('gInput', component_property = 'value'),
    [dash.dependencies.Input('colorDrop', 'value')],
    [dash.dependencies.State('colorFinal', 'children')]
)
def gCallback(dataset, colors):
    """Callback to set initial value of green slider from dict

    Positional arguments:
    dataset -- currently selected dataset
    colors -- dictionary containing the color values(json string)
    """
    colorsDict = json.loads(colors)
    try:
        colorVal = colorsDict[dataset][4:-1].split(',')[1]
        return int(colorVal)
    except KeyError:
        return 0

@app.callback(
    dash.dependencies.Output('bInput', component_property = 'value'),
    [dash.dependencies.Input('colorDrop', 'value')],
    [dash.dependencies.State('colorFinal', 'children')]
)
def bCallback(dataset, colors):
    """Callback to set initial value of blue slider from dict

    Positional arguments:
    dataset -- currently selected dataset
    colors -- dictionary containing the color values(json string)
    """
    colorsDict = json.loads(colors)
    try:
        colorVal = colorsDict[dataset][4:-1].split(',')[2]
        return int(colorVal)
    except KeyError:
        return 0
@app.callback(
    dash.dependencies.Output('colorFinal', component_property = 'children'),
    [dash.dependencies.Input('colorConfirm', 'n_clicks')],
    [dash.dependencies.State('rInput', 'value'),
     dash.dependencies.State('gInput', 'value'),
     dash.dependencies.State('bInput', 'value'),
     dash.dependencies.State('colorDrop', 'value'),
     dash.dependencies.State('colorFinal', 'children')]
)
def conFirmColor(nclicks, r, g, b, dataset, backup):
    """ Callback to confirm a color. This will overwrite the previous one.
    
    Positional arguments:
    nclicks -- button
    r -- red value
    g -- green value
    b -- blue value
    dataset -- dataset to overwrite color of
    backup -- previous value in case of error
    """
    if r == None or b == None or g == None:
        return backup
    else:
        colorDict = json.loads(backup)
        colorString = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        colorDict.update({dataset : colorString})
        return json.dumps(colorDict)

@app.callback(
    dash.dependencies.Output('colorDiv', component_property = 'children'),
    [dash.dependencies.Input('rInput', 'value'),
     dash.dependencies.Input('gInput', 'value'),
     dash.dependencies.Input('bInput', 'value')],
    [dash.dependencies.State('colorDrop', 'value'),
     dash.dependencies.State('colorDiv', 'children')]
)
def changeColor(r, g, b, dataset, oldColors):
    """Callback to set new color values and save them as json string

    Positional arguments:
    r -- red value
    g -- green value
    b -- blue value
    dataset -- currently selected dataset
    oldColors -- previous colors in case none values are provided for r/g/b
    """
    if r == None or b == None or g == None:
        return oldColors
    else:
        colorDict = json.loads(oldColors)
        colorString = 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        colorDict.update({dataset : colorString})
        return json.dumps(colorDict)

@app.callback(
    dash.dependencies.Output('headline', component_property = 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def setHeadline(clicks, name):
    """Callback to set the headline

    Positional arguments:
    clicks -- related to button, not needed otherwise
    name -- name of the currently selected gene
    """
    for i in geneAnnotations:
        currentGene = i[i['name'].str.contains(name)]
        if not currentGene.empty:
            break
    strand = currentGene['strand'].any() 
    title = name + ' (' + strand + ')'
    return title

@app.callback(
    dash.dependencies.Output('rnaDescDiv', component_property = 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def rnaDesc(clicks, name):
    if descAvail:
        try:
            return [
                html.P(html.B('Gene description: ')),
                html.P(
                    geneDescriptions.loc[
                        geneDescriptions['ensembl_gene_id'] == name,
                        ['description']
                    ].iloc[0]
                )
            ]
        except IndexError:
            return ['No description available']
    else:
        return['No description available']



@app.callback(
dash.dependencies.Output('spliceGraph', 'figure'),
    [dash.dependencies.Input('submit', 'n_clicks'),
     dash.dependencies.Input('colorConfirm', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value'),
    dash.dependencies.State('paramList', 'values'),
    dash.dependencies.State('sequenceRadio','value'),
    dash.dependencies.State('colorDiv', 'children')]
)
def rnaPlot(clicks, clicks2, geneName, dataSets, seqDisp, colors):
    """Main callback that handles the dynamic visualisation of the rnaSeq data

        Positional arguments:
        clicks -- Needed to trigger callback with button, not needed otherwise
        geneName -- Name of the selected gene in order to filter the data
        dataSets -- Selected data tracks with raw binding site data
        seqDisp -- Display mode for dna sequence trace
        """


    #Sort the list of selected data tracks to keep consistent order
    for i in sortKeys:
        try:
            dataSets.sort(key = eval(i[0],{'__builtins__':None},{}), reverse = eval(i[1],{'__builtins__':None},{}))
        except:
            print('Please check your keys. Each key should be added similar to this: -k \'lambda x : x[-2:]\' \'False\'	. For multiple keys use multiple instances of -k')
    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break

    # calculate gene models. We have to distinguish between coding region and non-coding region
    for i in currentGene.iterrows():

        # dict of dictionaries. data set name as key, posScoreDict as value.
        total_posScores = {}
        maxScore = 0
        color_dict = {} # color per mutant
        colors = ['#B8860B', '#DAA520 ', '#BDB76B ', '#808000 ']
        color_index = 0
        for ds in sorted(spliceProcDFs.keys()):
            if ds.split('_')[0] not in color_dict.keys():
                color_dict[ds.split('_')[0]] = colors[color_index]
                color_index += 1
            posScore = {}
            for index, row in spliceProcDFs[ds].iterrows():
                chrom = row['chrom']
                chromStart = row['chromStart']
                chromEnd = row['chromEnd']
                spliceType = row['type']
                score = row['score']
                strand = row['strand']
                if (chromStart >= i[1]['chromStart']) and (chromEnd <= i[1]['chromEnd']):
                    for posExon in range(chromStart, chromEnd):
                        if posExon in posScore.keys():
                            posScore[posExon] += 1
                        else:
                            posScore[posExon] = 1
            if posScore.values():
                if maxScore < max(posScore.values()):
                    maxScore = max(posScore.values())
            else:
                maxScore = 3
            for null_pos in range(i[1]['chromStart'], i[1]['chromEnd']):
                if null_pos not in posScore.keys():
                    posScore[null_pos] = 0
            total_posScores[ds] = posScore
    fig = createAreaChart(total_posScores, maxScore, color_dict)


    return fig

def createAreaChart(total_posScores, maxScore, color_dict):
    data = []
    for ds in sorted(total_posScores.keys()):
        xAxis = []
        yAxis = []
        organism = ds.split('_')[0]
        org_color = color_dict[organism]
        posScore = total_posScores[ds]
        for pos in sorted(posScore.keys()):
            xAxis.append(pos)
            yAxis.append(posScore[pos])
        trace = go.Scatter(
            x=xAxis,
            y=yAxis,
            name= ds,
            fill='toself',
            fillcolor=org_color,
            hoveron='points+fills',
            line=dict(color='black'),
            text=ds,
            hoverinfo='y'
        )
        data.append(trace)
    fig = tools.make_subplots(rows=len(data), cols=1)
    for index, t in enumerate(data):
        fig.append_trace(t, index+1, 1)
    fig['layout']['height'] = 1000 + (100 * maxScore)

    return fig


@app.callback(
    dash.dependencies.Output('descDiv', component_property = 'children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def setDesc(clicks, name):
    """Callback to update gene description

    Positional arguments:
    clicks -- related to button, not needed in code
    name -- name of the currently selected gene
    """
    if descAvail:
        try:
            return [
                html.P(html.B('Gene description: ')),
                html.P(
                    geneDescriptions.loc[
                        geneDescriptions['ensembl_gene_id'] == name,
                        ['description']
                    ].iloc[0]
                )
            ]
        except IndexError:
            return ['No description available']
    else:
        return['No description available']

@app.callback(
    dash.dependencies.Output('bsGraph', 'figure'),
    [dash.dependencies.Input('submit', 'n_clicks_timestamp'),
     dash.dependencies.Input('colorConfirm', 'n_clicks_timestamp')],
    [dash.dependencies.State('geneDrop', 'value'),
    dash.dependencies.State('paramList', 'values'),
    dash.dependencies.State('sequenceRadio','value'),
    dash.dependencies.State('colorDiv', 'children'),
    dash.dependencies.State('colorFinal', 'children')]
)
def concPlot(submit, confirm, geneName, dataSets, seqDisp, colors, colorsFinal):
    """Main callback that handles the dynamic visualisation of selected data
    
    Positional arguments:
    submit -- submit button time stamp
    confirm -- confirm button time stamp
    geneName -- Name of the selected gene in order to filter the data
    dataSets -- Selected data tracks with raw binding site data
    seqDisp -- Display mode for dna sequence trace
    colors -- color currently being confirmed. Needed to to lack of order on callbacks
    colorsFinal -- last confirmed color
    """
    
    if submit > confirm:
        colors = colorsFinal
    else:
        colors = colors
    #Sort the list of selected data tracks to keep consistent order
    for i in sortKeys:
        try:
            dataSets.sort(key = eval(i[0],{'__builtins__':None},{}), reverse = eval(i[1],{'__builtins__':None},{}))
        except:
            print('Please check your keys. Each key should be added similar to this: -k \'lambda x : x[-2:]\' \'False\'	. For multiple keys use multiple instances of -k') 
    numParams = len(dataSets) # number of selected data tracks
    rowOffset = 4 #relative size of data tracks compared to gene model tracks
    baseHeight = 30 # size of gene model row, for plot scaling
    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break
    # row heights and spacing
    if rawAvail == True:
        rawDataRows = numParams * rowOffset
    else:
        rawDataRows = 0
    if procAvail == True and rawDataRows > 0:
        procDataRows = numParams * 0.5
    else:
        procDataRows = 0
    numRowsW = rawDataRows + procDataRows + (len(currentGene)) + 1 # Big data rows + significant sites + isoforms + sequence
    numRows = numParams * dsElements + len(currentGene) + 1 # number of rows without weights for specific sizes, +1 for dna sequence track
    plotSpace = 0.8 #Room taken up by data tracks
    spacingSpace = 1.0 - plotSpace # room left for spacing tracks
    rowHeight = plotSpace / numRowsW
    if numRows > 1:
        vSpace = spacingSpace / (numRows - 1)
    else:
        vSpace = spacingSpace

    # final height values for rows respecting type, has to be in bottom-up order
    dataSetHeights = []
    if procAvail == True:
        dataSetHeights.append(rowHeight / 2)
    if rawAvail == True:
        dataSetHeights.append(rowHeight * rowOffset)
    rowHeights = [rowHeight] * len(currentGene) + dataSetHeights * numParams + [rowHeight] 
    nameList = currentGene['name'].tolist() # used for gene model titles
    fig = tools.make_subplots(rows = numRows,cols = 1,shared_xaxes = True, vertical_spacing = vSpace,row_width = rowHeights)
    fig['layout']['xaxis'].update(nticks = 6)
    fig['layout']['xaxis'].update(tickmode = 'array')
    fig['layout']['xaxis'].update(showgrid = True)
    fig['layout']['xaxis'].update(ticks = 'outside')
    fig['layout']['xaxis'].update(ticksuffix = 'b')
    fig['layout'].update(hovermode = 'x')
    
    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    strand = currentGene['strand'].any()
    # setup some variables to build master sequence from isoform-sequences
    if ensembl == False:
         if len(currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('_')) > 1:
             nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('.')[1].replace('_','.')
             nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name'].split('.')[1].replace('_','.')
         else:
             nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name']
             nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name']
    else:
         if len(currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('_')) > 1:
             nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('.')[1].replace('_','.')
             nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name'].split('.')[1].replace('_','.')
         else:
             nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name']
             nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name']
    rightStart = currentGene.loc[currentGene['chromEnd'].idxmax()]['chromStart']
    leftEnd = currentGene.loc[currentGene['chromStart'].idxmin()]['chromEnd']
    combinedSeq = ''

    if rightStart <= leftEnd: # left and right sequence have overlap, we don't need more parts to create master
        for i in sequences:
            try: 
                combinedSeq = str(i[nameLeftSeq].seq)+str(i[nameRightSeq].seq)[(leftEnd-rightStart):]
            except KeyError:
                pass
    else: # try to create master sequence by piecing together more than two sequences
        for i in sequences:
            try:
                currentSequenceSet = i
                break
            except KeyError:
                pass
        try:
            combinedSeq = str(currentSequenceSet[nameLeftSeq].seq)
            currentEnd = leftEnd
            for i in currentGene.iterrows():
                if i[1]['chromEnd'] > currentEnd:
                    if i[1]['chromStart'] <= currentEnd:
                        combinedSeq += str(currentSequenceSet[i[1]['name']].seq)[(currentEnd-i[1]['chromStart']):]
                        currentEnd = i[1]['chromEnd']
                if currentEnd >= xAxisMax:
                    break
            if currentEnd < rightStart: # Case that there is a gap between leftmost and rightmost sequence.
                fillerDist = rightStart-currentEnd
                combinedSeq += ['']*fillerDist
                combinedSeq += str(currentSequenceSet[nameRightSeq].seq)
        except KeyError:
            pass    

    try: # create traces for sequence display, either scatter or heatmap
        traces = generateSequenceTrace(seqDisp, strand, combinedSeq, xAxisMin, xAxisMax)
        for i in traces:
            fig.append_trace(i, 1, 1)
    except IndexError:
        pass
    except TypeError:
        pass
     #       pass



    chrom = currentGene['chrom'].any() # save strand info, necessary for arrow annotations. Should be same for all isoforms, so any will do
    chromEnds = [] # used for arrow positioning
    
    counter = 2
    for i in range(len(dataSets)):
        bsTraces = plotRaw(dataSets[i], xAxisMax, xAxisMin, chrom, strand, colors)# plot Binding site data
        fig.append_trace(bsTraces[0], counter, 1)
        if len(bsTraces[1]) > 0:
            for j in range(len(bsTraces[1])):
                fig.append_trace(bsTraces[1][j], counter + 1, 1)
        counter += dsElements

    
    # calculate gene models. We have to distinguish between coding region and non-coding region 
    for i in currentGene.iterrows():
        # setup various helpers to work out the different sized blocks
        chromEnds.append(i[1]['chromEnd'])
        blockStarts = [int(x) for x in i[1]['blockStarts'].rstrip(',').split(',')]
        blockSizes = [int(x) for x in i[1]['blockSizes'].rstrip(',').split(',')]
        genemodel = generateGeneModel(int(i[1]['chromStart']), int(i[1]['thickStart']), int(i[1]['thickEnd']-1), blockStarts, blockSizes, 
            0.4, i[1]['name']) 
        for j in range(len(genemodel)):
            fig.append_trace(genemodel[j], counter, 1) 
        # move on to the next gene model
        counter += 1


    # the trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode = 'relative',
        margin = go.layout.Margin(l = 30,r = 40,t = 25,b = 60),
    )
    fig['layout']['yaxis'].update(visible = False, showticklabels = False, showgrid = False, zeroline = False)
    if procAvail:
        for i in range(0, numParams * dsElements, 2):
             fig['layout']['yaxis' + str(i + 3)].update(showticklabels = False, showgrid = False, zeroline = False)
    arrows = [] # adding a whole list of annotations has better performance than adding them one by one
    for i in range(len(currentGene)):# edit all y axis in gene model plots
        fig['layout']['yaxis' + str(i + numParams * dsElements + 2)].update(showticklabels = False, showgrid = False, zeroline = False)   
        arrows.append(
            dict(
                x = chromEnds[i] + min(50,(xAxisMax-xAxisMin)*0.01),
                y = 0.0,
                xref = 'x',
                yref = 'y' + str(i + numParams * dsElements + 2),
                text = '',
                showarrow = True,
                arrowhead = 1,
                ax = -int(strand + '5'),#determine arrow direction. - strand left, + strand right
                ay = 0
            ),
        )
    fig['layout']['annotations'] = arrows               
    for i in range(numRows+1): #prevent zoom on y axis
        if i == 0:
            fig['layout']['yaxis'].update(fixedrange = True)
        else:
            fig['layout']['yaxis' + str(i)].update(fixedrange = True)
    # set correct graph height based on row number and type
    fig['layout']['height'] = (baseHeight * rawDataRows
                              + baseHeight * procDataRows 
                              + baseHeight * (len(currentGene) + 1) 
                              + 80)
    return fig

def plotRaw(name, xMax, xMin, chrom, strand, colors):
    """Helper method to plot the subplots containing raw binding site data
    
    Positional arguments:
    name -- name of the subplot to create a title
    xMax -- maximum x-axis value, used to select relevant data
    xMin -- minimum x-axis value
    chrom -- the chromosome we are looking for data on
    strand -- strand the gene is on, to look for correct binding sites
    colors -- json color string
    """
    colors = json.loads(colors)
    # selection criteria
    crit1 = bsRawDFs[name]['chrom'] == chrom
    crit21 = bsRawDFs[name]['chromStart'] >= xMin
    crit22 = bsRawDFs[name]['chromStart'] <= xMax
    crit31 = bsRawDFs[name]['chromEnd'] >= xMin
    crit32 = bsRawDFs[name]['chromEnd'] <= xMax
    rawSites = bsRawDFs[name].loc[crit1 & ((crit21 & crit22) | (crit31 & crit32))]
    # setup arrays to hold the values that will be needed for plotting
    countsX = []
    countsY = []
    countsW = []
    for i in rawSites.iterrows():
        countsX.append(i[1]['chromStart'])
        countsY.append(i[1]['count'])
        countsW.append(i[1]['chromEnd'] - i[1]['chromStart'])
    # plot data
    rawTrace = go.Bar(
        x = countsX,
        y = countsY,
        width = countsW,
        hoverinfo = 'x+y',
        name = name,
        marker = go.bar.Marker(
            color = colors[name]
        ),
        showlegend = True
    )

    # setup criteria to select binding sites that are within the current region of the genome
    procSitesList = []
    try:
        bcrit11 = bsProcDFs[name]['chrom'] == chrom
        bcrit12 = bsProcDFs[name]['strand'] == strand
        bcrit21 = bsProcDFs[name]['chromStart'] >= xMin
        bcrit22 = bsProcDFs[name]['chromStart'] <= xMax
        bcrit31 = bsProcDFs[name]['chromEnd'] >= xMin
        bcrit32 = bsProcDFs[name]['chromEnd'] <= xMax
        bindingSites = bsProcDFs[name].loc[bcrit11 & bcrit12 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
    # plot binding sites

        for k in bindingSites.iterrows():
                procSitesList.append(
                    go.Bar(
                        opacity = 0.5,
                        x = [k[1]['chromStart'] + (k[1]['chromEnd'] - k[1]['chromStart']) // 2],
                        y = [0.1],
                        hoverinfo = 'name',
                        width = k[1]['chromEnd'] - k[1]['chromStart'],
                        name = 'binding sites',
                        marker = go.bar.Marker(
                            color = colorMap[name]
                        ), showlegend = False
                    )
                )
    except KeyError:
        pass                    
    except Exception as e:
        print('Error in binding plot: ' + str(type(e).__name__) + str(e.args))
    return [rawTrace, procSitesList]

def generateGeneModel(chromStart, codingRegionStart, codingRegionEnd, blockStarts, blockSizes, blockHeight, name):
    """Generates gene model based on the given blocks and coding region
    
    Positional arguments:
    chromStart -- start of the chromosome, needed to offfset block values
    codingRegionStart -- start of the coding or thick region
    codingRegionEnd -- end of the coding or thick region
    blockStarts -- list of block startpoints, these are relative to ChromStart
    blockSizes -- lengths of the various blocks
    blockHeight -- height for the blocks, thin regions are drawn with half height
    name -- name for the trace
    """

    blockVals = []
    blockWidths = []
    blockYs = []
    for j in range(len(blockStarts)):
        blockStart = chromStart + blockStarts[j]
        blockEnd = chromStart + blockStarts[j] + blockSizes[j]-1 # same as codingRegionEnd
        if (blockStart >= codingRegionStart) & (blockEnd <= codingRegionEnd):
            blockVals.append(blockStart + (blockEnd - blockStart) / 2)
            blockWidths.append(blockEnd - blockStart + 1) 
            blockYs.append(blockHeight)
        if (blockStart >= codingRegionStart) & (blockEnd > codingRegionEnd):
            if (blockStart >= codingRegionEnd):
                blockVals.append(blockStart + (blockEnd - blockStart) / 2)
                blockWidths.append(blockEnd - blockStart + 1) 
                blockYs.append(blockHeight / 2)           
            else:
                blockVals.append(blockStart + (codingRegionEnd - blockStart) / 2)
                blockWidths.append(codingRegionEnd - blockStart + 1) 
                blockYs.append(blockHeight)
                blockVals.append(codingRegionEnd + (blockEnd - codingRegionEnd) / 2)
                blockWidths.append(blockEnd - codingRegionEnd + 1) 
                blockYs.append(blockHeight / 2)
        if (blockStart < codingRegionStart) & (blockEnd <= codingRegionEnd):
            if blockEnd <= codingRegionStart:
                blockVals.append(blockStart + (blockEnd - blockStart) / 2)
                blockWidths.append(blockEnd - blockStart + 1) 
                blockYs.append(blockHeight / 2)           
            else:
                blockVals.append(blockStart + (codingRegionStart - blockStart) / 2)
                blockWidths.append(codingRegionStart - blockStart + 1)
                blockYs.append(blockHeight / 2)
                blockVals.append(codingRegionStart + (blockEnd - codingRegionStart) / 2)
                blockWidths.append(blockEnd - codingRegionStart + 1)
                blockYs.append(blockHeight)
        if (blockStart < codingRegionStart) & (blockEnd > codingRegionEnd):
            blockVals.append(blockStart + (codingRegionStart - blockStart) / 2)
            blockWidths.append(codingRegionStart - blockStart + 1)
            blockYs.append(blockHeight / 2)
            blockVals.append(codingRegionStart + (codingRegionEnd - codingRegionStart) / 2)
            blockWidths.append(codingRegionEnd - codingRegionStart + 1) 
            blockYs.append(blockHeight)
            blockVals.append(codingRegionEnd + (blockEnd - codingRegionEnd) / 2)
            blockWidths.append(blockEnd-codingRegionEnd + 1) 
            blockYs.append(blockHeight / 2)

    f = lambda i: blockVals[i]
    amaxBlockVals = max(range(len(blockVals)), key = f)
    aminBlockVals = min(range(len(blockVals)), key = f)
    line = go.Scatter(
            x = [blockVals[aminBlockVals]-blockWidths[aminBlockVals]/2,
                 blockVals[amaxBlockVals]+blockWidths[amaxBlockVals]/2],
            y = [0,0],
            name = '',
            hoverinfo = 'none',
            mode = 'lines',
            line = dict(
                    color = 'rgb(0, 0, 0)',
                    ),
            showlegend = False,
            legendgroup = name.split('.')[-1]
            )
    upper = go.Bar(
            x = blockVals,
            y = blockYs,
            name = '',
            hoverinfo = 'none',
            width = blockWidths,
            marker = go.bar.Marker(
                color = 'rgb(0, 0, 0)'
            ),
            showlegend = False,
            legendgroup = name.split('.')[-1]
        )
    lower = go.Bar(
            x = blockVals,
            name = name.split('.')[-1],
            hoverinfo = 'name',
            hoverlabel = {
                    'namelength' : -1,},
            y = [-x for x in blockYs],
            width = blockWidths,
            marker = go.bar.Marker(
                color = 'rgb(0, 0, 0)'
            ),
            showlegend = True,
            legendgroup = name.split('.')[-1]
        )
    # return traces for gene model
    return [line, upper, lower]

def generateSequenceTrace(seqDisp, strand, combinedSeq, xAxisMin, xAxisMax):
    """ Method to generate sequence display trace, either heatmap or scatter
    
    Positional arguments:
    seqDisp -- determines which trace type is used
    strand -- if on minus strand invert dna sequence
    combinedSeq -- sequence for display
    xAxisMin -- startpoint
    xAxisMax -- endpoit
    """
    
    if seqDisp == 'letterSeq':
        xA = []
        xC = []
        xG = []
        xT = []
        Err = []
        if strand == '+':
             varMap = {'A' : xA, 'C' : xC, 'G' : xG, 'T' : xT}
        else: # reverse complement
             varMap = {'A' : xT, 'C' : xG, 'G' : xC, 'T' : xA}            
        for i in range(xAxisMin,xAxisMax):
            try:
                varMap[combinedSeq[i-xAxisMin]].append(i)
            except KeyError:
                Err.append(i)
        aTrace = go.Scatter(
            text = ['A']*len(xA),
            textfont = dict(color = colorA),
            mode = 'text',
            y = [1]*len(xA),
            x = xA,
            showlegend = False,
            opacity = 0.5,
            hoverinfo = 'x',
            textposition = "bottom center"
        )
        cTrace = go.Scatter(
            text = ['C']*len(xC),
            mode = 'text',
            textfont = dict(color = colorC),
            y = [1]*len(xC),
            x = xC,
            showlegend = False,
            opacity = 0.5,
            hoverinfo = 'x',
            textposition = "bottom center"     
        )
        gTrace = go.Scatter(
            text = ['G']*len(xG),
            textfont = dict(color = colorG),
            mode = 'text',
            y = [1]*len(xG),
            x = xG,
            showlegend = False,
            opacity = 0.5,
            hoverinfo = 'x',
            textposition = "bottom center"
        )
        tTrace = go.Scatter(
            text = ['T']*len(xT),
            textfont = dict(color = colorT),
            mode = 'text',
            y = [1]*len(xT),
            x = xT,
            showlegend = False,
            opacity = 0.5,
            hoverinfo = 'x',
            textposition = "bottom center"
        )
        errorTrace = go.Scatter(
            text = ['N']*len(Err),
            textfont = dict(color = 'rgb(0,0,0)'),
            mode = 'text',
            y = [1]*len(Err),
            x = Err,
            showlegend = False,
            opacity = 0.5,
            hoverinfo = 'x',
            textposition = "bottom center"
        )
        return [aTrace, cTrace, gTrace, tTrace, errorTrace]
    if seqDisp == 'heatSeq':
        colorE = 'rgb(0, 0, 0)'
        if strand == '+':
             valMap = {'A' : 0, 'C' : 2, 'G' : 3, 'T' : 1}
             textMap = {'A' : 'A', 'C' : 'C', 'G' : 'G', 'T' : 'T'}
        else: # reverse complement
             valMap = {'A' : 1, 'C' : 3, 'G' : 2, 'T' : 0}
             textMap = {'A' : 'T', 'C' : 'G', 'G' : 'C', 'T' : 'A'}
        zlist = []
        textList = []
        errorsPresent = False
        for i in range(xAxisMin,xAxisMax):
            try:
                zlist.append(valMap[combinedSeq[i-xAxisMin]])
                textList.append(textMap[combinedSeq[i-xAxisMin]])
            except KeyError:
                errorsPresent = True
                zlist.append(4)
                textList.append('N')
        if errorsPresent == True:
            colors =  [
                [0,colorA],
                [0.2,colorA],
                [0.2,colorT],
                [0.4,colorT],
                [0.4,colorC],
                [0.6,colorC],
                [0.6,colorG],
                [0.8,colorG],
                [0.8,colorE],
                [1.0,colorE]
            ]
        else:
             colors = [
                [0,colorA],
                [0.25,colorA],
                [0.25,colorT],
                [0.5,colorT],
                [0.5,colorC],
                [0.75,colorC],
                [0.75,colorG],
                [1.0,colorG]
            ]
        
        heatTrace = go.Heatmap(
            z = [zlist],
            x = list(range(xAxisMin,xAxisMax)),
            text = [textList],
            colorscale = colors,
            showscale = False,
            hoverinfo = 'x+text',
            colorbar = {
                'tick0' : 0,
                'dtick' : 1
            }
        )
        return [heatTrace]


if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = port, use_reloader = False)
