import sys
import pandas as pd


# ─────────────────────────────────────────────
#  Configurações — edite aqui se necessário
# ─────────────────────────────────────────────
ARQUIVO_ENTRADA = "DB_NPAtlas.xlsx"
SHEET_NAME      = "Metabólitos editada"

ANALISES = [
    {
        "nome": "Bioatividade × Habitat",
        "arquivo_saida": "resultado_bioatividadeXhabitat.csv",
        "coluna_molecula": "molecula",
        "coluna_id": "ID",
        "coluna_referencia": "autor",
        "colunas_grupo": ["bioatividade", "habitat"],
    },
    {
        "nome": "Bioatividade × Classe",
        "arquivo_saida": "resultado_bioatividadeXclasse.csv",
        "coluna_molecula": "molecula",
        "coluna_id": "ID",
        "coluna_referencia": "autor",
        "colunas_grupo": ["bioatividade", "classe"],
    },
]


# ─────────────────────────────────────────────
#  Função genérica de contagem
# ─────────────────────────────────────────────
def contar_moleculas_unicas(
    df: pd.DataFrame,
    coluna_molecula: str,
    coluna_id: str,
    coluna_referencia: str,
    colunas_grupo: list[str],
) -> pd.DataFrame:
    """
    Conta moléculas únicas por grupo, removendo duplicatas e entradas inválidas.

    Parâmetros
    ----------
    df               : DataFrame já carregado.
    coluna_molecula  : Coluna com o nome das moléculas.
    coluna_id        : Coluna de identificador único de linha.
    coluna_referencia: Coluna de referência bibliográfica (autor).
    colunas_grupo    : Colunas usadas no agrupamento (ex.: ["bioatividade", "habitat"]).

    Retorno
    -------
    DataFrame com: referência + colunas_grupo + Contagem.
    """
    # Validar colunas
    colunas_necessarias = {coluna_molecula, coluna_id, coluna_referencia} | set(colunas_grupo)
    ausentes = colunas_necessarias - set(df.columns)
    if ausentes:
        raise ValueError(f"Colunas ausentes na planilha: {sorted(ausentes)}")

    # Remover linhas com ID duplicado
    df = df.drop_duplicates(subset=coluna_id)

    # Remover NaN real nas colunas de grupo antes de converter para string
    df = df.dropna(subset=colunas_grupo)

    # Limpar espaços e padronizar como string em todas as colunas relevantes
    for col in [coluna_referencia, coluna_molecula] + colunas_grupo:
        df[col] = df[col].astype(str).str.strip()

    # Remover entradas que viraram string inválida após conversão
    valores_invalidos = {"nan", "na", "none", ""}
    for col in colunas_grupo:
        df = df[~df[col].str.lower().isin(valores_invalidos)]

    # Contar moléculas únicas por grupo
    chave_grupo = [coluna_referencia] + colunas_grupo
    resultado = (
        df.groupby(chave_grupo)[coluna_molecula]
        .nunique()
        .reset_index(name="Contagem")
        .sort_values(colunas_grupo + ["Contagem"], ascending=[True] * len(colunas_grupo) + [False])
        .reset_index(drop=True)
    )

    return resultado


# ─────────────────────────────────────────────
#  Execução principal
# ─────────────────────────────────────────────
def main():
    print(f"Carregando '{ARQUIVO_ENTRADA}' (aba: '{SHEET_NAME}')…")
    try:
        df = pd.read_excel(ARQUIVO_ENTRADA, engine="openpyxl", sheet_name=SHEET_NAME)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{ARQUIVO_ENTRADA}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO] Não foi possível ler a planilha: {e}")
        sys.exit(1)

    print(f"  → {len(df)} linhas carregadas.\n")

    for analise in ANALISES:
        nome = analise["nome"]
        print(f"Processando: {nome}")
        try:
            resultado = contar_moleculas_unicas(
                df=df,
                coluna_molecula=analise["coluna_molecula"],
                coluna_id=analise["coluna_id"],
                coluna_referencia=analise["coluna_referencia"],
                colunas_grupo=analise["colunas_grupo"],
            )

            if resultado.empty:
                print(f"  [AVISO] Nenhum dado gerado para '{nome}'. Verifique os filtros.")
                continue

            resultado.to_csv(analise["arquivo_saida"], index=False, encoding="utf-8")
            print(f"  → {len(resultado)} combinações únicas | salvo em '{analise['arquivo_saida']}'")
            print(resultado.head(5).to_string(index=False))
            print()

        except ValueError as e:
            print(f"  [ERRO] {e}\n")

    print("Concluído.")


if __name__ == "__main__":
    main()
