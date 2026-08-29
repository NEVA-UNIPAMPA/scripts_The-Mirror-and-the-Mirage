import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# 1. Configurações de Estilo (Arial 8pt, RGB, Alta Resolução)
# Definimos o fallback para garantir que funcione em qualquer sistema
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'Liberation Sans', 'DejaVu Sans']
mpl.rcParams['font.size'] = 8

# Cor RGB: Azul Marinho Profundo (Contraste > 4.5:1 garantido para acessibilidade)
BAR_COLOR = (0.0, 0.2, 0.4) 

def gerar_grafico_profissional(caminho_arquivo):
    try:
        # Carregar os dados
        # Ajuste o nome do arquivo e colunas conforme sua planilha
        df = pd.read_excel(caminho_arquivo, engine='openpyxl')
        
        # Limpeza básica (Mantendo a lógica do seu script original)
        df = df.drop_duplicates(subset='ID')
        df = df[df['especie'].notna()]
        
        # Contagem de espécies únicas por Ordem (em Inglês)
        res = df.groupby('ordem')['especie'].nunique().sort_values(ascending=True).reset_index()
        res.columns = ['Order', 'Species_Count']

        # --- CÁLCULO DE DIMENSÕES (84 mm) ---
        width_mm = 84
        width_in = width_mm / 25.4
        
        # Altura dinâmica para não esmagar as barras (ajusta conforme o número de ordens)
        # Se tiver muitas ordens, aumentamos a altura para manter a proporção
        height_in = (len(res) * 0.3) + 1.0 

        # Criar a figura
        fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=600)

        # GRÁFICO HORIZONTAL: É a melhor solução para nomes longos em colunas estreitas
        bars = ax.barh(res['Order'], res['Species_Count'], color=BAR_COLOR, height=0.7)

        # Labels em Inglês (Sem Título como solicitado)
        ax.set_xlabel('Number of Species', fontsize=8)
        
        # Estética Minimalista (Clean look)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.6)
        ax.spines['bottom'].set_linewidth(0.6)
        
        # Adicionar os números ao final de cada barra
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', va='center', fontsize=7)

        plt.tight_layout()

        # --- SALVAMENTO (Antes do plt.show) ---
        output_name = "species_distribution_84mm.png"
        plt.savefig(output_name, dpi=600, bbox_inches='tight')
        
        print(f"\n✅ SUCESSO!")
        print(f"Arquivo salvo em: {os.path.abspath(output_name)}")
        print(f"Configurações: 84mm largura, 600 DPI, Arial 8pt, RGB High Contrast.")

        # Mostrar na tela
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao processar o gráfico: {e}")

# --- EXECUÇÃO ---
# Certifique-se que o arquivo está na mesma pasta do script
nome_da_planilha = "planilha_base_oficial.xlsx"
if os.path.exists(nome_da_planilha):
    gerar_grafico_profissional(nome_da_planilha)
else:
    print(f"Arquivo '{nome_da_planilha}' não encontrado.")
