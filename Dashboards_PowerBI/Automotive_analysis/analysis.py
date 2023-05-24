# ---- Import Libs ---- #
import pandas as pd
# ---- DataFrame ---- #
df = pd.read_excel('./base/base_dados.xlsx')
# ---- Removendo espaçamento na Coluna de Preços ---- #
df = df.rename(columns={df.columns[3]:df.columns[3].strip()})
# ---- Criando novas colunas ---- #
df['DIA'] = df['DATA'].apply(lambda x: x.day)
df['MES'] = df['DATA'].apply(lambda x: x.month)
df['ANO'] = df['DATA'].apply(lambda x: x.year)
df['Trimestre'] = df['DATA'].apply(lambda x: f'Trimestre {x.quarter}')
# ---- Organizando base ---- #
df.reset_index(inplace=True)
df.sort_values(['DIA', 'ANO'], ascending=True, inplace=True) 