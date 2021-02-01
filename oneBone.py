import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import random
import dash_daq as daq
from datetime import datetime
from plotly.subplots import make_subplots

# Load data
cc = pd.read_csv('data/cumulative_cases.csv', skiprows=3)
cd = pd.read_csv('data/cumulative_deaths.csv', skiprows=3)
rc = pd.read_csv('data/sevenday_rolling_average_of_new_cases.csv', skiprows=3)
rd = pd.read_csv('data/sevenday_rolling_average_of_new_deaths.csv', skiprows=3)

dataVal = [cc, cd, rc, rd]


labels = ["Male", "Female"]

fig3 = make_subplots(1, 2, specs=[[{"type": "xy"}, {'type':'domain'} ]])

fig3.add_trace(go.Bar(y=[2, 3, 1]),
              row=1, col=1)
fig3.add_trace(go.Pie(labels=labels, values=[48,52], scalegroup='one'), 1, 2)

fig = go.Figure()
fig.add_trace(go.Scatter(x=rd['Day'], y=rd['TX'], mode='lines', name='TX'))
fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))


fig2 = go.Figure(go.Scattermapbox(), )

latCity = ['32.7767', '30.2672', '29.7604', '29.4241', '34.0522', '32.7157', '37.3382', '37.7749']
lonCity = ['-96.7970', '-97.7431', '-95.3698', '-98.4936', '-118.2437', '-117.1611', '-121.8863', '-122.4194']
cityName = ['Dallas', 'Austin', 'Houston', 'San Antonio', 'Los Angeles', 'San Diego', 'San Jose', 'San Francisco']
stateCityIn = ['TX', 'TX', 'TX', 'TX', 'CA', 'CA', 'CA', 'CA']

fig2 = go.Figure(go.Scattermapbox(
        lat=latCity,
        lon=lonCity,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=[56, 20, 25, 24, 60, 29, 40, 20]
        ),
        text=['Dallas', 'Austin', 'Houston', 'San Antonio', 'Los Angeles', 'San Diego', 'San Jose', 'San Francisco'],
    ))
fig2.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken="pk.eyJ1IjoibWluaHRyYW4yMSIsImEiOiJja2dlNG53YmYwZHhqMnJsN2tpNHUwZXR1In0.VOD0SAfL2ZQgAtZ0W6Vg0g",
        bearing=0,
        center=dict(
            lat=30,
            lon=-97,
        ),
        pitch=0,
        zoom=4,
    ),
    margin=dict(t=0, b=0, l=0, r=0)
)

fig2.update_layout(mapbox_style="dark", mapbox_accesstoken="pk.eyJ1IjoibWluaHRyYW4yMSIsImEiOiJja2dlNG53YmYwZHhqMnJsN2tpNHUwZXR1In0.VOD0SAfL2ZQgAtZ0W6Vg0g")


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1'),
        dcc.Tab(label='Tab 2', value='tab-2'),
        dcc.Tab(label='Tab 3', value='tab-3'),
        dcc.Tab(label='Tab 4', value='tab-4'),
        dcc.Tab(label='Tab 5', value='tab-5'),
    ], ),
    html.Div(id='tabs-content-inline')
])
dictCity = {}
for i in range(len(latCity)):
    dictCity[cityName[i]] = [(latCity[i], lonCity[i])]

@app.callback(Output('citySelector', 'options'),
              Input('stateSelector2', 'value'))
def updateCity(value):
    if value == 'TX':
        return [{'label': 'Dallas', 'value': 0},{'label': 'Austin', 'value': 1},{'label': 'Houston', 'value': 2},
            {'label': 'San Antonio', 'value': 3}]
    else:
        return [{'label': 'Los Angeles', 'value': 4},{'label': 'San Diego', 'value': 5},{'label': 'San Jose', 'value': 6},
            {'label': 'San Francisco', 'value': 7}]



@app.callback(Output('darkMap', 'figure'),
              Input('citySelector', 'value'))
def update_map(val):
    if(val == 999):
        return fig2
    fig2.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken="pk.eyJ1IjoibWluaHRyYW4yMSIsImEiOiJja2dlNG53YmYwZHhqMnJsN2tpNHUwZXR1In0.VOD0SAfL2ZQgAtZ0W6Vg0g",
            center=dict(
                lat=float(latCity[val]),
                lon=float(lonCity[val]),
            ),
            pitch=0,
            zoom=8,
        )
    )
    return fig2

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    style = {'padding': '5px', 'fontSize': '16px'}
    lon = random.randint(0, 10000000000)
    lat = random.randint(0, 10000000000)
    alt = random.randint(0, 10000000000)
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]

