import pandas as pd
import plotly.express as px
import os

# ===========================
# CONFIGURAÇÕES
# ===========================
INPUT_FILE = 'resultado_top_10_cepas_com_especie.csv'
OUTPUT_FILE = "Species_Strain_Bioactivity_English_Clean_300dpi.png"
WIDTH_PX = 1650
HEIGHT_PX = 1200
SCALE = 1

try:
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(INPUT_FILE, encoding='latin1')

# Criar coluna combinada
df['cepa'] = df['cepa'].fillna('')
df['especie_cepa'] = df.apply(lambda x: f"{x['especie']} {x['cepa']}".strip(), axis=1)

# ===========================
# 2. DICIONÁRIO PADRÃO (COMPLETO)
# ===========================
bio_translation = {
    "Inibidor proteico/ enzimático": "Prot./Enzyme Inh.",
    "Antitumoral e Citotóxico": "Antitumor/Cytotoxic",
    "Inibidor de canais iônicos": "Ion Channel Inh.",
    "Metabólicos e Reguladores Celulares": "Metab. & Cell Reg.",
    "Relacionados ao Sistema Imunológico": "Immune System",
    "Disfunções e Alterações Celulares": "Cell Dysfunction",
    "Tóxico em equinoderma": "Echinoderm Toxic",
    "Tóxico para peixes": "Fish Toxic",
    "Tóxico para lagostins": "Crayfish Toxic",
    "Herbicida/ alelopático": "Herbicide/Allelopathic",
    "Antiparasitários": "Antiparasitic",
    "Antifúngico": "Antifungal",
    "Antibacteriano": "Antibacterial",
    "Antiviral": "Antiviral",
    "Toxina": "Toxin",
    "Anticrustáceo": "Antifouling",
    "Algicida": "Anti-algal",
    "Antioxidante": "Antioxidant",
    "BRMT": "BRMT",
    "Molucicida": "Molluscicidal",
    "Protetores-UV": "Sunscreens",
    "Anti-inflamatorio": "Anti-inflammatory",
    "Anti-inflamatório": "Anti-inflammatory",
    "Canabinomimético": "Cannabimimetic",
    "Outros": "Other",
    "Biosurfactante": "Biosurfactant"
}

df['bioatividade_en'] = df['bioatividade'].map(bio_translation).fillna(df['bioatividade'])

# ===========================
# 3. FORMATAÇÃO (ITÁLICO)
# ===========================
def format_strain_name(name):
    if not isinstance(name, str): return str(name)
    parts = name.split()
    formatted_parts = []
    for part in parts:
        # Regra: Não italizar sp., cf., números ou letras maiúsculas soltas
        if part in ['sp.', 'cf.', 'spp.', 'var.', 'aff.'] or any(char.isdigit() for char in part) or (part.isupper() and len(part) > 1):
            formatted_parts.append(part)
        else:
            formatted_parts.append(f'<i>{part}</i>')
    return ' '.join(formatted_parts)

df['especie_cepa_formatted'] = df['especie_cepa'].apply(format_strain_name)

# ===========================
# 4. AGREGAÇÃO E PLOTAGEM
# ===========================
df_grouped = df.groupby(['bioatividade_en', 'especie_cepa_formatted'], as_index=False)['Contagem'].sum()
vmax = df_grouped['Contagem'].max()

fig = px.scatter(
    df_grouped,
    x='bioatividade_en',
    y='especie_cepa_formatted',
    size='Contagem',
    color='Contagem',
    color_continuous_scale='plasma',
    range_color=[0, vmax],
    size_max=60,
    labels={'bioatividade_en': 'Bioactivity', 'especie_cepa_formatted': 'Species/Strain', 'Contagem': 'Count'}
)

fig.update_layout(
    template='plotly_white',
    # Fontes gerais
    font=dict(family="Arial", size=20, color="black"),
    
    # Eixo X
    xaxis=dict(
        tickangle=-45, 
        title_font=dict(size=30, family="Arial Black"), 
        tickfont=dict(size=22), 
        title_standoff=20
    ),
    
    # Eixo Y
    yaxis=dict(
        title_font=dict(size=30, family="Arial Black"), 
        tickfont=dict(size=20), 
        categoryorder='category descending'
    ),
    
    # Barra de Cores (Sem Título)
    coloraxis_colorbar=dict(
        title=None,  # Remove o título "Record Count"
        tickfont=dict(size=20)
    ),
    
    # Margens
    margin=dict(l=80, r=50, t=50, b=180)
)

print(f"Gerando imagem: {OUTPUT_FILE}...")
try:
    fig.write_image(OUTPUT_FILE, width=WIDTH_PX, height=HEIGHT_PX, scale=SCALE)
    print("Concluído!")
except Exception as e:
    print(f"Erro ao salvar: {e}")
