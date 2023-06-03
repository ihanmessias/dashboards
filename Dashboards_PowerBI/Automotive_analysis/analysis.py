"""
Apenas realizando alguns tratamentos usando o Python, nada que não
possa ser feito usando o power query. Realizando ações aqui somente
para fins educativos.
"""

# ---- Import Libs ---- #
import pandas as pd
# ---- DataFrame ---- #
df = pd.read_excel('./base/base_dados.xlsx')
# ---- Removendo espaçamento na Coluna de Preço ---- #
df = df.rename(columns={df.columns[3]:'FATURAMENTO'})
# ---- Criando novo df xCalendar ---- #
xCalendar = pd.DataFrame()
xCalendar['DIA'] = df['DATA'].apply(lambda x: x.day)
xCalendar['MES'] = df['DATA'].apply(lambda x: x.month)
xCalendar['ANO'] = df['DATA'].apply(lambda x: x.year)
xCalendar['TRIMESTRE'] = df['DATA'].apply(lambda x: f'T{x.quarter}')
xCalendar.sort_values(['DIA', 'ANO'], ascending=True, inplace=True)
# ---- Salvando bases ---- #
df.to_excel('./base/base_dados.xlsx', index=False)
xCalendar.to_excel('./base/xCalendar.xlsx', index=False)