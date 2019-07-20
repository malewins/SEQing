#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Interactive visualizaton for iClIP-Seq and RNA-Seq data"""
import json
import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools
from textwrap import dedent



__author__ = "Yannik Bramkamp"

helpText = '''
            ##### General
            
            Welcome to SEQing, an interactive, web based visualisation and exploration tool for iCLIP-seq and RNA-seq data.
            Use the drop down menu at the top to select your gene of interest. You can search by gene identifier,
            and depending on provided data, also by gene name and partial descriptions. 
            For more detailed information on the different tabs please consult the following paragraphs.
            
            ##### iCLIP-seq
            
            In this tab you can explore raw iCLIP-seq data and, if available, also predicted binding sites. Besides the basic
            interactive plot controls provided by the Dash framework, which you can access by hovering over the graphs,
            there are two main control elements:
              -    On the left side you have checkboxes to select which datasets you wish to display, if more than one was provided to the tool.
              -    On the right side, if dna sequence data was provided, you can select the display mode for said sequences. You can choose from
                   heatmap, letters, and no display at all. heatmap is strongly recommended for interactive use, as 'letters' has a signifficantly
                   higher performance impact and is recommended only for the creation of static images.
                
            Please note that you will have to hit the submit button for changes to be applied.
                
            ##### RNA-seq
            
            ##### Details
            
            In this tab you can view further information on you selected gene. Which information is available depends on what you administrator has provided
            when setting up the tool.
            
            ##### Settings
            
            Here you can select colors for the graphs in the iCLIP-seq tab. Select a dataset from the dropdown, choose your color using
            the sliders and hit 'confirm'. You don't need to hit 'submit' for this.
            '''


if 'dropList' not in globals():
    print('Please start the program via validator.py')
    exit()

# Set defaults if no advanced descriptions are available
if advancedDesc is None:
    advList = []
    advStart = None
    advDisabled = True
else:
    advList = list(advancedDesc.columns.values)
    advList.remove('gene_ids')
    try:
        advStart = advList[0]
        advDisabled = False
    except:
        advStart = None
        advDisabled = True


# Hide sequence related controls if no sequence data is available
if len(sequences) == 0:
    seqDispStyle = {'display': 'none', 'height' : '100%', 'width' : '20vw'}
else:
    seqDispStyle = {'height' : '100%', 'width' : '20vw'}

# Try to setup color picker
try:
    initialColor = dataSetNames[0]
    disableSettings = False
except:
    initialColor = None
    disableSettings = True


def help_popup():
 return html.Div(
        id='help',
        className="model",
        style={'display': 'none'},
        children=(
            html.Div(
                className="help-container",
                children=[
                    html.Div(
                        className='close-container',
                        children=html.Button(
                            "Close",
                            id="help_close",
                            n_clicks=0,
                            className="closeButton",
                            style={'border': 'none', 'height': '100%'}
                        )
                    ),
                    html.Div(
                        className='help-text',
                        children=[dcc.Markdown(
                            children= dedent(helpText)
                            )
                        ]
                    )
                ]
            )
        )
)

# Default tab style
tabStyle = {'padding' : '0', 'line-height' : '5vh'}
# Colors for the alternating coloring in Details
tableColors = ['rgb(255, 255 ,255)', 'rgb(125, 244, 66)']

