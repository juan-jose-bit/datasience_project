# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

data = pd.read_csv('/home/juanjose/dash/spacex_launch_dash.csv')
min_payload = data['Payload Mass (kg)'].min()
max_payload = data['Payload Mass (kg)'].max()

site_labs  = data['Launch Site'].unique()
options=[
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': site_labs[0], 'value': site_labs[0]},
    {'label': site_labs[1], 'value': site_labs[1]},
    {'label': site_labs[2], 'value': site_labs[2]},
    {'label': site_labs[3], 'value': site_labs[3]}
    ]

app = dash.Dash(name = __name__)
app.layout = html.Div(children = [
    ###title
    html.H1(children='Spacex Launch Records Dashboard',style={'textAlign': 'center'}),
    html.Hr(),
    ##body
    html.Div(children = [
        ##dropdown
        html.Div(dcc.Dropdown(options = options, id = 'sites-dropdown', value = 'ALL', 
                                placeholder = 'Select a Launch Site here', searchable = True)),
        ##barchart
        html.Div(id = 'bar-chart'),
        ##silder
        html.Div(dcc.RangeSlider(min = 0, max =10000 , step = 1000, value = [min_payload, max_payload], id = 'payload-slider')),
        ##scatterplot
        html.Div(id = 'scatter-chart')
    ]
    )
]

)

@app.callback(Output(component_id = 'bar-chart', component_property = 'children'),
            Output(component_id = 'scatter-chart', component_property = 'children'),
            Input(component_id ='sites-dropdown', component_property = 'value'),
            Input(component_id ='payload-slider', component_property = 'value'))
def update(drop_value, slider_value):
    if drop_value!= 'ALL':
        dt = data[data['Launch Site'] == drop_value]
        dt = dt[(dt['Payload Mass (kg)'] >= int(slider_value[0])) & (dt['Payload Mass (kg)'] <= int(slider_value[1]))]
        fig1 = px.pie(dt,names = 'class', title = 'Total Succes Launches for Site {}'.format(drop_value) )
        fig2 = px.scatter(dt, x = 'Payload Mass (kg)', y = 'class', 
                        color="Booster Version Category", title = 'Correlation Between Payload and Succes for all sites')
        return [dcc.Graph(figure = fig1), dcc.Graph(figure = fig2)]
    else:
        dt = data[(data['Payload Mass (kg)'] >= int(slider_value[0])) & (data['Payload Mass (kg)'] <= int(slider_value[1]))]
        fig1 = px.pie(dt,values = 'class',names = 'Launch Site',title = 'Total Success Launches by Site')
        fig2 = px.scatter(dt, x = 'Payload Mass (kg)', y = 'class', 
                        color="Booster Version Category", title = 'Correlation Between Payload and Succes for {}'.format(drop_value))
        return [dcc.Graph(figure = fig1), dcc.Graph(figure = fig2)]

if __name__ == '__main__':
    app.run_server(debug=True)