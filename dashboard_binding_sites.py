#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Interactive visualizaton for iClIP-Seq and RNA-Seq data"""
import json
import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_auth
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
                   heatmap, letters, and no display at all. heatmap is strongly recommended for interactive use, as letters has a signifficantly
                   higher performance impact and is recommended only for the creation of static images.
                
            Please note that you will have to hit the submit button for changes to be applied.
                
            ##### RNA-seq
            
            In this tab you can view RNA-seq coverage plots as well as splice events, if the necessary data was provided.
            Use the checkboxes in the Datasets panel to select which plots you want to view. Functionality for the Options
            panel will be provided in the future.
            
            ##### Details
            
            In this tab you can view further information on your selected gene. Which information is available depends on what your administrator has provided
            when setting up the tool.
            
            ##### Settings
            
            Here you can select colors for the graphs in the iCLIP-seq tab. Select a dataset from the dropdown, choose your color using
            the sliders and hit confirm. You don't need to hit submit for this.
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
    except IndexError:
        advStart = None
        advDisabled = True


# Hide sequence related controls if no sequence data is available
if len(sequences) == 0:
    seqDispStyle = {'display': 'none', 'height' : '100%', 'width' : '20vw'}
else:
    seqDispStyle = {'height' : '100%', 'width' : '20vw'}
if len(dataSetNames) == 0:
    dataSetStyle = {'display': 'none', 'height' : '100%', 'width' : '15vw'}
else:
    dataSetStyle = {'height' : '100%', 'width' : '15vw'}
if len(spliceSetNames[1]) == 0:
    rnaDataStyle = {'display': 'none', 'height' : '100%', 'width' : '15vw'}
else:
    rnaDataStyle = {'height' : '100%', 'width' : '15vw'}


# Try to setup color picker for iCLIP-seq tracks
try:
    initialColor = dataSetNames[0]
    disableSettings = False
except IndexError:
    initialColor = None
    disableSettings = False
# Try to setup color picker for coverage tracks
try:
    initialColorCoverage = spliceSetNames[1][0]
    disableSettings = False
except IndexError:
    initialColorCoverage = None
    disableSettings = False
# Try to setup color picker for coverage tracks
try:
    initialColorEvents = eventTypes[0]
    disableSettings = False
except IndexError:
    initialColorEvents = None
    disableSettings = False
    
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
# For plots with multiple columns in the legend, basically anything using a color scale or heatmap,
# this value determines the margin between colorbar and legend items. For very wide or very narrow
# screens this value might need to be adjusted a bit, this can unfortunately not be done
# automatically right now.
legendColumnOffset = 1.05


