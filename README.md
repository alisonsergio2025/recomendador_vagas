# 🤖 Recomendador Inteligente de Vagas e Candidatos

Este projeto é um **sistema de recomendação de vagas e candidatos** que utiliza técnicas de *Machine Learning* e *Processamento de Linguagem Natural (NLP)* para encontrar os melhores pares entre profissionais e oportunidades, com base em similaridade de perfis, palavras-chave e histórico real de aceites.

---

## 🎯 Objetivo

Oferecer uma solução inteligente para recrutamento, ajudando empresas a **identificar os candidatos mais compatíveis para cada vaga**, e profissionais a **encontrarem vagas alinhadas ao seu perfil**.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.12
- Streamlit
- Google Colab (pré-processamento)
- Pandas, Seaborn, Scikit-learn, gTTS, PyDub
- TF-IDF + Cosine Similarity (similaridade textual)
- Processamento de arquivos JSON, CSV e ZIP

---

## ⚙️ Estrutura do Projeto

| Pasta/Arquivo | Descrição |
|---------------|-----------|
| `Fase5.py` | Interface visual e lógica do sistema com Streamlit |
| `*.zip` | Arquivos de dados (candidatos, vagas, base final) |
| `ler_dados_applicants_zip.py` | Script de leitura de arquivos `.zip` com CSV embutido |
| `requirements.txt` | Bibliotecas necessárias |
| `README.md` | Este arquivo de documentação |
| `narracao_apresentacao.mp3` | Áudio automático gerado com gTTS |
| `job_match_humanizado.png` | Imagem de capa do sistema |

---

## 🚀 Como Executar o Projeto Localmente

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/recomendador_vagas.git
cd recomendador_vagas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Rode o sistema:
```bash
streamlit run Fase5.py
```

---

## 🌐 Acesse Online

O projeto está hospedado gratuitamente no Streamlit Cloud:

🔗 [recomendadorvagas.streamlit.app](https://recomendadorvagas-7jzzxzysyvsrtka82fckep.streamlit.app/)

---

## 📈 Funcionalidades

- Filtros interativos por cliente, origem de ranking, vaga
- Gráficos de análise exploratória e performance
- Recomendação Top 5 candidatos por vaga
- Exportação dos matches aceitos com alto score
- Narração automática da introdução via gTTS

---

## 🔍 Observações

- A base de dados foi **reduzida para prototipagem**.
- Todo o processamento pesado foi feito no Google Colab.
- A interface e o storytelling foram desenvolvidos no VS Code com Streamlit.

---

## 👨‍💻 Autor

**Alison Sérgio de Amarins Germano**  
Pós-Graduação FIAP | Data Analytics  
RM: 357521  
📅 19/05/2025

---
