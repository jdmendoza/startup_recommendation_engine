import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv('data/clustered_df.csv')

app = dash.Dash()
server = app.server

intro_markdown = """
# SF Startup Recommender
By [Danny Mendoza](https://jdmendoza.github.io/about.html) | [Project Repository](https://github.com/jdmendoza/startup_recommendation_engine)

This demo uses unsupervised machine learning to cluster startups in SF.
Only companies that were in Crunchbase from 2004-2014 exist in the data.

Enter A Startup Below:
"""
app.layout = html.Div([
    dcc.Markdown(children=intro_markdown),
    dcc.Input(id='company-picker', value='Robinhood', type='text'),
    dcc.Graph(id='graph-funding'),
    dcc.Graph(id='graph-rounds'),
    dcc.Graph(id='table-all'),
])


@app.callback(Output('graph-funding', 'figure'),
              [Input('company-picker', 'value')])
def update_figure(selected_company):

    company_data = df[df["company_name"]==selected_company]
    cluster_group = company_data.iloc[0]['final_cluster']
    group = df[df['final_cluster']==cluster_group].sort_values(by=['total_funding'], ascending=False)

    data = [
        go.Bar(
            y=group['total_funding'],
            x=group['company_name']
        )
    ]

    return {
        'data': data,
        'layout': go.Layout(
            title = 'Total Funding',
            yaxis={'title': 'Funding Amount (Millions)'},
            hovermode='closest'
        )
    }

@app.callback(Output('graph-rounds', 'figure'),
              [Input('company-picker', 'value')])
def update_figure(selected_company):

    company_data = df[df["company_name"]==selected_company]
    cluster_group = company_data.iloc[0]['final_cluster']
    group = df[df['final_cluster']==cluster_group].sort_values(by=['company_max_round'], ascending=False)

    data = [
        go.Bar(
            y=group['company_max_round'],
            x=group['company_name']
        )
    ]

    return {
        'data': data,
        'layout': go.Layout(
            title = 'Total Funding Rounds',
            yaxis={'title': 'Number of Rounds'},
            hovermode='closest'
        )
    }

@app.callback(Output('table-all', 'figure'),
              [Input('company-picker', 'value')])
def update_figure(selected_company):

    company_data = df[df["company_name"]==selected_company]
    cluster_group = company_data.iloc[0]['final_cluster']
    group = df[df['final_cluster']==cluster_group].sort_values(by=['company_name'], ascending=True)

    group.drop(inplace=True, columns=['keyword_clusters','final_cluster'])

    data = [
        go.Table(
            header=dict(values=['Company Name','Market', 'City', 'Category List', 'Total Funding', 'Investor Rating', 'Max Rounds'],
                        #fill = dict(color='#C2D4FF'),
                        align = ['left'] * 5,
                        font = dict(color = 'black', size = 12)
                        ),
            cells=dict(values=np.transpose(group.to_numpy()),
                       #fill = dict(color='#F5F8FF'),
                       align = ['left'] * 5,
                       font = dict(color = 'black', size = 11)
                       )
                )
        ]

    return {
        'data': data,
        'layout': go.Layout(
            title = 'All Data',
        )
    }

if __name__ == '__main__':
    app.run_server()