app = dash.Dash(__name__)
if authentication != '':
    auth = dash_auth.BasicAuth(
            app,
            {'u' : authentication})
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
                                                    html.Details(open = 'open', children = [
                                                    html.Summary("Controls"),
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
                                                    html.Div(style = dataSetStyle,
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
                                            ])
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
                                                          html.Details(open = 'open', children = [
                                                          html.Summary("Controls"),
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
                                                              html.Div(style=rnaDataStyle,
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
                                                              html.Div(style={'height': '100%', 'width': '20vw'},
                                                                       className='table-cell column-3',
                                                                       children=[
                                                                           html.Fieldset(
                                                                               className='field-set',
                                                                               children=[
                                                                                   html.Legend('Options'),
                                                                                   dcc.RadioItems(
                                                                                       id='rnaRadio',
                                                                                       options=[
                                                                                           {'label': 'Default display',
                                                                                            'value': 'one'},
                                                                                           {'label': 'Color event types',
                                                                                            'value': 'two'},
                                                                                           {'label': 'Color event scores',
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
                                                          ])
                                                        
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
                                html.Div(style = {'display' : 'table'},
                                children =[
                                html.Div(style={'width': '100vw', 'display': 'table-row', 'verticalalign': 'middle'},
                                    children=[
                                        html.Div(className = 'table-cell', 
                                        children = [
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
                                        )]),
                                        html.Div(className = 'table-cell', 
                                        children = [
                                        html.Fieldset(title = 'coverage settings', 
                                            className = 'field-set',
                                            children = [ 
                                                html.Legend('Coverage plot settings'),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='covColorDiv',
                                                    children=json.dumps(coverageColors)
                                                ),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='covColorFinal',
                                                    children=json.dumps(coverageColors)
                                                ),
                                                dcc.Dropdown(
                                                    id='covColorDrop',
                                                    options=[{'label': i, 'value': i} for i in spliceSetNames[1]],
                                                    value=initialColorCoverage
                                                ),
                                                html.Div(
                                                    id='covRDisp',
                                                    children=html.P(html.B('R: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='covRInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='covGDisp',
                                                    children=html.P(html.B('G: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='covGInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='covBDisp',
                                                    children=html.P(html.B('B: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='covBInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.Div(id='covPreview',
                                                                 children=html.P(html.B('Preview')),
                                                                 style={'width': '30vw', 'display': 'table-cell',
                                                                        'verticalalign': 'middle'}
                                                                 ),
                                                        html.Div(
                                                            children=[
                                                                html.Button(id='covColorConfirm', n_clicks_timestamp=0,
                                                                            children='confirm')
                                                            ],
                                                            style={'width': '10vw', 'display': 'table-cell',
                                                                   'verticalalign': 'middle'}
                                                        )
                                                    ],
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                )
                                            ]
                                        )]),
                                        html.Div(className = 'table-cell', 
                                        children = [
                                        html.Fieldset(title = 'event settings', 
                                            className = 'field-set',
                                            children = [ 
                                                html.Legend('Splice event plot settings'),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='eventColorDiv',
                                                    children=json.dumps(eventColors)
                                                ),
                                                html.Div(
                                                    style={'display': 'none'},
                                                    id='eventColorFinal',
                                                    children=json.dumps(eventColors)
                                                ),
                                                dcc.Dropdown(
                                                    id='eventColorDrop',
                                                    options=[{'label': i, 'value': i} for i in eventTypes],
                                                    value=initialColorEvents
                                                ),
                                                html.Div(
                                                    id='eventRDisp',
                                                    children=html.P(html.B('R: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='eventRInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='eventGDisp',
                                                    children=html.P(html.B('G: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='eventGInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    id='eventBDisp',
                                                    children=html.P(html.B('B: ')),
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                ),
                                                dcc.Slider(
                                                    id='eventBInput',
                                                    min=0,
                                                    max=255,
                                                    step=1,
                                                    updatemode='drag'
                                                ),
                                                html.Div(
                                                    children=[
                                                        html.Div(id='eventPreview',
                                                                 children=html.P(html.B('Preview')),
                                                                 style={'width': '30vw', 'display': 'table-cell',
                                                                        'verticalalign': 'middle'}
                                                                 ),
                                                        html.Div(
                                                            children=[
                                                                html.Button(id='eventColorConfirm', n_clicks_timestamp=0,
                                                                            children='confirm')
                                                            ],
                                                            style={'width': '10vw', 'display': 'table-cell',
                                                                   'verticalalign': 'middle'}
                                                        )
                                                    ],
                                                    style={'width': '10vw', 'display': 'table-cell'}
                                                )
                                            ]
                                        )]),
                                        html.Div(className = 'table-cell', 
                                            children = [
                                                html.Fieldset(title = 'Legend Settings', 
                                                    className = 'field-set',
                                                    children = [
                                                        html.Legend('Legend Colorbar Margin'),
                                                        html.Div(
                                                            id = 'legendSpacingDiv',
                                                            style = {'display': 'none'},
                                                            children = json.dumps(legendColumnOffset)
                                                            ),
                                                        dcc.Slider(
                                                            id = 'legendSpacingSlider',
                                                            min = 1.02,
                                                            max = 1.08,
                                                            step = 0.005,
                                                            value = legendColumnOffset,
                                                            marks = {
                                                                1.02: '.02',
                                                                1.03: '',
                                                                1.04: '',
                                                                1.05: '.05',
                                                                1.06: '',
                                                                1.07: '',
                                                                1.08: '.08',
                                                                }
                                                        ),
                                                        html.Div(
                                                            style = {'height' : '15px'})
                                                    ]
                                                )
                                            ]
                                        )
                                    ],
                                ),
                            ])
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
    dash.dependencies.Output('legendSpacingDiv', 'children'),
    [dash.dependencies.Input('legendSpacingSlider', 'value')]
)
def changeLegendSpacing(value):
    return json.dumps(value)

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
    dash.dependencies.Output('covRDisp', component_property='children'),
    [dash.dependencies.Input('covRInput', component_property='value')]
)
def showRCov(r):
    """Callback to display current value for red

    Positional arguments:
    r -- Value for red
    """

    return html.P(html.B('R: ' + str(r)))


@app.callback(
    dash.dependencies.Output('covGDisp', component_property='children'),
    [dash.dependencies.Input('covGInput', component_property='value')]
)
def showGCov(g):
    """Callback to display current value for green

    Positional arguments:
    g -- Value for green
    """

    return html.P(html.B('G: ' + str(g)))


@app.callback(
    dash.dependencies.Output('covBDisp', component_property='children'),
    [dash.dependencies.Input('covBInput', component_property='value')]
)
def showBCov(b):
    """Callback to display current value for blue

    Positional arguments:
    b -- Value for blue
    """

    return html.P(html.B('B: ' + str(b)))


@app.callback(
    dash.dependencies.Output('covPreview', component_property='style'),
    [dash.dependencies.Input('covRInput', 'value'),
     dash.dependencies.Input('covGInput', 'value'),
     dash.dependencies.Input('covBInput', 'value')]
)
def previewColorCov(r, g, b):
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
    dash.dependencies.Output('covRInput', component_property='value'),
    [dash.dependencies.Input('covColorDrop', 'value')],
    [dash.dependencies.State('covColorFinal', 'children')]
)
def rCallbackCov(dataset, colors):
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
    dash.dependencies.Output('covGInput', component_property='value'),
    [dash.dependencies.Input('covColorDrop', 'value')],
    [dash.dependencies.State('covColorFinal', 'children')]
)
def gCallbackCov(dataset, colors):
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
    dash.dependencies.Output('covBInput', component_property='value'),
    [dash.dependencies.Input('covColorDrop', 'value')],
    [dash.dependencies.State('covColorFinal', 'children')]
)
def bCallbackCov(dataset, colors):
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
    dash.dependencies.Output('covColorFinal', component_property='children'),
    [dash.dependencies.Input('covColorConfirm', 'n_clicks')],
    [dash.dependencies.State('covRInput', 'value'),
     dash.dependencies.State('covGInput', 'value'),
     dash.dependencies.State('covBInput', 'value'),
     dash.dependencies.State('covColorDrop', 'value'),
     dash.dependencies.State('covColorFinal', 'children')]
)
def conFirmColorCov(nclicks, r, g, b, dataset, backup):
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
    dash.dependencies.Output('covColorDiv', component_property='children'),
    [dash.dependencies.Input('covRInput', 'value'),
     dash.dependencies.Input('covGInput', 'value'),
     dash.dependencies.Input('covBInput', 'value')],
    [dash.dependencies.State('covColorDrop', 'value'),
     dash.dependencies.State('covColorDiv', 'children')]
)
def changeColorCov(r, g, b, dataset, oldColors):
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
    dash.dependencies.Output('eventRDisp', component_property='children'),
    [dash.dependencies.Input('eventRInput', component_property='value')]
)
def showREvent(r):
    """Callback to display current value for red

    Positional arguments:
    r -- Value for red
    """

    return html.P(html.B('R: ' + str(r)))


@app.callback(
    dash.dependencies.Output('eventGDisp', component_property='children'),
    [dash.dependencies.Input('eventGInput', component_property='value')]
)
def showEvent(g):
    """Callback to display current value for green

    Positional arguments:
    g -- Value for green
    """

    return html.P(html.B('G: ' + str(g)))


@app.callback(
    dash.dependencies.Output('eventBDisp', component_property='children'),
    [dash.dependencies.Input('eventBInput', component_property='value')]
)
def showBevent(b):
    """Callback to display current value for blue

    Positional arguments:
    b -- Value for blue
    """

    return html.P(html.B('B: ' + str(b)))


@app.callback(
    dash.dependencies.Output('eventPreview', component_property='style'),
    [dash.dependencies.Input('eventRInput', 'value'),
     dash.dependencies.Input('eventGInput', 'value'),
     dash.dependencies.Input('eventBInput', 'value')]
)
def previewColorEvent(r, g, b):
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
    dash.dependencies.Output('eventRInput', component_property='value'),
    [dash.dependencies.Input('eventColorDrop', 'value')],
    [dash.dependencies.State('eventColorFinal', 'children')]
)
def rCallbackEvent(dataset, colors):
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
    dash.dependencies.Output('eventGInput', component_property='value'),
    [dash.dependencies.Input('eventColorDrop', 'value')],
    [dash.dependencies.State('eventColorFinal', 'children')]
)
def gCallbackEvent(dataset, colors):
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
    dash.dependencies.Output('eventBInput', component_property='value'),
    [dash.dependencies.Input('eventColorDrop', 'value')],
    [dash.dependencies.State('eventColorFinal', 'children')]
)
def bCallbackEvent(dataset, colors):
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
    dash.dependencies.Output('eventColorFinal', component_property='children'),
    [dash.dependencies.Input('eventColorConfirm', 'n_clicks')],
    [dash.dependencies.State('eventRInput', 'value'),
     dash.dependencies.State('eventGInput', 'value'),
     dash.dependencies.State('eventBInput', 'value'),
     dash.dependencies.State('eventColorDrop', 'value'),
     dash.dependencies.State('eventColorFinal', 'children')]
)
def conFirmColorEvent(nclicks, r, g, b, dataset, backup):
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
    dash.dependencies.Output('eventColorDiv', component_property='children'),
    [dash.dependencies.Input('eventRInput', 'value'),
     dash.dependencies.Input('eventGInput', 'value'),
     dash.dependencies.Input('eventBInput', 'value')],
    [dash.dependencies.State('eventColorDrop', 'value'),
     dash.dependencies.State('eventColorDiv', 'children')]
)
def changeColorEvent(r, g, b, dataset, oldColors):
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
    [dash.dependencies.Input('submit', 'n_clicks_timestamp'),
     dash.dependencies.Input('covColorConfirm', 'n_clicks_timestamp'),
     dash.dependencies.Input('eventColorConfirm', 'n_clicks_timestamp')],
    [dash.dependencies.State('geneDrop', 'value'),
     dash.dependencies.State('rnaRadio', 'value'),
     dash.dependencies.State('rnaParamList', 'values'),
     dash.dependencies.State('covColorDiv', 'children'),
     dash.dependencies.State('covColorFinal', 'children'),
     dash.dependencies.State('eventColorDiv', 'children'),
     dash.dependencies.State('eventColorFinal', 'children'),
     dash.dependencies.State('legendSpacingDiv', 'children')]
)
def rnaPlot(submit, confirm, eventConfirm, geneName, displayMode,rnaParamList, colors, colorsFinal, eventColors, eventColorsFinal, legendSpacing):
    """Main callback that handles the dynamic visualisation of the RNA-seq data

        Positional arguments:
        submit -- Needed to trigger callback with submit button
        confirm -- Needed to trigger callback with confirm button
        eventConfirm -- Triggers callback with confirm button of event color selector
        geneName -- Name of the selected gene in order to filter the data
        displaymode --determines how splice events will be visualized
        rnaParamList -- Selected RNA data sets to plot 
        colors -- Color currently being confirmed. Needed due to lack of order on callbacks
        colorsFinal -- Last confirmed color
        eventColors -- Colors for splice events being confirmed
        eventColorsFinal -- last confirmed colors for splice events
        legendSpacing -- Specifies margin between colorbar and other legend items
        """
    if submit > confirm:
        colors = colorsFinal
    else:
        colors = colors
    
    legendColumnSpacing = json.loads(legendSpacing)

    # select appropriate data from gene annotations
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break

    # Get axis minimum and maximum over all isoforms. Also get current chromosome
    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    chrom = currentGene['chrom'].iloc[0]

    color_dict = json.loads(colors)  # Color per mutant
    # Filter out needed datasets
    rnaDataSets = sorted(list(spliceProcDFs.keys()))
    displayed_rnaDataSet = []
    for rm in sorted(rnaParamList):
        for set in rnaDataSets:
            if rm == set.split('_')[0]:
                displayed_rnaDataSet.append(set)

    # Dicts for lists of axis values
    xVals = {}
    yVals = {}
    max_yVal = 0 # Used to scale y-axes later
    eventDict = {} # stores dataframes with relevant splice event data
    for ds in sorted(displayed_rnaDataSet):

        # Criteria to filter relevant lines from current dataframe
        bcrit11 = spliceProcDFs[ds]['chrom'] == chrom
        bcrit21 = spliceProcDFs[ds]['chromStart'] >= xAxisMin
        bcrit22 = spliceProcDFs[ds]['chromStart'] <= xAxisMax
        bcrit31 = spliceProcDFs[ds]['chromEnd'] >= xAxisMin
        bcrit32 = spliceProcDFs[ds]['chromEnd'] <= xAxisMax
        spliceSlice = spliceProcDFs[ds].loc[bcrit11 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
        # Pre-init y-value list
        yVal = [0] * (len(range(xAxisMin, xAxisMax)))
        organism = ds.split("_")[0] # Prefix of the curret data frame, first filter
        spliceEvents = pandas.DataFrame() # will hold splice event data for the current data set
        if organism in spliceEventNames[1]: # Check if there are splice events for the current prefix
            for d in sorted(spliceEventDFs.keys()):
                if ds in d: # Check for remaining filename, to match the correct files
                    # Criteria to filter relevant lines from current dataframe
                    bcrit11 = spliceEventDFs[d]['chrom'] == chrom
                    bcrit21 = spliceEventDFs[d]['chromStart'] >= xAxisMin
                    bcrit22 = spliceEventDFs[d]['chromStart'] <= xAxisMax
                    bcrit31 = spliceEventDFs[d]['chromEnd'] >= xAxisMin
                    bcrit32 = spliceEventDFs[d]['chromEnd'] <= xAxisMax
                    spliceEvents = spliceEventDFs[d].loc[bcrit11 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32))]
        # Use itertuples to iterate over rows, since itertuples is supposed to be faster
        for row in spliceSlice.itertuples():
            # Increment all values covered by the current row, will overshoot when row crosses border of gene, thus try except
            for j in range(row.chromStart, row.chromEnd):
                try:
                    yVal[j - xAxisMin] += row.count
                except IndexError:
                    pass
         # Store reference to value list in dict
        yVals[ds] = yVal
        # Safe event dataframe to be used in the next function
        eventDict[ds] = spliceEvents
        # Create x-axis values
        xVal = list(range(xAxisMin, xAxisMax))
        xVals[ds] = xVal
        colorScale = (-1.0,1.0)
        # Find maximum y-axis value for axis scaling
        if max(yVal) > max_yVal: max_yVal = max(yVal)
    fig = createAreaChart(xVals, yVals, max_yVal, eventDict, displayed_rnaDataSet, 
                          color_dict, geneName, displayMode, eventConfirm, submit, eventColors, eventColorsFinal, colorScale,
                          legendColumnSpacing)
    return fig

