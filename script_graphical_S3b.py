import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# 1. Configurações de Estilo (Arial 8pt, 600 DPI)
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Liberation Sans', 'DejaVu Sans']
mpl.rcParams['font.size'] = 8

# Dicionário de Tradução Específico
TRANSLATION_MAP = {
    'cocoide': 'Coccoid',
    'heterocitada': 'Heterocytous',
    'homocitada': 'Non-heterocytous'
}

def generate_scientific_doughnut(filename):
    try:
        # Carregamento dos dados
        df = pd.read_excel(filename, engine='openpyxl')
        df = df.drop_duplicates(subset='ID')
        
        # Filtros de espécies (Removendo cf., sp., etc.)
        invalid_terms = ['cf.', 'sp.', 'spp.', 'aff.', 'NA']
        df = df[~df['especie'].str.contains('|'.join(invalid_terms), case=False, na=False)]
        
        # Normalização e Tradução dos termos de Morfologia
        df['morfologia'] = df['morfologia'].str.lower().str.strip()
        df['morfologia_en'] = df['morfologia'].map(TRANSLATION_MAP).fillna(df['morfologia'].str.capitalize())
        
        # Agrupamento e Contagem
        res = df.groupby('morfologia_en')['especie'].nunique().sort_values(ascending=False).reset_index()
        res.columns = ['Morphology', 'Count']

        # --- DIMENSÕES (84 mm e Margens Mínimas) ---
        width_in = 84 / 25.4
        height_in = width_in  # Proporção 1:1

        # Criando a figura
        fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=600)

        # Paleta de Azuis (RGB de Alto Contraste)
        COLORS = ['#003366', '#336699', '#6699CC']

        # Gráfico de Rosca (Doughnut)
        wedges, texts, autotexts = ax.pie(
            res['Count'], 
            labels=res['Morphology'], 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=COLORS,
            pctdistance=0.75,
            wedgeprops={'width': 0.4, 'edgecolor': 'w'}
        )

        # Ajuste fino das fontes
        plt.setp(texts, size=7)
        plt.setp(autotexts, size=6, weight="bold", color="white")
        
        ax.axis('equal')  

        # --- REMOÇÃO DE ÁREA BRANCA ---
        # tight_layout ajusta o conteúdo, e pad_inches no savefig remove a borda externa
        plt.tight_layout()

        output_name = "morphology_fixed_84mm.png"
        
        # pad_inches=0.01 remove quase todo o espaço em branco ao redor da imagem
        plt.savefig(output_name, dpi=600, bbox_inches='tight', pad_inches=0.01)
        
        print(f"\n✅ SUCESSO! Gráfico salvo em: {os.path.abspath(output_name)}")
        print(f"Termos usados: {res['Morphology'].tolist()}")
        
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao processar: {e}")

# Execução
arquivo = "planilha_base_oficial.xlsx"
if os.path.exists(arquivo):
    generate_scientific_doughnut(arquivo)
else:
    print(f"Arquivo '{arquivo}' não encontrado.")
