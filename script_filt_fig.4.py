import pandas as pd

def contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima):
    """
    Conta o número de moléculas únicas por habitat, país, clima e referência, 
    considerando uma coluna de referência e evitando duplicatas dentro da mesma referência.

    Args:
        arquivo: Nome do arquivo da planilha (XLSX).
        coluna_molecula: Nome da coluna com o nome das moléculas.
        coluna_habitat: Nome da coluna com o habitat.
        coluna_id: Nome da coluna com o identificador único.
        coluna_referencia: Nome da coluna com a referência.
        coluna_pais: Nome da coluna com o país.
        coluna_clima: Nome da coluna com o clima.

    Returns:
        Um DataFrame com as contagens de moléculas por habitat, país, clima e referência.
    """

    try:
        # Carregar a planilha como XLSX (ou CSV se preferir alterar a engine)
        # Nota: Se o arquivo for .xlsx use read_excel, se for .csv use read_csv
        if arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo, engine='openpyxl')
            
        print("Colunas encontradas no arquivo:", list(df.columns))
        
        # Verificar se as colunas esperadas existem
        required_columns = [coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas ausentes no arquivo: {missing_columns}")

        # Remover duplicatas baseadas no ID
        df = df.drop_duplicates(subset=coluna_id)

        # Ordenar o DataFrame pelas colunas de referência, habitat, país, clima e molécula
        df = df.sort_values([coluna_referencia, coluna_habitat, coluna_pais, coluna_clima, coluna_molecula])

        # Agrupar e contar moléculas únicas
        # Adicionamos 'coluna_clima' aqui
        resultado = df.groupby([coluna_referencia, coluna_habitat, coluna_pais, coluna_clima])[coluna_molecula].nunique().reset_index(name="Contagem")

        return resultado

    except FileNotFoundError:
        print("Erro: Arquivo não encontrado. Verifique o caminho: ", arquivo)
        return None
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# --- Configurações de Uso ---

# Nome do arquivo (Verifique se é .xlsx ou o .csv que você subiu)
arquivo = "planilha_base_oficial.xlsx" 

# Definição dos nomes das colunas
coluna_molecula = "molecula"
coluna_habitat = "habitat"
coluna_id = "ID"
coluna_referencia = "autor"
coluna_pais = "pais"
coluna_clima = "clima"  # Nova coluna adicionada

# Chamada da função
resultado = contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima)

if resultado is not None:
    # Salvar o resultado
    nome_saida = "resultado_habitatXpaisXclima.csv"
    resultado.to_csv(nome_saida, index=False, encoding='utf-8')
    print(f"Processamento concluído! Arquivo salvo como: {nome_saida}")
    print(resultado.head())
