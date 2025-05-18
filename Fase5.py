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
import io
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
# Verificações e carregamento
assert os.path.exists("dados_applicants_limpo.zip"), "Arquivo dados_applicants_limpo.zip não encontrado"
df_applicants = carregar_csv_de_zip("dados_applicants_limpo.zip", "dados_applicants_limpo.csv",";")
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
# Filtro por origem do ranking
origens = df['ranking_origem'].dropna().unique().tolist()
origens_selecionadas = st.sidebar.multiselect("Filtrar por Origem do Ranking", options=origens, default=origens)
df_filtrado = df[df['ranking_origem'].isin(origens_selecionadas)]
#-------------------------------------------------------------------------
# Gráfico 1 – Filtrado por Origem do Ranking
st.subheader("Distribuição de Aceites Reais por Origem")
fig1, ax1 = plt.subplots()
sns.countplot(data=df_filtrado, x='match_real', palette='Set2', ax=ax1)
ax1.set_title("Distribuição de Aceites Reais")
ax1.set_xlabel("Match Real (0 = Não Aceitou, 1 = Aceitou)")
ax1.set_ylabel("Quantidade")
st.pyplot(fig1)
#-------------------------------------------------------------------------
# Gráfico 2 – Top 5 Score Médio por Cliente
st.subheader("Top 5 Clientes com Maior Score Médio")
fig2, ax2 = plt.subplots(figsize=(10, 5))
top5_clientes = (
    df_filtrado.groupby('cliente')['score']
    .mean()
    .sort_values(ascending=True)
)
# Verificar se há dados antes de plotar
if not top5_clientes.empty:
    top5_clientes.tail(5).plot(kind='barh', ax=ax2, color='skyblue')
    ax2.set_title("Top 5 Score Médio por Cliente")
    ax2.set_xlabel("Score Médio")
    ax2.set_ylabel("Cliente")
    st.pyplot(fig2)
else:
    #st.warning("⚠️ Nenhum dado disponível para o gráfico de Score Médio por Cliente com os filtros aplicados.")
    st.warning(f"⚠️ Nenhum dado disponível para os clientes selecionados ({', '.join(clientes)}).")
#-------------------------------------------------------------------------
# Gráfico 3 - Score Médio por Cliente e Origem do Ranking (Top 10 Clientes)
st.title("🔥 Score Médio por Cliente e Origem do Ranking (Top 10 Clientes)")
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
#-------------------------------------------------------------------------
# Gráfico 4 - Exemplo Real de Recomendação
st.title("🧾 Exemplo Real de Recomendação")
# Agrupar por vaga e contar apenas candidatos com score
vagas_com_score = df[df['score'].notnull()].groupby('titulo_vaga').size()
# Selecionar apenas vagas com pelo menos 1 candidato com score
vagas_validas = vagas_com_score[vagas_com_score > 0].index.tolist()
# Filtrar dropdown para exibir só essas vagas
vaga_selecionada = st.selectbox("Selecione uma vaga", sorted(vagas_validas))
# Filtrar os candidatos da vaga selecionada
df_vaga_ex = df[df['titulo_vaga'] == vaga_selecionada]
top5 = df_vaga_ex.sort_values(by='score', ascending=False).head(5)

#
if top5.empty:
    st.warning("⚠️ Nenhum candidato encontrado para essa vaga.")
else:
    st.subheader("Candidatos :")
    st.write(top5[['nome', 'cliente', 'score']].reset_index(drop=True))
#-------------------------------------------------------------------------
# Gráfico 5 - Exibir Matches Reais (Aceitos) com Alto Score 
st.title("📤 Exibir Matches Reais (Aceitos) com Alto Score")

# --- Multiselect de ranking_origem ---
ranking_opcoes = df['ranking_origem'].dropna().unique().tolist()
ranking_selecionados = st.multiselect(
    "Filtrar por Origem do Ranking",
    options=ranking_opcoes,
    default=ranking_opcoes,
    key="ranking_origem_filter"  # 🔑 ID único para evitar conflito
)


# --- Filtrar por matches reais, score alto e origens selecionadas ---
df_export = df[
    (df['match_real'] == 1) &
    (df['score'] >= 0.8) &
    (df['ranking_origem'].isin(ranking_selecionados))
]

# --- Remover duplicatas por nome + vaga + cliente ---
df_export = df_export.drop_duplicates(subset=['nome', 'titulo_vaga', 'cliente'])

# --- Selecionar colunas para exibição e ordenação ---
df_resultado = df_export[['nome', 'titulo_vaga', 'cliente', 'score']].sort_values(by='score', ascending=False)

# --- Exibir resultado ---
st.write(df_resultado.reset_index(drop=True))

# --- Gerar CSV e botão de download ---
csv = df_resultado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar CSV com Matches Reais",
    data=csv,
    file_name='melhores_matches_reais.csv',
    mime='text/csv'
)


#-------------------------------------------------------------------------
#st.title("📤 2 ----Exibir Matches Reais (Aceitos) com Alto Score")

# Adicionar filtro de ranking_origem
#origens_disponiveis = df['ranking_origem'].dropna().unique().tolist()
#origem_selecionada = st.selectbox("Filtrar por Origem do Ranking", options=origens_disponiveis, index=0)
# Aplicar filtro
#df_filtrado = df[
#    (df['match_real'] == 1) &
#    (df['score'] >= 0.8) &
#    (df['ranking_origem'] == origem_selecionada)
#]
# Selecionar e ordenar colunas
#df_result = df_filtrado[['nome', 'titulo_vaga', 'cliente', 'score']].sort_values(by='score', ascending=False).reset_index(drop=True)
# Mostrar tabela
#st.dataframe(df_result)
# Gerar CSV em memória
#csv_buffer = io.StringIO()
#df_result.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
#csv_bytes = csv_buffer.getvalue().encode('utf-8-sig')
# Botão de download
#st.download_button(
#    label="📥 Baixar CSV de Matches Reais com Score ≥ 0.8",
#    data=csv_bytes,
#    file_name="melhores_matches_reais.csv",
#    mime="text/csv"
#)
# Mensagem
#st.success(f"{len(df_result)} registros encontrados para a origem '{origem_selecionada}'.")



st.title("Conclusão")

'''

'''