def overlap(a, b):
    """check if two intervals overlap

    Positional arguments:
    a -- first interval
    b -- second interval
    """
    return a[1] > b[0] and a[0] < b[1]


def createAreaChart(xVals, yVals, max_yVal, eventData, displayed, color_dict, 
                    geneName, displayMode, eventConfirm, submit, eventColors, eventColorsFinal, colorScale,
                    legendColumnSpacing):
    """Create the plots for both coverage and splice events

    Positional arguments:
    xVals -- x-axis values for coverage plot
    yVals -- y-axis values for coverage plot
    max_yVal -- maximum y value across all coverage tracks, used to scale all y-axes
    eventData -- Dict containing the dataframes with relevant splice events
    displayed -- displayed datasets
    color_dict -- colors for the coverage plots
    geneName -- name of the selected gene, needed for gene models
    displayMode -- determines how splice events are visualized
    eventconfirm -- confirm button for event color selection
    submit -- global submit button 
    eventColors -- Colors for splice events being confirmed
    eventColorsFinal -- last confirmed colors for splice events
    colorScale -- unified colorscale used for score visualization
    LegendColumnSpacing -- Specifies margin between colorbar and other legend items
    """
    if submit > eventConfirm:
        evColors = json.loads(eventColorsFinal)
    else:
        evColors = json.loads(eventColors)
        
    data = []
    subplot_titles = []
    legendSet = {}
    colorbarSet = False
    for val in eventTypes:
                legendSet[val] = False
    for ds in sorted(displayed):
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
            if displayMode in ['one', 'two']:
                intervals = [] # Used to calculate overlaps, stores used intervals as well as row that interval was put on
                eventXValues = {} # Stores x-axis values per event type
                eventWidths = {} # Stores widths per event type
                eventBases = {} # Stores y offset per event type
                eventScores = {}
                # Iterate through dataframe rows and calculate stacking aswell as bar parameters
                maxStack = 0 # keeps track of the maximum number of stacked bars, to avoid empty rows
                for row in eventData[ds].itertuples():
                    if row.chromStart > row.chromEnd: # Handle errornous input where chromStart > chromEnd and print warning
                        print('Warning; Event in dataset ' + str(ds) +' on chromosome ' + str(row.chrom) + ' at startpoint ' + str(row.chromStart) +
                              ' startpoint is greater than endpoint.')
                    maxVal = max(row.chromStart, row.chromEnd) 
                    minVal = min(row.chromStart, row.chromEnd)
                    key = row.type # Type of the current event
                    if len(intervals) == 0: # Row is the first row, no comparisons
                        try: # If list already exist append
                            eventXValues[key].append(minVal + (maxVal - minVal) / 2)
                            eventWidths[key].append(maxVal - minVal)
                            eventBases[key].append(0)
                            eventScores[key].append(row.score)
                            intervals.append(((minVal, maxVal),0))
                        except KeyError: # Else create corresponding lists in dictionary
                            eventXValues[key] = [minVal + (maxVal - minVal) / 2]
                            eventWidths[key] = [maxVal - minVal]
                            eventBases[key] = [0]
                            eventScores[key] = [row.score]
                            intervals.append(((minVal, maxVal),0))
                        maxStack == 1
                    else: # Row is not the first row, check through already processed intervals to calculate offset
                        numOverlaps = 0
                        heights = [] # Store all rows on which overlaps occur
                        for i in intervals:
                            if overlap(i[0], (minVal, maxVal)) == True:
                                heights.append(i[1])
                                numOverlaps += 1
                        if len(heights) > 0:
                            slot = 0 # First free row the new bar can be placed on
                            for value in range(0, max(heights)+2): # Find first open slot
                                if value not in heights:
                                    slot = value
                                    break
                            numOverlaps = slot # Set numOverlaps accordingly
                        try:
                            eventXValues[key].append(minVal + (maxVal - minVal) / 2)
                            eventWidths[key].append(maxVal - minVal)
                            if numOverlaps > maxStack:
                                if numOverlaps > maxStack + 1:
                                    maxStack += 1
                                    numOverlaps = maxStack
                                else:
                                    maxStack = numOverlaps
                            eventBases[key].append(numOverlaps + 0.5*numOverlaps)
                            eventScores[key].append(row.score)
                            intervals.append(((minVal, maxVal),numOverlaps))
                        except KeyError:
                            eventXValues[key]  = [minVal + (maxVal - minVal) / 2]
                            eventWidths[key] = [maxVal - minVal]
                            if numOverlaps > maxStack:
                                if numOverlaps > maxStack + 1:
                                    maxStack += 1
                                    numOverlaps = maxStack
                                else:
                                    maxStack = numOverlaps
                            eventBases[key] = [numOverlaps + 0.5*numOverlaps]
                            eventScores[key] = [row.score]
                            intervals.append(((minVal, maxVal), numOverlaps))
                traces = []
                for k in sorted(eventXValues.keys()):
                    legend = False # Show legend item 
                    traceColor = 'darkblue'
                    if displayMode == 'two':
                        if legendSet[k] == False: # Legend item for this event type is not displayed, display it
                            legendSet[k] = True
                            legend = True
                        traceColor = evColors[k]
                    trace = go.Bar(
                        x=eventXValues[k],
                        y=[1]*len(eventXValues[k]),
                        width = eventWidths[k],
                        base = eventBases[k],
                        name = k,
                        showlegend = legend,
                        legendgroup = k, # Group traces from different datasets so they all repsond to the one legend item
                        insidetextfont=dict(
                            family="Arial",
                            color="black"
                        ),
                        textposition='auto',
                        marker=dict(
                            color= traceColor,
                        )
                    )
                    traces.append(trace)
                subplot_titles.append("")
                data.append(traces)
            else: # Displaymode: Score heatmap
                intervals = [] # Used to calculate overlaps, stores used intervals as well as row that interval was put on
                eventXValues = [] # Stores x-axis values per event type
                eventWidths = [] # Stores widths per event type
                eventBases = [] # Stores y offset per event type
                eventScores = [] # score for each event
                # Iterate through dataframe rows and calculate stacking aswell as bar parameters
                maxStack = 0 # keeps track of the maximum number of stacked bars, to avoid empty rows
                for row in eventData[ds].itertuples():
                    if row.chromStart > row.chromEnd: # Handle errornous input where chromStart > chromEnd and print warning
                        print('Warning; Event in dataset ' + str(ds) +' on chromosome ' + str(row.chrom) + ' at startpoint ' + str(row.chromStart) +
                              ' startpoint is greater than endpoint.')
                    maxVal = max(row.chromStart, row.chromEnd) 
                    minVal = min(row.chromStart, row.chromEnd)
                    if len(intervals) == 0: # Row is the first row, no comparisons
                        eventXValues.append(minVal + (maxVal - minVal) / 2)
                        eventWidths.append(maxVal - minVal)
                        eventBases.append(0)
                        eventScores.append(row.score)
                        intervals.append(((minVal, maxVal),0))
                        maxStack == 1
                    else: # Row is not the first row, check through already processed intervals to calculate offset
                        numOverlaps = 0
                        heights = [] # Store all rows on which overlaps occur
                        for i in intervals:
                            if overlap(i[0], (minVal, maxVal)) == True:
                                heights.append(i[1])
                                numOverlaps += 1
                        if len(heights) > 0:
                            slot = 0 # First free row the new bar can be placed on
                            for value in range(0, max(heights)+2): # Find first open slot
                                if value not in heights:
                                    slot = value
                                    break
                            numOverlaps = slot # Set numOverlaps accordingly
                        eventXValues.append(minVal + (maxVal - minVal) / 2)
                        eventWidths.append(maxVal - minVal)
                        if numOverlaps > maxStack:
                            if numOverlaps > maxStack + 1:
                                maxStack += 1
                                numOverlaps = maxStack
                            else:
                                maxStack = numOverlaps
                        eventBases.append(numOverlaps + 0.5*numOverlaps)
                        eventScores.append(row.score)
                        intervals.append(((minVal, maxVal),numOverlaps))
                if colorbarSet == False:
                    showBar = True
                    colorbarSet = True
                else:
                    showBar = True
                trace = go.Bar(
                    x=eventXValues,
                    y=[1]*len(eventXValues),
                    width = eventWidths,
                    base = eventBases,
                    showlegend = False,
                    insidetextfont=dict(
                        family="Arial",
                        color="black"
                    ),
                    text = eventScores,
                    hoverinfo = 'x+text',
                    
                    marker=dict(
                        color= eventScores,
                        colorscale = 'Viridis',
                        showscale = showBar,
                        cmin = colorScale[0],
                        cmax = colorScale[1],
                        colorbar =dict(
                            len = 1.0,
                            y = 0.0,
                            x = 1.0,
                            yanchor = 'bottom',
                        )
                    )
                )
                subplot_titles.append("")
                data.append(trace)   

                    
    currentGene = pandas.DataFrame()
    for index, elem in enumerate(geneAnnotations):
        currentGene = elem[elem['name'].str.contains(geneName)]
        if not currentGene.empty:
            break
        
    xAxisMax = currentGene['chromEnd'].max()
    xAxisMin = currentGene['chromStart'].min()
    chrom = currentGene['chrom'].iloc[0]
    strand = currentGene['strand'].iloc[0]
    overlappingGenes = []
    for i in geneAnnotations:
        bcrit11 = i['chrom'] == chrom
        bcrit12 = i['strand'] == strand
        bcrit21 = i['chromStart'] >= xAxisMin
        bcrit22 = i['chromStart'] <= xAxisMax
        bcrit31 = i['chromEnd'] >= xAxisMin
        bcrit32 = i['chromEnd'] <= xAxisMax
        bcrit41 = i['chromStart'] <= xAxisMin
        bcrit42 = i['chromEnd'] >= xAxisMax
        preDF = i.loc[bcrit11 & bcrit12 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32) | (bcrit41 & bcrit42))]
        result = preDF[~preDF['name'].str.contains(geneName)]
        overlappingGenes.append(result)
        
    overlaps = pandas.concat(overlappingGenes)
    isoformList = pandas.concat([currentGene, overlaps]) 
    
    numIsoforms = len(isoformList) # Number of isoforms in the gene model
    numRows = len(data)+numIsoforms

    # Setup row heights based on available data
    row_heights = []
    if spliceEventAvail:
        for i in range(numRows):
            if i > len(data)-1: row_heights.append(1/numRows) # Gene model row
            elif (i % 2 != 0):
                row_heights.append(3/numRows) # Splice event row
            else:
                row_heights.append(3/numRows) # Coverage row
    else:
        for i in range(numRows):
            if i > len(data)-1: row_heights.append(1/numRows) # Gene model row
            else:
                row_heights.append(3/numRows) # Coverage row
    fig = tools.make_subplots(rows=numRows, cols=1, subplot_titles=subplot_titles,
                              shared_xaxes=True, row_width=row_heights[::-1])

    eventIndices = [] # save indices of all elements that contain event traces
    for index, t in enumerate(data):
        try:
            fig.append_trace(t, index + 1, 1)
        except ValueError:
            eventIndices.append(index)
    for i in eventIndices: # add event traces after all coverage traces have been added for legend item positioning
        for x in data[i]:
            fig.append_trace(x, i + 1, 1)


    rnaSequencePlot(fig, geneName, numRows, len(data), isoformList, xAxisMax, xAxisMin, strand)
    fig['layout']['yaxis'].update(showticklabels=True, showgrid=True, zeroline=True)
    for i in range(1, numRows+1):
            if spliceEventAvail:
                if i % 2 != 0 and i <= len(data): # Coverage row
                    fig['layout']['yaxis' + str(i)].update(range=[0, max_yVal])
                    fig['layout']['yaxis' + str(i)].update(showticklabels=True, showgrid=True, zeroline=True)
                else: # Event row
                    fig['layout']['yaxis' + str(i)].update(showticklabels=False, showgrid=False, zeroline=False)
            else:
                if i <= len(data): # Coverage row
                    print('here')
                    fig['layout']['yaxis' + str(i)].update(range=[0, max_yVal])
                    fig['layout']['yaxis' + str(i)].update(showticklabels=True, showgrid=True, zeroline=True)
                else: # Gene model row
                    fig['layout']['yaxis' + str(i)].update(showticklabels=False, showgrid=False, zeroline=False)
    # Setup plot height, add 85 to account for margins
    fig['layout']['height'] = (80 * len(data) + 50 * numIsoforms +85)
    fig['layout']['legend'].update(x = legendColumnSpacing)
    return fig


