from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel('app\\dashboard\\Vendas.xlsx')
opcoes = list(df['ID Loja'].unique())
opcoes.append('Todas as Lojas')

fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o faturamento de todos os produtos separados por Loja'),

    html.Div(children='''
       OBS: Esse grafico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),
    dcc.Dropdown(opcoes, value='Todas as Lojas', id='Lista_Lojas'),

    dcc.Graph(
        id='grafico_vendas',
        figure=fig
    )
])

# call back
@app.callback(
    Output('grafico_vendas', 'figure'),
    Input('Lista_Lojas', 'value')
)
def update_output(value):
    if value == 'Todas as Lojas':
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID Loja'] == value, :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)