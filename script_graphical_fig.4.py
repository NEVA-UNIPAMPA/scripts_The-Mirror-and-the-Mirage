import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import unicodedata
from PIL import Image
import io

# ==============================================================================
# 1. CONFIGURAÇÕES FÍSICAS EXATAS DO GRÁFICO
# ==============================================================================
DPI = 600
TAMANHO_MM = 234 # Largura/Altura cravada em 234 mm
TAMANHO_IN = TAMANHO_MM / 25.4 

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['text.color'] = 'black' 

# ==============================================================================
# 2. CARREGAMENTO DOS DADOS
# ==============================================================================
try:
    df_data = pd.read_csv('resultado_habitatXpaisXclima.csv')
except FileNotFoundError:
    data = {
        'habitat': ['floresta', 'marinho', 'deserto', 'rio', 'urbano'] * 20,
        'pais': ['brasil', 'usa', 'china', 'australia', 'franca'] * 20,
        'clima': ['tropical', 'temperado', 'arido', 'subtropical', 'continental'] * 20,
        'Contagem': np.random.randint(10, 100, 100)
    }
    df_data = pd.DataFrame(data)

# ==============================================================================
# 3. LIMPEZA E MAPEAMENTO (INGLÊS)
# ==============================================================================
def normalize_str(text):
    if not isinstance(text, str): return str(text)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.lower().strip()

def clean_habitat_en(hab_str):
    if not isinstance(hab_str, str): return "Others"
    h = normalize_str(hab_str)
    if any(x in h for x in ['hot', 'thermal', 'termal', 'geo', 'hydro', 'spring']): return 'Thermal Spring'
    if any(x in h for x in ['doce', 'fresh', 'rio', 'river', 'lago', 'lake', 'pond']): return 'Freshwater'
    if any(x in h for x in ['salobra', 'brackish', 'estuari', 'mangue']): return 'Brackish'
    if any(x in h for x in ['salgada', 'marinho', 'marine', 'sea', 'ocean', 'recife', 'coral']): return 'Saltwater'
    if any(x in h for x in ['terrestre', 'terrestrial', 'solo', 'soil', 'terra', 'land', 'floresta', 'forest']): return 'Terrestrial'
    return "Others"

def clean_climate_en(clim_str):
    if not isinstance(clim_str, str): return "Unknown"
    c = normalize_str(clim_str)
    if 'subtropical' in c: return 'Subtropical'
    if 'tropical' in c: return 'Tropical'
    if 'temperado' in c or 'temperate' in c: return 'Temperate'
    if 'continental' in c: return 'Continental'
    if 'arido' in c or 'arid' in c: return 'Arid'
    if 'polar' in c or 'artico' in c: return 'Polar'
    return "Unknown"

normalized_country_map_en = {
    # South America
    'brasil': 'South America', 'brazil': 'South America', 'colombia': 'South America', 'argentina': 'South America',
    'chile': 'South America', 'peru': 'South America', 'equador': 'South America', 'venezuela': 'South America',
    'uruguai': 'South America', 'bolivia': 'South America', 'guiana francesa': 'South America',
    # North America
    'eua': 'North America', 'usa': 'North America', 'united states': 'North America', 'canada': 'North America',
    'mexico': 'North America', 'bermuda': 'North America',
    # Central America & Caribbean
    'panama': 'Central America', 'costa rica': 'Central America', 'curacao': 'Central America',
    'porto rico': 'Central America', 'bahamas': 'Central America', 'belize': 'Central America',
    'guatemala': 'Central America', 'cuba': 'Central America', 'jamaica': 'Central America',
    'honduras': 'Central America', 'granada': 'Central America', 'ilhas virgens': 'Central America',
    'ilhas virgens americanas': 'Central America',
    # Asia
    'china': 'Asia', 'japao': 'Asia', 'japan': 'Asia', 'india': 'Asia', 'coreia': 'Asia', 'korea': 'Asia',
    'south korea': 'Asia', 'tailandia': 'Asia', 'vietna': 'Asia', 'indonesia': 'Asia', 'israel': 'Asia',
    'singapura': 'Asia', 'malasia': 'Asia', 'malaysia': 'Asia', 'filipinas': 'Asia', 'taiwan': 'Asia',
    'ira': 'Asia', 'arabia saudita': 'Asia', 'turquia': 'Asia', 'sri lanka': 'Asia', 'myanmar': 'Asia',
    'mongolia': 'Asia', 'qatar': 'Asia', 'hong kong': 'Asia', 'nepal': 'Asia', 'palestina': 'Asia',
    'kuwait': 'Asia', 'libano': 'Asia', 'jordania': 'Asia', 'omam': 'Asia',
    # Oceania
    'australia': 'Oceania', 'nova zelandia': 'Oceania', 'papua nova guine': 'Oceania', 'guam': 'Oceania',
    'palau': 'Oceania', 'fiji': 'Oceania', 'saipan': 'Oceania', 'micronesia': 'Oceania', 'polinesia': 'Oceania',
    'oahu': 'Oceania', 'samoa': 'Oceania', 'samoa americana': 'Oceania', 'tahiti': 'Oceania', 'moorea': 'Oceania',
    'enewetak': 'Oceania', 'tabuaeran': 'Oceania', 'ilhas marshall': 'Oceania', 'atol palmyra': 'Oceania',
    'ilhas marianas': 'Oceania', 'vanuatu': 'Oceania', 'ilhas salomao': 'Oceania',
    # Europe
    'alemanha': 'Europe', 'germany': 'Europe', 'franca': 'Europe', 'france': 'Europe', 'espanha': 'Europe',
    'spain': 'Europe', 'italia': 'Europe', 'italy': 'Europe', 'portugal': 'Europe', 'reino unido': 'Europe',
    'uk': 'Europe', 'holanda': 'Europe', 'netherlands': 'Europe', 'paises baixos': 'Europe', 'grecia': 'Europe',
    'republica tcheca': 'Europe', 'hungria': 'Europe', 'suica': 'Europe', 'austria': 'Europe', 'polonia': 'Europe',
    'croacia': 'Europe', 'irlanda': 'Europe', 'noruega': 'Europe', 'suecia': 'Europe', 'dinamarca': 'Europe',
    'russia': 'Europe', 'finlandia': 'Europe', 'islandia': 'Europe', 'ilhas canarias': 'Europe', 'belgica': 'Europe',
    'chipre': 'Europe', 'eslovenia': 'Europe', 'slovenia': 'Europe', 'servia': 'Europe', 'malta': 'Europe',
    'escocia': 'Europe', 'inglaterra': 'Europe',
    # Africa
    'egito': 'Africa', 'africa do sul': 'Africa', 'marrocos': 'Africa', 'quenia': 'Africa', 'kenya': 'Africa',
    'madagascar': 'Africa', 'nigeria': 'Africa', 'tunisia': 'Africa', 'gana': 'Africa', 'camaroes': 'Africa',
    'uganda': 'Africa', 'republica centro-africana': 'Africa', 'prasilin': 'Africa', 'argelia': 'Africa',
    'tanzania': 'Africa', 'seychelles': 'Africa', 'cabo verde': 'Africa', 'cape verde': 'Africa',
    # Antarctica
    'antartica': 'Antarctica', 'antarctica': 'Antarctica',
}