def rnaSequencePlot(fig, geneName, numRows, len_data, isoformList, xAxisMax, xAxisMin, strand):
    """ Adds gene model plots to coverage and splice event plots
    
    Positional arguments:
    fig -- Current figure, needed to add additional rows
    geneName -- Name of the currently selected gene
    numRows -- Number of rows, needed to prevent zoom on y-axes
    len_data -- Number of RNA-seq rows, used as start point for gene model rows
    """


    fig['layout']['xaxis'].update(nticks=6)
    fig['layout']['xaxis'].update(tickmode='array')
    fig['layout']['xaxis'].update(showgrid=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')
    fig['layout']['yaxis'].update(fixedrange=True)

    chromEnds = []  # used for arrow positioning

    counter = len_data+1

    # Calculate gene models. We have to distinguish between coding region and non-coding region
    geneModels = generateGeneModel(isoformList, xAxisMin, xAxisMax, 0.4)
    for model in geneModels:
        for part in model:
            fig.append_trace(part, counter, 1)
        counter += 1

    # The trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode='relative',
    )
    if strand == '-':
        fig['layout']['xaxis'].update(autorange='reversed')
    for i in range(numRows):  # prevent zoom on y axis
        if i == 0:
            fig['layout']['yaxis'].update(fixedrange=True)
        else:
            fig['layout']['yaxis' + str(i)].update(fixedrange=True)
    # set spacing for the second legend column
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
     dash.dependencies.State('colorFinal', 'children'),
     dash.dependencies.State('legendSpacingDiv', 'children')]
)
def concPlot(submit, confirm, geneName, dataSets, seqDisp, colors, colorsFinal, legendSpacing):
    """Main callback that handles the dynamic visualisation of selected data

    Positional arguments:
    submit -- Submit button time stamp
    confirm -- Confirm button time stamp
    geneName -- Name of the selected gene in order to filter the data
    dataSets -- Selected data tracks with raw binding site data
    seqDisp -- Display mode for dna sequence trace
    colors -- Color currently being confirmed. Needed due to lack of order on callbacks
    colorsFinal -- Last confirmed color
    legendSpacing -- Specifies margin between colorbar and other legend items
    """
    
    # Check which of the two triggering buttons was pressed last
    if submit > confirm:
        colors = colorsFinal
    else:
        colors = colors
        
    legendColumnSpacing = json.loads(legendSpacing)
    
    # Sort the list of selected data tracks to keep consistent order
    for i in sortKeys:
        try:
            dataSets.sort(key=eval(i[0], {'__builtins__': None}, {}), reverse=eval(i[1], {'__builtins__': None}, {}))
        except (TypeError, SyntaxError):
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
    
    xAxisMax = currentGene['chromEnd'].max()

    xAxisMin = currentGene['chromStart'].min()
    strand = currentGene['strand'].iloc[0]
    chrom = currentGene['chrom'].iloc[0]
   
    overlappingGenes = []
    for i in geneAnnotations:
        bcrit11 = i['chrom'] == chrom
        bcrit12 = i['strand'] == strand
        bcrit21 = i['chromStart'] >= xAxisMin
        bcrit22 = i['chromStart'] <= xAxisMax
        bcrit31 = i['chromEnd'] >= xAxisMin
        bcrit32 = i['chromEnd'] <= xAxisMax
        bcrit41 = i['chromStart'] <= xAxisMin
        bcrit42 = i['chromEnd'] >= xAxisMax
        preDF = i.loc[bcrit11 & bcrit12 & ((bcrit21 & bcrit22) | (bcrit31 & bcrit32) | (bcrit41 & bcrit42))]
        result = preDF[~preDF['name'].str.contains(geneName)]
        overlappingGenes.append(result)
        
    overlaps = pandas.concat(overlappingGenes)
    isoformList = pandas.concat([currentGene, overlaps]) 
    
    if rawAvail == True:
        rawDataRows = numParams * rowOffset
    else:
        rawDataRows = 0
    if procAvail == True and rawDataRows > 0:
        procDataRows = numParams * 0.5
    else:
        procDataRows = 0
    numRows = numParams * dsElements + len(
        isoformList) + 1  # Number of rows without weights for specific sizes, +1 for dna sequence track
    plotSpace = 0.8  # Space taken up by data tracks
    spacingSpace = 1.0 - plotSpace  # Space left for spacer tracks
    rowHeight = plotSpace / numRows
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
    rowHeights = [rowHeight] * len(isoformList) + dataSetHeights * numParams + [rowHeight]
    fig = tools.make_subplots(rows=numRows, cols=1, shared_xaxes=True, vertical_spacing=vSpace, row_width=rowHeights)
    fig['layout']['xaxis'].update(nticks=6)
    fig['layout']['xaxis'].update(tickmode='array')
    fig['layout']['xaxis'].update(showgrid=True)
    fig['layout']['xaxis'].update(ticks='outside')
    fig['layout']['xaxis'].update(ticksuffix='b')
    fig['layout'].update(hovermode='x')

    if strand == '-':
        fig['layout']['xaxis'].update(autorange='reversed')
    # create list of 3-tupels containing start, end, name for each isoform.
    # Format name properly
    isoformRanges = []
    for elem in currentGene.itertuples():
        name = elem.name
        if len(elem.name.split('_')) > 1:
            name = elem.name.split('.')[1].replace('_', '.')
        isoformRanges.append((elem.chromStart, elem.chromEnd, name))
    # create master sequence
    combinedSeq = generateMasterSequence(sequences, isoformRanges, xAxisMax)

    try:  # Create traces for sequence display, either scatter or heatmap
        traces = generateSequenceTrace(seqDisp, strand, combinedSeq, xAxisMin, xAxisMax)
        for i in traces:
            fig.append_trace(i, 1, 1)
    except IndexError:
        pass
    except TypeError:
        pass

    counter = 2
    for i in range(len(dataSets)):
        bsTraces = plotICLIP(dataSets[i], xAxisMax, xAxisMin, chrom, strand, colors)  # Plot binding site data
        fig.append_trace(bsTraces[0], counter, 1)
        if len(bsTraces[1]) > 0:
            for j in range(len(bsTraces[1])):
                fig.append_trace(bsTraces[1][j], counter + 1, 1)
        counter += dsElements

    # Calculate gene models. We have to distinguish between coding region and non-coding region
    geneModels = generateGeneModel(isoformList, xAxisMin, xAxisMax, 0.4)
    for model in geneModels:
        for part in model:
            fig.append_trace(part, counter, 1)
        counter += 1
   # for i in currentGene.itertuples():
       # Setup various helpers to work out the different sized blocks
     #   blockStarts = [int(x) for x in i.blockStarts.rstrip(',').split(',')]
      #  blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
       # genemodel = generateGeneModel(int(i.chromStart), int(i.thickStart), int(i.thickEnd - 1),
      #                                blockStarts, blockSizes,
       #                               0.4, i.name)
        #for j in range(len(genemodel)):
         #   fig.append_trace(genemodel[j], counter, 1)
            # Move on to the next gene model
        #counter += 1

    # The trailing ',' actually matters for some reason, don't remove
    fig['layout'].update(
        barmode='relative',
        margin=go.layout.Margin(l=30, r=40, t=25, b=60),
    )
    fig['layout']['yaxis'].update(visible=False, showticklabels=False, showgrid=False, zeroline=False)
    if procAvail:
        for i in range(0, numParams * dsElements, 2):
            fig['layout']['yaxis' + str(i + 3)].update(showticklabels=False, showgrid=False, zeroline=False)
    for i in range(len(isoformList)):  # Edit all y axis in gene model plots
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
                               + baseHeight * (len(isoformList) + 1)
                               + 80)
    fig['layout']['legend'].update(x = legendColumnSpacing)
    return fig

