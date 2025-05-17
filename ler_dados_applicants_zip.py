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

def carregar_csv_de_zip(zip_path: str, csv_name: str, sep=';', encoding='utf-8') -> pd.DataFrame:
    """
    Lê um arquivo CSV de dentro de um arquivo ZIP e retorna um DataFrame.
    
    Parâmetros:
    - zip_path: caminho do arquivo .zip
    - csv_name: nome do arquivo CSV dentro do ZIP
    - sep: separador do CSV (padrão: ';')
    - encoding: codificação do CSV (padrão: 'utf-8')
    
    Retorna:
    - DataFrame do pandas
    """
    #with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    #    with zip_ref.open(csv_name) as file:
    #        df = pd.read_csv(file, sep=sep, encoding=encoding)
    #return df
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(csv_name) as file:
            df = pd.read_csv(
                file,
                sep=sep,
                encoding=encoding,
                on_bad_lines='skip'  # <- pula linhas com erro
            )
    return df