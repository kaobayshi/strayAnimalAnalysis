# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 20:34:55 2020

@author: miomio-NB
"""

import plotly_express as px
import pandas as pd
import dash_core_components as dcc 
import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import os



data_read = pd.read_csv("animal_data_copy.csv")
a = data_read["indays"][15]
b = data_read['type'][15]

col_options = [dict(label=x, value=x) for x in data_read.columns]

dimensions = ["X軸", "Y軸", "色彩", "點大小", "欄位", "列"]

asylum_data = pd.read_csv("asylum_data_copy.csv")
asylum_data = asylum_data[["asylumTag", "asylumnm", "asylumtel", "asylumaddr", "asylumprediction"]]
asylum_columns = ["收容所編號", "收容所名稱", "收容所電話", "收容所地址", "收容所現況預測"]
# print(asylum_data.values.T)

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)
app.title = "全國動物收容所預測分析"
app.layout = html.Div(
    [
        html.H1("公立動物收容所"),
        html.Div(
            [
                html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                for d in dimensions
            ],
            style={"width": "25%", "float": "left"},
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
        dcc.Graph(
        id='graph-table',
        className='my_table',
        figure={
            'data': [{
                'type': 'table',
                'columnwidth': 0.5,
                'header': {
                    'values': [['<b>{}</b>'.format(i)] for i in asylum_columns ],
                    'font': {'size': 12, 'color': 'white', },
                    'align': 'center',
                    'valign': 'top',
                    'height': 30,
                    'fill': {'color': '#0076BA'},
                },
                'cells': {
                    'values': asylum_data.values.T,
                    'line': {'color': 'rgb(50, 50, 50)'},
                    'align': 'center',
                    'valign': 'top',
                    'height': 35,
                    'fill': {'color': ['#56C1FF', '#f5f5fa']},
                    'format': [None]*5 + ['.2%']
                },
            }],

            'layout': {
                'height': 300,
                'margin': {'l': 10, 'r': 10, 't': 50, 'b': 50},
            }
        },
        config={'displayModeBar': False}
    ),
    ]
)


@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color, size, facet_col, facet_row):
    return px.scatter(
        data_read,
        x=x,
        y=y,
        color=color,
        size=size,
        facet_col=facet_col,
        facet_row=facet_row,
        height=700,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run_server(host='0.0.0.0', port = port)