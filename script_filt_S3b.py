import pandas as pd

def contar_moleculas_unicas(arquivo, coluna_molecula, coluna_especie, coluna_id, coluna_referencia, coluna_morfologia, formato='csv'):
    """
    Conta o número de moléculas únicas por espécie e morfologia, considerando uma coluna de referência e evitando duplicatas dentro da mesma referência e morfologia.

    Args:
        arquivo: Nome do arquivo da planilha (CSV ou XLSX).
        coluna_molecula: Nome da coluna com o nome das moléculas.
        coluna_especie: Nome da coluna com a espécie.
        coluna_id: Nome da coluna com o identificador único.
        coluna_referencia: Nome da coluna com a referência.
        coluna_morfologia: Nome da coluna com a morfologia.
        formato: Formato do arquivo (padrão 'csv', pode ser 'xlsx').

    Returns:
        Um DataFrame com as contagens de moléculas por espécie e morfologia, considerando a referência.
    """

    try:
        # Carregar a planilha
        if formato == 'csv':
            df = pd.read_csv(arquivo)
        elif formato == 'xlsx':
            df = pd.read_excel(arquivo, engine='openpyxl')
        else:
            raise ValueError("Formato de arquivo inválido. Utilize 'csv' ou 'xlsx'.")

        # Remover duplicatas
        df = df.drop_duplicates(subset=coluna_id)

        # Filtrar espécies com inconsistências
        invalid_terms = ['cf.', 'sp.', 'spp.', 'aff.', 'NA']
        df = df[~df[coluna_especie].str.contains('|'.join(invalid_terms), case=False, na=False)]

        # Ordenar o DataFrame pelas colunas de referência, espécie, morfologia e molécula
        df = df.sort_values([coluna_referencia, coluna_especie, coluna_morfologia, coluna_molecula])

        # Agrupar e contar, considerando a coluna de referência, espécie e morfologia
        resultado = df.groupby([coluna_referencia, coluna_especie, coluna_morfologia])[coluna_molecula].nunique().reset_index(name="Contagem")

        return resultado

    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)

# Exemplo de uso
arquivo = "planilha_base_oficial.xlsx"
coluna_molecula = "molecula"
coluna_especie = "especie"
coluna_id = "ID"
coluna_referencia = "autor"
coluna_morfologia = "morfologia"

resultado = contar_moleculas_unicas(arquivo, coluna_molecula, coluna_especie, coluna_id, coluna_referencia, coluna_morfologia, formato='xlsx')

if resultado is not None:
    resultado.to_csv("resultado_especieXmorfologia.csv", index=False, encoding='latin1')  # Use 'latin1' para salvar
    print("Resultados salvos em resultado_especieXmorfologia.csv")
else:
    print("Nenhum resultado foi gerado devido a um erro.")
