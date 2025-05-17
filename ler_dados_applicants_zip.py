import pandas as pd
import zipfile

import pandas as pd
import zipfile

def carregar_dados_applicants(zip_path="dados_applicants_limpo.zip", csv_name="dados_applicants_limpo.csv"):
    """
    Lê um arquivo CSV de dentro de um ZIP e retorna um DataFrame.
    Assume que o CSV está separado por ponto e vírgula (;)
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(csv_name) as file:
            df = pd.read_csv(file, sep=';', encoding='utf-8')
    return df