# Conjunto de keys que são seguras para busca parcial (comprimento >= 6, sem risco de falso-positivo)
_SAFE_PARTIAL_KEYS = {k: v for k, v in normalized_country_map_en.items() if len(k) >= 6}

def get_continent_en(pais_str):
    if not isinstance(pais_str, str): return "Others"
    p_clean = normalize_str(pais_str)
    # 1. Match exato (inclui keys curtas como 'ira', 'uk')
    if p_clean in normalized_country_map_en:
        return normalized_country_map_en[p_clean]
    # 2. Busca parcial apenas com keys longas (>= 6 chars), evitando falsos-positivos
    for k, v in _SAFE_PARTIAL_KEYS.items():
        if k in p_clean:
            return v
    return "Others"

col_hab, col_pais, col_clima, col_count = 'habitat', 'pais', 'clima', 'Contagem'

df_data['Habitat_EN'] = df_data[col_hab].apply(clean_habitat_en)
df_data['Climate_EN'] = df_data[col_clima].apply(clean_climate_en)
df_data['Continent_EN'] = df_data[col_pais].apply(get_continent_en)

df_data = df_data[df_data['Climate_EN'] != 'Unknown']

# ==============================================================================
# 4. ESTRUTURAÇÃO DOS DADOS
# ==============================================================================
df_grouped = df_data.groupby(['Continent_EN', 'Climate_EN', 'Habitat_EN'])[col_count].sum().reset_index()
df_grouped = df_grouped[df_grouped[col_count] > 0]

cont_totals = df_grouped.groupby('Continent_EN')[col_count].sum().sort_values(ascending=False)
cont_order = cont_totals.index.tolist()
if 'Others' in cont_order: cont_order.remove('Others'); cont_order.append('Others')

df_grouped['Continent_EN'] = pd.Categorical(df_grouped['Continent_EN'], categories=cont_order, ordered=True)
df_grouped = df_grouped.sort_values(['Continent_EN', 'Climate_EN', 'Habitat_EN'], ascending=[True, True, False])

l1_data = df_grouped.groupby('Continent_EN', observed=True)[col_count].sum()
l1_labels, l1_values = l1_data.index.tolist(), l1_data.values

l2_data = df_grouped.groupby(['Continent_EN', 'Climate_EN'], observed=True)[col_count].sum()
l2_data = l2_data[l2_data > 0]
l2_labels, l2_values = l2_data.index.get_level_values(1).tolist(), l2_data.values

l3_labels = df_grouped['Habitat_EN'].values
l3_values = df_grouped[col_count].values

# ==============================================================================
# 5. CORES
# ==============================================================================
continent_cmaps = {
    'South America': cm.Greens, 'Europe': cm.Blues, 'Asia': cm.Reds,
    'North America': cm.Purples, 'Oceania': cm.GnBu, 'Africa': cm.Oranges,
    'Central America': cm.YlOrBr, 'Antarctica': cm.PuBu, 'Others': cm.Greys
}

