import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool

# Carregar o arquivo Excel, pulando as primeiras três linhas
file_path = 'C:/Users/Destro/Documents/BASES_CEPEA/acucar.xlsx'
excel_data = pd.read_excel(file_path, skiprows=3)

# Renomear as colunas para algo mais legível
excel_data.columns = ['Data', 'Açúcar']

# Remover linhas que contêm NaN
excel_data = excel_data.dropna()

# Substituir vírgulas por pontos e converter a coluna 'Açúcar' para números
excel_data['Açúcar'] = excel_data['Açúcar'].str.replace(',', '.').astype(float)

# Dividir o valor do açúcar por 50
excel_data['Açúcar'] /= 50

# Converter a coluna 'Data' para o tipo datetime
excel_data['Data'] = pd.to_datetime(excel_data['Data'], format='%d/%m/%Y')

# Ordenar os dados pela data
excel_data = excel_data.sort_values(by='Data')

# 1. Mostrar o valor com a data mais atual
data_atual = excel_data.iloc[-1]['Data']
valor_atual = round(excel_data.iloc[-1]['Açúcar'], 2)
print("Valor mais atual em", data_atual.strftime('%b/%y'), "é", valor_atual)

# 2. Calcular a média da mesma semana do ano passado
excel_data['Semana'] = excel_data['Data'].dt.isocalendar().week

# Filtrar os valores para a semana atual do ano passado
semana_atual = data_atual.isocalendar().week
ano_passado = data_atual.year - 1

excel_data_ano_passado = excel_data[(excel_data['Semana'] == semana_atual) & (excel_data['Data'].dt.year == ano_passado)]
media_ano_passado = round(excel_data_ano_passado['Açúcar'].mean(), 2)

# Calcular a variação percentual em relação à média da mesma semana do ano passado
variacao_percentual = round(((valor_atual - media_ano_passado) / media_ano_passado) * 100, 2)
print("Variação percentual em relação à média da mesma semana do ano passado é", variacao_percentual, "%")

# 3. Fazer um gráfico de linha evolutivo do último ano
excel_data_ultimo_ano = excel_data[excel_data['Data'] >= data_atual - pd.DateOffset(years=1)]

# Configurar o output do Bokeh
output_file('grafico_acucar_interativo.html')

# Criar a figura do Bokeh
p = figure(x_axis_type="datetime", title="Valor do Açúcar ao longo do tempo", height=400, width=800)
p.xaxis.axis_label = 'Data'
p.yaxis.axis_label = 'Valor do Açúcar'

# Adicionar linha e pontos ao gráfico
p.line(excel_data_ultimo_ano['Data'], excel_data_ultimo_ano['Açúcar'], legend_label='Açúcar', line_width=2)
p.scatter(excel_data_ultimo_ano['Data'], excel_data_ultimo_ano['Açúcar'], fill_color="white", size=8)

# Adicionar ferramenta de hover
hover = HoverTool(tooltips=[("Data", "@x{%F}"), ("Valor do Açúcar", "@y{0.00}")],
                  formatters={'@x': 'datetime'})
p.add_tools(hover)

# Configurar o layout
p.legend.location = "top_left"

# Salvar o gráfico interativo em um arquivo HTML
save(p)

# Substituir ponto por vírgula nos valores monetários
valor_atual_str = "{:.2f}".format(valor_atual).replace(".", ",")
media_ano_passado_str = "{:.2f}".format(media_ano_passado).replace(".", ",")
variacao_percentual_str = "{:.2f}".format(variacao_percentual).replace(".", ",")

# Definir a cor para a variação percentual
variacao_percentual_cor = "red" if variacao_percentual > 0 else "green"

# Criar o arquivo HTML
with open('acucar.html', 'w', encoding='utf-8') as f:
    f.write(f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela de Dados e Gráfico Interativo do Açúcar</title>
    <style>
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
        }}
        .info-container {{
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 800px; /* Largura do gráfico ajustada */
        }}
        .info {{
            border: 2px solid black; /* Alteração na largura da borda */
            padding: 10px;
            margin: 5px;
            flex: 1;
            text-align: center;
            box-sizing: border-box;
            font-family: Calibri; /* Alteração da fonte */
            font-size: larger; /* Aumento do tamanho da fonte */
            display: flex;
            flex-direction: column;
            justify-content: center; /* Centraliza verticalmente */
            align-items: center; /* Centraliza horizontalmente */
        }}
        .info p {{
            margin: 5px 0; /* Ajuste das margens */
        }}
        .info .valor {{
            font-size: x-large; /* Aumento do tamanho da fonte dos valores */
        }}
    </style>
</head>
<body>

<div class="container">
    <iframe src="grafico_acucar_interativo.html" width="850" height="450" frameborder="0"></iframe>
</div>

<div class="container">
    <div class="info-container">
        <div class="info">
            <p><b>Valor mais atual:</b></p>
            <p class="valor">R$ {valor_atual_str}</p>
        </div>
        <div class="info">
            <p><b>Média da mesma semana do ano passado:</b></p>
            <p class="valor">R$ {media_ano_passado_str}</p>
        </div>
        <div class="info">
            <p><b>Variação percentual em relação à média do ano passado:</b></p>
            <p class="valor" style="color: {variacao_percentual_cor};">{variacao_percentual_str}%</p>
        </div>
    </div>
</div>

</body>
</html>
''')

print("Arquivo HTML com gráfico interativo e indicadores criado com sucesso!")