def randomNum():
    random.seed(datetime.now())
    retVal = random.randint(0, 10000000000)
    return retVal

@app.callback(Output('timeseries', 'figure'),
              [Input('stateSelector', 'value'),
               Input('plotSelector', 'value')])
def update_timeseries(selected_dropdown_value, selected_plot_value):
    selectedData = dataVal[selected_plot_value]
    fig = go.Figure()
    print("Update state", selected_dropdown_value)
    print("Update plot", selected_plot_value)
    if len(selected_dropdown_value) > 0:
        for i in range(len(selected_dropdown_value)):
            stateVal = selected_dropdown_value[i]
            fig.add_trace(go.Scatter(x=selectedData['Day'], y=selectedData[stateVal], mode='lines', name=stateVal))
    else:
        fig.add_trace(go.Scatter(x=selectedData['Day'], y=selectedData['TX'], mode='lines', name='TX'))
    return fig

@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(
            children=[
                html.Div(className='row',
                         children=[
                             html.Div(className='four columns div-user-controls',
                                      children=[
                                          html.H2('Dash - States Total Covid Cases'),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='plotSelector',
                                                           options=[
                                                               {'label': 'Cumulative Cases', 'value': 0},
                                                               {'label': 'Cumulative Deaths', 'value': 1},
                                                               {'label': '7-Day Rolling Cases', 'value': 2},
                                                               {'label': '7-Day Rolling Deaths', 'value': 3}
                                                           ],
                                                           value=3,
                                                           searchable=False,
                                                           clearable=False,
                                                           className='fuck'
                                                       )
                                                   ]),
                                          html.P('''Visualising time series with Plotly - Dash'''),
                                          html.P('''Pick one or more states from the dropdown below.'''),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='stateSelector',
                                                           options=[
                                                               {'label': 'California', 'value': 'CA'},
                                                               {'label': 'Florida', 'value': 'FL'},
                                                               {'label': 'Illionis', 'value': 'IL'},
                                                               {'label': 'North Carolina', 'value': 'NC'},
                                                               {'label': 'Texas', 'value': 'TX'},
                                                               {'label': 'Wisconsin', 'value': 'WI'}
                                                           ],
                                                           value=['TX'],
                                                           multi=True,
                                                           clearable=False,
                                                           className='stateSelector'
                                                       ),
                                                   ],
                                                   style={'color': '#1E1E1E'})
                                      ]
                                      ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                      children=[
                                          dcc.Graph(id='timeseries',
                                                    config={'displayModeBar': False},
                                                    figure=fig
                                                    )
                                      ])
                         ])
            ]
        )
    elif tab == 'tab-2':
        return html.Div(
            children=[
                html.Div(className='row',
                         children=[
                             html.Div(className='four columns div-user-controls',
                                      children=[
                                          html.H2('Dash - States Total Covid Cases'),
                                          html.P('''Visualising time series with Plotly - Dash'''),
                                          html.P('''Pick one or more states from the dropdown below.'''),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='stateSelector2',
                                                           options=[
                                                               {'label': 'Texas', 'value': 'TX'},
                                                               {'label': 'California', 'value': 'CA'},
                                                           ],
                                                           value='TX',
                                                           searchable=False,
                                                           clearable=False,
                                                           className='fuck'
                                                       ),
                                                       dcc.Dropdown(
                                                           id='citySelector',
                                                           options=[
                                                               {'label': 'Dallas', 'value': 0},
                                                               {'label': 'Austin', 'value': 1},
                                                               {'label': 'Houston', 'value': 2},
                                                               {'label': 'San Antonio', 'value': 3}
                                                           ],
                                                           value=999,
                                                           searchable=False,
                                                           clearable=False,
                                                           className='fuck'
                                                       )
                                                   ]),
                                      ]
                                      ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                      children=[
                                          dcc.Graph(id='darkMap',
                                                    config={'displayModeBar': False},
                                                    figure=fig2
                                                    )
                                      ])
                         ])
            ]
        )

    elif tab == 'tab-3':
        return html.Div(
            children=[
                html.Div(className='row',
                         children=[
                             html.Div(className='four columns div-user-controls',
                                      children=[
                                          html.H2('Dash - States Total Covid Cases'),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='plotSelector',
                                                           options=[
                                                               {'label': 'Cumulative Cases', 'value': 0},
                                                               {'label': 'Cumulative Deaths', 'value': 1},
                                                               {'label': '7-Day Rolling Cases', 'value': 2},
                                                               {'label': '7-Day Rolling Deaths', 'value': 3}
                                                           ],
                                                           value=3,
                                                           searchable=False,
                                                           className='fuck'
                                                       )
                                                   ]),
                                          html.P('''Visualising time series with Plotly - Dash'''),
                                          html.P('''Pick one or more states from the dropdown below.'''),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='stateSelector',
                                                           options=[
                                                               {'label': 'California', 'value': 'CA'},
                                                               {'label': 'Florida', 'value': 'FL'},
                                                               {'label': 'Illionis', 'value': 'IL'},
                                                               {'label': 'North Carolina', 'value': 'NC'},
                                                               {'label': 'Texas', 'value': 'TX'},
                                                               {'label': 'Wisconsin', 'value': 'WI'}
                                                           ],
                                                           value=['TX'],
                                                           multi=True,
                                                           className='stateSelector'
                                                       ),
                                                   ],
                                                   style={'color': '#1E1E1E'})
                                      ]
                                      ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                      children=[
                                          dcc.Graph(id='timeseries',
                                                    config={'displayModeBar': False},
                                                    figure=fig
                                                    )
                                      ])
                         ])
            ]
        )
    elif tab == 'tab-4':
        return html.Div(
            children=[
                html.Div(className='row',
                         children=[
                             html.Div(className='four columns div-user-controls',
                                      children=[
                                          html.H2('Dash - States Total Covid Cases'),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='plotSelector',
                                                           options=[
                                                               {'label': 'Cumulative Cases', 'value': 0},
                                                               {'label': 'Cumulative Deaths', 'value': 1},
                                                               {'label': '7-Day Rolling Cases', 'value': 2},
                                                               {'label': '7-Day Rolling Deaths', 'value': 3}
                                                           ],
                                                           value=3,
                                                           searchable=False,
                                                           className='fuck'
                                                       )
                                                   ]),
                                          html.P('''Visualising time series with Plotly - Dash'''),
                                          html.P('''Pick one or more states from the dropdown below.'''),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='stateSelector',
                                                           options=[
                                                               {'label': 'California', 'value': 'CA'},
                                                               {'label': 'Florida', 'value': 'FL'},
                                                               {'label': 'Illionis', 'value': 'IL'},
                                                               {'label': 'North Carolina', 'value': 'NC'},
                                                               {'label': 'Texas', 'value': 'TX'},
                                                               {'label': 'Wisconsin', 'value': 'WI'}
                                                           ],
                                                           value=['TX'],
                                                           multi=True,
                                                           className='stateSelector'
                                                       ),
                                                   ],
                                                   style={'color': '#1E1E1E'})
                                      ]
                                      ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                      children=[
                                          dcc.Graph(id='timeseries',
                                                    config={'displayModeBar': False},
                                                    figure=fig
                                                    )
                                      ])
                         ])
            ]
        )
    elif tab == 'tab-5':
        return html.Div(
            children=[
                html.Div(className='row',
                         children=[
                             html.Div(className='four columns div-user-controls',
                                      children=[
                                          html.H2('Dash - States Total Covid Cases'),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='plotSelector',
                                                           options=[
                                                               {'label': 'Cumulative Cases', 'value': 0},
                                                               {'label': 'Cumulative Deaths', 'value': 1},
                                                               {'label': '7-Day Rolling Cases', 'value': 2},
                                                               {'label': '7-Day Rolling Deaths', 'value': 3}
                                                           ],
                                                           value=3,
                                                           searchable=False,
                                                           className='fuck'
                                                       )
                                                   ]),
                                          html.P('''Visualising time series with Plotly - Dash'''),
                                          html.P('''Pick one or more states from the dropdown below.'''),
                                          html.Div(className='div-for-dropdown',
                                                   children=[
                                                       dcc.Dropdown(
                                                           id='stateSelector',
                                                           options=[
                                                               {'label': 'California', 'value': 'CA'},
                                                               {'label': 'Florida', 'value': 'FL'},
                                                               {'label': 'Illionis', 'value': 'IL'},
                                                               {'label': 'North Carolina', 'value': 'NC'},
                                                               {'label': 'Texas', 'value': 'TX'},
                                                               {'label': 'Wisconsin', 'value': 'WI'}
                                                           ],
                                                           value=['TX'],
                                                           multi=True,
                                                           className='stateSelector'
                                                       ),
                                                   ],
                                                   style={'color': '#1E1E1E'})
                                      ]
                                      ),
                             html.Div(className='eight columns div-for-charts bg-grey',
                                      children=[
                                          dcc.Graph(id='timeseries',
                                                    config={'displayModeBar': False},
                                                    figure=fig
                                                    )
                                      ])
                         ])
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True)