colors_l1, colors_l2, colors_l3 = [], [], []

for cont in l1_labels:
    base_cmap = continent_cmaps.get(cont, cm.Greys)
    colors_l1.append(base_cmap(0.5))
    
    cont_subset = df_grouped[df_grouped['Continent_EN'] == cont]
    clim_groups = cont_subset.groupby('Climate_EN', observed=True)[col_count].sum()
    clim_groups = clim_groups[clim_groups > 0]
    
    if len(clim_groups) > 0:
        colors_l2.extend(base_cmap(np.linspace(0.35, 0.55, len(clim_groups))))
        for clim in clim_groups.index:
            hab_subset = cont_subset[cont_subset['Climate_EN'] == clim]
            hab_groups = hab_subset.groupby('Habitat_EN', observed=True)[col_count].sum()
            if len(hab_groups) > 0:
                colors_l3.extend(base_cmap(np.linspace(0.2, 0.4, len(hab_groups))))

# ==============================================================================
# 6. PLOTAGEM MAXIMIZADA E ANOTAÇÕES EXTERNAS
# ==============================================================================
fig, ax = plt.subplots(figsize=(TAMANHO_IN, TAMANHO_IN), dpi=DPI)
ax.axis('equal')

size = 0.35 
r1 = 0.25   
r2 = r1 + size
r3 = r2 + size

wprops = dict(width=size, edgecolor='white', linewidth=1.2)

w1, _ = ax.pie(l1_values, radius=r1+size/2, colors=colors_l1, wedgeprops=wprops, startangle=90)
w2, _ = ax.pie(l2_values, radius=r2+size/2, colors=colors_l2, wedgeprops=wprops, startangle=90)
w3, _ = ax.pie(l3_values, radius=r3+size/2, colors=colors_l3, wedgeprops=wprops, startangle=90)

# --- RÓTULOS INTERNOS ---
def label_force_all(wedges, labels, values, radius, fontsize, mostrar_valor=True, min_perc=0.0, force_show=False, exceto=[]):
    total = sum(values)
    for i, p in enumerate(wedges):
        perc = (values[i]/total)*100
        txt_raw = labels[i]
        
        if any(ex in txt_raw for ex in exceto):
            continue
        
        if force_show or perc >= min_perc:
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            
            rot = ang
            if 90 < ang < 270:
                rot += 180
            
            r_pos = radius - (size/2)
            
            if force_show and perc < 4.0:
                r_pos = radius - (size * 0.6)
            
            txt = txt_raw.replace(" ", "\n") 
            
            if mostrar_valor and perc >= 3.0: 
                txt += f"\n{perc:.0f}%"
            
            ax.text(x*r_pos, y*r_pos, txt, 
                    ha="center", va="center", 
                    rotation=rot, rotation_mode='anchor', 
                    fontsize=fontsize, fontweight='bold', color='black')

# Desenha os textos internos
label_force_all(w1, l1_labels, l1_values, radius=r1+size/2, fontsize=8, mostrar_valor=False, force_show=True, exceto=['Others', 'Antarctica'])
label_force_all(w2, l2_labels, l2_values, radius=r2+size/2, fontsize=8,  mostrar_valor=True,  min_perc=1.0)  
label_force_all(w3, l3_labels, l3_values, radius=r3+size/2, fontsize=8,  mostrar_valor=True,  min_perc=1.0)  

# --- ASTERISCOS EXTERNOS (ANTARCTICA E OTHERS) ---
for i, p in enumerate(w1):
    label = l1_labels[i]
    if label in ['Antarctica', 'Others']:
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        
        rot = ang
        if 90 < ang < 270:
            rot += 180
            
        # Asterisco colado na borda externa
        r_out = (r3 + size/2) + 0.03 
        
        marker = "*" if label == 'Antarctica' else "**"
        
        ax.text(x*r_out, y*r_out, marker, 
                ha="center", va="center", 
                rotation=rot, rotation_mode='anchor', 
                fontsize=12, fontweight='bold', color='black')

# Ajuste de margem minimizado 
ax.set_xlim(-1.22, 1.22)
ax.set_ylim(-1.22, 1.22)

plt.tight_layout()

# ==============================================================================
# 7. EXPORTAÇÃO (PNG E TIFF, 600 DPI, 8-BIT RGB)
# ==============================================================================
png_filename = 'Sunburst_234mm_600dpi_Asteriscos_Colados.png'
tiff_filename = 'Sunburst_234mm_600dpi_Asteriscos_Colados.tiff'

# Salva primeiro em PNG (alta qualidade com margem apertada)
plt.savefig(png_filename, format='png', dpi=DPI, bbox_inches='tight', facecolor='white', pad_inches=0.02)

# Em seguida, abre o PNG gerado e converte estritamente para TIFF 8-bits
img = Image.open(png_filename).convert("RGB")
img.save(tiff_filename, format='TIFF', dpi=(DPI, DPI), compression='tiff_lzw')

print(f"Gráficos gerados com sucesso:\n- {png_filename}\n- {tiff_filename}")
