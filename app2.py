import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Load data
cc = pd.read_csv('data/cumulative_cases.csv', skiprows=3)
cd = pd.read_csv('data/cumulative_deaths.csv', skiprows=3)
rc = pd.read_csv('data/sevenday_rolling_average_of_new_cases.csv', skiprows=3)
rd = pd.read_csv('data/sevenday_rolling_average_of_new_deaths.csv', skiprows=3)

dataVal = [cc, cd, rc, rd]

fig2 = make_subplots(rows=1, cols=2)

fig2.add_trace(
    go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
    row=1, col=1
)

fig2.add_trace(
    go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
    row=1, col=2
)

fig2.update_layout(title_text="Side By Side Subplots")

# print(cc)

#dayS = cc.iloc[:, 0]

#stateS = cc.iloc[0:1]

#for i in cc.columns:
    #print(i)

#print(cc.columns[0])

fig = go.Figure()
fig.add_trace(go.Scatter(x=rd.iloc[:, 0], y=rd.iloc[:,5], mode='lines', name='TX'))

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app = dash.Dash(external_stylesheets=[dbc.themes.GRID])
app.layout = html.Div(
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
                                           ),
                                 html.P('''Visualising time series with Plotly - Dash'''),
                                 dcc.Graph(id='tpi',
                                           config={'displayModeBar': False},
                                           figure=fig2
                                           )
                             ])
                              ])
        ]

)

@app.callback(Output('timeseries', 'figure'),
              [Input('stateSelector', 'value'),
               Input('plotSelector', 'value')])
def update_timeseries(selected_dropdown_value, selected_plot_value):
    selectedData = dataVal[selected_plot_value]
    fig = go.Figure()
    print("Update state", selected_dropdown_value)
    print("Update plot", selected_plot_value)
    for i in range(len(selected_dropdown_value)):
        stateVal = selected_dropdown_value[i]
        fig.add_trace(go.Scatter(x=selectedData['Day'], y=selectedData[stateVal], mode='lines', name=stateVal))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)