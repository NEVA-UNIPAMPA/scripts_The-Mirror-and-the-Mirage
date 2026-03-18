import pandas as pd


def contar_moleculas_unicas(
    arquivo,
    coluna_molecula,
    coluna_especie,
    coluna_id,
    coluna_referencia,
    coluna_ordem,
    formato="csv"
):
    """
    Conta o número de moléculas únicas por referência, espécie e ordem,
    evitando duplicatas pelo ID.
    """

    try:
        # =========================
        # Leitura otimizada
        # =========================
        if formato == "csv":
            df = pd.read_csv(
                arquivo,
                dtype=str  # evita inferência desnecessária e economiza memória
            )
        elif formato == "xlsx":
            df = pd.read_excel(
                arquivo,
                engine="openpyxl",
                dtype=str
            )
        else:
            raise ValueError("Formato inválido. Use 'csv' ou 'xlsx'.")

        # =========================
        # Limpeza de dados
        # =========================

        # Remover duplicatas pelo ID
        df = df.drop_duplicates(subset=coluna_id)

        # Remover espécies inválidas
        df = df[
            ~df[coluna_especie]
            .str.contains("NA", case=False, na=False)
        ]

        # =========================
        # Agrupamento direto (sem sort desnecessário)
        # =========================
        resultado = (
            df.groupby(
                [coluna_referencia, coluna_especie, coluna_ordem],
                as_index=False
            )[coluna_molecula]
            .nunique()
            .rename(columns={coluna_molecula: "Contagem"})
        )

        return resultado

    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None
    except Exception as e:
        print("Erro inesperado:", e)
        return None


# =========================
# Execução
# =========================

arquivo = "planilha_base_oficial.xlsx"

resultado = contar_moleculas_unicas(
    arquivo,
    coluna_molecula="molecula",
    coluna_especie="especie",
    coluna_id="ID",
    coluna_referencia="autor",
    coluna_ordem="ordem",
    formato="xlsx"
)

if resultado is not None:
    resultado.to_csv(
        "resultado_especieXordem.csv",
        index=False,
        encoding="utf-8-sig"  # evita erro Unicode e abre bem no Excel
    )
    print("Resultados salvos com sucesso.")
else:
    print("Nenhum resultado foi gerado.")

