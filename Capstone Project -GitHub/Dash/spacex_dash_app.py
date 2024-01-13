# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import math

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
step = 1000
marks_dict = {}
for value in range(int(min_payload),(int(max_payload)+step), step):
    marks_dict[value] = str(value)



dropdown_options = [{'label':"All",
                    'value': "All"}]
for i, location in enumerate(spacex_df['Launch Site'].unique()):
    dropdown_options.append({'label':location,
                            'value':location})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options = dropdown_options,
                                            placeholder ='Select Launch Site',
                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = min_payload, 
                                                max = max_payload+step,
                                                step = step,
                                                marks=marks_dict,
                                                value = [min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site == 'All' or entered_site == None:
        grouped_data = spacex_df.groupby('Launch Site').count().reset_index()
        fig = px.pie(grouped_data,
                     values='class', 
                     names='Launch Site', 
                     title='Sucessful Launches by Launch Site'
                    )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # return the outcomes piechart for a selected site
        success = filtered_df['class'].sum()
        failure = filtered_df['class'].count() - success
        fig = px.pie(filtered_df,
                            values=[success, failure] ,
                            names=['Succes', 'Failure'], 
                            title='Launch Success at: ' + entered_site
                            )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, payload_range):
    if entered_site == 'All' or entered_site == None:
        
        fig = px.scatter(spacex_df,
                     x=spacex_df['Payload Mass (kg)'] , 
                     y= spacex_df['class'], 
                     color = spacex_df['Booster Version'], 
                     title='Launch Success By Payload',
                     range_x = payload_range
                    )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        fig = px.scatter(filtered_df,
                     x=spacex_df['Payload Mass (kg)'] , 
                     y= spacex_df['class'], 
                     color = spacex_df['Booster Version'], 
                     title='Launch Success By Payload for: ' + entered_site,
                     range_x = payload_range
                    )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
