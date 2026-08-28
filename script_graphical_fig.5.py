import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

# ==============================================================================
# STYLE
# ==============================================================================

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "text.color": "black"
})

# ==============================================================================
# FIGURE SIZE
# ==============================================================================

DPI = 600
WIDTH_MM = 234
WIDTH_IN = WIDTH_MM / 25.4
HEIGHT_IN = WIDTH_IN * (8 / 12)

# ==============================================================================
# LOAD DATA
# ==============================================================================

df_hab   = pd.read_csv("resultado_bioatividadeXhabitat.csv")
df_class = pd.read_csv("resultado_bioatividadeXclasse.csv")

COL_BIO   = "bioatividade"
COL_HAB   = "habitat"
COL_CLASS = "classe"
COL_COUNT = "Contagem"

# ==============================================================================
# TRANSLATIONS
# ==============================================================================

bio_translation = {
    "Inibidor proteico/ enzimático":        "Prot./Enzyme Inh.",
    "Antitumoral e Citotóxico":             "Antitumor/Cytotoxic",
    "Inibidor de canais iônicos":           "Ion Channel Inh.",
    "Metabólicos e Reguladores Celulares":  "Metab. & Cell Reg.",
    "Relacionados ao Sistema Imunológico":  "Immune System",
    "Disfunções e Alterações Celulares":    "Cell Dysfunction",
    "Tóxico em equinoderma":                "Echinoderm Toxic",
    "Tóxico para peixes":                   "Fish Toxic",
    "Tóxico para lagostins":                "Crayfish Toxic",
    "Herbicida/ alelopático":               "Herbicide/Allelopathic",
    "Antiparasitários":                     "Antiparasitic",
    "Antifúngico":                          "Antifungal",
    "Antibacteriano":                       "Antibacterial",
    "Antibiótico":                          "Antibiotic",
    "Antibiotico":                          "Antibiotic",
    "Antiviral":                            "Antiviral",
    "Toxina":                               "Toxin",
    "Anticrustáceo":                        "Antifouling",
    "Anti-incrustante":                     "Antifouling",
    "Algicida":                             "Anti-algal",
    "Antioxidante":                         "Antioxidant",
    "Molucicida":                           "Molluscicidal",
    "Moluscicida":                          "Molluscicidal",
    "Protetores-UV":                        "Sunscreens",
    "Anti-inflamatório":                    "Anti-inflammatory",
    "Canabinomimético":                     "Cannabimimetic",
    "Outros":                               "Other",
    "Biosurfactante":                       "Biosurfactant",
    "BRMT":                                 "BRMT",
    "Odorantes":                            "Odorants",
}

hab_translation = {
    # com acentos / maiúsculas variadas
    "Água Doce":    "Freshwater",
    "água doce":    "Freshwater",
    "Agua Doce":    "Freshwater",
    "agua doce":    "Freshwater",
    "Água Salgada": "Seawater",
    "água salgada": "Seawater",
    "Agua Salgada": "Seawater",
    "agua salgada": "Seawater",
    "Água Salobra": "Brackish Water",
    "água salobra": "Brackish Water",
    "Agua Salobra": "Brackish Water",
    "agua salobra": "Brackish Water",
    "Terrestre":    "Terrestrial",
    "terrestre":    "Terrestrial",
    "Outros":       "Other",
    "outros":       "Other",
    # formas em inglês (caso o CSV já venha traduzido)
    "Freshwater":   "Freshwater",
    "Seawater":     "Seawater",
    "Brackish Water":"Brackish Water",
    "Terrestrial":  "Terrestrial",
    "Other":        "Other",
}

# ==============================================================================
# CLEAN CHEMICAL CLASSES
# ==============================================================================

