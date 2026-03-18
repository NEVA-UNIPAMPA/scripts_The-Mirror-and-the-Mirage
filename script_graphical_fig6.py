import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.templates.default = "plotly_white"

# ===========================
# CONFIGURAÇÕES
# ===========================

DPI = 600
LARGURA_MM = 84

# conversão mm → px
LARGURA_PX = int((LARGURA_MM / 25.4) * DPI)
ALTURA_PX = 1200

COR_BARRA = "#3c1053"
COR_TEXTO = "black"

FILTRO_MIN = 4

HABITATS_ALVO = {
    'terrestre': 'Terrestrial',
    'água doce': 'Freshwater',
    'água salgada': 'Marine/Seawater',
    'água salobra': 'Brackish Water'
}

# ===========================
# PROCESSAMENTO DE DADOS
# ===========================

data = pd.read_csv('resultado_habitatXgenero.csv')

data['Contagem'] = pd.to_numeric(data['Contagem'], errors='coerce').fillna(0).astype(int)
data = data.dropna(subset=['habitat', 'genero'])

data['habitat'] = data['habitat'].str.lower().str.strip()
data['genero'] = data['genero'].str.capitalize()

data = data[data['habitat'].isin(HABITATS_ALVO.keys())]
data = data[~data['genero'].str.lower().str.endswith('ales')]

grouped = data.groupby(['habitat', 'genero'], as_index=False)['Contagem'].sum()

# ===========================
# CRIAÇÃO DO GRÁFICO
# ===========================

fig = make_subplots(
    rows=2,
    cols=2,
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

letras = ['a', 'b', 'c', 'd']

for i, (hab_pt, hab_en) in enumerate(HABITATS_ALVO.items()):

    df_hab = grouped[grouped['habitat'] == hab_pt].copy()
    df_hab = df_hab[df_hab['Contagem'] >= FILTRO_MIN]
    df_hab = df_hab.sort_values(by='Contagem', ascending=True)

    # nomes de gêneros em itálico
    df_hab['genero_fmt'] = df_hab['genero'].apply(lambda x: f"<i>{x}</i>")

    row = (i // 2) + 1
    col = (i % 2) + 1

    fig.add_trace(
        go.Bar(
            x=df_hab['Contagem'],
            y=df_hab['genero_fmt'],
            orientation='h',
            marker=dict(
                color=COR_BARRA,
                line=dict(color='white', width=1)
            ),
            text=df_hab['Contagem'],
            textposition='outside',
            textfont=dict(
                size=14,
                family="Arial",
                color=COR_TEXTO
            ),
            name=hab_en
        ),
        row=row, col=col
    )

    y_pos_title = 1.08

    # letra da subfigura
    fig.add_annotation(
        text=f"<b>{letras[i]}</b>",
        xref="x domain",
        yref="y domain",
        x=-0.05,
        y=y_pos_title,
        showarrow=False,
        font=dict(size=28, color='black', family="Arial"),
        xanchor='right',
        row=row, col=col
    )

    # título do habitat
    fig.add_annotation(
        text=hab_en,
        xref="x domain",
        yref="y domain",
        x=0.5,
        y=y_pos_title,
        showarrow=False,
        font=dict(size=24, color='black', family="Arial"),
        xanchor='center',
        row=row, col=col
    )

    fig.update_xaxes(
        title_text="Total Molecules",
        row=row,
        col=col,
        title_font=dict(size=16, family="Arial", color="black")
    )

    fig.update_yaxes(
        row=row,
        col=col,
        tickfont=dict(size=14, family="Arial", color="black")
    )

# ===========================
# LAYOUT FINAL
# ===========================

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=LARGURA_PX,
    height=ALTURA_PX,
    showlegend=False,
    margin=dict(l=120, r=100, t=120, b=100),
    font=dict(
        family="Arial",
        color="black"
    )
)

# ===========================
# EXPORTAÇÃO 600 DPI
# ===========================

output_file = "Habitats_84mm_600dpi.png"

print(f"Gerando imagem: {output_file}...")

fig.write_image(
    output_file,
    width=LARGURA_PX,
    height=ALTURA_PX,
    scale=1
)

from PIL import Image

png_file = "Habitats_84mm_600dpi.png"
tiff_file = "Habitats_84mm_600dpi.tiff"

img = Image.open(png_file)
img.save(tiff_file, dpi=(600,600))

print("TIFF 600 dpi gerado:", tiff_file)

print("TIFF 600 dpi gerado:", tiff_file)
print("Concluído!")
