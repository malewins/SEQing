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

__author__ = "Yannik Bramkamp"

if 'dropList' not in globals():
    print('Please start the program via validator.py')
    exit()

# Set defaults if no advanced descriptions are available
if advancedDesc is None:
    advList = []
    advStart = None
    advAvailable = True
else:
    advList = list(advancedDesc.columns.values)
    advList.remove('gene_ids')
    try:
        advStart = advList[0]
        advAvailable = False
    except:
        advStart = None
        advAvailable = True


# Hide sequence related controls if no sequence data is available
if len(sequences) == 0:
    seqDispStyle = {'display': 'none'}
else:
    seqDispStyle = {'width': '20vw', 'display': 'table-cell'}

# Try to setup color picker
try:
    initialColor = dataSetNames[0]
    disableSettings = False
except:
    initialColor = None
    disableSettings = True


# default tab style
tabStyle = {'padding' : '0', 'line-height' : '5vh'}
#colors for the alternating coloring in Details
tableColors = ['rgb(255, 255 ,255)', 'rgb(125, 244, 66)']

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(id='headline', children='Report'),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id='geneDrop',
                                    options=[{'label': i[0], 'value': i[1]} for i in dropList],
                                    value=dropList[0][1]
                                )
                            ],
                            style={'width': '70vw', 'display': 'table-cell', 'verticalalign': 'middle'}
                        ),
                        html.Div(
                            style={'width': '1vw', 'display': 'table-cell', 'verticalalign': 'middle'}
                        ),
                        html.Div(
                            children=[
                                html.Button(id='submit', n_clicks=0, n_clicks_timestamp=0, children='Submit')
                            ],
                            style={'width': '8vw', 'display': 'table-cell', 'verticalalign': 'middle'}
                        )
                    ]
                ),
                dcc.Tabs(
                    id='tabs',
                    style={
                        'width': '50%',
                        'height': '5vh'
                    },
                    children=[
                        dcc.Tab(
                            label='iCLIP data',
                            style=tabStyle,
                            selected_style=tabStyle,
                            id='clipTab',
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                dcc.Checklist(
                                                    id='paramList',
                                                    options=[{'label': i, 'value': i} for i in dataSetNames],
                                                    values=[i for i in dataSetNames]
                                                )
                                            ],
                                            style={'width': '10vw', 'display': 'table-cell'}
                                        ),
                                        html.Div(
                                            children=html.P(html.B('Gene description: ')),
                                            id='descDiv',
                                            style={'width': '58vw', 'display': 'table-cell'}
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.RadioItems(
                                                    id='sequenceRadio',
                                                    options=[
                                                        {'label': 'Do not show dna sequence', 'value': 'noSeq'},
                                                        {'label': 'Show dna sequence as letters', 'value': 'letterSeq'},
                                                        {'label': 'Show dna sequence as heatmap', 'value': 'heatSeq'}
                                                    ],
                                                    value='heatSeq'
                                                )
                                            ],
                                            style=seqDispStyle
                                        )
                                    ]
                                ),
                                dcc.Graph(id='bsGraph'),
                                html.Div(
                                    children = [
                                        html.Div(id = 'advMem',
                                            style = {'display' : 'none'}
                                        )
                                    ]
                                )
                            ]
                        ),
                        dcc.Tab(
                            label='Details',
                            id='deTab',
                            style=tabStyle,
                            selected_style=tabStyle,
                            children=[
                                html.Div(
                                    id='detailMainDiv',
                                    children=[]
                                )
                            ]
                        ),
                        dcc.Tab(
                            label='RNASeq',
                            style=tabStyle,
                            selected_style=tabStyle,
                            id='rnaTab',
                            children=[
                                html.Div(
                                    children=[
                                        html.H2("RNA Seq data to identify splice events",
                                                style={"text-align": "center"}),
                                        html.P("The width shows how often"
                                               " this position turned out as exon in this "
                                               "specific experiment line.", style={"text-align": "center"})
                                    ]
                                ),
                                html.Div(
                                    children=[
                                        html.B('Data set: '),
                                        dcc.Checklist(
                                            id='rnaParamList',
                                            options=[{'label': spliceSetNames[1][i], 'value': spliceSetNames[1][i]} for
                                                     i in range(len(spliceSetNames[1]))],
                                            values=[spliceSetNames[1][i] for i in range(len(spliceSetNames[1]))],
                                        ),
                                    ],
                                    style={'width': '20vw', 'display': 'table-cell'}
                                ),

                                html.Div(
                                    children=html.P(html.B('Gene description: ')),
                                    id='rnaDescDiv',
                                    style={'width': '58vw', 'display': 'table-cell'}
                                ),

                                html.Div(
                                    children=[
                                        html.B('Display type: '),
                                        dcc.RadioItems(
                                            id='rnaRadio',
                                            options=[
                                                {'label': 'Display type 1', 'value': 'one'},
                                                {'label': 'Display type 2', 'value': 'two'},
                                                {'label': 'Display type 3', 'value': 'three'}
                                            ],
                                            value='one'
                                        )
                                    ],
                                    style={'width': '20vw', 'display': 'table-cell'}
                                ),
                                dcc.Graph(id='spliceGraph')
                            ]
                        ),
                        dcc.Tab(
                            label='Settings',
                            id='settings',
                            style=tabStyle,
                            selected_style=tabStyle,
                            disabled=disableSettings,
                            disabled_style=tabStyle,
                            children=[
                                html.Div(
                                    children=[
                                        html.Fieldset(title = 'iCLIP Settings', 
                                            style = {
                                                'border' : 'solid',
                                                'borderWidth' : '1px',
                                                'padding' : '10px',
                                                'borderColor' : 'rgb(128,128,128)'
                                            },
                                            children = [ 
                                                html.Legend('iCLIP Settings'),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='colorDiv',
                                                    children=json.dumps(colorMap)
                                                ),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='colorFinal',
                                                    children=json.dumps(colorMap)
                                                ),
                                                dcc.Dropdown(
                                                    id='colorDrop',
                                                    options=[{'label': i, 'value': i} for i in dataSetNames],
                                                    value=initialColor
                                                ),
                                                html.Div(
                                                    id='rDisp',
                                                    children=html.P(html.B('R: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='rInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='gDisp',
                                                    children=html.P(html.B('G: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='gInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='bDisp',
                                                    children=html.P(html.B('B: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='bInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.Div(id='preview',
                                                                 children=html.P(html.B('Preview')),
                                                                 style={'width': '30vw', 'display': 'table-cell',
                                                                        'verticalalign': 'middle'}
                                                                 ),
                                                        html.Div(
                                                            children=[
                                                                html.Button(id='colorConfirm', n_clicks_timestamp=0,
                                                                            children='confirm')
                                                            ],
                                                            style={'width': '10vw', 'display': 'table-cell',
                                                                   'verticalalign': 'middle'}
                                                        )
                                                    ],
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                )
                                            ]
                                        )
                                    ],
                                    style={'width': '30vw', 'display': 'table-cell', 'verticalalign': 'middle'}
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
    dash.dependencies.Output('advMem', component_property='children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def storeDesc(nclicks, geneName):
    """ Save description data to hidden div for display
    
    Positional arguments:
    nlicks -- button parameter
    geneName -- name of the currently selected gene
    """
    
    if advancedDesc is not None:
        df = advancedDesc[advancedDesc['gene_ids'].str.contains(geneName)]

        return df.to_json(orient = 'split')

@app.callback(
    dash.dependencies.Output('detailMainDiv', component_property = 'children'),
    [dash.dependencies.Input('advMem', 'children')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def showDetails(data, name):
    """ Create tabular view of additional data

    Positional arguments:
    data -- data for the current gene, as json string(dict)
    name -- gene name for initialization
    """
    try:
        df = pandas.read_json(data, orient='split')
    except ValueError:
        try:
            df = advancedDesc[advancedDesc['gene_ids'].str.contains(name)]
        except TypeError:
            df = pandas.DataFrame()
    columns = list(df.columns.values)
    rowCounter = 1  # keep track of the row number to alternate coloring
    usedColumns = []  # keeps track of preset columns already added, needed later
    usedColumns.append('gene_ids')
    content = []  # table content to be displayed
    generalColumns = ['symbol', 'brief_description', 'is_obsolete', 'computational_description',
                      'curator_summary', 'name']
    tableRows = []  # will contain the table rows
    for i in generalColumns:
        if i in columns and str(df.iloc[0][i]) not in ['nan', ';""']:
            tableRows.append(html.Tr(children=[html.Td(html.B(i.replace('_', ' ').title())),
                                               html.Td(str(df.iloc[0][i]).strip())],
                                     style={'background-color': tableColors[rowCounter % 2]}))
            usedColumns.append(i)
            rowCounter += 1
    # go through a number of predefined columns
    if 'synonyms' in columns:
        synonyms = str(df.iloc[0]['synonyms'])
        usedColumns.append('synonyms')
        if synonyms not in ['nan', ';""']:
            tableRows.append(createDetailRow(synonyms, 'synonyms', rowCounter))
            rowCounter += 1
    if 'publications' in columns:
        usedColumns.append('publications')
        publications = str(df.iloc[0]['publications'])
        if publications not in ['nan', ';""']:
            tableRows.append(createDetailRow(publications, 'publications', rowCounter))
            rowCounter += 1
    if 'proteins' in columns:
        usedColumns.append('proteins')
        proteins = str(df.iloc[0]['proteins'])
        if publications not in ['nan', ';""']:
            tableRows.append(createDetailRow(proteins, 'proteins', rowCounter))
            rowCounter += 1
    if 'gene_ontology' in columns:
        usedColumns.append('gene_ontology')
        geneOntology = str(df.iloc[0]['gene_ontology'])
        if geneOntology not in ['nan', ';""']:
            tableRows.append(createDetailRow(geneOntology, 'gene_ontology', rowCounter))
            rowCounter += 1
    if 'pathways' in columns:
        usedColumns.append('pathways')
        pathways = str(df.iloc[0]['pathways'])
        if pathways not in ['nan', ';""']:
            tableRows.append(createDetailRow(pathways, 'pathways', rowCounter))
            rowCounter += 1
    if 'plant_ontology' in columns:
        usedColumns.append('plant_ontology')
        plantOntology = str(df.iloc[0]['plant_ontology'])
        if plantOntology not in ['nan', ';""']:
            tableRows.append(createDetailRow(plantOntology, 'plant_ontology', rowCounter))
            rowCounter += 1
    # go through all remaining columns using formatting standard
    remainingColumns = [x for x in columns if x not in usedColumns]
    for i in remainingColumns:
        value = str(df.iloc[0][i])
        if value not in ['nan', ';""']:
            tableRows.append(createDetailRow(value, i, rowCounter))
            rowCounter += 1

    if len(tableRows) >= 1:
        content.append(html.Table(tableRows))
    else:
        content.append(html.B('No additional information available for the currently selected gene'))
    return content


@app.callback(
    dash.dependencies.Output('rDisp', component_property='children'),
    [dash.dependencies.Input('rInput', component_property='value')]
)
def showR(r):
    """Callback to display current value for red

    Positional arguments:
    r -- value for red
    """

    return html.P(html.B('R: ' + str(r)))


@app.callback(
    dash.dependencies.Output('gDisp', component_property='children'),
    [dash.dependencies.Input('gInput', component_property='value')]
)
def showG(g):
    """Callback to display current value for green

    Positional arguments:
    g -- value for green
    """

    return html.P(html.B('G: ' + str(g)))


@app.callback(
    dash.dependencies.Output('bDisp', component_property='children'),
    [dash.dependencies.Input('bInput', component_property='value')]
)
def showB(b):
    """Callback to display current value for blue

    Positional arguments:
    b -- value for blue
    """

    return html.P(html.B('B: ' + str(b)))


@app.callback(
    dash.dependencies.Output('preview', component_property='style'),
    [dash.dependencies.Input('rInput', 'value'),
     dash.dependencies.Input('gInput', 'value'),
     dash.dependencies.Input('bInput', 'value')]
)
def previewColor(r, g, b):
    """Callback for rgb color preview

    Positional arguments:
    r -- value for red
    g -- value for green
    b -- value for blue
    """

    if r == None or b == None or g == None:
        return {'backgroundColor': 'rgb(255, 255, 255)', 'color': 'rgb(255, 255, 255)'}
    else:
        return {'backgroundColor': 'rgb(' + str(r) + ',' + str(g) + ','
                                   + str(b) + ')', 'color': 'rgb(' + str(r)
                                                            + ',' + str(g) + ',' + str(b) + ')'}


@app.callback(
    dash.dependencies.Output('rInput', component_property='value'),
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
    dash.dependencies.Output('gInput', component_property='value'),
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
    dash.dependencies.Output('bInput', component_property='value'),
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
    dash.dependencies.Output('colorFinal', component_property='children'),
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
        colorDict.update({dataset: colorString})
        return json.dumps(colorDict)


@app.callback(
    dash.dependencies.Output('colorDiv', component_property='children'),
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
        colorDict.update({dataset: colorString})
        return json.dumps(colorDict)


@app.callback(
    dash.dependencies.Output('headline', component_property='children'),
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
    dash.dependencies.Output('rnaDescDiv', component_property='children'),
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
        return ['No description available']


@app.callback(
    dash.dependencies.Output('spliceGraph', 'figure'),
    [dash.dependencies.Input('submit', 'n_clicks'),
     dash.dependencies.Input('colorConfirm', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value'),
    dash.dependencies.State('paramList', 'values'),
     dash.dependencies.State('rnaParamList', 'values')]
)
def rnaPlot(clicks, clicks2, geneName, dataSets, rnaParamList):
    """Main callback that handles the dynamic visualisation of the rnaSeq data

        Positional arguments:
        clicks -- Needed to trigger callback with button, not needed otherwise
        geneName -- Name of the selected gene in order to filter the data
        seqDisp -- Display mode for dna sequence trace
        """

    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break



    # Get axis minimum and maximum over all isoforms. Also get current chromosome
    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    chrom = currentGene['chrom'].any()
    color_dict = {}  # color per mutant
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet',
              'red', 'orange', 'yellow', 'green', 'blue', 'violet',
              'red', 'orange', 'yellow', 'green', 'blue', 'violet',
              'red', 'orange', 'yellow', 'green', 'blue', 'violet']
    color_index = 0
    rnaDataSets = list(spliceProcDFs.keys())
    displayed_rnaDataSet = []
    for rm in rnaParamList:
        for set in rnaDataSets:
            if rm in set:
                displayed_rnaDataSet.append(set)

    # dicts for lists of axis values
    xVals = {}
    yVals = {}
    max_yVal = 0

    for ds in displayed_rnaDataSet:
        if ds.split('_')[0] not in color_dict.keys():
            color_dict[ds.split('_')[0]] = colors[color_index]
            color_index += 1
        # criteria to filter relevant lines from current dataframe
        bcrit11 = spliceProcDFs[ds]['chrom'] == chrom
        bcrit21 = spliceProcDFs[ds]['chromStart'] >= xAxisMin
        bcrit22 = spliceProcDFs[ds]['chromStart'] <= xAxisMax
        bcrit31 = spliceProcDFs[ds]['chromEnd'] >= xAxisMin
        bcrit32 = spliceProcDFs[ds]['chromEnd'] <= xAxisMax
        spliceSlice = spliceProcDFs[ds].loc[bcrit11 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
        # pre-init y-value list
        yVal = [0] * (len(range(xAxisMin, xAxisMax)))
        xVal = []
        # use itertuples to iterate over rows, since itertuples is supposed to be faster
        for row in spliceSlice.itertuples():
            # increment all values covered by the current row, will overshoot when row crosses border of gene, thus try except
            for j in range(row.chromStart, row.chromEnd):
                try:
                    yVal[j - xAxisMin] += row.count
                except IndexError:
                    pass
            # store reference to value list in dict
        yVals[ds] = yVal
        # create x-axis values
        xVal = list(range(xAxisMin, xAxisMax))
        xVals[ds] = xVal
        if max(yVal) > max_yVal: max_yVal = max(yVal)
    fig = createAreaChart(xVals, yVals, displayed_rnaDataSet, color_dict, dataSets, geneName)
    fig['layout']['height'] = (30 * (len(currentGene) + 1)
                               + 400)

    for i in range(1,len(displayed_rnaDataSet)):  # edit all y axis in gene model plots
        fig['layout']['yaxis' + str(i)].update(range=[0,max_yVal], showgrid=True)
    return fig


def createAreaChart(xVals, yVals, displayed, color_dict, dataSets, geneName):
    data = []
    subplot_titles = []
    for ds in displayed:
        xAxis = xVals[ds]
        yAxis = yVals[ds]
        organism = ds.split('_')[0]
        org_color = color_dict[organism]
        trace = go.Scatter(
            x=xAxis,
            y=yAxis,
            name=ds,
            fill='tozeroy',
            fillcolor=org_color,
            hoveron='points+fills',
            line=dict(color='black'),
            text=ds,
            hoverinfo='y',
            cliponaxis=True
        )
        # trace1 = go.Bar(
        #     x=xAxis,
        #     y=yAxis_events,
        #     width=yAxis_width,
        #     showlegend=False,
        #     text=yAxis_text,
        #     insidetextfont=dict(
        #         family="Arial",
        #         color="black"
        #     ),
        #     textposition='auto',
        #     marker=dict(
        #         color='yellow',
        #         line=dict(
        #             color='black',
        #             width=1),
        #     )
        # )
        subplot_titles.append(ds)
        # subplot_titles.append("")
        data.append(trace)
        # data.append(trace1)

    numRows = len(dataSets) * dsElements
    plotSpace = 0.8  # Room taken up by data tracks
    spacingSpace = 1.0 - plotSpace  # room left for spacing tracks
    rowHeight = plotSpace
    if numRows > 1:
        vSpace = spacingSpace / (numRows - 1)
    else:
        vSpace = spacingSpace


    for i in range(numRows):
        subplot_titles.append("")

    fig = tools.make_subplots(rows=len(data)+numRows, cols=1, subplot_titles=subplot_titles,
                              vertical_spacing=vSpace, shared_xaxes=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')
    fig['layout'].update(
        barmode='relative',
        margin=go.layout.Margin(l=30, r=40, t=25, b=60),
    )
    # if spliceAvail:
    #     for i in range(2, len(data) + 1):
    #         fig['layout']['yaxis' + str(i)].update(showticklabels=False, showgrid=False, zeroline=False)

    for index, t in enumerate(data):
        fig.append_trace(t, index + 1, 1)

    rnaSequencePlot(fig, geneName, dataSets)

    return fig



def rnaSequencePlot(fig, geneName, dataSets):
    """Callback that handles the dynamic visualisation of the rna data."""

    numParams = len(dataSets)  # number of selected data tracks
    baseHeight = 30  # size of gene model row, for plot scaling
    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break
    numRows = numParams * dsElements + len(
        currentGene) + 1  # number of rows without weights for specific sizes, +1 for dna sequence track


    # final height values for rows respecting type, has to be in bottom-up order
    dataSetHeights = []
    fig['layout']['xaxis'].update(nticks=6)
    fig['layout']['xaxis'].update(tickmode='array')
    fig['layout']['xaxis'].update(showgrid=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')
    fig['layout']['yaxis'].update(fixedrange=True)

    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    strand = currentGene['strand'].any()

    chromEnds = []  # used for arrow positioning

    counter = 1
    for i in range(len(dataSets)):
        counter += dsElements

    # calculate gene models. We have to distinguish between coding region and non-coding region
    for i in currentGene.iterrows():
        # setup various helpers to work out the different sized blocks
        chromEnds.append(i[1]['chromEnd'])
        blockStarts = [int(x) for x in i[1]['blockStarts'].rstrip(',').split(',')]
        blockSizes = [int(x) for x in i[1]['blockSizes'].rstrip(',').split(',')]
        genemodel = generateGeneModel(int(i[1]['chromStart']), int(i[1]['thickStart']), int(i[1]['thickEnd'] - 1),
                                      blockStarts, blockSizes,
                                      0.4, i[1]['name'])
        for j in range(len(genemodel)):
            fig.append_trace(genemodel[j], counter, 1)
            fig['layout']['yaxis'].update(visible=False, showticklabels=False, showgrid=False, zeroline=False)
            # move on to the next gene model
        counter += 1

    # the trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode='relative',
        margin=go.layout.Margin(l=30, r=40, t=25, b=60),
    )
    fig['layout']['yaxis'].update(visible=False, showticklabels=True, showgrid=False, zeroline=False)
    if strand == '-':
        fig['layout']['xaxis'].update(autorange='reversed')
    arrows = []  # adding a whole list of annotations has better performance than adding them one by one
    for i in range(len(currentGene)):  # edit all y axis in gene model plots
        fig['layout']['yaxis' + str(i + numParams * dsElements + 1)].update(showticklabels=False, showgrid=False,
                                                                            zeroline=False)
        arrows.append(
            dict(
                x=chromEnds[i] + min(50, (xAxisMax - xAxisMin) * 0.01),
                y=0.0,
                xref='x',
                yref='y' + str(i + numParams * dsElements + 1),
                text='',
                showarrow=True,
                arrowhead=1,
                ax=-int(strand + '5'),  # determine arrow direction. - strand left, + strand right
                ay=0
            ),
        )
    fig['layout']['annotations'] = arrows
    for i in range(len(dataSets)):  # prevent zoom on y axis
        if i == 0:
            fig['layout']['yaxis'].update(fixedrange=True)
        else:
            fig['layout']['yaxis' + str(i)].update(fixedrange=True)
    return fig


@app.callback(
    dash.dependencies.Output('descDiv', component_property='children'),
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
        return ['No description available']


@app.callback(
    dash.dependencies.Output('bsGraph', 'figure'),
    [dash.dependencies.Input('submit', 'n_clicks_timestamp'),
     dash.dependencies.Input('colorConfirm', 'n_clicks_timestamp')],
    [dash.dependencies.State('geneDrop', 'value'),
     dash.dependencies.State('paramList', 'values'),
     dash.dependencies.State('sequenceRadio', 'value'),
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
    
    # check which of the two triggering buttons was pressed last
    if submit > confirm:
        colors = colorsFinal
    else:
        colors = colors
        
    # Sort the list of selected data tracks to keep consistent order
    for i in sortKeys:
        try:
            dataSets.sort(key=eval(i[0], {'__builtins__': None}, {}), reverse=eval(i[1], {'__builtins__': None}, {}))
        except:
            print(
                'Please check your keys. Each key should be added similar to this: -k \'lambda x : x[-2:]\' \'False\'	. For multiple keys use multiple instances of -k')
    numParams = len(dataSets)  # number of selected data tracks
    rowOffset = 4  # relative size of data tracks compared to gene model tracks
    baseHeight = 30  # size of gene model row, for plot scaling
    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for elem in geneAnnotations:
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
    numRowsW = rawDataRows + procDataRows + (
        len(currentGene)) + 1  # Big data rows + significant sites + isoforms + sequence
    numRows = numParams * dsElements + len(
        currentGene) + 1  # number of rows without weights for specific sizes, +1 for dna sequence track
    plotSpace = 0.8  # Room taken up by data tracks
    spacingSpace = 1.0 - plotSpace  # room left for spacing tracks
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
    nameList = currentGene['name'].tolist()  # used for gene model titles
    fig = tools.make_subplots(rows=numRows, cols=1, shared_xaxes=True, vertical_spacing=vSpace, row_width=rowHeights)
    fig['layout']['xaxis'].update(nticks=6)
    fig['layout']['xaxis'].update(tickmode='array')
    fig['layout']['xaxis'].update(showgrid=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')

    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    strand = currentGene['strand'].any()
    if strand == '-':
        fig['layout']['xaxis'].update(autorange='reversed')
    # setup some variables to build master sequence from isoform-sequences
    if ensembl == False:
        if len(currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('_')) > 1:
            nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('.')[1].replace('_', '.')
            nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name'].split('.')[1].replace('_', '.')
        else:
            nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name']
            nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name']
    else:
        if len(currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('_')) > 1:
            nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name'].split('.')[1].replace('_', '.')
            nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name'].split('.')[1].replace('_', '.')
        else:
            nameRightSeq = currentGene.loc[currentGene['chromEnd'].idxmax()]['name']
            nameLeftSeq = currentGene.loc[currentGene['chromStart'].idxmin()]['name']
    rightStart = currentGene.loc[currentGene['chromEnd'].idxmax()]['chromStart']
    leftEnd = currentGene.loc[currentGene['chromStart'].idxmin()]['chromEnd']
    combinedSeq = ''

    if rightStart <= leftEnd:  # left and right sequence have overlap, we don't need more parts to create master
        for i in sequences:
            try:
                combinedSeq = str(i[nameLeftSeq].seq) + str(i[nameRightSeq].seq)[(leftEnd - rightStart):]
            except KeyError:
                pass
    else:  # try to create master sequence by piecing together more than two sequences
        for i in sequences:
            try:
                currentSequenceSet = i
                break
            except KeyError:
                pass
        try:
            combinedSeq = str(currentSequenceSet[nameLeftSeq].seq)
            currentEnd = leftEnd
            for i in currentGene.itertuples():
                if i.chromEnd > currentEnd:
                    if i.chromStart <= currentEnd:
                        combinedSeq += str(currentSequenceSet[i.name].seq)[(currentEnd - i.chromStart):]
                        currentEnd = i.chromEnd
                if currentEnd >= xAxisMax:
                    break
            if currentEnd < rightStart:  # Case that there is a gap between leftmost and rightmost sequence.
                fillerDist = rightStart - currentEnd
                combinedSeq += [''] * fillerDist
                combinedSeq += str(currentSequenceSet[nameRightSeq].seq)
        except KeyError:
            pass

    try:  # create traces for sequence display, either scatter or heatmap
        traces = generateSequenceTrace(seqDisp, strand, combinedSeq, xAxisMin, xAxisMax)
        for i in traces:
            fig.append_trace(i, 1, 1)
    except IndexError:
        pass
    except TypeError:
        pass
    #       pass

    # save strand info, necessary for arrow annotations. Should be same for all isoforms, so any will do
    chrom = currentGene['chrom'].any() 

    counter = 2
    for i in range(len(dataSets)):
        bsTraces = plotICLIP(dataSets[i], xAxisMax, xAxisMin, chrom, strand, colors)  # plot Binding site data
        fig.append_trace(bsTraces[0], counter, 1)
        if len(bsTraces[1]) > 0:
            for j in range(len(bsTraces[1])):
                fig.append_trace(bsTraces[1][j], counter + 1, 1)
        counter += dsElements

    # calculate gene models. We have to distinguish between coding region and non-coding region
    for i in currentGene.itertuples():
        # setup various helpers to work out the different sized blocks
        blockStarts = [int(x) for x in i.blockStarts.rstrip(',').split(',')]
        blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
        genemodel = generateGeneModel(int(i.chromStart), int(i.thickStart), int(i.thickEnd - 1),
                                      blockStarts, blockSizes,
                                      0.4, i.name)
        for j in range(len(genemodel)):
            fig.append_trace(genemodel[j], counter, 1)
            # move on to the next gene model
        counter += 1

    # the trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode='relative',
        margin=go.layout.Margin(l=30, r=40, t=25, b=60),
    )
    fig['layout']['yaxis'].update(visible=False, showticklabels=False, showgrid=False, zeroline=False)
    if procAvail:
        for i in range(0, numParams * dsElements, 2):
            fig['layout']['yaxis' + str(i + 3)].update(showticklabels=False, showgrid=False, zeroline=False)
    for i in range(len(currentGene)):  # edit all y axis in gene model plots
        fig['layout']['yaxis' + str(i + numParams * dsElements + 2)].update(showticklabels=False, showgrid=False,
                                                                            zeroline=False)
    for i in range(numRows + 1):  # prevent zoom on y axis
        if i == 0:
            fig['layout']['yaxis'].update(fixedrange=True)
        else:
            fig['layout']['yaxis' + str(i)].update(fixedrange=True)
    # set correct graph height based on row number and type
    fig['layout']['height'] = (baseHeight * rawDataRows
                               + baseHeight * procDataRows
                               + baseHeight * (len(currentGene) + 1)
                               + 80)
    return fig


def plotICLIP(name, xMax, xMin, chrom, strand, colors):
    """Helper method to plot the subplots containing iCLIP data
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
    for i in rawSites.itertuples():
        countsX.append(i.chromStart)
        countsY.append(i.count)
        countsW.append(i.chromEnd - i.chromStart)
    # plot data
    rawTrace = go.Bar(
        x=countsX,
        y=countsY,
        width=countsW,
        hoverinfo='x+y',
        name=name,
        legendgroup=name,
        marker=go.bar.Marker(
            color=colors[name]
        ),
        showlegend=True
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
        for k in bindingSites.itertuples():
                procSitesList.append(
                    go.Bar(
                        opacity = 0.5,
                        x = [k.chromStart + (k.chromEnd - k.chromStart) // 2],
                        y = [0.1],
                        hoverinfo = 'name',
                        legendgroup = name,
                        width = k.chromEnd - k.chromStart,
                        name = name + '_bs',
                        marker = go.bar.Marker(
                            color = colors[name]
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
    # calculte blocks from block start and end positions, as well as thickness
    for j in range(len(blockStarts)):
        blockStart = chromStart + blockStarts[j]
        blockEnd = chromStart + blockStarts[j] + blockSizes[j] - 1  # same as codingRegionEnd
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
            blockWidths.append(blockEnd - codingRegionEnd + 1)
            blockYs.append(blockHeight / 2)

    # find first and last block o draw line properly
    f = lambda i: blockVals[i]
    amaxBlockVals = max(range(len(blockVals)), key=f)
    aminBlockVals = min(range(len(blockVals)), key=f)
    line = go.Scatter(
        x=[blockVals[aminBlockVals] - blockWidths[aminBlockVals] / 2,
           blockVals[amaxBlockVals] + blockWidths[amaxBlockVals] / 2],
        y=[0, 0],
        name='',
        hoverinfo='none',
        mode='lines',
        line=dict(
            color='rgb(0, 0, 0)',
        ),
        showlegend=False,
        legendgroup=name.split('.')[-1]
    )
    upper = go.Bar(
        x=blockVals,
        y=blockYs,
        name=name.split('.')[-1],
        hoverinfo='none',
        width=blockWidths,
        marker=go.bar.Marker(
            color='rgb(0, 0, 0)'
        ),
        showlegend=False,
        legendgroup=name.split('.')[-1]
    )
    lower = go.Bar(
        x=blockVals,
        name=name.split('.')[-1],
        hoverinfo='name',
        hoverlabel={
            'namelength': -1, },
        y=[-x for x in blockYs],
        width=blockWidths,
        marker=go.bar.Marker(
            color='rgb(0, 0, 0)'
        ),
        showlegend=True,
        legendgroup=name.split('.')[-1]
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
            varMap = {'A': xA, 'C': xC, 'G': xG, 'T': xT}
        else:  # reverse complement
            varMap = {'A': xT, 'C': xG, 'G': xC, 'T': xA}
        for i in range(xAxisMin, xAxisMax):
            try:
                varMap[combinedSeq[i - xAxisMin]].append(i)
            except KeyError:
                Err.append(i)
        aTrace = go.Scatter(
            text=['A'] * len(xA),
            textfont=dict(color=colorA),
            mode='text',
            name='seqA',
            y=[1] * len(xA),
            x=xA,
            showlegend=False,
            opacity=0.5,
            hoverinfo='x',
            textposition="bottom center"
        )
        cTrace = go.Scatter(
            text=['C'] * len(xC),
            mode='text',
            textfont=dict(color=colorC),
            y=[1] * len(xC),
            x=xC,
            name='seqC',
            showlegend=False,
            opacity=0.5,
            hoverinfo='x',
            textposition="bottom center"
        )
        gTrace = go.Scatter(
            text=['G'] * len(xG),
            textfont=dict(color=colorG),
            mode='text',
            y=[1] * len(xG),
            name='seqG',
            x=xG,
            showlegend=False,
            opacity=0.5,
            hoverinfo='x',
            textposition="bottom center"
        )
        tTrace = go.Scatter(
            text=['T'] * len(xT),
            textfont=dict(color=colorT),
            mode='text',
            y=[1] * len(xT),
            name='seqT',
            x=xT,
            showlegend=False,
            opacity=0.5,
            hoverinfo='x',
            textposition="bottom center"
        )
        errorTrace = go.Scatter(
            text=['N'] * len(Err),
            textfont=dict(color='rgb(0,0,0)'),
            mode='text',
            name='seqN',
            y=[1] * len(Err),
            x=Err,
            showlegend=False,
            opacity=0.5,
            hoverinfo='x',
            textposition="bottom center"
        )
        return [aTrace, cTrace, gTrace, tTrace, errorTrace]
    if seqDisp == 'heatSeq':
        colorE = 'rgb(0, 0, 0)'
        if strand == '+':
            valMap = {'A': 0, 'C': 2, 'G': 3, 'T': 1}
            textMap = {'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T'}
        else:  # reverse complement
            valMap = {'A': 1, 'C': 3, 'G': 2, 'T': 0}
            textMap = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        zlist = []
        textList = []
        errorsPresent = False
        for i in range(xAxisMin, xAxisMax):
            try:
                zlist.append(valMap[combinedSeq[i - xAxisMin]])
                textList.append(textMap[combinedSeq[i - xAxisMin]])
            except KeyError:
                errorsPresent = True
                zlist.append(4)
                textList.append('N')
        if errorsPresent == True:
            colors = [
                [0, colorA],
                [0.2, colorA],
                [0.2, colorT],
                [0.4, colorT],
                [0.4, colorC],
                [0.6, colorC],
                [0.6, colorG],
                [0.8, colorG],
                [0.8, colorE],
                [1.0, colorE]
            ]
        else:
            colors = [
                [0, colorA],
                [0.25, colorA],
                [0.25, colorT],
                [0.5, colorT],
                [0.5, colorC],
                [0.75, colorC],
                [0.75, colorG],
                [1.0, colorG]
            ]

        heatTrace = go.Heatmap(
            z=[zlist],
            x=list(range(xAxisMin, xAxisMax)),
            text=[textList],
            colorscale=colors,
            showscale=False,
            name='seq',
            hoverinfo='x+text',
            colorbar={
                'tick0': 0,
                'dtick': 1
            }
        )
        return [heatTrace]


def createDetailRow(content, name, rowNumber):
    """ returns a single row for the details table

    Positional arguments:
    content -- the attribute data as String
    name -- name for the attribute
    rowNumber -- used for odd/even coloring
    """
    # Check subtable information
    try:
        headerLine = subTables[subTables['column_id'].str.contains(name)]
    except:
        headerLine = None
    try:
        headers = str(headerLine.iloc[0]['columns']).split(';')
    except:
        headers = None
        
    subRows = [] # holds elements for multivalue attributes
    subTable = [] # holds elements for subtables
    if headers != None: # we have subtable information, so try and create one
        headerRow = []
        for k in headers: # build table header line
            headerRow.append(html.Th(k))
        subTable.append(html.Tr(children = headerRow))
        tableError = False
        for i in content.split(';'): # build subtable rows dictated by ; delimitation
            subSubRow = []
            if len(i.split(',')) == len(headers):
                for j in i.split(','): # build subtable columns dictated by , delimitation
                    if j != '':
                        if j[0] == '?':
                            subSubRow.append(html.Td(html.A(j[1:], href=j[1:].strip(), target='_blank')))
                        else:
                            subSubRow.append(html.Td(j.strip()))    
                subTable.append(html.Tr(children = subSubRow))
            else: 
                tableError = True
        if tableError == True: # Column numbers didn't match, default display
            print('Warning: Number of columns specified in subtable file do not match number of columns in description file')
            subTable = []
            for l in content.split(';'):
                if l != '' :
                    if l[0] == '?': # create hyperlinks
                        subRows.append(html.Tr(html.Td(html.A(l[1:], href = l[1:].strip(), target = '_blank'))))
                    else:
                        subRows.append(html.Tr(html.Td(l.strip())))
    else: # No subtable information
        for i in content.split(';'):
            if i != '' :
                    if i[0] == '?':
                        subRows.append(html.Tr(html.Td(html.A(i[1:], href = i[1:].strip(), target = '_blank'))))
                    else:
                        subRows.append(html.Tr(html.Td(i.strip())))
    if len(subRows) > 5: # Hide values in details element if more than 5 values
        tableRow = html.Tr(children = [html.Td(html.B(name.replace('_',' ').title())),
                               html.Td(html.Details(title = str(len(subRows)) + ' values', children = [html.Summary(str(len(subRows)) + ' values'), html.Table(children = 
                                       subRows)]))], style = {'background-color' : tableColors[rowNumber%2]})
    else:
        tableRow = html.Tr(children=[html.Td(html.B(name.replace('_', ' ').title())),
                                     html.Td(html.Table(children=
                                                        subRows))],
                           style={'background-color': tableColors[rowNumber % 2]})
    if len(subTable) > 0:
        return html.Tr(
            children=[html.Td(html.B(name.replace('_', ' ').title())), html.Td(html.Table(children=subTable))],
            style={'background-color': tableColors[rowNumber % 2]})
    else:
        return tableRow


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=port, use_reloader=False)