def clean_class(text):
    if not isinstance(text, str):
        return text
    t = text.lower().strip()
    if "pept"                          in t: return "Peptides"
    if "macrol" in t or "policet"      in t: return "Macrolides/Polyketides"
    if "alcaloid"                      in t: return "Alkaloids"
    if "lacton"                        in t: return "Lactones"
    if "terpen" in t or "esteroid"     in t: return "Terpenes/Steroids"
    if "fenol"  in t or "aromat" in t or "aromát" in t: return "Phenols/Aromatics"
    if "grax"   in t or "acil"         in t: return "Fatty Acids"
    if "nucleos"                       in t: return "Nucleosides"
    if "heteroc"                       in t: return "Heterocyclic Compds."
    if "cíclic" in t or "ciclic"       in t: return "Specialized Cyclic Compds."
    if "voláteis" in t or "volatil"    in t: return "Volatile Org. Compds."
    if "isopren" in t or "caroten"     in t: return "Isoprenoid/Carotenoid Deriv."
    if "antibi"                        in t: return "Antibiotics"
    if "miscel" in t or "diverso" in t or "outro" in t: return "Miscellaneous Compds."
    if "compostos aromáticos e fenólicos" in t: return "Phenols/Aromatics"
    if "maas"                          in t: return "MAAs"
    return text.title()

# ==============================================================================
# APPLY CLEANING & PREPARATION
# ==============================================================================

# Normalizar capitalização antes de traduzir — evita duplicatas por capitalização
# inconsistente no CSV (ex.: "água doce" vs "Água Doce")
df_hab[COL_HAB] = (
    df_hab[COL_HAB]
    .astype(str).str.strip()
    .replace(hab_translation)
)

df_hab[COL_BIO]   = df_hab[COL_BIO].astype(str).str.strip().replace(bio_translation)
df_class[COL_BIO] = df_class[COL_BIO].astype(str).str.strip().replace(bio_translation)

df_class[COL_CLASS] = df_class[COL_CLASS].astype(str).str.strip().apply(clean_class)

# ==============================================================================
# GROUP DATA
# ==============================================================================

df_hab_group   = df_hab.groupby([COL_BIO, COL_HAB])[COL_COUNT].sum().reset_index()
df_class_group = df_class.groupby([COL_BIO, COL_CLASS])[COL_COUNT].sum().reset_index()

# Top 25 bioatividades por contagem total
top_bio = (
    df_hab_group.groupby(COL_BIO)[COL_COUNT]
    .sum()
    .sort_values(ascending=False)
    .head(25)
    .index
)

df_hab_group   = df_hab_group[df_hab_group[COL_BIO].isin(top_bio)]
df_class_group = df_class_group[df_class_group[COL_BIO].isin(top_bio)]

pivot_hab   = df_hab_group.pivot(index=COL_BIO, columns=COL_HAB,   values=COL_COUNT).fillna(0)
pivot_class = df_class_group.pivot(index=COL_BIO, columns=COL_CLASS, values=COL_COUNT).fillna(0)

order = pivot_hab.sum(axis=1).sort_values(ascending=False).index
pivot_hab   = pivot_hab.reindex(order)
pivot_class = pivot_class.reindex(order)

# ==============================================================================
# COLORS
# ==============================================================================

hab_colors = {
    "Terrestrial":   "#8B4513",
    "Freshwater":    "#20B2AA",
    "Brackish Water":"#2ca02c",
    "Seawater":      "#4169E1",
    "Other":         "#D3D3D3",
}

high_contrast_palette = [
    "#e6194B", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#42d4f4", "#f032e6", "#bfef45", "#fabed4",
    "#469990", "#dcbeff", "#9A6324", "#fffac8", "#800000",
    "#aaffc3", "#808000", "#ffd8b1", "#000075", "#a9a9a9",
    "#FF1493", "#00FF7F", "#D2691E", "#5A4FCF", "#8B008B",
]

class_colors = (high_contrast_palette * 3)[:len(pivot_class.columns)]

# ==============================================================================
# PLOT
# ==============================================================================

fig = plt.figure(figsize=(WIDTH_IN, HEIGHT_IN), dpi=DPI)
gs  = GridSpec(1, 3, width_ratios=[1, 0.6, 1], wspace=0.03)

