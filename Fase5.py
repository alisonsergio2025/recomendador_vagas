"""
# Tech Challenge Fase 5
# Data Analytics FIAP - 05/2025
# Alison Sérgio de Amarins Germano - RM 357521

*Ambiente de desenvolvimento utilizado foi o Colab e VS CODE

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
from PIL import Image
from gtts import gTTS
# Importação da função que carrega o zip
from ler_dados_applicants_zip import carregar_csv_de_zip
# Texto que será narrado
texto_narracao = """
Bem-vindo ao sistema de recomendação de vagas. Esta solução ajuda empresas a encontrar os candidatos ideais 
analisando perfis, palavras-chave e históricos de aceites. 
Os dados foram preparados no Colab e a experiência criada com Streamlit."""
# Cabeçalho
st.write("# Tech Challenge Fase 5")
st.markdown("**Alison Sérgio de Amarins Germano - RM 357521**") 
st.markdown("**Data Analytics FIAP - 05/2025 - 6DTAT**") 
st.write("## Sistema de Recomendação de Vagas e Candidatos")
st.image("job_match_humanizado.png", caption='"O prazer no trabalho aperfeiçoa a obra." - Aristóteles')
st.markdown("**Problema:**")
st.markdown("""
Empresa enfrenta dificuldades para identificar os melhores candidatos para cada vaga e, 
inversamente, oferecer as melhores vagas aos profissionais cadastrados.
""")

# Gerar e salvar áudio MP3
audio_file = "narracao_apresentacao.mp3"
if os.path.exists(audio_file):
    os.remove(audio_file)

tts = gTTS(text=texto_narracao, lang='pt')
tts.save(audio_file)

# Painel de Introdução Interativo
with st.expander("ℹ️ Sobre este sistema de recomendação", expanded=True):
    # Tocar o áudio com um player
    st.audio(audio_file, format="audio/mp3")

    st.markdown("""
    Este sistema tem como objetivo **recomendar automaticamente os melhores pares entre vagas e candidatos**.

    🔍 **Como funciona:**
    - Utiliza técnicas de **Processamento de Linguagem Natural (NLP)** para extrair palavras-chave de currículos e vagas.
    - Calcula a similaridade entre candidatos e vagas usando **TF-IDF + Cosine Similarity**.
    - Usa a coluna `data_aceite` como indicação real de que houve **match verdadeiro**, permitindo análises supervisionadas.

    📊 **Gráficos disponíveis:**
    - **Distribuição de Aceites:** mostra quantos candidatos aceitaram as vagas.
    - **Top 5 Clientes e Candidatos:** análise dos melhores com base na média dos scores.
    - **Heatmap:** comparação entre origens dos rankings e clientes.
    - **Matches Reais com Alto Score:** candidatos aceitos com alta compatibilidade.

    🔧 **Filtros disponíveis:** selecione origem do ranking ou título da vaga.

    ---
    ⚙️ Projeto construído em duas etapas:
    - Pré-processamento e Machine Learning via **Google Colab**.
    - Visualização e Storytelling com **Streamlit no VS Code**.

    """)
# Carregar os dados
assert os.path.exists("base_final_ml_com_nome_cliente.zip"), "Arquivo base_final_ml_com_nome_cliente.zip não encontrado"
#df = pd.read_csv("base_final_ml_com_nome_cliente.csv")
df = carregar_csv_de_zip("base_final_ml_com_nome_cliente.zip", "base_final_ml_com_nome_cliente.csv", ",")
# Verificações e carregamento
assert os.path.exists("dados_applicants_limpo.zip"), "Arquivo dados_applicants_limpo.zip não encontrado"
df_applicants = carregar_csv_de_zip("dados_applicants_limpo.zip", "dados_applicants_limpo.csv",";")
#
assert os.path.exists("df_base.zip"), "Arquivo df_base.zip não encontrado"
df_base = carregar_csv_de_zip("df_base.zip", "df_base.csv",";")
#
df_vagas = carregar_csv_de_zip("df_vagas_limpo.zip", "df_vagas_limpo.csv",";")
# Criar coluna binária para match real
df_applicants['match_real'] = df_applicants['data_aceite'].notnull().astype(int)
df = df.merge(df_applicants[['codigo_profissional', 'match_real']], on='codigo_profissional', how='left')

df['match_real'] = df['match_real'].fillna(0).astype(int)
df = df.drop_duplicates(subset='codigo_profissional')

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
st.caption("Este gráfico mostra a quantidade de candidatos que aceitaram ou não as vagas recomendadas.")
fig1, ax1 = plt.subplots()
sns.countplot(data=df_filtrado, x='match_real', palette='Set2', ax=ax1)
ax1.set_title("Distribuição de Aceites Reais")
ax1.set_xlabel("Match Real (0 = Não Aceitou, 1 = Aceitou)")
ax1.set_ylabel("Quantidade")
st.pyplot(fig1)
#-------------------------------------------------------------------------
# Gráfico 2 – Top 5 Score Médio por Cliente
st.subheader("Top 5 Clientes com Maior Score Médio")
st.caption("Clientes que receberam candidatos com maior compatibilidade média de perfil.")
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
st.caption("Mostra como a qualidade (score) das recomendações varia entre os clientes e a origem do ranking (vaga/candidato).")
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
st.caption("Visualização da performance média das recomendações por cliente e origem do ranking.")
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
st.caption("Exibe combinações bem-sucedidas (match_real = 1) com alta similaridade (score ≥ 0.8).")
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
st.title("Conclusão")
with st.expander("📘 Ver Conclusão do Projeto"):
    st.markdown("### 🧾 Conclusão do Projeto")
    st.markdown("""
    O projeto Fase 5 (Datathon) teve como principal objetivo desenvolver um sistema de recomendação inteligente que conectasse candidatos e vagas com base em critérios técnicos, linguísticos e históricos de aceitação real. Para atingir esse objetivo, foi utilizada uma abordagem estruturada, dividindo o projeto em duas frentes principais:
    """)

    st.markdown("#### 1️⃣ Google Colab – Processamento e Modelagem de Dados")
    st.markdown("""
    Nesta etapa, foi realizada toda a **Análise Exploratória de Dados (EDA)**, **limpeza e tratamento de inconsistências**, normalização de estruturas complexas (como listas em colunas), além da aplicação de **técnicas de NLP (Processamento de Linguagem Natural)** para extração de palavras-chave tanto dos currículos quanto das descrições das vagas.  
    A partir dessas informações, foram construídas bases estruturadas para **cálculo de similaridade textual com TF-IDF**, gerando scores de match entre candidatos e vagas. Também foi feita a engenharia de variáveis e a identificação de casos reais de aceite por meio da variável `data_aceite`, permitindo criar uma **variável alvo (match_real)** para análises supervisionadas futuras.
    """)

    st.markdown("#### 2️⃣ Streamlit – Interface Interativa e Storytelling")
    st.markdown("""
    Com as bases prontas, foi migrada para o ambiente **Streamlit** para construir uma interface de **análise visual e tomada de decisão**.  
    Nesta fase, o foco foi na criação de gráficos interativos, filtros dinâmicos e consultas específicas, como o *Top 5 candidatos por vaga* ou *Top 5 vagas por candidato*.  
    Foram incluídos ainda filtros por origem do ranking, permitindo aos usuários explorarem os dados de forma intuitiva e direcionada.  

    Um painel analítico e humanizado com storytelling orienta a interpretação dos resultados, oferecendo não apenas uma visualização, mas também **insights de valor para recrutamento inteligente**.
    """)

    st.markdown("### 🔍 Conclusão Técnica do Sistema")
    st.markdown("""
    Este modelo híbrido entre **Colab (processamento e modelagem)** e **Streamlit (visualização e entrega)** se mostrou eficiente e robusto para o objetivo proposto, permitindo separar claramente o esforço computacional da experiência final de uso.  

    💡 **Observação:** Por se tratar de um **protótipo funcional**, foi utilizada uma **base de dados reduzida**, com o objetivo de otimizar desempenho e facilitar testes durante o desenvolvimento iterativo.  

    ⚙️ Entretanto, como toda solução baseada em dados, o modelo ainda **demanda validações adicionais** e **ciclos contínuos de aprimoramento**, especialmente para:  
    - Aumentar a **assertividade nas recomendações**  
    - Proporcionar uma **experiência mais fluida e estratégica** ao processo de recrutamento.
    """)