def generateMasterSequence(sequences, isoforms, xAxisMax):
    """Helper function that creates a master sequence given a dataframe with sequences and a list containing
        start and end points as well as names for the relevant isoforms
    
    Positional arguments:
    sequences -- The list of sequence dicts
    isoforms -- List containing three-tuples(start, end, name) for each isoform
    xAxisMax -- endpoint of the gene on the x-axis, used for potential early termination
    """  
    # Sort tuples by start point. this ensures that the algorithm will cover the whole
    # gene sequence, if possible, albeit not necessarily with the least amount of subsequences
    isoforms.sort()
    # Initialize using the leftmost sequence
    currentEnd = isoforms[0][1]
    seqDict = None
    for i in sequences: # Determine which dict contains the relevant sequences, all have to be in the same dict
        if isoforms[0][2] in i:
            seqDict = i
    combinedSeq = str(seqDict[isoforms[0][2]].seq)
    # loop through elements and try to append sequences
    for elem in isoforms:
        if elem[1] > currentEnd: 
            if elem[0] <= currentEnd: # current element overlaps and adds to the sequence
                combinedSeq += str(seqDict[elem[2]].seq)[(currentEnd - elem[0]):]
                currentEnd = elem[1]
            else: # current element does not overlap but will add to the sequence, fill with gaps
                fillerDist = elem[0] - currentEnd
                combinedSeq += [''] * fillerDist
                combinedSeq += str(seqDict[elem[2]].seq)
                currentEnd = elem[1]                    
        if currentEnd >= xAxisMax: # The master sequence is complete, the entire region is covered
            break
    return combinedSeq