axL = fig.add_subplot(gs[0])
axC = fig.add_subplot(gs[1])
axR = fig.add_subplot(gs[2])

y = np.arange(len(order))
h = 0.8

# ------------------------------------------------------------------------------
# LEFT — HABITATS
# ------------------------------------------------------------------------------

base = np.zeros(len(pivot_hab))
for col in pivot_hab.columns:
    axL.barh(y, pivot_hab[col], h, left=base,
             color=hab_colors.get(col, "grey"),
             edgecolor="white", linewidth=0.5, label=col)
    base += pivot_hab[col].values

axL.invert_xaxis()
axL.set_xlabel("Number of Records (Habitats)", fontweight="bold", fontsize=9)
axL.set_yticks([])
axL.grid(axis="x", linestyle=":", alpha=0.5)
for spine in axL.spines.values():
    spine.set_visible(False)

# ------------------------------------------------------------------------------
# CENTER — LABELS
# Usa as mesmas configurações de fonte do rcParams
# ------------------------------------------------------------------------------

axC.set_xlim(0, 1)
axC.set_ylim(axL.get_ylim())
axC.axis("off")

for yi, label in zip(y, order):
    axC.text(
        0.5, yi, label,
        ha="center", va="center",
        fontsize=plt.rcParams["font.size"],       # respeita rcParams
        fontfamily=plt.rcParams["font.sans-serif"][0],
        color=plt.rcParams["text.color"],
    )

# ------------------------------------------------------------------------------
# RIGHT — CHEMICAL CLASSES
# ------------------------------------------------------------------------------

base = np.zeros(len(pivot_class))
for i, col in enumerate(pivot_class.columns):
    axR.barh(y, pivot_class[col], h, left=base,
             color=class_colors[i],
             edgecolor="white", linewidth=0.5, label=col)
    base += pivot_class[col].values

axR.set_xlabel("Number of Records (Chemical Classes)", fontweight="bold", fontsize=9)
axR.set_yticks([])
axR.grid(axis="x", linestyle=":", alpha=0.5)
for spine in axR.spines.values():
    spine.set_visible(False)

# ==============================================================================
# LEGENDS — posicionamento dinâmico baseado no número de classes
# ==============================================================================

handles_h, labels_h = axL.get_legend_handles_labels()
handles_c, labels_c = axR.get_legend_handles_labels()

n_classes   = len(labels_c)
ncol_classes = min(4, n_classes)   # máximo 4 colunas na legenda de classes

# Calcula quantas linhas a legenda de classes vai ocupar para ajustar o bottom
n_linhas_legenda = -(-n_classes // ncol_classes)  # divisão teto
espaco_legenda   = 0.045 + n_linhas_legenda * 0.045
bottom_ajustado  = espaco_legenda + 0.06

plt.subplots_adjust(
    bottom=bottom_ajustado,
    top=0.96, left=0.08, right=0.92
)

# Ancora as legendas em coordenadas de figura ajustadas dinamicamente
y_hab   = espaco_legenda + 0.02
y_class = espaco_legenda - 0.035

fig.legend(
    handles_h, labels_h,
    loc="upper center", bbox_to_anchor=(0.5, y_hab),
    ncol=len(labels_h), title="Habitats",
    title_fontproperties={"weight": "bold"},
    frameon=False,
)

fig.legend(
    handles_c, labels_c,
    loc="upper center", bbox_to_anchor=(0.5, y_class),
    ncol=ncol_classes, title="Chemical Classes",
    title_fontproperties={"weight": "bold"},
    frameon=False,
)

# ==============================================================================
# EXPORT — plt.savefig suporta TIFF diretamente, sem precisar de PIL
# ==============================================================================

png  = "figure_fig5_600dpi.png"
tiff = "figure_fig5_600dpi.tiff"

plt.savefig(png,  dpi=DPI, bbox_inches="tight")
plt.savefig(tiff, dpi=DPI, bbox_inches="tight")

print("Gerado:", png, tiff)
plt.show()
