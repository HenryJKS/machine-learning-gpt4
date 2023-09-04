import base64
import dash
from ChatBotWeb.components import navbar
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from ChatBotWeb.components import navbar

NAVBAR = navbar.create_navbar()

dash.register_page(
    __name__,
    name='tranformFiles',
    top_navbar=True,
    path='/transform',
    external_stylesheets=[dbc.themes.LITERA]
)

layout = dbc.Container([

    dbc.Row([
        NAVBAR
    ]),

    html.Div([
        html.H2("Página de Transformação de Arquivos", className='text-center mt-2'),
    ]),

    html.Hr(),

    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arraste ou Solte ou ',
                html.A('Selecione o Arquivo')
            ]),
            multiple=False
        ),
    ], className='mt-2'),

    html.Div([
        dcc.Dropdown(
            id='transform-options',
            options=[
                {'label': 'Converter para letras maiúsculas', 'value': 'uppercase'}
            ],
            value='uppercase'
        ),
    ], className='mt-2'),

    html.Div([
        html.Button('Aplicar Transformação', id='apply-button', className='btn btn-primary'),
    ], className='mt-2'),


    html.Div(id='output-data')
], fluid=True, style={'background-color': '#e8f5ff', 'height': '100%'})


def apply_transformation(contents, transformation):
    decoded_contents = base64.b64decode(contents.split(',')[1])
    data = decoded_contents.decode('utf-8')

    if transformation == 'uppercase':
        transformed_data = data.upper()
    else:
        transformed_data = data

    return transformed_data


@callback(
    Output('output-data', 'children'),
    [Input('apply-button', 'n_clicks')],
    [dash.dependencies.State('upload-data', 'contents'),
     dash.dependencies.State('transform-options', 'value')]
)
def update_output(n_clicks, contents, transformation):
    if n_clicks is None or contents is None:
        return ""

    transformed_data = apply_transformation(contents, transformation)

    return html.Div([
        html.H3("Resultado da Transformação:"),
        html.Pre(transformed_data)
    ])