app = dash.Dash(__name__)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div(
    children=[
        html.Div(
            children = [
                html.H1(id='headline', children='Report')
            ],
            style={'width': '90vw', 'display': 'table-cell', 'verticalalign': 'middle'}
        ),
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
                                html.Button(id='submit', n_clicks=0, n_clicks_timestamp=0, children='Submit', 
                                            style = {'backgroundColor' : 'rgb(255,255,255)'})
                            ],
                            style={'width': '8vw', 'display': 'table-cell', 'verticalalign': 'middle'}
                        ),
                        html.Div(
                            style={'width': '3vw', 'display': 'table-cell', 'verticalalign': 'middle'}
                        ),
                        html.Div(
                            children = [
                                html.Button(id='helpButton', n_clicks=0, n_clicks_timestamp=0, children='help',
                                        style = {'backgroundColor' : 'rgb(255,255,255)'}
                                )
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
                            label='iCLIP-seq',
                            style=tabStyle,
                            selected_style=tabStyle,
                            id='clipTab',
                            children=[
                                html.Div(children = [
                                    html.Div(className = 'table-cont',
                                        children=[
                                                html.Div(className = 'table-row',
                                                    children = [
                                                    html.Div(
                                                        className = 'table-cell column-1',
                                                        children = [
                                                            html.Fieldset(
                                                                className = 'field-set',
                                                                children = [ 
                                                                    html.Legend('Gene Description'),
                                                                    html.Div(id='descDiv',
                                                                        children = html.P(html.B(''))
                                                                    )
                                                                ],
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(style = {'height' : '100%', 'width' : '15vw'},
                                                        className = 'table-cell column-2',
                                                        children = [
                                                            html.Fieldset(
                                                                className = 'field-set',
                                                                children = [
                                                                    html.Legend('Datasets'),                                                     
                                                                    dcc.Checklist(
                                                                        id='paramList',
                                                                        options=[{'label': i, 'value': i} for i in dataSetNames],
                                                                        values=[i for i in dataSetNames]
                                                                    )
                                                                ]
                                                            
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(style = seqDispStyle,
                                                        className = 'table-cell column-3',
                                                        children = [
                                                            html.Fieldset(
                                                                className = 'field-set',
                                                                children = [
                                                                    html.Legend('DNA sequence options'),
                                                                    dcc.RadioItems(
                                                                        id='sequenceRadio',
                                                                        options=[
                                                                            {'label': 'Do not show dna sequence', 'value': 'noSeq'},
                                                                            {'label': 'Show dna sequence as letters', 'value': 'letterSeq'},
                                                                            {'label': 'Show dna sequence as heatmap', 'value': 'heatSeq'}
                                                                        ],
                                                                        value='heatSeq'
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),
    
                                        ],
                                    ),
                                    html.Div(style = {'height' : '25px'}),
                                    html.Div(
                                        children = [
                                                    dcc.Graph(id='bsGraph',
                                                        style = {'padding' : '3px'},
                                                        config = {'toImageButtonOptions' : 
                                                            {'filename' : 'iCLIP', 'width' : None,
                                                            'scale' : 3.0, 'height' : None, 'format' : 'png'} }
                                                    ),
                                                    html.Div(
                                                        children = [
                                                            html.Div(id = 'advMem',
                                                                style = {'display' : 'none'}
                                                            )
                                                        ]
                                                    )    
                                           
                                           
                                        ]         
                                    )
                                ]
                            )
                            ]
                        ),
                        dcc.Tab(
                            label='RNA-seq',
                            style=tabStyle,
                            selected_style=tabStyle,
                            id='rnaTab',
                            children=[
                                html.Div(children=[
                                    html.Div(className='table-cont',
                                             children=[
                                                 html.Div(className='table-row',
                                                          children=[
                                                              html.Div(
                                                                  className='table-cell column-1',
                                                                  children=[
                                                                      html.Fieldset(
                                                                          className='field-set',
                                                                          children=[
                                                                              html.Legend('Gene Description'),
                                                                              html.Div(id='rnaDescDiv',
                                                                                       children=html.P(html.B(''))
                                                                                       )
                                                                          ],
                                                                      )
                                                                  ]
                                                              ),
                                                              html.Div(style={'height': '100%', 'width': '15vw'},
                                                                       className='table-cell column-2',
                                                                       children=[
                                                                           html.Fieldset(
                                                                               className='field-set',
                                                                               children=[
                                                                                   html.Legend('Datasets'),
                                                                                   dcc.Checklist(
                                                                                       id='rnaParamList',
                                                                                       options=[{'label':
                                                                                                     spliceSetNames[1][
                                                                                                         i], 'value':
                                                                                                     spliceSetNames[1][
                                                                                                         i]} for
                                                                                                i in range(
                                                                                               len(spliceSetNames[1]))],
                                                                                       values=[spliceSetNames[1][i] for
                                                                                               i in range(
                                                                                               len(spliceSetNames[1]))],
                                                                                   ),
                                                                               ]

                                                                           )
                                                                       ]
                                                                       ),
                                                              html.Div(style=seqDispStyle,
                                                                       className='table-cell column-3',
                                                                       children=[
                                                                           html.Fieldset(
                                                                               className='field-set',
                                                                               children=[
                                                                                   html.Legend('Options'),
                                                                                   dcc.RadioItems(
                                                                                       id='rnaRadio',
                                                                                       options=[
                                                                                           {'label': 'Display type 1',
                                                                                            'value': 'one'},
                                                                                           {'label': 'Display type 2',
                                                                                            'value': 'two'},
                                                                                           {'label': 'Display type 3',
                                                                                            'value': 'three'}
                                                                                       ],
                                                                                       value='one'
                                                                                   )
                                                                               ]
                                                                           )
                                                                       ]
                                                                       )
                                                          ]
                                                          ),

                                                    ],

                                ),
                                html.Div(style = {'height' : '25px'}),
                                dcc.Graph(id='spliceGraph',
                                    style = {'padding' : '3px'},
                                    config = {'toImageButtonOptions' : 
                                        {'filename' : 'iCLIP', 'width' : None, 'scale' : 3.0, 'height' : None, 'format' : 'png'} }
                                )
                            ])
                        ]
                        ),
                        dcc.Tab(
                            label = 'Details',
                            id = 'deTab',
                            disabled = advDisabled,
                            style = tabStyle,
                            selected_style = tabStyle,
                            disabled_style = tabStyle,
                            children = [
                                html.Div(
                                    id='detailMainDiv',
                                    children=[]
                                )
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
                                            className = 'field-set',
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
        ),
        help_popup()
    ],
    style = {'backgroundColor' : 'rgb(240,240,240)'}
)

@app.callback(
    dash.dependencies.Output('help', 'style'),
    [dash.dependencies.Input("helpButton", "n_clicks"),
     dash.dependencies.Input("help_close", "n_clicks")]
)
def update_click_output(button_click, close_click):
    if button_click > close_click:
        return {"display": "block"}
    else:
        return {"display": "none"}

@app.callback(
    dash.dependencies.Output('advMem', component_property='children'),
    [dash.dependencies.Input('submit', 'n_clicks')],
    [dash.dependencies.State('geneDrop', 'value')]
)
def storeDesc(nclicks, geneName):
    """ Save description data to hidden div for display
    
    Positional arguments:
    nlicks -- Button parameter
    geneName -- Name of the currently selected gene
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
    data -- Data for the current gene, as json string(dict)
    name -- Gene name for initialization
    """
    try:
        df = pandas.read_json(data, orient='split')
    except ValueError:
        try:
            df = advancedDesc[advancedDesc['gene_ids'].str.contains(name)]
        except TypeError:
            df = pandas.DataFrame()
    columns = list(df.columns.values)
    rowCounter = 1  # Keep track of the row number to alternate coloring
    usedColumns = []  # Keeps track of preset columns already added, needed later
    usedColumns.append('gene_ids')
    content = []  # Table content to be displayed
    generalColumns = ['symbol', 'brief_description', 'is_obsolete', 'computational_description',
                      'curator_summary', 'name']
    tableRows = []  # Will contain the table rows
    for i in generalColumns:
        if i in columns and str(df.iloc[0][i]) not in ['nan', ';""']:
            tableRows.append(html.Tr(children=[html.Td(html.B(i.replace('_', ' ').title())),
                                               html.Td(str(df.iloc[0][i]).strip())],
                                     style={'background-color': tableColors[rowCounter % 2]}))
            usedColumns.append(i)
            rowCounter += 1
    # Go through a number of predefined columns
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
    # Go through all remaining columns using formatting standard
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
    r -- Value for red
    """

    return html.P(html.B('R: ' + str(r)))


@app.callback(
    dash.dependencies.Output('gDisp', component_property='children'),
    [dash.dependencies.Input('gInput', component_property='value')]
)
def showG(g):
    """Callback to display current value for green

    Positional arguments:
    g -- Value for green
    """

    return html.P(html.B('G: ' + str(g)))


@app.callback(
    dash.dependencies.Output('bDisp', component_property='children'),
    [dash.dependencies.Input('bInput', component_property='value')]
)
def showB(b):
    """Callback to display current value for blue

    Positional arguments:
    b -- Value for blue
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
    r -- Value for red
    g -- Value for green
    b -- Value for blue
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
    dataset -- Currently selected dataset
    colors -- Dictionary containing the color values(json string)
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
    dataset -- Currently selected dataset
    colors -- Dictionary containing the color values(json string)
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
    dataset -- Currently selected dataset
    colors -- Dictionary containing the color values(json string)
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
    nclicks -- Button value
    r -- Red value
    g -- Green value
    b -- Blue value
    dataset -- Dataset to overwrite color of
    backup -- Previous value in case of error
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
    r -- Red value
    g -- Green value
    b -- Blue value
    dataset -- Currently selected dataset
    oldColors -- Previous colors in case none values are provided for r/g/b
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
    clicks -- Related to button, not needed otherwise
    name -- Name of the currently selected gene
    """
    for i in geneAnnotations:
        currentGene = i[i['name'].str.contains(name)]
        if not currentGene.empty:
            break
    strand = currentGene['strand'].iloc[0]
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
    chrom = currentGene['chrom'].iloc[0]
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
            if rm == set.split('_')[0]:
                displayed_rnaDataSet.append(set)

    # dicts for lists of axis values
    xVals = {}
    yVals = {}
    max_yVal = 0
    eventDict = {}

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
        #yVal_events = [0] * (len(range(xAxisMin, xAxisMax)))
        organism = ds.split("_")[0]
        spliceEvents = pandas.DataFrame()
        if organism in spliceEventNames[1]:
            for d in spliceEventDFs.keys():
                if ds in d:
                    # criteria to filter relevant lines from current dataframe
                    bcrit11 = spliceEventDFs[d]['chrom'] == chrom
                    bcrit21 = spliceEventDFs[d]['chromStart'] >= xAxisMin
                    bcrit22 = spliceEventDFs[d]['chromStart'] <= xAxisMax
                    bcrit31 = spliceEventDFs[d]['chromEnd'] >= xAxisMin
                    bcrit32 = spliceEventDFs[d]['chromEnd'] <= xAxisMax
                    spliceEvents = spliceEventDFs[d].loc[bcrit11 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
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
        eventDict[ds] = spliceEvents
        # create x-axis values
        xVal = list(range(xAxisMin, xAxisMax))
        xVals[ds] = xVal
        if max(yVal) > max_yVal: max_yVal = max(yVal)
    fig = createAreaChart(xVals, yVals, eventDict, displayed_rnaDataSet, color_dict, dataSets, geneName)

    if spliceEventAvail:
        for i in range(1, len(displayed_rnaDataSet), 2):  # edit all y axis in gene model plots
            fig['layout']['yaxis' + str(i)].update(range=[0, max_yVal])
    else:
        for i in range(1,len(displayed_rnaDataSet)):  # edit all y axis in gene model plots
            fig['layout']['yaxis' + str(i)].update(range=[0,max_yVal])
    return fig

def overlap(a, b):
    return a[1] > b[0] and a[0] < b[1]

def createAreaChart(xVals, yVals, eventData, displayed, color_dict, dataSets, geneName):
    data = []
    subplot_titles = []
    for ds in displayed:
        xAxis = xVals[ds]
        yAxis = yVals[ds]
        organism = ds.split('_')[0]
        org_color = color_dict[organism]
        if spliceAvail:
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
            subplot_titles.append(ds)
            data.append(trace)
        if spliceEventAvail:
            intervals = []
            eventXValues = []
            eventWidths = []
            eventBases = []
            # iterate through dataframe rows and calculate stacking aswell as bar parameters
            for row in eventData[ds].itertuples():
                if len(intervals) == 0:
                    intervals.append((row.chromStart, row.chromEnd))
                    eventXValues.append(row.chromStart + (row.chromEnd - row.chromStart) / 2)
                    eventWidths.append(row.chromEnd - row.chromStart)
                    eventBases.append(0)
                else:
                    numOverlaps = 0
                    for i in intervals:
                        if overlap(i, (row.chromStart, row.chromEnd)) == True:
                            numOverlaps += 1
                    intervals.append((row.chromStart, row.chromEnd))
                    eventXValues.append(row.chromStart + (row.chromEnd - row.chromStart) / 2)
                    eventWidths.append(row.chromEnd - row.chromStart)
                    eventBases.append(numOverlaps)               
            trace1 = go.Bar(
                x=eventXValues,
                y=[1]*len(eventXValues),
                width = eventWidths,
                base = eventBases,
                showlegend=False,
                insidetextfont=dict(
                    family="Arial",
                    color="black"
                ),
                textposition='auto',
                marker=dict(
                    color='darkblue',
                    line=dict(
                        color='darkblue',
                        width=1),
                )
            )
            subplot_titles.append("")
            data.append(trace1)


    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break
    numIsoforms = len(currentGene)
    numRows = len(data)+numIsoforms

    row_heights = []
    if spliceEventAvail:
        for i in range(numRows):
            if i > len(data)-1: row_heights.append(2/numRows)
            elif (i % 2 != 0):
                row_heights.append(1/numRows)
            else:
                row_heights.append(3/numRows)
    else:
        for i in range(numRows):
            if i > len(data)-1: row_heights.append(2/numRows)
            else:
                row_heights.append(3/numRows)

    fig = tools.make_subplots(rows=numRows, cols=1, subplot_titles=subplot_titles,
                              shared_xaxes=True, row_width=row_heights[::-1])

    for index, t in enumerate(data):
        fig.append_trace(t, index + 1, 1)


    rnaSequencePlot(fig, geneName, numRows, len(data), dataSets)

    for i in range(numRows+1):
        if i == 0:
            fig['layout']['yaxis'].update(showticklabels=True, showgrid=True, zeroline=True)

        else:
            if spliceEventAvail:
                if i % 2 != 0 and i <= len(data):
                    fig['layout']['yaxis' + str(i)].update(showticklabels=True, showgrid=True, zeroline=True)
                else:
                    fig['layout']['yaxis' + str(i)].update(showticklabels=False, showgrid=False, zeroline=False)
            else:
                if i <= len(data):
                    fig['layout']['yaxis' + str(i)].update(showticklabels=True, showgrid=True, zeroline=True)
                else:
                    fig['layout']['yaxis' + str(i)].update(showticklabels=False, showgrid=False, zeroline=False)

    fig['layout']['height'] = (80 * len(data) + 50 * numIsoforms)
    return fig


def rnaSequencePlot(fig, geneName, numRows, len_data, dataSets):

    numParams = len(dataSets)  # number of selected data tracks
    baseHeight = 30  # size of gene model row, for plot scaling
    # select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break


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
    strand = currentGene['strand'].iloc[0]

    chromEnds = []  # used for arrow positioning

    counter = len_data+1

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
    for i in range(numRows):  # prevent zoom on y axis
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
    clicks -- Related to button, not needed in code
    name -- Name of the currently selected gene
    """
    if descAvail:
        try:
            return [
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
    submit -- Submit button time stamp
    confirm -- Confirm button time stamp
    geneName -- Name of the selected gene in order to filter the data
    dataSets -- Selected data tracks with raw binding site data
    seqDisp -- Display mode for dna sequence trace
    colors -- Color currently being confirmed. Needed due to lack of order on callbacks
    colorsFinal -- Last confirmed color
    """
    
    # Check which of the two triggering buttons was pressed last
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
    numParams = len(dataSets)  # Number of selected data tracks
    rowOffset = 4  # Relative size of data tracks compared to gene model tracks
    baseHeight = 30  # Size of gene model row, for plot scaling
    # Select appropriate data from either the coding or non-coding set
    currentGene = pandas.DataFrame()
    for elem in geneAnnotations:
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break
    # Row heights and spacing
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
        currentGene) + 1  # Number of rows without weights for specific sizes, +1 for dna sequence track
    plotSpace = 0.8  # Space taken up by data tracks
    spacingSpace = 1.0 - plotSpace  # Space left for spacer tracks
    rowHeight = plotSpace / numRowsW
    if numRows > 1:
        vSpace = spacingSpace / (numRows - 1)
    else:
        vSpace = spacingSpace

    # Final height values for rows respecting type, has to be in bottom-up order
    dataSetHeights = []
    if procAvail == True:
        dataSetHeights.append(rowHeight / 2)
    if rawAvail == True:
        dataSetHeights.append(rowHeight * rowOffset)
    rowHeights = [rowHeight] * len(currentGene) + dataSetHeights * numParams + [rowHeight]
    fig = tools.make_subplots(rows=numRows, cols=1, shared_xaxes=True, vertical_spacing=vSpace, row_width=rowHeights)
    fig['layout']['xaxis'].update(nticks=6)
    fig['layout']['xaxis'].update(tickmode='array')
    fig['layout']['xaxis'].update(showgrid=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')

    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    strand = currentGene['strand'].iloc[0]
    if strand == '-':
        fig['layout']['xaxis'].update(autorange='reversed')
    # Setup some variables to build master sequence from isoform-sequences
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

    if rightStart <= leftEnd:  # Left and right sequence have overlap, we don't need more parts to create master
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

    try:  # Create traces for sequence display, either scatter or heatmap
        traces = generateSequenceTrace(seqDisp, strand, combinedSeq, xAxisMin, xAxisMax)
        for i in traces:
            fig.append_trace(i, 1, 1)
    except IndexError:
        pass
    except TypeError:
        pass
    #       pass

    # Save strand info, necessary for binding site traces. Should be same for all isoforms, so any will do
    chrom = currentGene['chrom'].iloc[0]

    counter = 2
    for i in range(len(dataSets)):
        bsTraces = plotICLIP(dataSets[i], xAxisMax, xAxisMin, chrom, strand, colors)  # Plot binding site data
        fig.append_trace(bsTraces[0], counter, 1)
        if len(bsTraces[1]) > 0:
            for j in range(len(bsTraces[1])):
                fig.append_trace(bsTraces[1][j], counter + 1, 1)
        counter += dsElements

    # Calculate gene models. We have to distinguish between coding region and non-coding region
    for i in currentGene.itertuples():
        # Setup various helpers to work out the different sized blocks
        blockStarts = [int(x) for x in i.blockStarts.rstrip(',').split(',')]
        blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
        genemodel = generateGeneModel(int(i.chromStart), int(i.thickStart), int(i.thickEnd - 1),
                                      blockStarts, blockSizes,
                                      0.4, i.name)
        for j in range(len(genemodel)):
            fig.append_trace(genemodel[j], counter, 1)
            # Move on to the next gene model
        counter += 1

    # The trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode='relative',
        margin=go.layout.Margin(l=30, r=40, t=25, b=60),
    )
    fig['layout']['yaxis'].update(visible=False, showticklabels=False, showgrid=False, zeroline=False)
    if procAvail:
        for i in range(0, numParams * dsElements, 2):
            fig['layout']['yaxis' + str(i + 3)].update(showticklabels=False, showgrid=False, zeroline=False)
    for i in range(len(currentGene)):  # Edit all y axis in gene model plots
        fig['layout']['yaxis' + str(i + numParams * dsElements + 2)].update(showticklabels=False, showgrid=False,
                                                                            zeroline=False)
    for i in range(numRows + 1):  # Prevent zoom on y axis
        if i == 0:
            fig['layout']['yaxis'].update(fixedrange=True)
        else:
            fig['layout']['yaxis' + str(i)].update(fixedrange=True)
    # Set correct graph height based on row number and type
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
    # Selection criteria
    crit1 = bsRawDFs[name]['chrom'] == chrom
    crit21 = bsRawDFs[name]['chromStart'] >= xMin
    crit22 = bsRawDFs[name]['chromStart'] <= xMax
    crit31 = bsRawDFs[name]['chromEnd'] >= xMin
    crit32 = bsRawDFs[name]['chromEnd'] <= xMax
    rawSites = bsRawDFs[name].loc[crit1 & ((crit21 & crit22) | (crit31 & crit32))]
    # Setup arrays to hold the values that will be needed for plotting
    countsX = []
    countsY = []
    countsW = []
    for i in rawSites.itertuples():
        countsX.append(i.chromStart)
        countsY.append(i.count)
        countsW.append(i.chromEnd - i.chromStart)
    # Plot data
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

    # Setup criteria to select binding sites that are within the current region of the genome
    procSitesList = []
    try:
        bcrit11 = bsProcDFs[name]['chrom'] == chrom
        bcrit12 = bsProcDFs[name]['strand'] == strand
        bcrit21 = bsProcDFs[name]['chromStart'] >= xMin
        bcrit22 = bsProcDFs[name]['chromStart'] <= xMax
        bcrit31 = bsProcDFs[name]['chromEnd'] >= xMin
        bcrit32 = bsProcDFs[name]['chromEnd'] <= xMax
        bindingSites = bsProcDFs[name].loc[bcrit11 & bcrit12 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
        # Plot binding sites
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
    chromStart -- Start of the chromosome, needed to offfset block values
    codingRegionStart -- Start of the coding or thick region
    codingRegionEnd -- End of the coding or thick region
    blockStarts -- List of block startpoints, these are relative to ChromStart
    blockSizes -- Lengths of the various blocks
    blockHeight -- Height for the blocks, thin regions are drawn with half height
    name -- Name for the trace
    """

    blockVals = []
    blockWidths = []
    blockYs = []
    # Calculate blocks from block start and end positions, as well as thickness
    for j in range(len(blockStarts)):
        blockStart = chromStart + blockStarts[j]
        blockEnd = chromStart + blockStarts[j] + blockSizes[j] - 1  # Same as codingRegionEnd
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

    # Find first and last block to draw line properly
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
    """ Function to generate sequence display trace, either heatmap or scatter

    Positional arguments:
    seqDisp -- Determines which trace type is used
    strand -- If on minus strand invert dna sequence
    combinedSeq -- Sequence for display
    xAxisMin -- Startpoint
    xAxisMax -- Endpoit
    """

    if seqDisp == 'letterSeq':
        xA = []
        xC = []
        xG = []
        xT = []
        Err = []
        if strand == '+':
            varMap = {'A': xA, 'C': xC, 'G': xG, 'T': xT}
        else:  # Reverse complement
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
        else:  # Reverse complement
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
    """ Returns a single row for the details table

    Positional arguments:
    content -- The attribute data as String
    name -- Name for the attribute
    rowNumber -- Used for odd/even coloring
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
        
    subRows = [] # Holds elements for multivalue attributes
    subTable = [] # Holds elements for subtables
    if headers != None: # We have subtable information, so try and create one
        headerRow = []
        for k in headers: # Build table header line
            headerRow.append(html.Th(k))
        subTable.append(html.Tr(children = headerRow))
        tableError = False
        for i in content.split(';'): # Build subtable rows dictated by ; delimitation
            subSubRow = []
            if len(i.split(',')) == len(headers):
                for j in i.split(','): # Build subtable columns dictated by , delimitation
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
                    if l[0] == '?': # Create hyperlinks
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
