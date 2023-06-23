# ---- Import Libs ---- #
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---- DataFrame ---- #
df = pd.read_csv('dataset_asimov.csv')
# -> Object to Int64:
meses_ordenados = {'Jan':1, 'Fev':2, 'Mar':3,'Abr':4,
                   'Mai':5,'Jun':6,'Jul':7, 'Ago':8,
                   'Set':9, 'Out':10, 'Nov':11, 'Dez':12}
df['Mês'] = df['Mês'].map(meses_ordenados)
df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
df['Valor Pago'] = df['Valor Pago'].astype(int)

df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0
df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)
# -> DFs to Figures:
# Qual valor totol por equipe?
df1 = df.groupby('Equipe')['Valor Pago'].sum().reset_index()
# Quantidade de Chamadas por dia?
df2 = df.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()
# Quantidade de Chamadas por mês?
df3 = df.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
# Valor pago total por Mês do Meio de Propaganda?
df4 = df.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
# Qual valor total por Meio de Propaganda?
df5 = df.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
# Qual valor pago total por Equipe em cada Mês?
df6 = df.groupby(['Mês', 'Equipe'])['Valor Pago'].sum().reset_index()
# Qual Valor pago total por mês?
df6_group = df.groupby('Mês')['Valor Pago'].sum().reset_index()
# Qual a quantidade de chamadas realizadas e não realizadas?
df7 = df.groupby('Status de Pagamento')['Chamadas Realizadas'].sum()
# Qual valor pago total por equipe e consultor?
df8 = df.groupby(['Consultor', 'Equipe'])['Valor Pago'].sum().reset_index()
df8.sort_values(by='Valor Pago',ascending=False, inplace=True)
# Qual valor pago total por equipe?
df9 = df.groupby('Equipe')['Valor Pago'].sum().reset_index()
df9.sort_values(by='Valor Pago',ascending=False, inplace=True)
# df10 = df.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum().reset_index()
# df11 = df.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
# df11 = df11.sort_values(ascending=False)
# Quais os consultores de cada equipe tem o valor pago mais alto?
df10 = df8.groupby('Equipe').head(1).reset_index()
# -> Figures:
fig1 = go.Figure(go.Bar(
        x=df1['Valor Pago'],
        y=df1['Equipe'],
        orientation='h',
        textposition='auto',
        text=df1['Valor Pago'],
        insidetextfont=dict(family='Times', size=14)))
##
fig2 = go.Figure(go.Scatter(
    x=df2['Dia'], y=df2['Chamadas Realizadas'], mode='lines', fill='tonexty'))

fig2.add_annotation(text='Chamadas Médias por dia do Mês',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
fig2.add_annotation(text=f"Média : {round(df2['Chamadas Realizadas'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=30,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)
##
fig3 = go.Figure(go.Scatter(
    x=df3['Mês'], y=df3['Chamadas Realizadas'], mode='lines', fill='tonexty'))

fig3.add_annotation(text='Chamadas Médias por Mês',
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
fig3.add_annotation(text=f"Média : {round(df3['Chamadas Realizadas'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=30,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)
##
fig4 = px.line(df4, y="Valor Pago", x="Mês", color="Meio de Propaganda")
##
fig5 = go.Figure()
fig5.add_trace(go.Pie(labels=df5['Meio de Propaganda'], values=df5['Valor Pago'], hole=.7))
##
fig6 = px.line(df6, y="Valor Pago", x="Mês", color="Equipe")
fig6.add_trace(go.Scatter(y=df6_group["Valor Pago"], x=df6_group["Mês"], mode='lines+markers', fill='tonexty', fillcolor='rgba(255, 0, 0, 0.2)', name='Total de Vendas'))
##
fig7 = go.Figure()
fig7.add_trace(go.Pie(labels=['Não Pago', 'Pago'], values=df7, hole=.6))
##
fig8 = go.Figure()
fig8.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:150%'>{df8['Consultor'].iloc[0]} - Top Consultant</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = df8['Valor Pago'].iloc[0],
        number = {'prefix': "R$"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df8['Valor Pago'].mean()}
))
## 
fig9 = go.Figure()
fig9.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:150%'>{df9['Equipe'].iloc[0]} - Top Team</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = df9['Valor Pago'].iloc[0],
        number = {'prefix': "R$"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df9['Valor Pago'].mean()}
))
##
fig10 = go.Figure()
fig10.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'>Em Reais</span><br>"},
        value = df['Valor Pago'].sum(),
        number = {'prefix': "R$"}
))
##
fig11 = go.Figure()
fig11.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Chamadas Realizadas</span>"},
        value = len(df[df['Status de Pagamento'] == 1])
))
##
fig12 = go.Figure(go.Pie(labels=df10['Consultor'] + ' - ' + df10['Equipe'], values=df10['Valor Pago'], hole=.6))
fig12.show()
##
fig13 = go.Figure(go.Bar(x=df10['Consultor'], y=df10['Valor Pago'], textposition='auto', text=df10['Valor Pago']))
fig13.show()