def plotICLIP(name, xMax, xMin, chrom, strand, colors):
    """Helper function to plot the subplots containing iCLIP data
    
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


def generateGeneModel(isoforms, xAxisMin, xAxisMax, blockHeight):
    """Generates gene model based on the given blocks and coding region

    Positional arguments:
        isoforms -- List of all isoforms overlapping relevant region
        xAxisMin -- Start of the relevant region
        xAxisMax -- End of the relevant region
        blockHeight -- Hight for thick blocks
    name -- Name for the trace
    """
    traces = []
    for i in isoforms.itertuples(): # This loop will check and if necessary cut blockstarts and sizes
        # depending on the form of overlap
        if i.chromStart >= xAxisMin:
            if i.chromEnd <= xAxisMax: # Gene contained entirely in region, no cutting necessary
                blockStarts = [int(x)+i.chromStart for x in i.blockStarts.rstrip(',').split(',')]
                blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]

            else: # Gene overlaps region on right, cut end
                blockStarts = [int(x)+i.chromStart for x in i.blockStarts.rstrip(',').split(',')]
                blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
                for index, elem in enumerate(blockStarts):
                    if elem >= xAxisMax: # The current block starts right of the relevant region, disregard
                        blockStarts[index] = -1
                    else:
                        blockEnd = elem + blockSizes[index]
                        if  blockEnd > xAxisMax:
                            blockSizes[index] = blockSizes[index] - (blockEnd-xAxisMax)
        else: 
            if i.chromEnd <= xAxisMax: # Gene overlaps on the left, cut start
                blockStarts = [int(x)+i.chromStart for x in i.blockStarts.rstrip(',').split(',')]
                blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
                for index, elem in enumerate(blockStarts):
                    if elem + blockSizes[index] < xAxisMin: # Block ends left of relevant regeion, disregard
                        blockStarts[index] = -1
                    else: 
                        if  elem < xAxisMin: 
                            startOffset = xAxisMin - elem
                            blockStarts[index] = xAxisMin
                            blockSizes[index] = blockSizes[index] - startOffset
            else: # Gene extends to the left and right of the region, cut on both ends
                blockStarts = [int(x)+i.chromStart for x in i.blockStarts.rstrip(',').split(',')]
                blockSizes = [int(x) for x in i.blockSizes.rstrip(',').split(',')]
                for index, elem in enumerate(blockStarts):
                    blockEnd = elem + blockSizes[index]
                    if  blockEnd < xAxisMin or elem >= xAxisMax: # Block lies left or right of relevant region, disregard
                        blockStarts[index] = -1
                    else:
                        if  elem < xAxisMin: # Block overlaps on the left
                            startOffset = xAxisMin - elem
                            blockStarts[index] = xAxisMin
                            blockSizes[index] = blockSizes[index] - startOffset
                        if blockEnd > xAxisMax: # Block overlaps on the right
                            blockSizes[index] = blockSizes[index] - (blockEnd-xAxisMax)
        blockVals = []
        blockWidths = []
        blockYs = []
        name = i.name
    # Calculate blocks from block start and end positions, as well as thickness
        for j in range(len(blockStarts)):
            blockStart = blockStarts[j]
            if blockStart != -1:
                blockEnd = blockStart + blockSizes[j] - 1  # Same as codingRegionEnd
                codingRegionStart = int(i.thickStart)
                codingRegionEnd = int(i.thickEnd) - 1
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
        lineCoords = []
        lineName = ''
        lineHover = 'none'
        lineLegend = False
        try:
            amaxBlockVals = max(range(len(blockVals)), key=f)
            aminBlockVals = min(range(len(blockVals)), key=f)
            lineCoords.append(blockVals[amaxBlockVals] + blockWidths[amaxBlockVals] / 2)
            lineCoords.append(blockVals[aminBlockVals] - blockWidths[aminBlockVals] / 2)
        except ValueError:
            lineCoords.append(xAxisMin)
            lineCoords.append(xAxisMax)
            lineName = name
            lineHover = 'name'
            lineLegend = True
        line = go.Scatter(
            x = lineCoords,
            y = [0, 0],
            name = lineName,
            hoverinfo = lineHover,
            hoverlabel = {
                'namelength' : -1, },
            mode = 'lines',
            line = dict(
                color = 'rgb(0, 0, 0)',
            ),
            showlegend = lineLegend,
            legendgroup = name
        )
        upper = go.Bar(
            x = blockVals,
            y = blockYs,
            name = name,
            hoverinfo = 'none',
            width = blockWidths,
            marker = go.bar.Marker(
                color = 'rgb(0, 0, 0)'
            ),
            showlegend = False,
            legendgroup = name
        )
        lower = go.Bar(
            x = blockVals,
            name = name,
            hoverinfo = 'name',
            hoverlabel = {
                'namelength' : -1, },
            y = [-x for x in blockYs],
            width = blockWidths,
            marker = go.bar.Marker(
                color = 'rgb(0, 0, 0)'
            ),
            showlegend=True,
            legendgroup=name
        )
        traces.append([line, upper, lower])
    # return traces for gene model
    return traces


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
            showscale=True,
            name='seq',
            hoverinfo='x+text',
            colorbar={
                'x' : 1.0,
                'y' : 0.0,
                'tickmode' : 'array',
                'tickvals' : [0.4,1.1,1.86,2.6  ],
                'ticktext' : ['A', 'T', 'C', 'G'],
                'yanchor' : 'bottom',
                'len' : 1.0
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
    except (TypeError, AttributeError):
        headerLine = None
    try:
        headers = str(headerLine.iloc[0]['columns']).split(';')
    except (TypeError, AttributeError):
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
