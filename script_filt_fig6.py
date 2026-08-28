import pandas as pd
import os

def contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_genero, coluna_id, coluna_referencia, coluna_especie, formato='xlsx'):
    """
    Conta o número de moléculas únicas por habitat, gênero e espécie, considerando uma coluna de referência e evitando duplicatas dentro da mesma referência e espécie.

    Args:
        arquivo: Nome do arquivo da planilha (CSV ou XLSX).
        coluna_molecula: Nome da coluna com o nome das moléculas.
        coluna_habitat: Nome da coluna com o habitat.
        coluna_genero: Nome da coluna com o gênero.
        coluna_id: Nome da coluna com o identificador único.
        coluna_referencia: Nome da coluna com a referência.
        coluna_especie: Nome da coluna com a espécie.
        formato: Formato do arquivo (padrão 'xlsx', pode ser 'csv').

    Returns:
        Um DataFrame com as contagens de moléculas por habitat, gênero e espécie, considerando a referência.
    """

    try:
        # Verificar se o arquivo existe
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"O arquivo {arquivo} não foi encontrado no diretório {os.getcwd()}.")

        # Carregar a planilha
        if formato == 'csv':
            df = pd.read_csv(arquivo)
        elif formato == 'xlsx':
            df = pd.read_excel(arquivo, engine='openpyxl')
        else:
            raise ValueError("Formato de arquivo inválido. Utilize 'csv' ou 'xlsx'.")

        # Remover duplicatas
        df = df.drop_duplicates(subset=coluna_id)

        # Ordenar o DataFrame pelas colunas de referência, habitat, gênero, espécie e molécula
        df = df.sort_values([coluna_referencia, coluna_habitat, coluna_genero, coluna_especie, coluna_molecula])

        # Agrupar e contar, considerando a coluna de referência, habitat e espécie
        resultado = df.groupby([coluna_referencia, coluna_habitat, coluna_genero, coluna_especie])[coluna_molecula].nunique().reset_index(name="Contagem")

        return resultado

    except FileNotFoundError as e:
        print(e)
        return pd.DataFrame()  # Retorna DataFrame vazio
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)
        return pd.DataFrame()  # Retorna DataFrame vazio

# Exemplo de uso
arquivo = "DB_NPAtlas.xlsx"
coluna_molecula = "molecula"
coluna_habitat = "habitat"
coluna_genero = "genero"
coluna_id = "ID"
coluna_referencia = "autor"
coluna_especie = "especie"

# Verificar diretório atual e arquivos disponíveis
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())

resultado = contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_genero, coluna_id, coluna_referencia, coluna_especie)
if resultado is not None and not resultado.empty:
    resultado.to_csv("resultado_habitatXgenero.csv", index=False)
    print("Resultados salvos em resultado_habitatXgenero.csv")
else:
    print("Nenhum resultado para salvar.")
