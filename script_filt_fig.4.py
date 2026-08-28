import pandas as pd
import unicodedata

def normalizar_texto(texto):
    """Remove acentos extras, espaços e padroniza capitalização (title case)."""
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize('NFKC', texto).strip()
    return texto.strip().title()

def contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima):
    """
    Conta o numero de moleculas unicas por habitat, pais, clima e referencia,
    considerando uma coluna de referencia e evitando duplicatas dentro da mesma referencia.

    Args:
        arquivo: Nome do arquivo da planilha (XLSX ou CSV).
        coluna_molecula: Nome da coluna com o nome das moleculas.
        coluna_habitat: Nome da coluna com o habitat.
        coluna_id: Nome da coluna com o identificador unico.
        coluna_referencia: Nome da coluna com a referencia.
        coluna_pais: Nome da coluna com o pais.
        coluna_clima: Nome da coluna com o clima.

    Returns:
        Um DataFrame com as contagens de moleculas por habitat, pais, clima e referencia.
    """

    try:
        # Carregar o arquivo
        if arquivo.endswith('.csv'):
            df = pd.read_csv(arquivo, encoding='utf-8')
        else:
            df = pd.read_excel(arquivo, engine='openpyxl')

        print("Colunas encontradas no arquivo:", list(df.columns))

        # Verificar se as colunas esperadas existem
        required_columns = [coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas ausentes no arquivo: {missing_columns}")

        n_antes = len(df)

        # Normalizar texto nas colunas categoricas antes de qualquer agrupamento.
        # Isso evita que "agua doce", "Agua Doce" e "AGUA DOCE" virem grupos diferentes.
        for col in [coluna_habitat, coluna_pais, coluna_clima]:
            df[col] = df[col].apply(normalizar_texto)

        # Remover duplicatas baseadas no ID e avisar quantas foram removidas
        df = df.drop_duplicates(subset=coluna_id, keep='first')
        n_depois = len(df)
        n_removidas = n_antes - n_depois
        if n_removidas > 0:
            print(f"Aviso: {n_removidas} linha(s) duplicadas pelo ID foram removidas "
                  f"(de {n_antes} para {n_depois} registros).")

        # Ordenar o DataFrame
        df = df.sort_values([coluna_referencia, coluna_habitat, coluna_pais, coluna_clima, coluna_molecula])

        # Agrupar e contar moleculas unicas
        resultado = df.groupby(
            [coluna_referencia, coluna_habitat, coluna_pais, coluna_clima]
        )[coluna_molecula].nunique().reset_index(name="Contagem")

        # Avisar se o resultado estiver vazio
        if resultado.empty:
            print("Atencao: o resultado esta vazio. Verifique se os dados e colunas estao corretos.")
            return None

        print(f"Processamento concluido: {len(resultado)} combinacoes unicas encontradas.")
        return resultado

    except FileNotFoundError:
        print("Erro: Arquivo nao encontrado. Verifique o caminho:", arquivo)
        return None
    except ValueError as ve:
        print(f"Erro de validacao: {ve}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None


# --- Configuracoes de Uso ---

# Nome do arquivo
arquivo = "DB_NPAtlas.xlsx"

# Definicao dos nomes das colunas
coluna_molecula = "molecula"
coluna_habitat = "habitat"
coluna_id = "ID"
coluna_referencia = "autor"
coluna_pais = "pais"
coluna_clima = "clima"

# Chamada da funcao
resultado = contar_moleculas_unicas(arquivo, coluna_molecula, coluna_habitat, coluna_id, coluna_referencia, coluna_pais, coluna_clima)

if resultado is not None:
    nome_saida = "resultado_habitatXpaisXclima.csv"
    resultado.to_csv(nome_saida, index=False, encoding='utf-8')
    print(f"Arquivo salvo como: {nome_saida}")
    print(resultado.head())
