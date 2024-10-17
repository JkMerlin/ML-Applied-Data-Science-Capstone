import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout =html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
            # TASK 1: Add a dropdown list to enable Launch Site selection
            # The default select value is for ALL sites
            html.Div([
       				    html.Label("Select Site:",
                		style={'width': '80%','height':'30px','font-size':'20px','padding':'3px'}),
            # The default select value is for ALL sites
            dcc.Dropdown(id='site-dropdown',
                         options=[{'label': 'All Sites', 'value': 'ALL'},
                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
	                     value='ALL',
                         placeholder='Select a Launch Site here',
                         style={'height':'30px', 'font-size': 20},
                         searchable=True)]),
            html.Br(),

            # TASK 2: Add a pie chart to show the total successful launches count for all sites
            # If a specific launch site was selected, show the Success vs. Failed counts for the site
            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),
            # TASK 3: Add a slider to select payload range
            dcc.RangeSlider(id='payload-slider',
                            min=0, max=10000, step=1000,
                            marks={0: '0',10000: '10000'},
                            value=[min_payload, max_payload]),

            # TASK 4: Add a scatter chart to show the correlation between payload and launch success
            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
	    # If all sites are selected, show the total success launches
        success_count = spacex_df.groupby('Launch Site')['class'].sum()
	    
        total_launches = spacex_df.shape[0]
        fig = px.pie(values=success_count, #total_launches - success_count],
                     names=spacex_df.groupby('Launch Site')['Launch Site'].first())#['Successful Launches', 'Failed Launches'])
        # Update layout for figure size and title
        fig.update_layout(
                width=600,
                height=400,
                title=dict(
                        text='Total Launch Success By Site',
                        x=0.5,  # Center the title horizontally
                        y=0.95,  # Adjust vertical position as needed
                        xanchor='center',  # Anchor the title to the center point
                        yanchor='top'   # Anchor the title to the top
                        ))

    else:
        # return the outcomes piechart for a selected site
	    
        success_count = filtered_df['class'].sum()
        
        failed_count = filtered_df.shape[0] - success_count
        fig = px.pie(values=[success_count, failed_count],
                     names=['Successful Launches', 'Failed Launches']
                    )
        # Update layout for figure size and title
        fig.update_layout(
                width=600,
                height=400,
                title=dict(
                        text=f'Launch Success for {entered_site}',
                        x=0.5,  # Center the title horizontally
                        y=0.95,  # Adjust vertical position as needed
                        xanchor='center',  # Anchor the title to the center point
                        yanchor='top'   # Anchor the title to the top
                            ))

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_scatter(entered_site, payload_slider_value):

    if entered_site == 'ALL':
        # If all sites are selected, show a scatter plot to display all values
        fig = px.scatter(spacex_df, x="Payload Mass (kg)", y="class",
                        color="Booster Version Category",
                        title='Correlation Between  Payload Mass & ALL Sites')
    else:
        # Filter the data based on the selected site and payload slider value
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                                (spacex_df['Payload Mass (kg)'].between(payload_slider_value[0],payload_slider_value[1]))]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                        color="Booster Version Category",
                        title=f'Correlation Between Payload Mass & {entered_site}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
                                   