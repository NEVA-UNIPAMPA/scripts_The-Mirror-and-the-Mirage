import pandas as pd

def contar_moleculas_unicas(arquivo, coluna_molecula, coluna_bioatividade, coluna_id, coluna_referencia, coluna_cepa, coluna_especie):
    """
    Conta o número de moléculas únicas por bioatividade, cepa e espécie, considerando uma coluna de referência e evitando duplicatas dentro da mesma referência.
    Linhas com valores NA na coluna 'bioatividade' são desconsideradas.

    Args:
        arquivo: Nome do arquivo da planilha (XLSX).
        coluna_molecula: Nome da coluna com o nome das moléculas.
        coluna_bioatividade: Nome da coluna com a bioatividade.
        coluna_id: Nome da coluna com o identificador único.
        coluna_referencia: Nome da coluna com a referência.
        coluna_cepa: Nome da coluna com a cepa.
        coluna_especie: Nome da coluna com a espécie.

    Returns:
        Um DataFrame com as contagens de moléculas por bioatividade, cepa e espécie, considerando a referência.
    """

    try:
        # Carregar a planilha (formato XLSX)
        df = pd.read_excel(arquivo, engine='openpyxl')

        # Verificar se as colunas necessárias estão presentes
        colunas_necessarias = [coluna_molecula, coluna_bioatividade, coluna_id, coluna_referencia, coluna_cepa, coluna_especie]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise ValueError(f"A coluna '{coluna}' não foi encontrada no arquivo.")

        # Remover duplicatas
        df = df.drop_duplicates(subset=coluna_id)

        # Remover linhas onde a coluna 'bioatividade' tem valores NA
        df = df.dropna(subset=[coluna_bioatividade])

        # Converter todas as colunas relevantes para strings (para evitar problemas de ordenação)
        df[coluna_referencia] = df[coluna_referencia].astype(str)
        df[coluna_bioatividade] = df[coluna_bioatividade].astype(str)
        df[coluna_cepa] = df[coluna_cepa].astype(str)
        df[coluna_especie] = df[coluna_especie].astype(str)

        # Ordenar o DataFrame pelas colunas de referência, bioatividade, cepa, espécie e molécula
        df = df.sort_values([coluna_referencia, coluna_bioatividade, coluna_cepa, coluna_especie, coluna_molecula])

        # Agrupar e contar, considerando a coluna de referência, bioatividade, cepa e espécie
        resultado = df.groupby([coluna_referencia, coluna_bioatividade, coluna_cepa, coluna_especie])[coluna_molecula].nunique().reset_index(name="Contagem")

        return resultado

    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print("Ocorreu um erro inesperado:", e)

# Exemplo de uso
arquivo = "DB_NPAtlas.xlsx"  # Arquivo de entrada no formato XLSX
coluna_molecula = "molecula"
coluna_bioatividade = "bioatividade"
coluna_id = "ID"
coluna_referencia = "autor"
coluna_cepa = "cepa"  # Coluna de cepa
coluna_especie = "especie"  # Coluna de espécie (acrescentada)

resultado = contar_moleculas_unicas(arquivo, coluna_molecula, coluna_bioatividade, coluna_id, coluna_referencia, coluna_cepa, coluna_especie)

if resultado is not None:
    resultado.to_csv("resultado_bioatividadeXcepaXespecie.csv", index=False, encoding='utf-8')  # Usar 'utf-8' para salvar
    print("Resultados salvos em resultado_bioatividadeXcepaXespecie.csv")
else:
    print("Nenhum resultado foi gerado devido a um erro.")
