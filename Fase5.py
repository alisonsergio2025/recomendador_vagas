"""
# Tech Challenge Fase 4
# Data Analytics FIAP - 02/2025
# Alison Sérgio de Amarins Germano - RM 357521

*Ambiente de desenvolvimento utilizado foi o VS CODE

**1. Desenvolver um modelo preditivo com dados da Cotação do preço de barril de petróleo para criar uma série temporal e prever o fechamento.**

**1. Instalando Bibliotecas**
"""
# Importando e Aplicando o álias a cada biblioteca
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ignorar avisos específicos emitidos pelo Pandas tipo SettingWithCopyWarning
import warnings
from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore")

st.write("# Tech Challenge Fase 5")
st.write('<b><span style="font-size: 20px;">Alison Sérgio de Amarins Germano - RM 357521</b>', unsafe_allow_html=True) 
st.write("# Sistema de Recomendação de Vagas e Candidatos")
st.write('<b><span style="font-size: 20px;">Problema :</b>', unsafe_allow_html=True) 
'''
Empresa enfrenta dificuldades para identificar os melhores candidatos para cada vaga e, 
inversamente, oferecer as melhores vagas aos profissionais cadastrados.

'''
st.write('<b><span style="font-size: 20px;">Objetivos : </b>', unsafe_allow_html=True)
'''
Recomendar automaticamente os melhores pares vaga ↔ candidato.
''' 
st.write("# Solução Proposta")
st.write('<b><span style="font-size: 20px;">Desenvolvemos um sistema inteligente que combina:</b>', unsafe_allow_html=True) 
'''
- Processamento de textos (descrições de currículos e vagas)
'''
'''
- Técnicas de similaridade (TF-IDF)
'''
'''
- Modelos supervisionados com base em data_aceite (match real)
'''
'''
- Visualizações analíticas
'''
st.write('<b><span style="font-size: 20px;"></b>', unsafe_allow_html=True) 
#"""**1**.Acessando a base de dados"""



st.title("Conclusão")
'''

Se considerarmos todas as métricas, o modelo "SeasWA" parece ter um desempenho geral melhor, pois apresenta os menores valores de MAE, RMSE e MASE, que são métricas críticas para avaliação da previsão.

Se focarmos apenas em WMAPE, o Prophet seria o melhor.

Se analisarmos MAPE e SMAPE, o XGBoost se destaca.

Porém, como o SeasWA tem os melhores resultados em várias métricas importantes, ele parece ser a melhor escolha globalmente
'''
