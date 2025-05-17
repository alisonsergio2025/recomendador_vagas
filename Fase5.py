"""
# Tech Challenge Fase 5
# Data Analytics FIAP - 05/2025
# Alison Sérgio de Amarins Germano - RM 357521

*Ambiente de desenvolvimento utilizado foi o VS CODE

**1. Empresa enfrenta dificuldades para identificar os melhores candidatos para cada vaga e, 
inversamente, oferecer as melhores vagas aos profissionais cadastrados.

"""
# Importando e Aplicando o álias a cada biblioteca
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
# Importação da função que carrega o zip
from ler_dados_applicants_zip import carregar_csv_de_zip
# Cabeçalho do app
st.write("# Tech Challenge Fase 5")
st.markdown("**Alison Sérgio de Amarins Germano - RM 357521**") 
st.write("## Sistema de Recomendação de Vagas e Candidatos")
st.markdown("**Problema:**")
st.markdown("""
Empresa enfrenta dificuldades para identificar os melhores candidatos para cada vaga e, 
inversamente, oferecer as melhores vagas aos profissionais cadastrados.
""")

st.markdown("**Objetivos:**")
st.markdown("Recomendar automaticamente os melhores pares vaga ↔ candidato.")

st.markdown("## Solução Proposta")
st.markdown("""
- Processamento de textos (descrições de currículos e vagas)  
- Técnicas de similaridade (TF-IDF)  
- Modelos supervisionados com base em `data_aceite` (match real)  
- Visualizações analíticas
""")

# Carregar os dados
assert os.path.exists("base_final_ml_com_nome_cliente.zip"), "Arquivo base_final_ml_com_nome_cliente.zip não encontrado"
#df = pd.read_csv("base_final_ml_com_nome_cliente.csv")
df = carregar_csv_de_zip("base_final_ml_com_nome_cliente.zip", "base_final_ml_com_nome_cliente.csv", ",")
st.write(df.head(5))
# Verificações e carregamento
assert os.path.exists("dados_applicants_limpo.zip"), "Arquivo dados_applicants_limpo.zip não encontrado"
#df_applicants = carregar_dados_applicants()
#df_applicants = pd.read_csv("df_applicants_limpo.csv", sep=';')
df_applicants = carregar_csv_de_zip("dados_applicants_limpo.zip", "dados_applicants_limpo.csv",";")
st.write(df_applicants.head(5))
# Criar coluna binária para match real
df_applicants['match_real'] = df_applicants['data_aceite'].notnull().astype(int)
df = df.merge(df_applicants[['codigo_profissional', 'match_real']], on='codigo_profissional', how='left')
df['match_real'] = df['match_real'].fillna(0).astype(int)

# Filtros
# Calcular top 5 clientes por score médio
top5_clientes = (
    df.groupby('cliente')['score']
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

# Filtro de cliente com default nos top 5
#clientes = st.sidebar.multiselect(
#    "Filtrar por Cliente",
#    options=df['cliente'].dropna().unique(),
#    default=top5_clientes
#)
#origens = st.sidebar.multiselect("Filtrar por Origem do Ranking", options=df['ranking_origem'].unique(), default=df['ranking_origem'].unique())

origens =  df['ranking_origem'].unique()
clientes = df['cliente'].dropna().unique()
df_filtrado = df[df['cliente'].isin(clientes) & df['ranking_origem'].isin(origens)]

# Gráfico 1
st.subheader("Distribuição de Aceites Reais")
fig1, ax1 = plt.subplots()
sns.countplot(data=df_filtrado, x='match_real', palette='Set2', ax=ax1)
ax1.set_title("Distribuição de Aceites Reais")
ax1.set_xlabel("Match Real (0 = Não Aceitou, 1 = Aceitou)")
ax1.set_ylabel("Quantidade")
st.pyplot(fig1)

# Gráfico 2 – Top 5 Score Médio por Cliente
st.subheader("Top 5 Clientes com Maior Score Médio")
fig2, ax2 = plt.subplots(figsize=(10, 5))
top5_clientes = df_filtrado.groupby('cliente')['score'].mean().sort_values(ascending=False).head(5)
top5_clientes.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_title("Top 5 Score Médio por Cliente")
ax2.set_ylabel("Score Médio")
ax2.set_xlabel("Cliente")
st.pyplot(fig2)

st.title("🔥 Score Médio por Cliente e Origem do Ranking (Top 10 Clientes)")

# Carregar dados
#df = pd.read_csv("base_final_ml_com_nome_cliente.csv")

# Preencher valores nulos
df['cliente'] = df['cliente'].fillna("desconhecido")
df['ranking_origem'] = df['ranking_origem'].fillna("indefinido")

# Filtrar Top 10 clientes
top_clientes = df['cliente'].value_counts().head(10).index
df_top = df[df['cliente'].isin(top_clientes)]

# Criar a tabela dinâmica (pivot)
pivot_simplificado = df_top.pivot_table(
    index='cliente',
    columns='ranking_origem',
    values='score',
    aggfunc='mean'
)

# Plotar o heatmap
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(
    pivot_simplificado,
    cmap='YlGnBu',
    annot=True,
    fmt=".2f",
    linewidths=0.5,
    cbar_kws={'label': 'Score Médio'},
    ax=ax
)
ax.set_title("🔥 Score Médio por Cliente e Origem do Ranking (Top 10 Clientes)")
ax.set_xlabel("Origem do Ranking")
ax.set_ylabel("Cliente")
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


st.title("Conclusão")

'''

'''
