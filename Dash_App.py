
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Sample data
df = pd.DataFrame({
    'Launch Site': ['A', 'B', 'C', 'A', 'B', 'C'],
    'Payload Mass': [1000, 2000, 3000, 4000, 5000, 6000],
    'Launch Outcome': ['Success', 'Failure', 'Success', 'Success', 'Failure', 'Success']
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Launch Site:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': site, 'value': site} for site in df['Launch Site'].unique()],
            value='A',
            placeholder="Select a Launch Site",
        )
    ]),

    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),

    html.Div([
        html.Label("Select Payload Range:"),
        dcc.RangeSlider(
            id='payload-slider',
            min=df['Payload Mass'].min(),
            max=df['Payload Mass'].max(),
            step=1000,
            value=[1000, 6000],
            marks={i: str(i) for i in range(1000, 7000, 1000)}
        )
    ]),

    html.Div([
        dcc.Graph(id='success-payload-scatter')
    ])
])

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(site):
    filtered_df = df[df['Launch Site'] == site]
    fig = px.pie(filtered_df, names='Launch Outcome', title=f'Launch Outcome for {site}')
    return fig

@app.callback(
    Output('success-payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(site, payload_range):
    filtered_df = df[(df['Launch Site'] == site) &
                     (df['Payload Mass'] >= payload_range[0]) &
                     (df['Payload Mass'] <= payload_range[1])]
    fig = px.scatter(filtered_df, x='Payload Mass', y='Launch Outcome',
                     color='Launch Outcome', title='Payload vs. Launch Outcome')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
