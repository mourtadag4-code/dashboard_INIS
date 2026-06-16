"""
Dashboard Avicole — Diagnostic Financier par Cycle
Lancer avec : streamlit run dashboard_avicole.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import os

# ─────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Avicole | INIS",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# STYLES GLOBAUX (conservé identique)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fond global */
.stApp {
    background: #EFE2D1;
    color: #163F36;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #F4E8D8 !important;
    border-right: 1px solid #E2B75F;
}
[data-testid="stSidebar"] * {
    color: #163F36 !important;
}

/* Titres */
h1, h2, h3 { 
    font-family: 'Syne', sans-serif !important;
    color: #163F36 !important;
}

/* Cards métriques */
.metric-card {
    background: #F4E8D8;
    border: 1px solid #E2B75F;
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: #163F36;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #E2B75F);
    border-radius: 16px 16px 0 0;
}
.metric-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #163F36;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #163F36;
    line-height: 1.1;
}
.metric-sub {
    font-size: 12px;
    color: #163F36;
    margin-top: 6px;
}
.metric-delta-pos { color: #163F36; font-size: 13px; font-weight: 500; }
.metric-delta-neg { color: #E2B75F; font-size: 13px; font-weight: 500; }

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #163F36;
    letter-spacing: -0.02em;
    margin: 32px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #E2B75F;
}

/* Hero banner */
.hero {
    background: #F4E8D8;
    border: 1px solid #E2B75F;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '🐔';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 72px;
    opacity: 0.1;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #163F36 !important;
    margin: 0 !important;
    letter-spacing: -0.03em;
}
.hero p {
    color: #163F36;
    font-size: 14px;
    margin-top: 8px;
}

/* Reco cards */
.reco-card {
    border-radius: 12px;
    padding: 18px 20px;
    margin: 10px 0;
    border-left: 4px solid;
    background: #F4E8D8;
}
.reco-urgente  { border-color: #E2B75F; background: #F4E8D8; }
.reco-attention{ border-color: #E2B75F; background: #F4E8D8; }
.reco-positive { border-color: #163F36; background: #F4E8D8; }
.reco-titre { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 6px; color: #163F36; }
.reco-texte { font-size: 13px; color: #163F36; line-height: 1.6; }

/* Alert boxes */
.alert-box {
    background: #F4E8D8;
    border: 1px solid #E2B75F;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 13px;
    color: #163F36;
}
.success-box {
    background: #F4E8D8;
    border: 1px solid #163F36;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 13px;
    color: #163F36;
}

/* Interprétation card */
.interp-card {
    background: #F4E8D8;
    border: 1px solid #E2B75F;
    border-radius: 20px;
    padding: 22px 28px;
    margin: 24px 0;
    position: relative;
    overflow: hidden;
}
.interp-card::before {
    content: '📊';
    position: absolute;
    right: 24px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 64px;
    opacity: 0.08;
    pointer-events: none;
}
.interp-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #163F36;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid #E2B75F;
}
.interp-card-content {
    font-size: 13px;
    color: #163F36;
    line-height: 1.7;
}

/* Selectbox widgets */
[data-testid="stSelectbox"] > div > div {
    background: #F4E8D8 !important;
    border: 1px solid #E2B75F !important;
    border-radius: 10px !important;
    color: #163F36 !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
    background: #F4E8D8 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #163F36 !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: #E2B75F !important;
    color: #163F36 !important;
}
/* Style pour les labels des selectbox */
[data-testid="stSelectbox"] label {
    color: #163F36 !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETTES & CONSTANTES
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# PALETTES & CONSTANTES
# ─────────────────────────────────────────────
COLORS = {
    "Cycle1": "#163F36",      # vert foncé
    "Cycle2": "#E2B75F",      # doré
    "Cycle3": "#D4A373",      # beige
    "Cycle4": "#4e7cff",      # bleu
    "Cycle5": "#a78bfa",      # violet
    "Cycle6": "#34d399",      # vert clair
    "Cycle7": "#f87171",      # rouge
    "Cycle8": "#fbbf24",      # jaune
}
ACCENT = ["#4e7cff", "#a78bfa", "#34d399", "#fbbf24", "#f87171"]
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
GRID_COLOR = "#1e2230"
TEXT_COLOR = "#9ca3af"
FONT_FAMILY = "DM Sans, sans-serif"

# Génération automatique des couleurs pour les cycles non définis
def get_cycle_color(cycle_id):
    if cycle_id in COLORS:
        return COLORS[cycle_id]
    
    # Palette par défaut pour les cycles supplémentaires
    default_colors = ["#4e7cff", "#a78bfa", "#34d399", "#f87171", "#fbbf24", "#06b6d4", "#ec4899", "#84cc16"]
    cycle_num = int(cycle_id.replace("Cycle", "")) if cycle_id.startswith("Cycle") else 0
    return default_colors[(cycle_num - 1) % len(default_colors)]

def plotly_light_layout(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=16, color="#163F36"), x=0, pad=dict(l=4)),
        plot_bgcolor="#EFE2D1",
        paper_bgcolor="#EFE2D1",
        font=dict(family=FONT_FAMILY, color="#163F36"),
        height=height,
        xaxis=dict(gridcolor="#E2B75F", zerolinecolor="#E2B75F", title_font=dict(color="#163F36", size=11), tickfont=dict(color="#163F36")),
        yaxis=dict(gridcolor="#E2B75F", zerolinecolor="#E2B75F", title_font=dict(color="#163F36", size=11), tickfont=dict(color="#163F36")),
        legend=dict(
            bgcolor="#F4E8D8",
            bordercolor="#E2B75F",
            borderwidth=1,
            font=dict(size=10)
        ),
        margin=dict(l=12, r=12, t=44, b=12)
    )
    return fig
def fmt_fcfa(val):
    if pd.isna(val): return "—"
    return f"{val:,.0f} FCFA"

def fmt_num(val, dec=1):
    if pd.isna(val): return "—"
    return f"{val:,.{dec}f}"

def card(label, value, sub="", accent="#4e7cff", delta=None):
    delta_html = ""
    if delta is not None:
        cls = "metric-delta-pos" if delta >= 0 else "metric-delta-neg"
        sign = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="{cls}">{sign} {abs(delta):,.0f}</div>'
    return f"""
    <div class="metric-card" style="--accent:{accent}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {f'<div class="metric-sub">{sub}</div>' if sub else ''}
        {delta_html}
    </div>"""

def section_header(title, subtitle=""):
    """Crée un en-tête de section stylisé comme le hero de la page d'accueil"""
    if subtitle:
        st.markdown(f"""
        <div class="hero" style="padding: 24px 32px; margin-bottom: 24px;">
            <h1 style="font-size: 24px !important; margin: 0 !important;">{title}</h1>
            <p style="margin-top: 8px; font-size: 13px;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="hero" style="padding: 20px 28px; margin-bottom: 24px;">
            <h1 style="font-size: 22px !important; margin: 0 !important;">{title}</h1>
        </div>
        """, unsafe_allow_html=True)

def afficher_interpretation(titre, texte):
    st.html(f"""
    <div class="interp-card" style="color: #ffffff;">
        <div class="interp-card-title" style="color: #ffffff; font-size: 18px; font-weight: 700; margin-bottom: 16px; border-bottom: 1px solid #242838; padding-bottom: 10px;">
            {titre}
        </div>
        <div class="interp-card-content" style="color: #ffffff; font-size: 13px; line-height: 1.7;">
            {texte}
        </div>
    </div>
    """)

# ─────────────────────────────────────────────
# CHARGEMENT DONNÉES
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path="donnees_avicole_bd.xlsx"):
    xls = pd.ExcelFile(path)
    journalier   = pd.read_excel(xls, "journalier",   parse_dates=["date"])
    cycles_recap = pd.read_excel(xls, "cycles_recap", parse_dates=["date_nettoyage","date_desinfection","date_arrivage"])
    ventes       = pd.read_excel(xls, "ventes",       parse_dates=["date"])
    return journalier, cycles_recap, ventes

# Chercher le fichier dans le répertoire courant ou là où le script est
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "donnees_avicole_bd.xlsx")
if not os.path.exists(data_path):
    data_path = "donnees_avicole_bd.xlsx"

try:
    journalier, cycles_recap, ventes = load_data(data_path)
except FileNotFoundError:
    st.error("⚠️ Fichier 'donnees_avicole_bd.xlsx' introuvable. Placez-le dans le même dossier que ce script.")
    st.stop()

CYCLES = list(cycles_recap["cycle_id"].unique())

# Calcul du prix de revient unitaire
cycles_recap["prix_revient_unitaire"] = cycles_recap["depenses_totales_fcfa"] / cycles_recap["volume_vendu"]

# Calcul de l'homogénéité par cycle
if "poids_10plus" in journalier.columns and "poids_10moins" in journalier.columns:
    # Prendre la dernière pesée de chaque cycle (la plus proche de la fin)
    dernieres_pesees = journalier.dropna(subset=["poids_10plus", "poids_10moins"])\
                                   .sort_values(["cycle_id", "jour"])\
                                   .groupby("cycle_id").last()[["poids_10plus", "poids_10moins"]]
    
    cycles_recap["homogeneite"] = (dernieres_pesees["poids_10moins"] / dernieres_pesees["poids_10plus"]).round(2)
else:
    cycles_recap["homogeneite"] = None

# ─────────────────────────────────────────────
# FONCTIONS DE CALCUL
# ─────────────────────────────────────────────
# === CALCUL DE L'IC (INDICE DE CONSOMMATION) ===
# === RECALCUL DE L'IC POUR TOUS LES CYCLES ===
def calculer_ic(row):
    """Calcule l'Indice de Consommation"""
    conso = row.get("conso_totale_kg", 0)
    poids = row.get("poids_final_kg", 0)
    volume = row.get("volume_vendu", 0)
    
    if conso and poids and volume and poids > 0 and volume > 0:
        poids_total = poids * volume
        if poids_total > 0:
            return conso / poids_total
    return None

# Appliquer le calcul
cycles_recap["ic_calcule"] = cycles_recap.apply(calculer_ic, axis=1)

# Pour les cycles où le calcul a échoué (ex: Cycle 1, Cycle 2), utiliser une valeur par défaut
cycles_recap["ic_calcule"] = cycles_recap["ic_calcule"].fillna(1.7)

# Vérification
print("=== IC recalculé ===")
print(cycles_recap[["cycle_id", "conso_totale_kg", "poids_final_kg", "volume_vendu", "ic_calcule"]].to_string())

def calculer_roi(row):
    """Calcule le Retour sur Investissement"""
    if row.get("depenses_totales_fcfa") and row.get("depenses_totales_fcfa") > 0:
        return (row.get("resultat_net_fcfa", 0) / row["depenses_totales_fcfa"]) * 100
    return None

def calculer_prix_revient(row):
    """Calcule le prix de revient unitaire"""
    if row.get("depenses_totales_fcfa") and row.get("volume_vendu"):
        return row["depenses_totales_fcfa"] / row["volume_vendu"]
    return None

# Ajouter les colonnes calculées à cycles_recap
for idx, row in cycles_recap.iterrows():
    cycles_recap.loc[idx, "ic_calcule"] = calculer_ic(row)
    cycles_recap.loc[idx, "roi_pct"] = calculer_roi(row)
    cycles_recap.loc[idx, "prix_revient_unitaire"] = calculer_prix_revient(row)


# Chargement des données
@st.cache_data
def load_data(path="donnees_avicole_bd.xlsx"):
    xls = pd.ExcelFile(path)
    journalier   = pd.read_excel(xls, "journalier",   parse_dates=["date"])
    cycles_recap = pd.read_excel(xls, "cycles_recap", parse_dates=["date_nettoyage","date_desinfection","date_arrivage"])
    ventes       = pd.read_excel(xls, "ventes",       parse_dates=["date"])
    return journalier, cycles_recap, ventes



# Recalculer l'effectif restant (valeurs entières)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
AFFICHER_FILTRE = False  # True pour afficher, False pour masquer

with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 24px 0'>
        <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#f0ece4;letter-spacing:-0.02em'>
            🐔 INIS AVICOLE
        </div>
        <div style='font-size:11px;color:#4b5563;letter-spacing:0.08em;text-transform:uppercase;margin-top:4px'>
            Diagnostic des Cycles
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#4b5563;margin-bottom:10px'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Vue d'ensemble", "📊 Analyse par Cycle", "💰 Finance", "⚖️ Bilan Comparatif", "🎯 Recommandations"],
        label_visibility="collapsed"
    )

    # Filtre masqué par défaut
    if AFFICHER_FILTRE:
        st.markdown("---")
        st.markdown("<div style='font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#4b5563;margin-bottom:10px'>Filtres</div>", unsafe_allow_html=True)
        
        selected_cycles = st.multiselect(
            "Cycles à afficher",
            CYCLES,
            default=CYCLES,
            label_visibility="collapsed"
        )
    else:
        selected_cycles = CYCLES  # Tous les cycles par défaut

    
    
    st.markdown("---")
    # Mini-stats sidebar
    total_ca = cycles_recap["ca_fcfa"].sum()
    total_vol = cycles_recap["volume_vendu"].sum()
    total_dep = cycles_recap["depenses_totales_fcfa"].sum()
    total_res = cycles_recap["resultat_net_fcfa"].sum()

    st.markdown(f"""
    <div style='font-size:11px;color:#4b5563;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px'>Totaux des cycles</div>

    <div style='margin-bottom:10px'>
        <div style='font-size:11px;color:#6b7280'>Sujets vendus</div>
        <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#34d399'>{total_vol:,}</div>
    </div>

    <div style='margin-bottom:10px'>
        <div style='font-size:11px;color:#6b7280'>CA Total</div>
        <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#4e7cff'>{total_ca/1e6:.2f} M</div>
        <div style='font-size:10px;color:#4b5563'>FCFA</div>
    </div>

    

    <div style='margin-bottom:10px'>
        <div style='font-size:11px;color:#6b7280'>Dépenses totales</div>
        <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:#fbbf24'>{total_dep/1e6:.2f} M</div>
        <div style='font-size:10px;color:#4b5563'>FCFA</div>
    </div>

    <div style='margin-bottom:10px'>
        <div style='font-size:11px;color:#6b7280'>Résultat net</div>
        <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;color:{"#34d399" if total_res >= 0 else "#f87171"}'>{total_res/1e6:+.2f} M</div>
        <div style='font-size:10px;color:#4b5563'>FCFA</div>
    </div>
    """, unsafe_allow_html=True)

# Filtre données (tous les cycles car selected_cycles = CYCLES)
cr = cycles_recap[cycles_recap["cycle_id"].isin(selected_cycles)]
jf = journalier[journalier["cycle_id"].isin(selected_cycles)]
vf = ventes[ventes["cycle_id"].isin(selected_cycles)]

st.markdown("""
<div style="max-width: 1400px; margin: 0 auto; padding: 0 16px;">
""", unsafe_allow_html=True)

# Conversion des fillcolors en rgba
def hex_to_rgba(hex_color, alpha=0.15):
    """Convertit une couleur hexadécimale en rgba pour Plotly"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"

# ═══════════════════════════════════════════════════
# PAGE 1 : VUE D'ENSEMBLE
# ═══════════════════════════════════════════════════
if page == "🏠 Vue d'ensemble":

    # Hero
    st.markdown("""
    <div class="hero">
        <h1>Tableau de Bord Avicole</h1>
        <p>Exploitation Poulets de Chair · Diagnostic Financier Complet</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs row 1
    cols = st.columns(3)
    total_ca  = cr["ca_fcfa"].sum()
    total_dep = cr["depenses_totales_fcfa"].sum()
    total_res = cr["resultat_net_fcfa"].sum()
    total_vol = cr["volume_vendu"].sum()

    
    with cols[0]:
        st.markdown(card("Effectif Vendu", f"{total_vol:,} têtes", "Tous les cycles cumulés", "#a78bfa"), unsafe_allow_html=True)
    
    

    # Calcul du nombre total de morts sur les cycles sélectionnés
    total_morts = cr["mortalite_totale"].sum()

    with cols[1]:  # adapte le nom de la colonne (ex: col5)
        st.markdown(f"""
        <div class="metric-card" style="--accent:#f87171">
            <div class="metric-label">Nombre total de morts</div>
            <div class="metric-value">{total_morts:,.0f}</div>
            <div class="metric-sub">sujets (tous cycles)</div>
        </div>
        """, unsafe_allow_html=True)

    # Mortalité moyenne
    mortalite_moyenne = cr["taux_mortalite_pct"].mean()
    est_bon = mortalite_moyenne <= 4

    with cols[2]:  # adapte le nom de ta colonne
        st.markdown(f"""
        <div class="metric-card" style="--accent:{'#34d399' if est_bon else '#f87171'}">
            <div class="metric-label">Mortalité moyenne</div>
            <div class="metric-value">{mortalite_moyenne:.2f}%</div>
            <div class="metric-sub">moyenne des cycles</div>
            <div class="metric-sub" style="color:{'#34d399' if est_bon else '#f87171'}">
                {'≤ 4% ✅' if est_bon else '> 4% ⚠️'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # KPIs row 2 - Indicateurs clés par cycle
    col_a, col_b, col_c, col_d, col_e, col_f = st.columns(6)
    
    with col_a:
        st.markdown(card("CA Total", f"{total_ca/1e6:.2f} M FCFA", f"{len(selected_cycles)} cycles", "#4e7cff"), unsafe_allow_html=True)
    
    with col_b:
        st.markdown(card("Prix de revient", f"{total_dep/1e6:.2f} M FCFA", "Charges visibles", "#fbbf24"), unsafe_allow_html=True)
    
    with col_e:
        color = "#34d399" if total_res >= 0 else "#f87171"
        sign = "+" if total_res >= 0 else ""
        st.markdown(card("Résultat Net", f"{sign}{total_res/1e6:.2f} M FCFA", "Cumulé", color), unsafe_allow_html=True)
    
    prix_revient_moyen = cr["prix_revient_unitaire"].mean() if "prix_revient_unitaire" in cr.columns else 0
    with col_c:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#a78bfa">
            <div class="metric-label">Prix de revient moyen</div>
            <div class="metric-value">{prix_revient_moyen:,.0f} FCFA</div>
            <div class="metric-sub">par sujet</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    
    # Prix de revient moyen
    prix_revient_moy = cr["prix_revient_unitaire"].mean()
    prix_moyen = cr["prix_moyen_fcfa"].mean()
    delta_marge = prix_moyen - prix_revient_moy
    with col_f:
        color_delta = "#34d399" if delta_marge >= 0 else "#f87171"
        st.markdown(card("Marge nette/sujet", f"{delta_marge:+.0f} FCFA", f"Prix: {prix_moyen:.0f} / Revient: {prix_revient_moy:.0f}", color_delta), unsafe_allow_html=True)

    prix_vente_moyen = cr["prix_moyen_fcfa"].mean()
    with col_d:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#4e7cff">
            <div class="metric-label">Prix de vente moyen</div>
            <div class="metric-value">{prix_vente_moyen:,.0f} FCFA</div>
            <div class="metric-sub">par sujet</div>
        </div>
        """, unsafe_allow_html=True)
    
    
    # === DEUXIÈME LIGNE : MÉTRIQUES AVANCÉES (VUE D’ENSEMBLE) ===
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    # Calcul des moyennes sur les cycles sélectionnés
    
    
    ic_moyen = cr["ic_calcule"].mean() if "ic_calcule" in cr.columns else cr["ic_standard"].mean()
    homogeneite_moyenne = cr["homogeneite"].mean() if "homogeneite" in cr.columns else 0

    # Affichage dans 4 colonnes
    col1, col2 = st.columns(2)
    # IC moyen (calculé)
    with col1:
        ic_moyen = cr["ic_calcule"].mean() if "ic_calcule" in cr.columns else cr["ic_standard"].mean()
        delta_ic = ic_moyen - 1.7
        st.markdown(f"""
        <div class="metric-card" style="--accent:#fbbf24">
            <div class="metric-label">Indice de consommation (IC)</div>
            <div class="metric-value">{ic_moyen:.2f}</div>
            <div class="metric-sub">objectif ≤ 1.7</div>
            <div class="metric-delta-{'pos' if delta_ic <= 0 else 'neg'}">{'▲' if delta_ic <= 0 else '▼'} {abs(delta_ic):.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    

    

    # ROI global
    roi_moyen = cr["roi_pct"].mean() if "roi_pct" in cr.columns else 0
    est_positif = roi_moyen >= 0

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{'#34d399' if est_positif else '#f87171'}">
            <div class="metric-label">Retour sur investissement (ROI)</div>
            <div class="metric-value">{roi_moyen:+.1f}%</div>
            <div class="metric-sub">moyenne des cycles</div>
            <div class="metric-sub" style="color:{'#34d399' if est_positif else '#f87171'}">
                {'> 0' if est_positif else '< 0'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # ============================================================
    # VUE D'ENSEMBLE - UNE COURBE PAR LIGNE
    # ============================================================

    # 1. CA · Dépenses · Résultat par Cycle
    st.markdown("### 📊 CA, Dépenses et Résultat par Cycle")
    afficher_graphique = st.checkbox("", value=True, key="check_ca_dep_res")

    if afficher_graphique:
        fig = go.Figure()
        # ... ton code du graphique ...
        fig = go.Figure()
        cycs = cr["cycle_id"].tolist()
        ca_vals  = cr["ca_fcfa"].tolist()
        dep_vals = cr["depenses_totales_fcfa"].tolist()
        res_vals = cr["resultat_net_fcfa"].tolist()

        fig.add_trace(go.Bar(name="CA", x=cycs, y=ca_vals,
                            marker_color="#0145ff", marker_line_width=0, opacity=0.9))
        fig.add_trace(go.Bar(name="Dépenses", x=cycs, y=dep_vals,
                            marker_color="#374151", marker_line_width=0, opacity=0.9))
        fig.add_trace(go.Scatter(name="Résultat Net", x=cycs, y=res_vals,
                                mode="lines+markers",
                                line=dict(color="#fbbf24", width=2.5, dash="dot"),
                                marker=dict(size=9, symbol="diamond")))
        fig.update_layout(
        barmode="group",
        legend=dict(
            font=dict(color="#163F36", size=12)  # ← Légende en vert foncé
        )
    )
        plotly_light_layout(fig, "", height=400)
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # 2. Résultat Net par Cycle (graphique seul)
    st.markdown("### 💰 Résultat Net par Cycle")
    afficher_graphique = st.checkbox("", value=True, key="check_resultat_net")

    if afficher_graphique:
        
        # ... ton code du graphique ...
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=cr["cycle_id"],
            y=cr["resultat_net_fcfa"],
            marker_color=["#4e7cff", "#a78bfa", "#34d399"],
            text=cr["resultat_net_fcfa"].apply(lambda x: f"{x:+,.0f}"),
            textposition="outside"
        ))
        fig2.add_hline(y=0, line_color="#f87171", line_dash="dash")
        plotly_light_layout(fig2, "", height=400)
        fig2.update_yaxes(title_text="FCFA")
        st.plotly_chart(fig2, use_container_width=True)
    

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    # 3. Évolution de l'Effectif Restant
    # Graphique : Évolution de l'effectif restant (en %) avec sélection multiple des cycles
    st.markdown("### 📈 Évolution de l'effectif restant (en %)")
    afficher_effectif_evol = st.checkbox("", value=True, key="check_effectif_evol")

    if afficher_effectif_evol:
        # Sélection multiple des cycles à comparer
        cycles_a_comparer = st.multiselect(
            "Cycles à comparer",
            options=CYCLES,
            default=CYCLES,
            key="cycles_comparaison_effectif"
        )
        
        if cycles_a_comparer:
            fig = go.Figure()
            
            for cid in cycles_a_comparer:
                j_cycle = journalier[journalier["cycle_id"] == cid]
                if not j_cycle.empty:
                    effectif_initial = j_cycle["effectif_restant"].iloc[0]
                    pourcentage_effectif = (j_cycle["effectif_restant"] / effectif_initial) * 100
                    
                    color = get_cycle_color(cid)
                    hex_color = color.lstrip('#')
                    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                    rgba_color = f"rgba({r}, {g}, {b}, 0.15)"
                    
                    fig.add_trace(go.Scatter(
                        x=j_cycle["jour"],
                        y=pourcentage_effectif,
                        name=cid,
                        mode="lines",
                        line=dict(color=color, width=2),
                        fill="tozeroy",
                        fillcolor=rgba_color,
                        hovertemplate=f"<b>{cid}</b><br>Jour %{{x}}<br>Effectif restant : %{{y:.1f}}%<extra></extra>"
                    ))
            fig.update_layout(
                barmode="group",
                legend=dict(
                    font=dict(color="#163F36", size=12)  # ← Légende en vert foncé
                )
            )
            plotly_light_layout(fig, "Évolution de l'effectif restant (en % de l'effectif initial)", height=400)
            fig.update_xaxes(title_text="Jour du cycle")
            fig.update_yaxes(title_text="Effectif restant (%)", range=[0, 105])
            st.plotly_chart(fig, use_container_width=True)
            
            
        else:
            st.info("Sélectionnez au moins un cycle à afficher.")
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")

    # Mortalité Cumulée par Cycle (en pourcentage) avec case à cocher
    st.markdown("### Mortalité Cumulée par Cycle")
    afficher_mortalite_cumulee_pct = st.checkbox("", value=True, key="check_mortalite_cumulee_pct")

    if afficher_mortalite_cumulee_pct:
        fig = go.Figure()
        
        for cid in selected_cycles:
            j = jf[jf["cycle_id"] == cid]
            effectif_initial = j["effectif_restant"].iloc[0] if not j.empty else 1
            pourcentage_mortalite_cumulee = (j["mortalite_cumulee"] / effectif_initial) * 100
            
            fig.add_trace(go.Scatter(
                x=j["jour"],
                y=pourcentage_mortalite_cumulee,
                name=cid,
                mode="lines",
                line=dict(color=COLORS.get(cid, "#fff"), width=2),
                hovertemplate=f"<b>{cid}</b><br>Jour %{{x}}<br>Mortalité cumulée : %{{y:.1f}}%<extra></extra>"
            ))
        fig.update_layout(
        barmode="group",
        legend=dict(
            font=dict(color="#163F36", size=12)  # ← Légende en vert foncé
        )
    )
        plotly_light_layout(fig, "", height=400)
        fig.update_xaxes(title_text="Jour du cycle")
        fig.update_yaxes(title_text="Mortalité cumulée (%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
    



# ═══════════════════════════════════════════════════
# PAGE 2 : ANALYSE PAR CYCLE
# ═══════════════════════════════════════════════════
elif page == "📊 Analyse par Cycle":

    section_header("📊 Analyse Détaillée par Cycle", "Effectifs, mortalité, consommation, poids et finances")

    cycle_sel = st.selectbox("Choisir un cycle", CYCLES, key="cycle_detail")
    c = cycles_recap[cycles_recap["cycle_id"] == cycle_sel].iloc[0]
    j = journalier[journalier["cycle_id"] == cycle_sel]
    v = ventes[ventes["cycle_id"] == cycle_sel]
    color = COLORS.get(cycle_sel, "#4e7cff")

    # Cycle badge + dates
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:16px; margin-bottom:24px;'>
        <div class="cycle-badge" style='background:{color}20; color:{color}; border:1px solid {color}40;'>
            {cycle_sel}
        </div>
        <div style='font-size:13px; color:#6b7280;'>
            Arrivage : <b style='color:#c8c4bc'>{str(c.get('date_arrivage','—'))[:10]}</b> ·
            Souche : <b style='color:#c8c4bc'>{c.get('souche','—')}</b> ·
            Couvoir : <b style='color:#c8c4bc'>{c.get('couvoir','—')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # 1. PRODUCTION
    # ============================================================
    st.markdown("#### 🟢 Production")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(card("Effectif Initial", f"{c['effectif_initial']:,}", "têtes", COLORS.get(cycle_sel, "#4e7cff")), unsafe_allow_html=True)

    with col2:
        st.markdown(card("Effectif Vendu", f"{c['volume_vendu']:,}", "têtes", "#34d399"), unsafe_allow_html=True)

    with col3:
        nb_morts = c.get("mortalite_totale", 0)
        if hasattr(nb_morts, 'iloc'):
            nb_morts = nb_morts.iloc[0]
        st.markdown(card("Nombre total de morts", f"{nb_morts:,.0f}", "sujets", "#f87171"), unsafe_allow_html=True)

    # ============================================================
    # HOMOGÉNÉITÉ - MÉTHODE ADAPTATIVE SELON LE CYCLE
    # ============================================================
    
    # Vérifier si c'est Cycle 4 ou supérieur (données détaillées disponibles)
    cycle_num = int(cycle_sel.replace("Cycle", "")) if cycle_sel.startswith("Cycle") else 0
    
    if cycle_num >= 4:
        # === NOUVELLE MÉTHODE : CV (Coefficient de variation) pour Cycle 4+ ===
        
        # Chercher la ligne avec les poids des 5 groupes
        ligne_poids = j[j["poids_g1"].notna() & j["poids_g2"].notna() & 
                       j["poids_g3"].notna() & j["poids_g4"].notna() & j["poids_g5"].notna()]
        
        if not ligne_poids.empty:
            # Prendre la dernière pesée disponible
            derniere = ligne_poids.iloc[-1]
            
            # Extraire les 5 poids (convertir en grammes pour le calcul)
            poids_groupes = [
                derniere["poids_g1"] * 1000,
                derniere["poids_g2"] * 1000,
                derniere["poids_g3"] * 1000,
                derniere["poids_g4"] * 1000,
                derniere["poids_g5"] * 1000,
            ]
            
            # Calcul du CV
            moyenne_g = np.mean(poids_groupes)
            ecart_type_g = np.std(poids_groupes)
            cv = (ecart_type_g / moyenne_g) * 100
            
            homogeneite_affichee = f"{cv:.1f}%"
            
            # Référence CV
            if cv < 8:
                reference = "✅ < 8% (très homogène)"
                couleur = "#34d399"
            elif cv < 10:
                reference = "✅ < 10% (bon)"
                couleur = "#34d399"
            elif cv < 12:
                reference = "⚠️ < 12% (acceptable)"
                couleur = "#fbbf24"
            else:
                reference = "⚠️ > 12% (hétérogène)"
                couleur = "#f87171"
        else:
            homogeneite_affichee = "Non disponible"
            reference = "Données CV manquantes"
            couleur = "#6b7280"
    
    else:
        # === ANCIENNE MÉTHODE : Rapport min/max pour Cycles 1, 2, 3 ===
        if "poids_10plus" in j.columns and "poids_10moins" in j.columns:
            dernier_poids_lourd = j["poids_10plus"].dropna().iloc[-1] if not j["poids_10plus"].dropna().empty else None
            dernier_poids_faible = j["poids_10moins"].dropna().iloc[-1] if not j["poids_10moins"].dropna().empty else None
            
            if dernier_poids_lourd and dernier_poids_faible and dernier_poids_lourd > 0:
                homogeneite = dernier_poids_faible / dernier_poids_lourd
                homogeneite_affichee = f"{homogeneite:.2f}"
                
                # Référence : 0,70
                if homogeneite >= 0.70:
                    reference = "✅ ≥ 0,70 (bon)"
                    couleur = "#34d399"
                else:
                    reference = "⚠️ < 0,70 (pas bon)"
                    couleur = "#f87171"
            else:
                homogeneite_affichee = "Non disponible"
                reference = ""
                couleur = "#6b7280"
        else:
            homogeneite_affichee = "Non disponible"
            reference = ""
            couleur = "#6b7280"

    # Affichage
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{couleur}">
            <div class="metric-label">Homogénéité</div>
            <div class="metric-value">{homogeneite_affichee}</div>
            <div class="metric-sub">{reference}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ==================== POINT MORT (EN ÉVIDENCE - PLEINE LARGEUR) ====================
    point_mort = c.get("point_mort_jours", 0)
    if hasattr(point_mort, 'iloc'):
        point_mort = point_mort.iloc[0]

    if point_mort > 0:
        est_bon = point_mort <= 53
        delta = point_mort - 53
        couleur = "#34d399" if est_bon else "#f87171"
        
        st.markdown(f"""
        <div style="width: 100%; margin: 20px 0;">
            <div class="metric-card" style="--accent:{couleur}; text-align: center; width: 100%;">
                <div class="metric-label" style="text-align: center;"> POINT MORT DU CYCLE</div>
                <div class="metric-value" style="font-size: 36px; text-align: center;">{point_mort:.0f} jours</div>
                <div class="metric-sub" style="text-align: center;">objectif ≤ 53 jours</div>
                <div class="metric-delta-{'pos' if est_bon else 'neg'}" style="font-size: 16px; text-align: center;">
                    {delta:+.0f} jours {'✅' if est_bon else '⚠️'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="width: 100%; margin: 20px 0;">
            <div class="metric-card" style="--accent:#6b7280; text-align: center; width: 100%;">
                <div class="metric-label" style="text-align: center;">POINT MORT</div>
                <div class="metric-value" style="text-align: center;">Non calculé</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # 2. FINANCIER
    # ============================================================
    st.markdown("#### 🟡 Financier")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(card("Chiffre d'affaires", f"{c['ca_fcfa']/1e6:.2f} M", "FCFA", COLORS.get(cycle_sel, "#4e7cff")), unsafe_allow_html=True)

    with col2:
        st.markdown(card("Prix de revient", f"{c['depenses_totales_fcfa']/1e6:.2f} M", "FCFA", "#fbbf24"), unsafe_allow_html=True)

    # === NOUVEAU : Prix de revient par sujet ===
    with col3:
        prix_revient = c.get("prix_revient_unitaire", 0)
        if hasattr(prix_revient, 'iloc'):
            prix_revient = prix_revient.iloc[0]
        st.markdown(card("Prix de revient", f"{prix_revient:,.0f}", "FCFA/sujet", "#a78bfa"), unsafe_allow_html=True)

    # === NOUVEAU : Prix de vente moyen par sujet ===
    with col4:
        prix_vente = c.get("prix_moyen_fcfa", 0)
        if hasattr(prix_vente, 'iloc'):
            prix_vente = prix_vente.iloc[0]
        st.markdown(card("Prix de vente moyen", f"{prix_vente:,.0f}", "FCFA/sujet", "#4e7cff"), unsafe_allow_html=True)

    with col5:
        resultat = c['resultat_net_fcfa']
        st.markdown(card("Résultat net", f"{resultat:+,.0f}", "FCFA", "#34d399" if resultat >= 0 else "#f87171"), unsafe_allow_html=True)

    with col6:
        marge_nette = c.get("marge_unitaire_fcfa", 0)
        if hasattr(marge_nette, 'iloc'):
            marge_nette = marge_nette.iloc[0]
        st.markdown(card("Marge nette/sujet", f"{marge_nette:+.0f}", "FCFA/sujet", "#34d399" if marge_nette >= 0 else "#f87171"), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    

    # ============================================================
    # 3. INDICES DE PERFORMANCE
    # ============================================================
    st.markdown("#### 🔵 Indices de performance")

    col1, col2, col3= st.columns(3)


    # Calcul direct de l'IC à partir des colonnes existantes
    conso_totale = c.get("conso_totale_kg", 0)
    poids_final = c.get("poids_final_kg", 0)
    volume_vendu = c.get("volume_vendu", 0)

    if conso_totale and poids_final and volume_vendu and volume_vendu > 0 and poids_final > 0:
        ic_val = conso_totale / (poids_final * volume_vendu)
    else:
        ic_val = None  # Pas de calcul possible

    # Fallback propre si le calcul échoue
    if ic_val is None or ic_val <= 0:
        ic_val = 1.7  # Valeur standard par défaut

    delta_ic = ic_val - 1.7
    est_bon_ic = delta_ic <= 0

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{'#34d399' if est_bon_ic else '#f87171'}">
            <div class="metric-label">Indice de consommation (IC)</div>
            <div class="metric-value">{ic_val:.2f}</div>
            <div class="metric-sub">objectif 1.7</div>
            <div class="metric-delta-{'pos' if est_bon_ic else 'neg'}">{delta_ic:+.2f} {'✅' if est_bon_ic else '⚠️'}</div>
        </div>
        """, unsafe_allow_html=True)

    # Mortalité
    with col2:
        mortalite = c.get("taux_mortalite_pct", 0)
        if hasattr(mortalite, 'iloc'):
            mortalite = mortalite.iloc[0]
        est_bon_mort = mortalite <= 4
        st.markdown(f"""
        <div class="metric-card" style="--accent:{'#34d399' if est_bon_mort else '#f87171'}">
            <div class="metric-label">Taux de mortalité</div>
            <div class="metric-value">{mortalite:.2f}%</div>
            <div class="metric-sub">objectif ≤ 4%</div>
            <div class="metric-sub" style="color:{'#34d399' if est_bon_mort else '#f87171'}">{'≤ 4% ✅' if est_bon_mort else '> 4% ⚠️'}</div>
        </div>
        """, unsafe_allow_html=True)

    # ROI
    with col3:
        roi = c.get("roi_pct", 0)
        if hasattr(roi, 'iloc'):
            roi = roi.iloc[0]
        est_bon_roi = roi >= 0
        st.markdown(f"""
        <div class="metric-card" style="--accent:{'#34d399' if est_bon_roi else '#f87171'}">
            <div class="metric-label">Retour sur investissement (ROI)</div>
            <div class="metric-value">{roi:+.1f}%</div>
            <div class="metric-sub">objectif ≥ 0%</div>
            <div class="metric-sub" style="color:{'#34d399' if est_bon_roi else '#f87171'}">{'≥ 0% ✅' if est_bon_roi else '< 0% ⚠️'}</div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ============================================================
    # 4. CONTRÔLE DE LA TEMPÉRATURE (NOUVEAU)
    # ============================================================
    st.markdown("#### 🌡️ Contrôle de la température")
    
    # Récupérer les données du cycle sélectionné
    j_temp = journalier[journalier["cycle_id"] == cycle_sel].copy()
    
    # Vérifier que les colonnes nécessaires existent
    if "temperature_matin" in j_temp.columns and "temperature_standard_min" in j_temp.columns:
        
        # Filtrer les jours avec données de température
        jours_avec_temp = j_temp["temperature_matin"].notna()
        if jours_avec_temp.any():
            j_temp_filtre = j_temp[jours_avec_temp].copy()
            
            # Compter les jours hors norme
            jours_hors_norme = j_temp_filtre[
                (j_temp_filtre["temperature_matin"] > j_temp_filtre["temperature_standard_max"]) |
                (j_temp_filtre["temperature_matin"] < j_temp_filtre["temperature_standard_min"])
            ].shape[0]
            
            jours_totaux = len(j_temp_filtre)
            taux_conformite = ((jours_totaux - jours_hors_norme) / jours_totaux) * 100 if jours_totaux > 0 else 0
            
            # Détection des pics d'écart
            ecarts = j_temp_filtre["temperature_matin"] - j_temp_filtre["temperature_standard_max"]
            ecarts_neg = j_temp_filtre["temperature_standard_min"] - j_temp_filtre["temperature_matin"]
            ecarts_max = max(ecarts.max(), ecarts_neg.max()) if len(ecarts) > 0 else 0
            
            # Cartes des métriques
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                couleur = "#f87171" if jours_hors_norme > 10 else ("#fbbf24" if jours_hors_norme > 5 else "#34d399")
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur}; text-align:center;">
                    <div class="metric-label">Jours hors norme</div>
                    <div class="metric-value" style="font-size: 28px;">{jours_hors_norme}</div>
                    <div class="metric-sub">sur {jours_totaux} jours</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                couleur = "#34d399" if taux_conformite >= 80 else ("#fbbf24" if taux_conformite >= 60 else "#f87171")
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur}; text-align:center;">
                    <div class="metric-label">Taux de conformité</div>
                    <div class="metric-value" style="font-size: 28px;">{taux_conformite:.1f}%</div>
                    <div class="metric-sub">objectif ≥ 80%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                couleur = "#f87171" if ecarts_max > 5 else ("#fbbf24" if ecarts_max > 3 else "#34d399")
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur}; text-align:center;">
                    <div class="metric-label">Écart maximum</div>
                    <div class="metric-value" style="font-size: 28px;">{ecarts_max:.1f}°C</div>
                    <div class="metric-sub">par rapport à la norme</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Calcul de la mortalité les jours hors norme
            jours_normaux = j_temp_filtre[
                (j_temp_filtre["temperature_matin"] <= j_temp_filtre["temperature_standard_max"]) &
                (j_temp_filtre["temperature_matin"] >= j_temp_filtre["temperature_standard_min"])
            ]
            
            mortalite_hors_norme = j_temp_filtre[~j_temp_filtre.index.isin(jours_normaux.index)]["morts_jour"].mean() if jours_hors_norme > 0 else 0
            mortalite_normale = jours_normaux["morts_jour"].mean() if len(jours_normaux) > 0 else 0
            impact_mortalite = mortalite_hors_norme - mortalite_normale
            
            with col4:
                couleur = "#f87171" if impact_mortalite > 1 else ("#fbbf24" if impact_mortalite > 0.5 else "#34d399")
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur}; text-align:center;">
                    <div class="metric-label">Impact sur mortalité</div>
                    <div class="metric-value" style="font-size: 28px;">{impact_mortalite:+.1f}</div>
                    <div class="metric-sub">morts/jour supplémentaires</div>
                </div>
                """, unsafe_allow_html=True)
            
            
        
        else:
            st.info("⚠️ Aucune donnée de température disponible pour ce cycle.")
    else:
        st.info("⚠️ Données de température ou normes manquantes pour ce cycle.")


    # Graphiques détaillés
    tab1, tab2 = st.tabs(["📈 Journalier", "🥩 Pesées & Poids"])

    with tab1:
        
        

        # Graphique : Effectif restant (en %) et ventes journalières (cycle sélectionné)
        st.markdown("<span style='font-size:22px; font-weight:600;'>📊 Effectif restant et Ventes Journalier</span>", unsafe_allow_html=True)
        afficher_effectif_ventes_pct = st.checkbox("", value=True, key="check_effectif_ventes_pct_cycle")

        if afficher_effectif_ventes_pct:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Données du cycle sélectionné (déjà filtré dans j et v)
            effectif_initial = j["effectif_restant"].iloc[0] if not j.empty else 1
            pourcentage_effectif = (j["effectif_restant"] / effectif_initial) * 100
            
            color = COLORS.get(cycle_sel, "#4e7cff")
            hex_color = color.lstrip('#')
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            rgba_color = f"rgba({r}, {g}, {b}, 0.15)"
            
            # Courbe de l'effectif restant (en %)
            fig.add_trace(go.Scatter(
                x=j["jour"],
                y=pourcentage_effectif,
                name="Effectif restant (%)",
                mode="lines",
                line=dict(color=color, width=2),
                fill="tozeroy",
                fillcolor=rgba_color,
                hovertemplate=f"Jour %{{x}}<br>Effectif restant : %{{y:.1f}}%<extra></extra>"
            ), secondary_y=False)
            
            # Barres des ventes
            if not v.empty:
                fig.add_trace(go.Bar(
                    x=v["jour"],
                    y=v["quantite"],
                    name="Ventes",
                    marker_color="#fbbf24",
                    opacity=0.7,
                    hovertemplate=f"Jour %{{x}}<br>Ventes : %{{y}} sujets<extra></extra>"
                ), secondary_y=True)
            
            # Mise en page
            fig.update_layout(
                legend=dict(font=dict(color="#163F36", size=12))
            )
            
            plotly_light_layout(fig, f"- {cycle_sel}", height=400)
            fig.update_xaxes(title_text="Jour du cycle")
            fig.update_yaxes(title_text="Effectif restant (%)", secondary_y=False, range=[0, 105])
            fig.update_yaxes(
                title_text="Ventes (sujets)",
                secondary_y=True,
                showgrid=False,
                title_font=dict(color="#163F36"),
                tickfont=dict(color="#163F36")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # ============================================================
            # INTERPRÉTATIONS DYNAMIQUES - EFFECTIF RESTANT ET VENTES
            # ============================================================
            with st.expander("📖 Interprétations", expanded=False):
                
                # Calculs dynamiques
                effectif_final = j["effectif_restant"].iloc[-1] if not j.empty else 0
                taux_reliquat = (effectif_final / effectif_initial) * 100 if effectif_initial > 0 else 0
                
                # Détection de la forme de la courbe d'effectif
                descente_progressive = (pourcentage_effectif.diff().abs() < 5).all()
                
                # Détection des ventes
                if not v.empty:
                    premier_vente = v["jour"].min()
                    dernier_vente = v["jour"].max()
                    total_ventes = v["quantite"].sum()
                    nb_pics = v["jour"].nunique()  
                    max_vente = v["quantite"].max()
                    ventes_concentrees = (max_vente / total_ventes) > 0.4 if total_ventes > 0 else False
                else:
                    premier_vente = None
                    dernier_vente = None
                    total_ventes = 0
                    nb_pics = 0
                    ventes_concentrees = False
                
                # Relation entre effectif et ventes
                baisse_avant_ventes = pourcentage_effectif.iloc[0] - pourcentage_effectif.iloc[min(10, len(pourcentage_effectif)-1)] > 10 if premier_vente and premier_vente > 10 else False
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Conteneur 1 : Évolution de l'effectif restant
                    if descente_progressive:
                        texte_effectif = "Descente progressive → mortalité naturelle + ventes étalées"
                    elif taux_reliquat > 5:
                        texte_effectif = f"⚠️ Effectif final > 5% ({taux_reliquat:.1f}%) → reliquat important"
                    else:
                        texte_effectif = "Descente avec variations → pic de mortalité ou ventes massives"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Évolution de l'effectif restant</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_effectif}<br>
                            • Effectif initial : {effectif_initial:,.0f} sujets → Effectif final : {effectif_final:,.0f} sujets
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 2 : Relation entre les courbes
                    if premier_vente and baisse_avant_ventes:
                        texte_relation = "Baisse avant les premières ventes → mortalité seule cause des pertes en début de cycle"
                    else:
                        texte_relation = "La baisse de l'effectif est principalement due aux ventes"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">Relation entre les courbes</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_relation}<br>
                            • Les jours de vente, l'effectif diminue proportionnellement
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # Conteneur 3 : Ventes journalières AVEC RÉFÉRENCE J38
                    if premier_vente:
                        if premier_vente <= 38:
                            texte_ventes = f"Première vente précoce (J{premier_vente}) → bonne trésorerie"
                            reference_vente = "(≤ J38 : vente précoce - référence standard)"
                        elif premier_vente <= 42:
                            texte_ventes = f" Première vente à J{premier_vente} → acceptable"
                            reference_vente = "(J39-42 : correct mais peut être amélioré)"
                        else:
                            texte_ventes = f"⚠️ Première vente tardive (J{premier_vente}) → risque de tension de trésorerie"
                            reference_vente = "(> J42 : vente tardive, impact sur prix et trésorerie)"
                    else:
                        texte_ventes = "⚠️ Aucune vente enregistrée pour ce cycle"
                        reference_vente = ""
                    
                    if ventes_concentrees:
                        texte_concentration = f"⚠️ Vente concentrée : {max_vente} sujets sur un seul jour ({max_vente/total_ventes*100:.0f}%)"
                        reference_concentration = "(> 40% : dépendance client, risque commercial)"
                    else:
                        texte_concentration = "Ventes réparties sur plusieurs jours → clientèle diversifiée"
                        reference_concentration = "(< 25% par pic : bonne répartition)"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#E2B75F;">
                        <div class="metric-label" style="font-size: 16px;">Ventes journalières</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_ventes}<br>
                            • <span style="color: #6b7280; font-size: 11px;">{reference_vente}</span><br>
                            • {texte_concentration}<br>
                            • Volume total vendu : {total_ventes:,.0f} sujets sur {nb_pics} jour(s)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Point d'attention ou positif AVEC RÉFÉRENCE J38
                    if taux_reliquat > 5:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#f87171;">
                            <div class="metric-label" style="font-size: 16px;">⚠️ Point d'attention</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Reliquat non vendu : {effectif_final} sujets ({taux_reliquat:.1f}%)<br>
                                • Impact économique direct sur la rentabilité du cycle
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif premier_vente and premier_vente <= 38:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#34d399;">
                            <div class="metric-label" style="font-size: 16px;">Point positif</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Démarrage commercial précoce (J{premier_vente})<br>
                                • <strong>Référence : ≤ J38</strong> → vente précoce, bonne trésorerie
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif premier_vente and premier_vente <= 42:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#fbbf24;">
                            <div class="metric-label" style="font-size: 16px;">Point de vigilance</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Première vente à J{premier_vente}<br>
                                • <strong>Référence : ≤ J38</strong> → objectif à atteindre
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Graphique : Mortalité journalière en pourcentage
        st.markdown("<span style='font-size:22px; font-weight:600;'>💀 Mortalité journalière (%)</span>", unsafe_allow_html=True)
        afficher_mortalite_pct = st.checkbox("", value=True, key="check_mortalite_pct")
        
        if afficher_mortalite_pct:
            # Calcul du pourcentage de mortalité journalière
            j_mortalite = j.copy()
            effectif_initial = j_mortalite["effectif_restant"].iloc[0]
            j_mortalite["mortalite_journaliere_pct"] = (j_mortalite["morts_jour"] / effectif_initial) * 100
            
            # Création du graphique
            fig_mortalite = go.Figure()
            
            # Barres de mortalité journalière
            fig_mortalite.add_trace(go.Bar(
                x=j_mortalite["jour"],
                y=j_mortalite["mortalite_journaliere_pct"],
                name="Mortalité journalière",
                marker_color="#f87171",
                opacity=0.8,
                hovertemplate="<b>Mortalité journalière</b><br>Jour: %{x}<br>Mortalité: %{y:.2f}%<extra></extra>"
            ))
            
            # Ajouter une ligne d'alerte à 1%
            fig_mortalite.add_hline(y=1, line_dash="dash", line_color="#fbbf24", 
                                   annotation_text="Alerte > 1%", annotation_position="bottom right")
            
            # Ajouter une ligne d'objectif à 0.5%
            fig_mortalite.add_hline(y=0.5, line_dash="dot", line_color="#34d399", 
                                   annotation_text="Objectif ≤ 0.5%", annotation_position="top right")
            
            # Mise en page
            plotly_light_layout(fig_mortalite, f"Évolution de la mortalité journalière - {cycle_sel}", height=400)
            fig_mortalite.update_xaxes(title_text="Jour du cycle")
            
            # Gérer le cas où toutes les valeurs sont NaN
            max_mortalite_jour = j_mortalite["mortalite_journaliere_pct"].max()
            if pd.notna(max_mortalite_jour):
                fig_mortalite.update_yaxes(title_text="Mortalité journalière (%)", range=[0, max(5, max_mortalite_jour + 1)])
            else:
                fig_mortalite.update_yaxes(title_text="Mortalité journalière (%)", range=[0, 5])
            
            fig_mortalite.update_layout(
                legend=dict(
                    font=dict(color="#163F36", size=10),
                    bgcolor="#F4E8D8",
                    bordercolor="#E2B75F",
                    borderwidth=1
                )
            )
            st.plotly_chart(fig_mortalite, use_container_width=True)
            
            # === INTERPRÉTATION DE LA MORTALITÉ ===
            with st.expander("📖 Interprétations", expanded=False):
                
                # Calculs dynamiques avec gestion des NaN
                mortalite_totale = j_mortalite["mortalite_cumulee"].iloc[-1] if not j_mortalite.empty and pd.notna(j_mortalite["mortalite_cumulee"].iloc[-1]) else 0
                mortalite_totale_pct = (mortalite_totale / effectif_initial) * 100
                
                # Calcul du pic de mortalité journalière (en %)
                mortalite_jour_non_nan = j_mortalite["mortalite_journaliere_pct"].dropna()
                if not mortalite_jour_non_nan.empty:
                    idx_pic = mortalite_jour_non_nan.idxmax()
                    jour_pic = j_mortalite.loc[idx_pic, "jour"] if idx_pic in j_mortalite.index else 0
                    pic_mortalite = mortalite_jour_non_nan.max()
                else:
                    jour_pic = 0
                    pic_mortalite = 0
                
                # Calcul du nombre de jours avec mortalité > 1%
                jours_alerte = len(j_mortalite[j_mortalite["mortalite_journaliere_pct"] > 1])
                
                # Calcul du nombre de jours avec mortalité > 0.5%
                jours_surveillance = len(j_mortalite[j_mortalite["mortalite_journaliere_pct"] > 0.5])
                
                # Évaluation de la mortalité
                if mortalite_totale_pct <= 4:
                    niveau_mortalite = "Excellent"
                    couleur_mortalite = "#34d399"
                    texte_mortalite = f"Mortalité totale maîtrisée ({mortalite_totale_pct:.2f}%)"
                    reference_mortalite = "(≤ 4% → objectif atteint)"
                elif mortalite_totale_pct <= 6:
                    niveau_mortalite = "Bon"
                    couleur_mortalite = "#34d399"
                    texte_mortalite = f"Mortalité totale correcte ({mortalite_totale_pct:.2f}%)"
                    reference_mortalite = "(4-6% → acceptable mais à surveiller)"
                elif mortalite_totale_pct <= 8:
                    niveau_mortalite = "Moyen"
                    couleur_mortalite = "#fbbf24"
                    texte_mortalite = f"Mortalité totale élevée ({mortalite_totale_pct:.2f}%)"
                    reference_mortalite = "(6-8% → attention requise)"
                else:
                    niveau_mortalite = "Critique"
                    couleur_mortalite = "#f87171"
                    texte_mortalite = f"Mortalité totale très élevée ({mortalite_totale_pct:.2f}%)"
                    reference_mortalite = "(> 8% → action urgente)"
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Conteneur 1 : Statistiques de mortalité
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Statistiques de mortalité</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Mortalité totale : <strong>{mortalite_totale_pct:.2f}%</strong> ({mortalite_totale:,.0f} sujets)<br>
                            • Pic de mortalité journalière : <strong>{pic_mortalite:.2f}%</strong> (J{jour_pic})<br>
                            • Jours avec mortalité > 1% : <strong>{jours_alerte}</strong> jour(s)<br>
                            • Jours avec mortalité > 0.5% : <strong>{jours_surveillance}</strong> jour(s)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 2 : Analyse des pics
                    if pic_mortalite > 2:
                        texte_pic = f"⚠️ Pic critique de mortalité ({pic_mortalite:.2f}%) au J{jour_pic}"
                        couleur_pic = "#f87171"
                    elif pic_mortalite > 1:
                        texte_pic = f"🟡 Pic modéré de mortalité ({pic_mortalite:.2f}%) au J{jour_pic}"
                        couleur_pic = "#fbbf24"
                    else:
                        texte_pic = f"✅ Pas de pic significatif (max {pic_mortalite:.2f}%)"
                        couleur_pic = "#34d399"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_pic};">
                        <div class="metric-label" style="font-size: 16px;">Pics de mortalité</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_pic}<br>
                            • Référence : un pic > 1% est considéré comme anormal
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Niveau de mortalité
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_mortalite};">
                        <div class="metric-label" style="font-size: 16px;">Niveau de mortalité</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_mortalite}<br>
                            • <span style="color: #6b7280; font-size: 11px;">{reference_mortalite}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Synthèse et recommandations
                    if mortalite_totale_pct <= 4:
                        synthese = "✅ Bonne maîtrise sanitaire → maintenir les protocoles"
                    elif mortalite_totale_pct <= 6:
                        synthese = "🟡 Mortalité à surveiller → renforcer la biosécurité"
                    elif mortalite_totale_pct <= 8:
                        synthese = "🟠 Mortalité élevée → analyser les causes (température, alimentation, vaccination)"
                    else:
                        synthese = "🔴 Action urgente → revoir vaccination, température et hygiène"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {synthese}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("Graphique masqué. Cochez la case pour l'afficher.")

        # ════════════════════════════════════════════════════════════════
        # NOUVEAU : GRAPHIQUE DE LA TEMPÉRATURE (DÉPLACÉ ICI)
        # ════════════════════════════════════════════════════════════════
        st.markdown("<span style='font-size:22px; font-weight:600;'>🌡️ Évolution de la température</span>", unsafe_allow_html=True)
        afficher_temp = st.checkbox("", value=True, key="check_temperature")
        
        if afficher_temp:
            # Récupérer les données du cycle sélectionné
            j_temp = journalier[journalier["cycle_id"] == cycle_sel].copy()
            
            # Vérifier que les colonnes nécessaires existent
            if "temperature_matin" in j_temp.columns and "temperature_standard_min" in j_temp.columns:
                
                # Filtrer les jours avec données de température
                jours_avec_temp = j_temp["temperature_matin"].notna()
                if jours_avec_temp.any():
                    j_temp_filtre = j_temp[jours_avec_temp].copy()
                    
                    # Créer la figure
                    fig_temp = go.Figure()
                    
                    # Température max recommandée
                    fig_temp.add_trace(go.Scatter(
                        x=j_temp_filtre["jour"],
                        y=j_temp_filtre["temperature_standard_max"],
                        name="Température max recommandée",
                        line=dict(color="#1a1a1a", width=3, dash="dash"),
                        opacity=0.9,
                        hovertemplate="<b>Température max recommandée</b><br>Jour: %{x}<br>Valeur: %{y:.1f}°C<extra></extra>"
                    ))
                    
                    # Température min recommandée
                    fig_temp.add_trace(go.Scatter(
                        x=j_temp_filtre["jour"],
                        y=j_temp_filtre["temperature_standard_min"],
                        name="Température min recommandée",
                        line=dict(color="#1a1a1a", width=3, dash="dash"),
                        opacity=0.9,
                        fill="tonexty",
                        fillcolor="rgba(26, 26, 26, 0.08)",
                        hovertemplate="<b>Température min recommandée</b><br>Jour: %{x}<br>Valeur: %{y:.1f}°C<extra></extra>"
                    ))
                    
                    # Température mesurée (matin)
                    fig_temp.add_trace(go.Scatter(
                        x=j_temp_filtre["jour"],
                        y=j_temp_filtre["temperature_matin"],
                        name="Température (matin)",
                        mode="lines+markers",
                        line=dict(color="#163F36", width=2),
                        marker=dict(size=6, color="#E2B75F"),
                        hovertemplate="<b>Température mesurée (matin)</b><br>Jour: %{x}<br>Température: %{y:.1f}°C<extra></extra>"
                    ))
                    
                    # Température mesurée (midi) - optionnelle
                    if "temperature_midi" in j_temp_filtre.columns and j_temp_filtre["temperature_midi"].notna().any():
                        fig_temp.add_trace(go.Scatter(
                            x=j_temp_filtre["jour"],
                            y=j_temp_filtre["temperature_midi"],
                            name="Température (midi)",
                            mode="lines+markers",
                            line=dict(color="#D4A373", width=1.5, dash="dot"),
                            marker=dict(size=4, color="#D4A373"),
                            hovertemplate="<b>Température mesurée (midi)</b><br>Jour: %{x}<br>Température: %{y:.1f}°C<extra></extra>"
                        ))
                    
                    # Température mesurée (soir) - optionnelle
                    if "temperature_soir" in j_temp_filtre.columns and j_temp_filtre["temperature_soir"].notna().any():
                        fig_temp.add_trace(go.Scatter(
                            x=j_temp_filtre["jour"],
                            y=j_temp_filtre["temperature_soir"],
                            name="Température (soir)",
                            mode="lines+markers",
                            line=dict(color="#E2B75F", width=1.5, dash="dot"),
                            marker=dict(size=4, color="#E2B75F"),
                            hovertemplate="<b>Température mesurée (soir)</b><br>Jour: %{x}<br>Température: %{y:.1f}°C<extra></extra>"
                        ))
                    
                    # Jours hors norme
                    jours_hors_norme = j_temp_filtre[
                        (j_temp_filtre["temperature_matin"] > j_temp_filtre["temperature_standard_max"]) |
                        (j_temp_filtre["temperature_matin"] < j_temp_filtre["temperature_standard_min"])
                    ]
                    if not jours_hors_norme.empty:
                        fig_temp.add_trace(go.Scatter(
                            x=jours_hors_norme["jour"],
                            y=jours_hors_norme["temperature_matin"],
                            name="⚠️ Jours hors norme",
                            mode="markers",
                            marker=dict(size=10, color="#f87171", symbol="x"),
                            hovertemplate="<b>⚠️ JOUR HORS NORME</b><br>Jour: %{x}<br>Température: %{y:.1f}°C<br>Hors des limites recommandées<extra></extra>"
                        ))
                    
                    plotly_light_layout(fig_temp, f"Évolution de la température - {cycle_sel}", height=400)
                    fig_temp.update_xaxes(title_text="Jour du cycle")
                    fig_temp.update_yaxes(title_text="Température (°C)")
                    fig_temp.update_layout(
                        legend=dict(
                            font=dict(color="#163F36", size=10),
                            bgcolor="#F4E8D8",
                            bordercolor="#E2B75F",
                            borderwidth=1
                        )
                    )
                    st.plotly_chart(fig_temp, use_container_width=True)
                    
                    
                    
                    # === INTERPRÉTATION DE LA TEMPÉRATURE (style identique à la conso) ===
                    with st.expander("📖 Interprétations", expanded=False):
                        
                        # Calculs dynamiques
                        nb_jours_hors_norme = len(jours_hors_norme)
                        temp_moyenne = j_temp_filtre["temperature_matin"].mean() if not j_temp_filtre.empty else 0
                        temp_max = j_temp_filtre["temperature_matin"].max() if not j_temp_filtre.empty else 0
                        temp_min = j_temp_filtre["temperature_matin"].min() if not j_temp_filtre.empty else 0
                        
                        # Trouver le jour de la température max
                        if not j_temp_filtre.empty and temp_max > 0:
                            idx_max_temp = j_temp_filtre["temperature_matin"].idxmax()
                            jour_max_temp = j_temp_filtre.loc[idx_max_temp, "jour"]
                        else:
                            jour_max_temp = 0
                        
                        # Détection des phases de température
                        temp_debut = j_temp_filtre[j_temp_filtre["jour"] <= 14]["temperature_matin"].mean() if not j_temp_filtre.empty else 0
                        temp_milieu = j_temp_filtre[(j_temp_filtre["jour"] > 14) & (j_temp_filtre["jour"] <= 35)]["temperature_matin"].mean() if not j_temp_filtre.empty else 0
                        temp_fin = j_temp_filtre[j_temp_filtre["jour"] > 35]["temperature_matin"].mean() if not j_temp_filtre.empty else 0
                        
                        # Détection de la tendance
                        if len(j_temp_filtre) >= 2:
                            debut_temp = j_temp_filtre["temperature_matin"].iloc[0]
                            fin_temp = j_temp_filtre["temperature_matin"].iloc[-1]
                            tendance = fin_temp - debut_temp
                        else:
                            tendance = 0
                        
                        # Calcul de la variabilité
                        ecart_type_temp = j_temp_filtre["temperature_matin"].std() if not j_temp_filtre.empty else 0
                        
                        # Détection de la conformité
                        est_conforme = nb_jours_hors_norme <= 5
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Conteneur 1 : Statistiques générales
                            if temp_max > 0:
                                texte_temp = f"Pic de température : {temp_max:.1f}°C au J{jour_max_temp}"
                            else:
                                texte_temp = "⚠️ Données de température insuffisantes"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#163F36;">
                                <div class="metric-label" style="font-size: 16px;">Statistiques de température</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_temp}<br>
                                    • Température moyenne : {temp_moyenne:.1f}°C<br>
                                    • Température minimale : {temp_min:.1f}°C<br>
                                    • Phase démarrage (J1-14) : {temp_debut:.1f}°C<br>
                                    • Phase croissance (J15-35) : {temp_milieu:.1f}°C<br>
                                    • Phase finition (J36+) : {temp_fin:.1f}°C
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 2 : Conformité et variabilité
                            if tendance > 0:
                                texte_tendance = f"Tendance à la hausse (+{tendance:.1f}°C sur le cycle)"
                                couleur_tendance = "#fbbf24"
                            elif tendance < 0:
                                texte_tendance = f"Tendance à la baisse ({tendance:.1f}°C sur le cycle)"
                                couleur_tendance = "#fbbf24"
                            else:
                                texte_tendance = "Température stable sur tout le cycle"
                                couleur_tendance = "#34d399"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_tendance};">
                                <div class="metric-label" style="font-size: 16px;">Conformité et variabilité</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_tendance}<br>
                                    • Écart-type : {ecart_type_temp:.1f}°C (variabilité des températures)<br>
                                    • {nb_jours_hors_norme} jours hors norme sur {jours_totaux} jours
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Conteneur 3 : Impact sur la mortalité
                            if impact_mortalite > 1:
                                texte_impact = f"⚠️ Impact très significatif : +{impact_mortalite:.1f} morts/jour"
                                couleur_impact = "#f87171"
                            elif impact_mortalite > 0.5:
                                texte_impact = f"Impact modéré : +{impact_mortalite:.1f} morts/jour"
                                couleur_impact = "#fbbf24"
                            elif impact_mortalite > 0:
                                texte_impact = f"Impact faible : +{impact_mortalite:.1f} morts/jour"
                                couleur_impact = "#34d399"
                            else:
                                texte_impact = "Aucun impact détecté"
                                couleur_impact = "#34d399"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_impact};">
                                <div class="metric-label" style="font-size: 16px;">Impact sur la mortalité</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Mortalité normale : {mortalite_normale:.2f} morts/jour<br>
                                    • Mortalité hors norme : {mortalite_hors_norme:.2f} morts/jour<br>
                                    • {texte_impact}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 4 : Synthèse
                            if est_conforme:
                                synthese_temp = "Température bien maîtrisée → maintenir les réglages actuels"
                                couleur_synthese = "#34d399"
                            elif nb_jours_hors_norme <= 10:
                                synthese_temp = "Température à surveiller → ajustements nécessaires"
                                couleur_synthese = "#fbbf24"
                            else:
                                synthese_temp = "🔴 Température mal maîtrisée → action urgente requise"
                                couleur_synthese = "#f87171"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_synthese};">
                                <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {synthese_temp}<br>
                                    • Taux de conformité : {taux_conformite:.1f}% (objectif ≥ 80%)
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("⚠️ Aucune donnée de température disponible pour ce cycle.")
            else:
                st.info("⚠️ Données de température ou normes manquantes pour ce cycle.")
        else:
            st.caption("Graphique masqué. Cochez la case pour l'afficher.")

        # ════════════════════════════════════════════════════════════════
        # GRAPHIQUE DE L'HUMIDITÉ
        # ════════════════════════════════════════════════════════════════
        st.markdown("<span style='font-size:22px; font-weight:600;'>💧 Évolution de l'humidité</span>", unsafe_allow_html=True)
        afficher_hum = st.checkbox("", value=True, key="check_humidite")
        
        if afficher_hum:
            # Récupérer les données du cycle sélectionné
            j_hum = journalier[journalier["cycle_id"] == cycle_sel].copy()
            
            # Vérifier que les colonnes nécessaires existent
            if "humidite_matin" in j_hum.columns and "humidite_standard_min" in j_hum.columns:
                
                # Filtrer les jours avec données d'humidité
                jours_avec_hum = j_hum["humidite_matin"].notna()
                if jours_avec_hum.any():
                    j_hum_filtre = j_hum[jours_avec_hum].copy()
                    
                    # === CORRECTION : Inverser min et max si nécessaire ===
                    if j_hum_filtre["humidite_standard_min"].iloc[0] > j_hum_filtre["humidite_standard_max"].iloc[0]:
                        temp_min = j_hum_filtre["humidite_standard_min"].copy()
                        j_hum_filtre["humidite_standard_min"] = j_hum_filtre["humidite_standard_max"]
                        j_hum_filtre["humidite_standard_max"] = temp_min
                    
                    # === CALCUL DES MÉTRIQUES ===
                    jours_totaux_hum = len(j_hum_filtre)
                    
                    jours_hors_norme_hum_mask = (j_hum_filtre["humidite_matin"] > j_hum_filtre["humidite_standard_max"]) | \
                                                (j_hum_filtre["humidite_matin"] < j_hum_filtre["humidite_standard_min"])
                    jours_hors_norme_hum = j_hum_filtre[jours_hors_norme_hum_mask]
                    nb_jours_hors_norme_hum = len(jours_hors_norme_hum)
                    taux_conformite_hum = ((jours_totaux_hum - nb_jours_hors_norme_hum) / jours_totaux_hum) * 100 if jours_totaux_hum > 0 else 0
                    
                    hum_moyenne = j_hum_filtre["humidite_matin"].mean() if not j_hum_filtre.empty else 0
                    hum_max = j_hum_filtre["humidite_matin"].max() if not j_hum_filtre.empty else 0
                    hum_min = j_hum_filtre["humidite_matin"].min() if not j_hum_filtre.empty else 0
                    
                    if not j_hum_filtre.empty and hum_max > 0:
                        idx_max_hum = j_hum_filtre["humidite_matin"].idxmax()
                        jour_max_hum = j_hum_filtre.loc[idx_max_hum, "jour"]
                    else:
                        jour_max_hum = 0
                    
                    hum_debut = j_hum_filtre[j_hum_filtre["jour"] <= 14]["humidite_matin"].mean() if not j_hum_filtre.empty else 0
                    hum_milieu = j_hum_filtre[(j_hum_filtre["jour"] > 14) & (j_hum_filtre["jour"] <= 35)]["humidite_matin"].mean() if not j_hum_filtre.empty else 0
                    hum_fin = j_hum_filtre[j_hum_filtre["jour"] > 35]["humidite_matin"].mean() if not j_hum_filtre.empty else 0
                    
                    if len(j_hum_filtre) >= 2:
                        debut_hum = j_hum_filtre["humidite_matin"].iloc[0]
                        fin_hum = j_hum_filtre["humidite_matin"].iloc[-1]
                        tendance_hum = fin_hum - debut_hum
                    else:
                        tendance_hum = 0
                    
                    jours_normaux_hum = j_hum_filtre[~jours_hors_norme_hum_mask]
                    mortalite_hors_norme_hum = jours_hors_norme_hum["morts_jour"].mean() if nb_jours_hors_norme_hum > 0 else 0
                    mortalite_normale_hum = jours_normaux_hum["morts_jour"].mean() if len(jours_normaux_hum) > 0 else 0
                    impact_mortalite_hum = mortalite_hors_norme_hum - mortalite_normale_hum
                    
                    # === CRÉATION DU GRAPHIQUE AVEC HOVERTEMPLATE COMPLET ===
                    fig_hum = go.Figure()
                    
                    # Humidité max recommandée
                    fig_hum.add_trace(go.Scatter(
                        x=j_hum_filtre["jour"],
                        y=j_hum_filtre["humidite_standard_max"],
                        name="Humidité max recommandée (65%)",
                        line=dict(color="#1a1a1a", width=3, dash="dash"),
                        opacity=0.9,
                        hovertemplate="<b>Humidité max recommandée</b><br>Jour: %{x}<br>Valeur: %{y:.0f}%<extra></extra>"
                    ))
                    
                    # Humidité min recommandée
                    fig_hum.add_trace(go.Scatter(
                        x=j_hum_filtre["jour"],
                        y=j_hum_filtre["humidite_standard_min"],
                        name="Humidité min recommandée (45%)",
                        line=dict(color="#1a1a1a", width=3, dash="dash"),
                        opacity=0.9,
                        fill="tonexty",
                        fillcolor="rgba(26, 26, 26, 0.08)",
                        hovertemplate="<b>Humidité min recommandée</b><br>Jour: %{x}<br>Valeur: %{y:.0f}%<extra></extra>"
                    ))
                    
                    # Humidité mesurée (matin)
                    fig_hum.add_trace(go.Scatter(
                        x=j_hum_filtre["jour"],
                        y=j_hum_filtre["humidite_matin"],
                        name="Humidité (matin)",
                        mode="lines+markers",
                        line=dict(color="#163F36", width=2.5),
                        marker=dict(size=6, color="#E2B75F"),
                        hovertemplate="<b>Humidité mesurée (matin)</b><br>Jour: %{x}<br>Humidité: %{y:.0f}%<extra></extra>"
                    ))
                    
                    # Humidité mesurée (midi)
                    if "humidite_midi" in j_hum_filtre.columns and j_hum_filtre["humidite_midi"].notna().any():
                        fig_hum.add_trace(go.Scatter(
                            x=j_hum_filtre["jour"],
                            y=j_hum_filtre["humidite_midi"],
                            name="Humidité (midi)",
                            mode="lines+markers",
                            line=dict(color="#D4A373", width=1.5, dash="dot"),
                            marker=dict(size=4, color="#D4A373"),
                            hovertemplate="<b>Humidité mesurée (midi)</b><br>Jour: %{x}<br>Humidité: %{y:.0f}%<extra></extra>"
                        ))
                    
                    # Humidité mesurée (soir)
                    if "humidite_soir" in j_hum_filtre.columns and j_hum_filtre["humidite_soir"].notna().any():
                        fig_hum.add_trace(go.Scatter(
                            x=j_hum_filtre["jour"],
                            y=j_hum_filtre["humidite_soir"],
                            name="Humidité (soir)",
                            mode="lines+markers",
                            line=dict(color="#E2B75F", width=1.5, dash="dot"),
                            marker=dict(size=4, color="#E2B75F"),
                            hovertemplate="<b>Humidité mesurée (soir)</b><br>Jour: %{x}<br>Humidité: %{y:.0f}%<extra></extra>"
                        ))
                    
                    # Jours hors norme
                    if not jours_hors_norme_hum.empty:
                        fig_hum.add_trace(go.Scatter(
                            x=jours_hors_norme_hum["jour"],
                            y=jours_hors_norme_hum["humidite_matin"],
                            name="⚠️ Jours hors norme",
                            mode="markers",
                            marker=dict(size=10, color="#f87171", symbol="x"),
                            hovertemplate="<b>⚠️ JOUR HORS NORME</b><br>Jour: %{x}<br>Humidité: %{y:.0f}%<br>Hors des limites recommandées<extra></extra>"
                        ))
                    
                    plotly_light_layout(fig_hum, f"Évolution de l'humidité - {cycle_sel}", height=400)
                    fig_hum.update_xaxes(title_text="Jour du cycle")
                    fig_hum.update_yaxes(title_text="Humidité (%)", range=[0, 100])
                    fig_hum.update_layout(
                        legend=dict(
                            font=dict(color="#163F36", size=10),
                            bgcolor="#F4E8D8",
                            bordercolor="#E2B75F",
                            borderwidth=1
                        )
                    )
                    st.plotly_chart(fig_hum, use_container_width=True)
                    
                    # === INTERPRÉTATION DE L'HUMIDITÉ ===
                    with st.expander("📖 Interprétations", expanded=False):
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Conteneur 1 : Statistiques générales
                            if hum_max > 0:
                                texte_hum = f"Pic d'humidité : {hum_max:.0f}% au J{jour_max_hum}"
                            else:
                                texte_hum = "⚠️ Données d'humidité insuffisantes"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#163F36;">
                                <div class="metric-label" style="font-size: 16px;">Statistiques d'humidité</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_hum}<br>
                                    • Humidité moyenne : {hum_moyenne:.0f}%<br>
                                    • Humidité minimale : {hum_min:.0f}%<br>
                                    • Phase démarrage (J1-14) : {hum_debut:.0f}%<br>
                                    • Phase croissance (J15-35) : {hum_milieu:.0f}%<br>
                                    • Phase finition (J36+) : {hum_fin:.0f}%
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 2 : Conformité et variabilité
                            if tendance_hum > 0:
                                texte_tendance_hum = f"Tendance à la hausse (+{tendance_hum:.0f}% sur le cycle)"
                                couleur_tendance_hum = "#fbbf24"
                            elif tendance_hum < 0:
                                texte_tendance_hum = f"Tendance à la baisse ({tendance_hum:.0f}% sur le cycle)"
                                couleur_tendance_hum = "#fbbf24"
                            else:
                                texte_tendance_hum = "Humidité stable sur tout le cycle"
                                couleur_tendance_hum = "#34d399"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_tendance_hum};">
                                <div class="metric-label" style="font-size: 16px;">Conformité et variabilité</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_tendance_hum}<br>
                                    • {nb_jours_hors_norme_hum} jours hors norme sur {jours_totaux_hum} jours<br>
                                    • Taux de conformité : {taux_conformite_hum:.1f}%
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Conteneur 3 : Impact sur la mortalité
                            if impact_mortalite_hum > 1:
                                texte_impact_hum = f"⚠️ Impact très significatif : +{impact_mortalite_hum:.1f} morts/jour"
                                couleur_impact_hum = "#f87171"
                            elif impact_mortalite_hum > 0.5:
                                texte_impact_hum = f"Impact modéré : +{impact_mortalite_hum:.1f} morts/jour"
                                couleur_impact_hum = "#fbbf24"
                            elif impact_mortalite_hum > 0:
                                texte_impact_hum = f"Impact faible : +{impact_mortalite_hum:.1f} morts/jour"
                                couleur_impact_hum = "#34d399"
                            else:
                                texte_impact_hum = "Aucun impact détecté"
                                couleur_impact_hum = "#34d399"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_impact_hum};">
                                <div class="metric-label" style="font-size: 16px;">Impact sur la mortalité</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Mortalité normale : {mortalite_normale_hum:.2f} morts/jour<br>
                                    • Mortalité hors norme : {mortalite_hors_norme_hum:.2f} morts/jour<br>
                                    • {texte_impact_hum}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 4 : Synthèse
                            if taux_conformite_hum >= 80:
                                synthese_hum = "Humidité bien maîtrisée → maintenir les réglages actuels"
                                couleur_synthese_hum = "#34d399"
                            elif taux_conformite_hum >= 60:
                                synthese_hum = "Humidité à surveiller → ajustements nécessaires"
                                couleur_synthese_hum = "#fbbf24"
                            else:
                                synthese_hum = "Humidité mal maîtrisée → action urgente requise"
                                couleur_synthese_hum = "#f87171"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_synthese_hum};">
                                <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {synthese_hum}<br>
                                    • Objectif : ≥ 80% de conformité
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                else:
                    st.info("⚠️ Aucune donnée d'humidité disponible pour ce cycle.")
            else:
                st.info("⚠️ Données d'humidité ou normes manquantes pour ce cycle.")
        else:
            st.caption("Graphique masqué. Cochez la case pour l'afficher.")

        # Graphique : Consommation Alimentaire (pleine largeur)
        st.markdown("<span style='font-size:22px; font-weight:600;'>🍗 Consommation Alimentaire</span>", unsafe_allow_html=True)
        afficher_conso = st.checkbox("", value=True, key="check_conso")

        if afficher_conso:
            fig2 = go.Figure()
            
            # Consommation journalière (barres)
            fig2.add_trace(go.Bar(
                x=j["jour"], 
                y=j["conso_jour"], 
                name="Conso/jour",
                marker_color=color, 
                opacity=0.8,
                hovertemplate="Jour %{x}<br>Consommation : %{y:.0f} kg<extra></extra>"
            ))
            
            # Consommation cumulée (courbe, axe secondaire)
            fig2.add_trace(go.Scatter(
                x=j["jour"], 
                y=j["conso_cumulee"], 
                name="Conso cumulée",
                line=dict(color="#fbbf24", width=2.5),
                yaxis="y2",
                hovertemplate="Jour %{x}<br>Cumul : %{y:.0f} kg<extra></extra>"
            ))
            
            plotly_light_layout(fig2, "Consommation Alimentaire (kg/jour)", height=400)
            fig2.update_layout(
                legend=dict(font=dict(color="#163F36", size=12), x= 1.12, y=0.5),
                yaxis2=dict(
                    overlaying="y", 
                    side="right", 
                    showgrid=False,
                    tickfont=dict(color="#163F36", size=10), 
                    title_font=dict(color="#163F36"),
                    title_text="Consommation cumulée (kg)"
                ),
                yaxis=dict(
                    title_text="Consommation journalière (kg)",
                    title_font=dict(color="#163F36"),
                    tickfont=dict(color="#163F36")
                ),
                xaxis=dict(title_text="Jour du cycle")
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            
            # ============================================================
            # INTERPRÉTATIONS DYNAMIQUES - CONSOMMATION ALIMENTAIRE
            # ============================================================
            with st.expander("📖 Interprétations", expanded=False):
                
                # Calculs dynamiques
                conso_totale = j["conso_cumulee"].iloc[-1] if not j.empty else 0
                conso_jour_max = j["conso_jour"].max() if not j.empty else 0
                if not j.empty and conso_jour_max > 0:
                    idx_max = j["conso_jour"].idxmax()
                    jour_max_conso = j.loc[idx_max, "jour"]
                else:
                    jour_max_conso = 0
                conso_jour_moyenne = j["conso_jour"].mean() if not j.empty else 0
                
                # Détection des phases d'alimentation
                conso_debut = j[j["jour"] <= 14]["conso_jour"].mean() if not j.empty else 0
                conso_milieu = j[(j["jour"] > 14) & (j["jour"] <= 35)]["conso_jour"].mean() if not j.empty else 0
                conso_fin = j[j["jour"] > 35]["conso_jour"].mean() if not j.empty else 0
                
                # Détection de la pente de la courbe cumulée
                if len(j) >= 2:
                    pente_cumul = (j["conso_cumulee"].iloc[-1] - j["conso_cumulee"].iloc[0]) / (j["jour"].iloc[-1] - j["jour"].iloc[0])
                else:
                    pente_cumul = 0
                
                # Détection d'anomalies
                pic_anormal = conso_jour_max > conso_jour_moyenne * 3 if conso_jour_moyenne > 0 else False
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Conteneur 1 : Consommation journalière
                    if pic_anormal:
                        texte_conso_jour = f"⚠️ Pic anormal de consommation : {conso_jour_max:.0f} kg au J{jour_max_conso} (vérifier saisie)"
                    elif conso_jour_max > 0:
                        texte_conso_jour = f" Pic de consommation : {conso_jour_max:.0f} kg au J{jour_max_conso} → phase de finition"
                    else:
                        texte_conso_jour = "⚠️ Données de consommation journalière manquantes"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Consommation journalière (barres)</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_conso_jour}<br>
                            • Consommation moyenne : {conso_jour_moyenne:.0f} kg/jour<br>
                            • Phase démarrage (J1-14) : {conso_debut:.0f} kg/jour<br>
                            • Phase croissance (J15-35) : {conso_milieu:.0f} kg/jour<br>
                            • Phase finition (J36+) : {conso_fin:.0f} kg/jour
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 2 : Relation et performance
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">Analyse de la performance</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Consommation totale : {conso_totale:.0f} kg<br>
                            • Pente de la courbe cumulée : {pente_cumul:.0f} kg/jour<br>
                            • IC (indice de consommation) : {c.get('ic_calcule', 0):.2f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Consommation cumulée
                    if pente_cumul > 400:
                        texte_pente = "⚠️ Pente très raide → forte augmentation des besoins en fin de cycle"
                    elif pente_cumul > 200:
                        texte_pente = "Pente régulière → consommation constante et prévisible"
                    else:
                        texte_pente = " Pente faible → vérifier les données de consommation"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#E2B75F;">
                        <div class="metric-label" style="font-size: 16px;">Consommation cumulée (courbe)</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_pente}<br>
                            • La courbe progresse de manière continue (pas de rupture)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Point d'attention
                    if pic_anormal:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#f87171;">
                            <div class="metric-label" style="font-size: 16px;">Point d'attention</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Pic de consommation anormalement élevé<br>
                                • Vérifier la cohérence des données de saisie
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif conso_totale > 0:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#34d399;">
                            <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Consommation conforme aux phases d'élevage<br>
                                • IC : {c.get('ic_calcule', 0):.2f} {'(bon)' if c.get('ic_calcule', 0) <= 1.7 else '(à améliorer)'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.caption("Graphique masqué. Cochez la case pour l'afficher.")
        
        # Timeline textuelle : événements et pics de mortalité (cycle sélectionné)
        st.markdown(f"<h5 style='margin: 0 0 5px 0;'>📅 Timeline des événements - {cycle_sel}</h5>", unsafe_allow_html=True)
        afficher_timeline_text = st.checkbox("", value=True, key="check_timeline_cycle")

        if afficher_timeline_text:
            effectif_initial = j["effectif_restant"].iloc[0] if not j.empty else 1
            
            # Calcul du pourcentage de mortalité
            pourcentage_mortalite = (j["morts_jour"] / j["effectif_restant"].shift(1)) * 100
            pourcentage_mortalite = pourcentage_mortalite.fillna(0)
            
            # Préparer les données
            tableau_data = []
            
            # Ajouter les événements
            events = j[j["action"].notna() & (j["action"] != "")][["jour", "action"]]
            for _, row in events.iterrows():
                tableau_data.append({
                    "Jour": row["jour"],
                    "Événement": row["action"]
                })
            
            # Ajouter les pics de mortalité
            pics = j[pourcentage_mortalite > 1.0][["jour", "morts_jour"]]
            for _, row in pics.iterrows():
                tableau_data.append({
                    "Jour": row["jour"],
                    "Événement": f"⚠️ Pic de mortalité : {row['morts_jour']} mort(s)"
                })
            
            if tableau_data:
                df_timeline = pd.DataFrame(tableau_data)
                df_timeline = df_timeline.sort_values("Jour")
                
                st.markdown(f"**{cycle_sel}**")
                st.dataframe(df_timeline, use_container_width=True, hide_index=True)
            else:
                st.caption(f"Aucun événement ni pic de mortalité significatif (>1%) pour {cycle_sel}.")
        else:
            st.caption("Timeline masquée. Cochez la case pour l'afficher.")
        

    
    with tab2:
            # Graphique des poids avec case à cocher
            st.markdown("<span style='font-size:22px; font-weight:600;'>🥩 Évolution des Poids</span>", unsafe_allow_html=True)
            afficher_poids = st.checkbox("", value=True, key="check_poids")

            if afficher_poids:
                fig_p = go.Figure()
                
                # === DÉTERMINER LA MÉTHODE SELON LE CYCLE ===
                cycle_num = int(cycle_sel.replace("Cycle", "")) if cycle_sel.startswith("Cycle") else 0
                
                if cycle_num >= 4:
                    # === NOUVELLE MÉTHODE : Poids des 5 groupes (Cycle 4+) ===
                    
                    # Chercher les lignes avec les poids des groupes
                    pesees_g1 = j[j["poids_g1"].notna()].copy()
                    pesees_g2 = j[j["poids_g2"].notna()].copy()
                    pesees_g3 = j[j["poids_g3"].notna()].copy()
                    pesees_g4 = j[j["poids_g4"].notna()].copy()
                    pesees_g5 = j[j["poids_g5"].notna()].copy()
                    
                    # Calculer la moyenne des 5 groupes pour chaque jour de pesée
                    # Fusionner les dates de pesée
                    jours_pesees = set()
                    for df in [pesees_g1, pesees_g2, pesees_g3, pesees_g4, pesees_g5]:
                        jours_pesees.update(df["jour"].tolist())
                    
                    # Créer un DataFrame avec la moyenne par jour
                    moyennes_par_jour = []
                    for jour in sorted(jours_pesees):
                        poids_jour = []
                        if jour in pesees_g1["jour"].values:
                            poids_jour.append(pesees_g1[pesees_g1["jour"] == jour]["poids_g1"].values[0])
                        if jour in pesees_g2["jour"].values:
                            poids_jour.append(pesees_g2[pesees_g2["jour"] == jour]["poids_g2"].values[0])
                        if jour in pesees_g3["jour"].values:
                            poids_jour.append(pesees_g3[pesees_g3["jour"] == jour]["poids_g3"].values[0])
                        if jour in pesees_g4["jour"].values:
                            poids_jour.append(pesees_g4[pesees_g4["jour"] == jour]["poids_g4"].values[0])
                        if jour in pesees_g5["jour"].values:
                            poids_jour.append(pesees_g5[pesees_g5["jour"] == jour]["poids_g5"].values[0])
                        
                        if poids_jour:
                            moyennes_par_jour.append({
                                "jour": jour,
                                "moyenne_kg": np.mean(poids_jour)
                            })
                    
                    if moyennes_par_jour:
                        df_moyennes = pd.DataFrame(moyennes_par_jour)
                        df_moyennes = df_moyennes.sort_values("jour")
                        
                        # Courbe de la moyenne des groupes
                        fig_p.add_trace(go.Scatter(
                            x=df_moyennes["jour"],
                            y=df_moyennes["moyenne_kg"],
                            name="Poids moyen (5 groupes)",
                            mode="lines+markers",
                            line=dict(color="#163F36", width=3.0),
                            marker=dict(size=10, symbol="circle", color="#E2B75F"),
                            connectgaps=True
                        ))
                        
                        # Optionnel : Ajouter les points individuels des groupes
                        fig_p.add_trace(go.Scatter(
                            x=pesees_g1["jour"] if not pesees_g1.empty else [],
                            y=pesees_g1["poids_g1"] if not pesees_g1.empty else [],
                            name="Groupe 1",
                            mode="markers",
                            marker=dict(size=6, symbol="circle", color="#a78bfa", opacity=0.6),
                            showlegend=True
                        ))
                        
                        fig_p.add_trace(go.Scatter(
                            x=pesees_g2["jour"] if not pesees_g2.empty else [],
                            y=pesees_g2["poids_g2"] if not pesees_g2.empty else [],
                            name="Groupe 2",
                            mode="markers",
                            marker=dict(size=6, symbol="circle", color="#818cf8", opacity=0.6),
                            showlegend=True
                        ))
                        
                        fig_p.add_trace(go.Scatter(
                            x=pesees_g3["jour"] if not pesees_g3.empty else [],
                            y=pesees_g3["poids_g3"] if not pesees_g3.empty else [],
                            name="Groupe 3",
                            mode="markers",
                            marker=dict(size=6, symbol="circle", color="#c084fc", opacity=0.6),
                            showlegend=True
                        ))
                        
                        fig_p.add_trace(go.Scatter(
                            x=pesees_g4["jour"] if not pesees_g4.empty else [],
                            y=pesees_g4["poids_g4"] if not pesees_g4.empty else [],
                            name="Groupe 4",
                            mode="markers",
                            marker=dict(size=6, symbol="circle", color="#e879f9", opacity=0.6),
                            showlegend=True
                        ))
                        
                        fig_p.add_trace(go.Scatter(
                            x=pesees_g5["jour"] if not pesees_g5.empty else [],
                            y=pesees_g5["poids_g5"] if not pesees_g5.empty else [],
                            name="Groupe 5",
                            mode="markers",
                            marker=dict(size=6, symbol="circle", color="#f472b6", opacity=0.6),
                            showlegend=True
                        ))
                        
                        # Poids standard si disponible
                        pesees_std = j[j["poids_standard"].notna()].copy()
                        if not pesees_std.empty:
                            fig_p.add_trace(go.Scatter(
                                x=pesees_std["jour"],
                                y=pesees_std["poids_standard"],
                                name="Standard",
                                mode="lines+markers",
                                line=dict(color="#1e293b", width=3.0, dash="dot"),
                                marker=dict(size=8, symbol="diamond", color="#1e293b")
                            ))
                        
                        # Forcer l'affichage
                        fig_p.update_xaxes(range=[0, df_moyennes["jour"].max() + 2])
                    
                    else:
                        st.info("⚠️ Aucune donnée de poids détaillée disponible pour ce cycle")
                
                else:
                    # === ANCIENNE MÉTHODE : poids_10plus / poids_10moins (Cycles 1, 2, 3) ===
                    
                    # Préparer les données de pesée
                    pesees_graph = j[j["poids_10plus"].notna() | j["poids_10moins"].notna()].copy()
                    pesees_graph = pesees_graph.sort_values("jour")

                    if not pesees_graph.empty:
                        # Poids des plus lourds
                        fig_p.add_trace(go.Scatter(
                            x=pesees_graph["jour"], 
                            y=pesees_graph["poids_10plus"],
                            name=">10% poids", 
                            mode="lines+markers",
                            line=dict(color="#34d399", width=2.0),
                            marker=dict(size=6, symbol="circle", color="#34d399"),
                            connectgaps=True
                        ))
                        
                        # Poids des plus faibles
                        fig_p.add_trace(go.Scatter(
                            x=pesees_graph["jour"], 
                            y=pesees_graph["poids_10moins"],
                            name="<10% poids", 
                            mode="lines+markers",
                            line=dict(color="#f87171", width=2.0),
                            marker=dict(size=6, symbol="circle", color="#f87171"),
                            connectgaps=False
                        ))
                        
                        # Poids standard
                        pesees_std = j[j["poids_standard"].notna()].copy()
                        if not pesees_std.empty:
                            fig_p.add_trace(go.Scatter(
                                x=pesees_std["jour"], 
                                y=pesees_std["poids_standard"],
                                name="Standard", 
                                mode="lines+markers",
                                line=dict(color="#1e293b", width=3.0, shape="linear"), 
                                marker=dict(size=10, symbol="diamond", color="#1e293b")
                            ))
                        
                        # Forcer l'affichage
                        fig_p.update_xaxes(range=[0, pesees_graph["jour"].max() + 2])
                    else:
                        st.info("⚠️ Aucune donnée de pesée disponible pour ce cycle")

                # Configuration du graphique (commune aux deux méthodes)
                plotly_light_layout(fig_p, "Évolution des Poids lors des Contrôles (kg)", 400)
                fig_p.update_layout(
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=-0.25,
                        xanchor="center",
                        x=0.8,
                        bgcolor="#F4E8D8",
                        bordercolor="#E2B75F",
                        borderwidth=1,
                        font=dict(color="#163F36", size=10)
                    ),
                    margin=dict(b=70)
                )
                fig_p.update_xaxes(title_text="Jour du cycle", dtick=5)
                fig_p.update_yaxes(title_text="Poids (kg)")

                st.plotly_chart(fig_p, use_container_width=True)
                
                # ============================================================
                # INTERPRÉTATIONS DYNAMIQUES (adaptées selon le cycle)
                # ============================================================
                with st.expander("📖 Interprétations", expanded=False):
                    
                    if cycle_num >= 4:
                        # === INTERPRÉTATION POUR CYCLE 4+ (basée sur les groupes) ===
                        if moyennes_par_jour:
                            df_moyennes = pd.DataFrame(moyennes_par_jour).sort_values("jour")
                            
                            # Dernier poids moyen
                            dernier_poids = df_moyennes["moyenne_kg"].iloc[-1]
                            dernier_jour = df_moyennes["jour"].iloc[-1]
                            
                            # Premier poids
                            premier_poids = df_moyennes["moyenne_kg"].iloc[0]
                            premier_jour = df_moyennes["jour"].iloc[0]
                            
                            # Gain quotidien
                            gain_quotidien = (dernier_poids - premier_poids) / (dernier_jour - premier_jour) if dernier_jour > premier_jour else 0
                            
                            # Récupérer les données des groupes pour le CV
                            ligne_j37 = j[j["jour"] == 37]
                            if not ligne_j37.empty:
                                poids_groupes = [
                                    ligne_j37["poids_g1"].values[0] if pd.notna(ligne_j37["poids_g1"].values[0]) else None,
                                    ligne_j37["poids_g2"].values[0] if pd.notna(ligne_j37["poids_g2"].values[0]) else None,
                                    ligne_j37["poids_g3"].values[0] if pd.notna(ligne_j37["poids_g3"].values[0]) else None,
                                    ligne_j37["poids_g4"].values[0] if pd.notna(ligne_j37["poids_g4"].values[0]) else None,
                                    ligne_j37["poids_g5"].values[0] if pd.notna(ligne_j37["poids_g5"].values[0]) else None,
                                ]
                                poids_valides = [p for p in poids_groupes if p is not None]
                                if len(poids_valides) >= 3:
                                    cv = (np.std(poids_valides) / np.mean(poids_valides)) * 100
                                else:
                                    cv = None
                            else:
                                cv = None
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"""
                                <div class="metric-card" style="--accent:#163F36;">
                                    <div class="metric-label" style="font-size: 16px;">🍗 Poids final et croissance</div>
                                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                        • Poids moyen final : <strong>{dernier_poids:.3f} kg</strong> (J{dernier_jour})<br>
                                        • Gain quotidien moyen : <strong>{gain_quotidien:.3f} kg/jour</strong><br>
                                        • {len(df_moyennes)} pesée(s) effectuée(s)
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if cv:
                                    if cv < 8:
                                        texte_cv = f"CV = {cv:.1f}% → lot très homogène"
                                        couleur_cv = "#34d399"
                                    elif cv < 10:
                                        texte_cv = f"CV = {cv:.1f}% → lot homogène"
                                        couleur_cv = "#34d399"
                                    elif cv < 12:
                                        texte_cv = f"CV = {cv:.1f}% → homogénéité acceptable"
                                        couleur_cv = "#fbbf24"
                                    else:
                                        texte_cv = f"CV = {cv:.1f}% → lot hétérogène"
                                        couleur_cv = "#f87171"
                                    
                                    st.markdown(f"""
                                    <div class="metric-card" style="--accent:{couleur_cv};">
                                        <div class="metric-label" style="font-size: 16px;">⚖️ Homogénéité du lot (CV)</div>
                                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                            • {texte_cv}<br>
                                            • Basé sur les 5 groupes de pesée (100 oiseaux)
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            with col2:
                                if gain_quotidien >= 0.055:
                                    texte_gain = f"Excellente progression : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(> 0,055 kg/jour → très bonne croissance)"
                                    couleur_gain = "#34d399"
                                elif gain_quotidien >= 0.045:
                                    texte_gain = f"Bonne progression : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(0,045 - 0,055 kg/jour → croissance standard)"
                                    couleur_gain = "#34d399"
                                else:
                                    texte_gain = f"⚠️ Progression lente : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(< 0,045 kg/jour → croissance insuffisante)"
                                    couleur_gain = "#f87171"
                                
                                st.markdown(f"""
                                <div class="metric-card" style="--accent:{couleur_gain};">
                                    <div class="metric-label" style="font-size: 16px;">📈 Gain de poids quotidien</div>
                                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                        • {texte_gain}<br>
                                        • <span style="color: #6b7280; font-size: 11px;">{reference_gain}</span>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Synthèse
                                if dernier_poids < 1.8:
                                    synthese = "⚠️ Poids insuffisant → prolonger le cycle ou améliorer l'alimentation de finition"
                                elif dernier_poids > 2.2:
                                    synthese = "Excellent poids → valorisable comme poulet lourd"
                                else:
                                    synthese = "Poids conforme aux attentes du marché"
                                
                                st.markdown(f"""
                                <div class="metric-card" style="--accent:#D4A373;">
                                    <div class="metric-label" style="font-size: 16px;">✅ Synthèse croissance</div>
                                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                        • {synthese}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Données insuffisantes pour l'interprétation")
                    
                    else:
                        # === ANCIENNE INTERPRÉTATION POUR CYCLES 1, 2, 3 ===
                        # (garder le code existant des interprétations)
                        
                        # Calculs dynamiques avec sécurité
                        if not pesees_graph.empty:
                            # Dernières valeurs de poids (non nulles)
                            dernier_poids_lourd = None
                            dernier_poids_faible = None
                            dernier_jour = None
                            
                            if "poids_10plus" in pesees_graph.columns:
                                poids_lourd_valides = pesees_graph["poids_10plus"].dropna()
                                if not poids_lourd_valides.empty:
                                    dernier_poids_lourd = poids_lourd_valides.iloc[-1]
                                    dernier_jour = pesees_graph.loc[poids_lourd_valides.index[-1], "jour"]
                            
                            if "poids_10moins" in pesees_graph.columns:
                                poids_faible_valides = pesees_graph["poids_10moins"].dropna()
                                if not poids_faible_valides.empty:
                                    dernier_poids_faible = poids_faible_valides.iloc[-1]
                            
                            # Poids standard
                            poids_std_final = None
                            if not pesees_std.empty:
                                std_valides = pesees_std["poids_standard"].dropna()
                                if not std_valides.empty:
                                    poids_std_final = std_valides.iloc[-1]
                            
                            # Homogénéité
                            homogeneite = None
                            if dernier_poids_lourd and dernier_poids_faible and dernier_poids_lourd > 0:
                                homogeneite = dernier_poids_faible / dernier_poids_lourd
                            
                            # Gain quotidien
                            gain_quotidien = None
                            poids_debut = None
                            jour_debut = None
                            if len(pesees_graph) >= 2:
                                if "poids_10plus" in pesees_graph.columns:
                                    debut_valides = pesees_graph["poids_10plus"].dropna()
                                    if len(debut_valides) >= 2:
                                        poids_debut = debut_valides.iloc[0]
                                        jour_debut = pesees_graph.loc[debut_valides.index[0], "jour"]
                                        if poids_debut and dernier_poids_lourd and dernier_jour and dernier_jour > jour_debut:
                                            gain_quotidien = (dernier_poids_lourd - poids_debut) / (dernier_jour - jour_debut)
                            
                            nb_pesees = len(pesees_graph["poids_10plus"].dropna())
                        else:
                            dernier_poids_lourd = None
                            dernier_poids_faible = None
                            poids_std_final = None
                            homogeneite = None
                            gain_quotidien = None
                            dernier_jour = None
                            jour_debut = None
                            nb_pesees = 0
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Conteneur 1 : Poids final et objectif
                            if dernier_poids_lourd:
                                if poids_std_final:
                                    ecart_std = dernier_poids_lourd - poids_std_final
                                    if ecart_std > 0:
                                        texte_poids = f"Poids final ({dernier_poids_lourd:.2f} kg) > standard ({poids_std_final:.2f} kg) → croissance rapide"
                                    elif ecart_std < 0:
                                        texte_poids = f"Poids final ({dernier_poids_lourd:.2f} kg) < standard ({poids_std_final:.2f} kg) → retard de croissance"
                                    else:
                                        texte_poids = f"Poids final conforme au standard ({dernier_poids_lourd:.2f} kg)"
                                else:
                                    texte_poids = f"Poids final des plus lourds : {dernier_poids_lourd:.2f} kg (J{dernier_jour})"
                            else:
                                texte_poids = "Données de poids final manquantes pour ce cycle"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#163F36;">
                                <div class="metric-label" style="font-size: 16px;">🍗 Poids final et objectif</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_poids}<br>
                                    • Poids des plus faibles : {f"{dernier_poids_faible:.2f} kg" if dernier_poids_faible else 'Non disponible'}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 2 : Homogénéité du lot
                            if homogeneite:
                                if homogeneite >= 0.85:
                                    texte_homo = f"Lot très homogène (rapport : {homogeneite:.2f})"
                                elif homogeneite >= 0.70:
                                    texte_homo = f"Homogénéité acceptable (rapport : {homogeneite:.2f})"
                                else:
                                    texte_homo = f"⚠️ Lot hétérogène (rapport : {homogeneite:.2f}) → écart important entre sujets"
                            else:
                                texte_homo = "⚠️ Données d'homogénéité non disponibles pour ce cycle"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#D4A373;">
                                <div class="metric-label" style="font-size: 16px;">⚖️ Homogénéité du lot</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_homo}<br>
                                    • Écart entre plus lourds et plus faibles : {f"{dernier_poids_lourd - dernier_poids_faible:.2f} kg" if dernier_poids_lourd and dernier_poids_faible else 'Non disponible'}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            # Conteneur 3 : Gain de poids quotidien
                            if gain_quotidien:
                                if gain_quotidien >= 0.055:
                                    texte_gain = f"Excellente progression : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(> 0,055 kg/jour → très bonne croissance)"
                                elif gain_quotidien >= 0.045:
                                    texte_gain = f"Bonne progression : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(0,045 - 0,055 kg/jour → croissance standard)"
                                else:
                                    texte_gain = f"⚠️ Progression lente : {gain_quotidien:.3f} kg/jour"
                                    reference_gain = "(< 0,045 kg/jour → croissance insuffisante)"
                            else:
                                texte_gain = "⚠️ Données de gain quotidien non disponibles pour ce cycle"
                                reference_gain = ""
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#E2B75F;">
                                <div class="metric-label" style="font-size: 16px;">📈 Gain de poids quotidien</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_gain}<br>
                                    • <span style="color: #6b7280; font-size: 11px;">{reference_gain}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 4 : Synthèse
                            if nb_pesees == 0:
                                synthese = "⚠️ Aucune pesée enregistrée pour ce cycle"
                            elif nb_pesees < 3:
                                synthese = f"Seulement {nb_pesees} pesée(s) → suivi insuffisant pour analyser la croissance"
                            elif dernier_poids_lourd:
                                if dernier_poids_lourd < 1.8:
                                    synthese = "⚠️ Poids insuffisant → prolonger le cycle ou améliorer l'alimentation de finition"
                                elif dernier_poids_lourd > 2.2:
                                    synthese = "Excellent poids → valorisable comme poulet lourd"
                                else:
                                    synthese = "Poids conforme aux attentes du marché"
                            else:
                                synthese = "Données de poids partielles pour ce cycle"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#34d399;">
                                <div class="metric-label" style="font-size: 16px;">✅ Synthèse croissance</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {synthese}<br>
                                    • {nb_pesees} pesée(s) effectuée(s) pendant le cycle
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            

                
            # Graphique des poids avec case à cocher (EXISTANT)
            
            
                # ============================================================
                # GRAPHIQUE 1 : GAIN DE POIDS QUOTIDIEN (GMQ)
                # ============================================================
                st.markdown("<span style='font-size:22px; font-weight:600;'>📈 Gain Moyen Quotidien (GMQ)</span>", unsafe_allow_html=True)
                afficher_gmq = st.checkbox("", value=True, key="check_gmq")

                if afficher_gmq:
                    if cycle_num >= 4:
                        # Cycle 4+ : utiliser la moyenne des groupes
                        if 'df_moyennes' in locals() and len(df_moyennes) >= 2:
                            df_gmq = df_moyennes.copy()
                            df_gmq["gmq"] = df_gmq["moyenne_kg"].diff() / df_gmq["jour"].diff()
                            
                            fig_gmq = go.Figure()
                            fig_gmq.add_trace(go.Bar(
                                x=df_gmq["jour"],
                                y=df_gmq["gmq"],
                                name="GMQ (kg/jour)",
                                marker_color="#E2B75F",
                                hovertemplate="<b>GMQ</b><br>Jour: %{x}<br>Gain: %{y:.3f} kg/jour<extra></extra>"
                            ))
                            fig_gmq.add_hline(y=0.055, line_dash="dash", line_color="#34d399", 
                                            annotation_text="Objectif 0.055 kg/jour")
                            
                            plotly_light_layout(fig_gmq, f"Gain de poids quotidien - {cycle_sel}", 350)
                            fig_gmq.update_yaxes(title_text="kg/jour")
                            st.plotly_chart(fig_gmq, use_container_width=True, key=f"plotly_gmq_{cycle_sel}")
                        else:
                            st.info("⚠️ Données insuffisantes pour calculer le GMQ (minimum 2 pesées requises)")
                    else:
                        # Cycles 1-3 : utiliser poids_10plus
                        if "poids_10plus" in j.columns:
                            pesees_gmq = j[j["poids_10plus"].notna()].copy()
                            if len(pesees_gmq) >= 2:
                                pesees_gmq = pesees_gmq.sort_values("jour")
                                pesees_gmq["gmq"] = pesees_gmq["poids_10plus"].diff() / pesees_gmq["jour"].diff()
                                
                                fig_gmq = go.Figure()
                                fig_gmq.add_trace(go.Bar(
                                    x=pesees_gmq["jour"],
                                    y=pesees_gmq["gmq"],
                                    name="GMQ (kg/jour)",
                                    marker_color="#E2B75F",
                                    hovertemplate="<b>GMQ</b><br>Jour: %{x}<br>Gain: %{y:.3f} kg/jour<extra></extra>"
                                ))
                                fig_gmq.add_hline(y=0.055, line_dash="dash", line_color="#34d399", 
                                                annotation_text="Objectif 0.055 kg/jour")
                                
                                plotly_light_layout(fig_gmq, f"Gain de poids quotidien - {cycle_sel}", 350)
                                fig_gmq.update_yaxes(title_text="kg/jour")
                                st.plotly_chart(fig_gmq, use_container_width=True, key=f"plotly_gmq_{cycle_sel}")
                            else:
                                st.info("⚠️ Données insuffisantes pour calculer le GMQ (minimum 2 pesées requises)")
                        else:
                            st.info("⚠️ Données de poids insuffisantes pour le GMQ")

                                    # === INTERPRÉTATION DU GMQ ===
                with st.expander("📖 Interprétations du GMQ", expanded=False):
                    
                    # Calculs dynamiques avec valeurs par défaut
                    gmq_moyen = 0
                    gmq_max = 0
                    gmq_min = 0
                    jour_max = 0
                    tendance = 0
                    gmq_debut = 0
                    gmq_fin = 0
                    
                    if 'df_gmq' in locals() and not df_gmq.empty and not df_gmq["gmq"].isna().all():
                        gmq_moyen = df_gmq["gmq"].mean()
                        gmq_max = df_gmq["gmq"].max()
                        gmq_min = df_gmq["gmq"].min()
                        idx_max = df_gmq["gmq"].idxmax()
                        jour_max = df_gmq.loc[idx_max, "jour"] if idx_max in df_gmq.index else 0
                        
                        # Détection de la tendance
                        gmq_non_nan = df_gmq["gmq"].dropna()
                        if len(gmq_non_nan) > 1:
                            gmq_debut = gmq_non_nan.iloc[0] if len(gmq_non_nan) > 0 else 0
                            gmq_fin = gmq_non_nan.iloc[-1] if len(gmq_non_nan) > 0 else 0
                            tendance = gmq_fin - gmq_debut
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Conteneur 1 : Statistiques GMQ
                        if gmq_moyen > 0:
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#163F36;">
                                <div class="metric-label" style="font-size: 16px;">Statistiques du GMQ</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • GMQ moyen : <strong>{gmq_moyen:.3f}</strong> kg/jour<br>
                                    • GMQ maximum : <strong>{gmq_max:.3f}</strong> kg/jour (J{jour_max})<br>
                                    • GMQ minimum : <strong>{gmq_min:.3f}</strong> kg/jour
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#6b7280;">
                                <div class="metric-label" style="font-size: 16px;">Statistiques du GMQ</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Données insuffisantes pour l'analyse
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Conteneur 2 : Tendance
                        if gmq_moyen > 0:
                            if tendance > 0.01:
                                texte_tendance = f"Tendance à la hausse (+{tendance:.3f} kg/jour)"
                                couleur_tendance = "#34d399"
                            elif tendance < -0.01:
                                texte_tendance = f"Tendance à la baisse ({tendance:.3f} kg/jour)"
                                couleur_tendance = "#f87171"
                            else:
                                texte_tendance = "Tendance stable"
                                couleur_tendance = "#E2B75F"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_tendance};">
                                <div class="metric-label" style="font-size: 16px;">Évolution du GMQ</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_tendance}<br>
                                    • Début : {gmq_debut:.3f} kg/jour → Fin : {gmq_fin:.3f} kg/jour
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#6b7280;">
                                <div class="metric-label" style="font-size: 16px;">Évolution du GMQ</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Données insuffisantes pour analyser la tendance
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        # Conteneur 3 : Niveau de performance
                        if gmq_moyen > 0:
                            if gmq_moyen >= 0.055:
                                niveau_gmq = "Excellent"
                                couleur_gmq = "#34d399"
                                texte_gmq = f"GMQ moyen excellent ({gmq_moyen:.3f} kg/jour)"
                                reference_gmq = "(≥ 0,055 kg/jour → très bonne croissance)"
                            elif gmq_moyen >= 0.045:
                                niveau_gmq = "Bon"
                                couleur_gmq = "#34d399"
                                texte_gmq = f"GMQ moyen correct ({gmq_moyen:.3f} kg/jour)"
                                reference_gmq = "(0,045-0,055 kg/jour → croissance standard)"
                            elif gmq_moyen >= 0.035:
                                niveau_gmq = "Moyen"
                                couleur_gmq = "#fbbf24"
                                texte_gmq = f"GMQ moyen faible ({gmq_moyen:.3f} kg/jour)"
                                reference_gmq = "(0,035-0,045 kg/jour → croissance insuffisante)"
                            else:
                                niveau_gmq = "Critique"
                                couleur_gmq = "#f87171"
                                texte_gmq = f"GMQ moyen très faible ({gmq_moyen:.3f} kg/jour)"
                                reference_gmq = "(< 0,035 kg/jour → croissance alarmante)"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_gmq};">
                                <div class="metric-label" style="font-size: 16px;">Niveau de croissance</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_gmq}<br>
                                    • <span style="color: #6b7280; font-size: 11px;">{reference_gmq}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#6b7280;">
                                <div class="metric-label" style="font-size: 16px;">Niveau de croissance</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Données insuffisantes pour évaluer la croissance
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Conteneur 4 : Synthèse
                        if gmq_moyen >= 0.055:
                            synthese = "Très bonne croissance → les conditions d'élevage sont optimales"
                        elif gmq_moyen >= 0.045:
                            synthese = "Croissance correcte → peut être améliorée avec l'alimentation"
                        elif gmq_moyen >= 0.035:
                            synthese = "Croissance insuffisante → revoir l'alimentation et les conditions"
                        elif gmq_moyen > 0:
                            synthese = "🔴 Croissance alarmante → action urgente sur l'alimentation et l'environnement"
                        else:
                            synthese = "⚠️ Données insuffisantes pour établir une synthèse"
                        
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#D4A373;">
                            <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • {synthese}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                
                # ============================================================
                # GRAPHIQUE 2 : COMPARAISON DES GROUPES (Cycle 4+ uniquement)
                # ============================================================
                if cycle_num >= 4:
                    st.markdown("<span style='font-size:22px; font-weight:600;'>📊 Comparaison des groupes</span>", unsafe_allow_html=True)
                    afficher_groupes = st.checkbox("", value=True, key="check_groupes")

                    if afficher_groupes:
                        fig_groupes = go.Figure()
                        
                        for g in range(1, 6):
                            col = f"poids_g{g}"
                            if col in j.columns:
                                data = j[j[col].notna()][["jour", col]]
                                if not data.empty:
                                    fig_groupes.add_trace(go.Scatter(
                                        x=data["jour"],
                                        y=data[col],
                                        name=f"Groupe {g}",
                                        mode="lines+markers",
                                        line=dict(width=1.5),
                                        marker=dict(size=4)
                                    ))
                        
                        if fig_groupes.data:
                            plotly_light_layout(fig_groupes, f"Évolution des poids par groupe - {cycle_sel}", 350)
                            fig_groupes.update_yaxes(title_text="Poids (kg)")
                            st.plotly_chart(fig_groupes, use_container_width=True, key=f"plotly_groupes_{cycle_sel}")
                        else:
                            st.info("⚠️ Aucune donnée de groupe disponible pour ce cycle")

                    # === INTERPRÉTATION DE LA COMPARAISON DES GROUPES ===
                    with st.expander("📖 Interprétations - Comparaison des groupes", expanded=False):
                        
                        # Récupérer les données des groupes
                        groupes_data = {}
                        for g in range(1, 6):
                            col = f"poids_g{g}"
                            if col in j.columns:
                                data = j[j[col].notna()][["jour", col]]
                                if not data.empty:
                                    groupes_data[f"Groupe {g}"] = data[col].values
                        
                        if groupes_data:
                            # Calculs dynamiques
                            moyennes_groupes = [np.mean(vals) for vals in groupes_data.values()]
                            ecarts_types = [np.std(vals) for vals in groupes_data.values()]
                            
                            meilleur_groupe = list(groupes_data.keys())[np.argmax(moyennes_groupes)]
                            moins_bon_groupe = list(groupes_data.keys())[np.argmin(moyennes_groupes)]
                            ecart_max = max(moyennes_groupes) - min(moyennes_groupes)
                            
                            # Coefficient de variation (homogénéité)
                            moyenne_totale = np.mean(moyennes_groupes)
                            cv = (np.std(moyennes_groupes) / moyenne_totale) * 100 if moyenne_totale > 0 else 0
                            
                            if cv < 5:
                                niveau_homogeneite = "Très homogène"
                                couleur_homo = "#34d399"
                                texte_homo = f"CV = {cv:.1f}% (< 5% → très bon)"
                            elif cv < 10:
                                niveau_homogeneite = "Homogène"
                                couleur_homo = "#34d399"
                                texte_homo = f"CV = {cv:.1f}% (5-10% → bon)"
                            elif cv < 15:
                                niveau_homogeneite = "Acceptable"
                                couleur_homo = "#fbbf24"
                                texte_homo = f"CV = {cv:.1f}% (10-15% → acceptable)"
                            else:
                                niveau_homogeneite = "Hétérogène"
                                couleur_homo = "#f87171"
                                texte_homo = f"CV = {cv:.1f}% (> 15% → problème)"
                            
                        else:
                            meilleur_groupe = "N/A"
                            moins_bon_groupe = "N/A"
                            ecart_max = 0
                            cv = 0
                            niveau_homogeneite = "Données insuffisantes"
                            texte_homo = "Données insuffisantes"
                            couleur_homo = "#6b7280"
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Conteneur 1 : Performance par groupe
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#163F36;">
                                <div class="metric-label" style="font-size: 16px;">Performance des groupes</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • Meilleur groupe : <strong>{meilleur_groupe}</strong> ({max(moyennes_groupes):.3f} kg)<br>
                                    • Groupe le moins performant : <strong>{moins_bon_groupe}</strong> ({min(moyennes_groupes):.3f} kg)<br>
                                    • Écart max/min : <strong>{ecart_max:.3f}</strong> kg
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            
                        
                        with col2:
                            # Conteneur 3 : Homogénéité du lot
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:{couleur_homo};">
                                <div class="metric-label" style="font-size: 16px;">Homogénéité du lot</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {texte_homo}<br>
                                    • Coefficient de variation : <strong>{cv:.1f}%</strong>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Conteneur 4 : Synthèse
                            if cv < 5:
                                synthese = "Lot très homogène → excellente uniformité de croissance"
                            elif cv < 10:
                                synthese = "Lot homogène → quelques écarts acceptables"
                            elif cv < 15:
                                synthese = "Lot acceptable → tri recommandé avant commercialisation"
                            else:
                                synthese = "Lot hétérogène → tri impératif avant vente"
                            
                            st.markdown(f"""
                            <div class="metric-card" style="--accent:#D4A373;">
                                <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                                <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                    • {synthese}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
                else:
                    st.info("⚠️ Colonnes poids par groupe non disponibles pour ce cycle")


    
        

# ═══════════════════════════════════════════════════
# PAGE 3 : FINANCE (ex Ventes & Prix)
# ═══════════════════════════════════════════════════
elif page == "💰 Finance":
    section_header("💰 Analyse Financière et Commerciale", "Cascade financière, point mort, coûts par jour et détails des ventes")
    
    # ============================================================
    # SÉLECTION DU CYCLE (tout le contenu dépend de ce choix)
    # ============================================================
    cycle_finance = st.selectbox(
    "Choisir un cycle",
    CYCLES,
    key="cycle_finance",
    label_visibility="visible"
    )
    
    # Récupérer les données du cycle sélectionné
    c_fin = cycles_recap[cycles_recap["cycle_id"] == cycle_finance].iloc[0]
    j_fin = journalier[journalier["cycle_id"] == cycle_finance]
    
    # ============================================================
    # SECTION 1 : VENTES ET PRIX (conservé)
    # ============================================================
    # ============================================================
    # MEILLEURS ACHETEURS DU CYCLE
    # ============================================================
    st.markdown("### 🏆 Meilleurs acheteurs du cycle") 

    # Récupérer les ventes du cycle sélectionné (cycle_finance est déjà défini)
    ventes_cycle = vf[vf["cycle_id"] == cycle_finance].copy()

    if not ventes_cycle.empty and "acheteur" in ventes_cycle.columns:
        # Grouper par acheteur et sommer les quantités
        top_acheteurs = ventes_cycle.groupby("acheteur")["quantite"].sum().sort_values(ascending=False).head(2)
        
        if not top_acheteurs.empty:
            col_a, col_b = st.columns(2)
            for i, (acheteur, qte) in enumerate(top_acheteurs.items()):
                if acheteur and acheteur != "":
                    col = col_a if i == 0 else col_b
                    col.markdown(f"""
                    <div class="metric-card" style="--accent:#E2B75F; text-align:center;">
                        <div class="metric-label"> {acheteur}</div>
                        <div class="metric-value">{qte:,.0f}</div>
                        <div class="metric-sub">sujets achetés</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Aucun acheteur enregistré pour ce cycle")
    else:
        st.info("Données d'acheteurs non disponibles. Exécutez d'abord le pipeline d'extraction.")

    # Graphique : Évolution du Prix Unitaire
    st.markdown("<span style='font-size:22px; font-weight:600;'>💰 Évolution du Prix Unitaire</span>", unsafe_allow_html=True)
    afficher_prix = st.checkbox("", value=True, key="check_prix_finance")

    if afficher_prix:
        fig = go.Figure()
        v_cycle = ventes[ventes["cycle_id"] == cycle_finance]
        if not v_cycle.empty:
            fig.add_trace(go.Scatter(
                x=v_cycle["jour"], 
                y=v_cycle["prix_unitaire"], 
                name=cycle_finance,
                mode="lines+markers",
                line=dict(color=COLORS.get(cycle_finance, "#163F36"), width=2),
                marker=dict(size=7),
                hovertemplate=f"<b>{cycle_finance}</b><br>Jour %{{x}}<br>Prix : %{{y:,.0f}} FCFA<extra></extra>"
            ))
        plotly_light_layout(fig, "", height=350)
        fig.update_layout(
            legend=dict(font=dict(color="#163F36", size=12))
        )
        fig.update_xaxes(title_text="Jour du cycle")
        fig.update_yaxes(title_text="Prix unitaire (FCFA)")
        st.plotly_chart(fig, use_container_width=True)
        
        # ============================================================
        # INTERPRÉTATIONS DYNAMIQUES - PRIX UNITAIRE
        # ============================================================
        with st.expander("📖 Interprétations", expanded=False):
            
            if not v_cycle.empty:
                # Calculs dynamiques
                prix_min = v_cycle["prix_unitaire"].min()
                prix_max = v_cycle["prix_unitaire"].max()
                prix_moy = v_cycle["prix_unitaire"].mean()
                prix_final = v_cycle["prix_unitaire"].iloc[-1] if len(v_cycle) > 0 else None
                jour_min = v_cycle.loc[v_cycle["prix_unitaire"].idxmin(), "jour"] if len(v_cycle) > 0 else None
                jour_max = v_cycle.loc[v_cycle["prix_unitaire"].idxmax(), "jour"] if len(v_cycle) > 0 else None
                prix_evolution = prix_max - prix_min
                nb_ventes = v_cycle["jour"].nunique()
                
                # Détection de la tendance
                if len(v_cycle) >= 2:
                    prix_debut = v_cycle["prix_unitaire"].iloc[0]
                    if prix_final > prix_debut:
                        tendance = "Tendance à la hausse"
                        couleur_tendance = "#34d399"
                    elif prix_final < prix_debut:
                        tendance = "Tendance à la baisse"
                        couleur_tendance = "#f87171"
                    else:
                        tendance = "Tendance stable"
                        couleur_tendance = "#E2B75F"
                else:
                    tendance = "Données insuffisantes"
                    couleur_tendance = "#6b7280"
                
                # Seuils de référence
                if prix_moy < 2600:
                    niveau_prix = "Prix moyen bas (< 2600 FCFA)"
                    couleur_prix = "#f87171"
                elif prix_moy > 2700:
                    niveau_prix = "Bon prix moyen (> 2700 FCFA)"
                    couleur_prix = "#34d399"
                else:
                    niveau_prix = "Prix moyen dans la norme (2600-2700 FCFA)"
                    couleur_prix = "#E2B75F"
            
            else:
                prix_min = prix_max = prix_moy = None
                jour_min = jour_max = None
                prix_evolution = None
                nb_ventes = 0
                tendance = "Aucune donnée de vente pour ce cycle"
                niveau_prix = "Données insuffisantes"
                couleur_tendance = "#6b7280"
                couleur_prix = "#6b7280"
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Conteneur 1 : Statistiques générales
                if nb_ventes > 0:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Statistiques des prix</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Prix moyen : {prix_moy:.0f} FCFA/sujet<br>
                            • Prix minimum : {prix_min:.0f} FCFA (J{jour_min})<br>
                            • Prix maximum : {prix_max:.0f} FCFA (J{jour_max})<br>
                            • Écart : {prix_evolution:.0f} FCFA entre min et max
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#6b7280;">
                        <div class="metric-label" style="font-size: 16px;">Statistiques des prix</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Aucune donnée de vente disponible
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Conteneur 2 : Niveau de prix et référence
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_prix};">
                    <div class="metric-label" style="font-size: 16px;">Niveau de prix</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {niveau_prix}<br>
                        • Référence secteur : 2 700 - 2 800 FCFA/sujet
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Conteneur 3 : Tendance
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_tendance};">
                    <div class="metric-label" style="font-size: 16px;">Tendance des prix</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {tendance}<br>
                        • {nb_ventes} vente(s) enregistrée(s)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur 4 : Synthèse et recommandation
                if nb_ventes > 0:
                    if prix_moy < 2600:
                        synthese = "Prix trop bas → négocier avec les acheteurs ou vendre pendant les périodes de fête"
                    elif prix_moy > 2700:
                        synthese = "Bon niveau de prix → maintenir cette stratégie commerciale"
                    else:
                        synthese = "Prix correct → peut être amélioré pour atteindre 2 700-2 800 FCFA"
                else:
                    synthese = "Données de prix manquantes pour ce cycle"
                
                st.markdown(f"""
                <div class="metric-card" style="--accent:#D4A373;">
                    <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {synthese}<br>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
    
    # Graphique : Volume Vendu Cumulé
    st.markdown("<span style='font-size:22px; font-weight:600;'>Volume Vendu Cumulé</span>", unsafe_allow_html=True)
    afficher_volume = st.checkbox("", value=True, key="check_volume_finance")

    if afficher_volume:
        fig2 = go.Figure()
        v_cycle = ventes[ventes["cycle_id"] == cycle_finance].sort_values("jour")
        if not v_cycle.empty:
            v_cycle = v_cycle.copy()
            v_cycle["qte_cum"] = v_cycle["quantite"].cumsum()
            color = COLORS.get(cycle_finance, "#163F36")
            hex_color = color.lstrip('#')
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            fig2.add_trace(go.Scatter(
                x=v_cycle["jour"], 
                y=v_cycle["qte_cum"], 
                name=cycle_finance,
                mode="lines+markers",
                line=dict(color=color, width=2),
                fill="tozeroy",
                fillcolor=f"rgba({r}, {g}, {b}, 0.15)",
                hovertemplate=f"<b>{cycle_finance}</b><br>Jour %{{x}}<br>Cumulé : %{{y:,}} têtes<extra></extra>"
            ))
        plotly_light_layout(fig2, "", height=350)
        fig2.update_layout(
            legend=dict(font=dict(color="#163F36", size=12))
        )
        fig2.update_xaxes(title_text="Jour du cycle")
        fig2.update_yaxes(title_text="Têtes vendues cumulées")
        st.plotly_chart(fig2, use_container_width=True)
        
        # ============================================================
        # INTERPRÉTATIONS DYNAMIQUES - VOLUME VENDU CUMULÉ
        # ============================================================
        with st.expander("📖 Interprétations", expanded=False):
            
            if not v_cycle.empty:
                # Calculs dynamiques
                volume_total = v_cycle["quantite"].sum()
                premier_vente = v_cycle["jour"].min()
                dernier_vente = v_cycle["jour"].max()
                nb_jours_vente = v_cycle["jour"].nunique()
                duree_etalement = dernier_vente - premier_vente
                
                # Calcul de la pente (ventes par jour)
                if duree_etalement > 0:
                    pente = volume_total / duree_etalement
                else:
                    pente = volume_total
                
                # Ventes par pallier (25%, 50%, 75%)
                pallier_25 = volume_total * 0.25
                pallier_50 = volume_total * 0.50
                pallier_75 = volume_total * 0.75
                
                jour_pallier_25 = None
                jour_pallier_50 = None
                jour_pallier_75 = None
                
                # Trier par jour pour le cumul
                v_cycle_trie = v_cycle.sort_values("jour")
                v_cycle_trie["qte_cum"] = v_cycle_trie["quantite"].cumsum()
                
                for _, row in v_cycle_trie.iterrows():
                    if jour_pallier_25 is None and row["qte_cum"] >= pallier_25:
                        jour_pallier_25 = row["jour"]
                    if jour_pallier_50 is None and row["qte_cum"] >= pallier_50:
                        jour_pallier_50 = row["jour"]
                    if jour_pallier_75 is None and row["qte_cum"] >= pallier_75:
                        jour_pallier_75 = row["jour"]
                
                # Évaluation de la vitesse de vente avec référence J38
                if premier_vente <= 38:
                    vitesse_vente = "Démarrage précoce (avant J38)"
                    reference_vitesse = "(≤ J38 : vente précoce → bonne trésorerie)"
                    couleur_vitesse = "#34d399"
                else:
                    vitesse_vente = f"Démarrage tardif (J{premier_vente})"
                    reference_vitesse = "(> J38 : vente tardive → risque de tension de trésorerie)"
                    couleur_vitesse = "#f87171"
                
                # Évaluation de l'étalement avec références
                if duree_etalement <= 7:
                    etalement_texte = "Ventes concentrées"
                    reference_etalement = "(≤ 7 jours : logistique optimisée, trésorerie rapide)"
                    couleur_etalement = "#34d399"
                elif duree_etalement <= 10:
                    etalement_texte = f"Étalement correct ({duree_etalement} jours)"
                    reference_etalement = "(8-10 jours : acceptable mais peut être amélioré)"
                    couleur_etalement = "#E2B75F"
                elif duree_etalement <= 14:
                    etalement_texte = f"Ventes étalées ({duree_etalement} jours)"
                    reference_etalement = "(11-14 jours : surveillance recommandée)"
                    couleur_etalement = "#f97316"
                else:
                    etalement_texte = f"Ventes très étalées ({duree_etalement} jours)"
                    reference_etalement = "(> 14 jours : risque logistique et de trésorerie)"
                    couleur_etalement = "#f87171"
                
                # Évaluation de la pente avec références
                if pente > 30:
                    pente_texte = f"Ventes rapides ({pente:.0f} sujets/jour)"
                    reference_pente = "(> 30 sujets/jour : très bonne dynamique)"
                    couleur_pente = "#34d399"
                elif pente > 20:
                    pente_texte = f"Ventes correctes ({pente:.0f} sujets/jour)"
                    reference_pente = "(20-30 sujets/jour : rythme satisfaisant)"
                    couleur_pente = "#E2B75F"
                elif pente > 10:
                    pente_texte = f"Ventes modérées ({pente:.0f} sujets/jour)"
                    reference_pente = "(10-20 sujets/jour : peut être amélioré)"
                    couleur_pente = "#f97316"
                else:
                    pente_texte = f"Ventes lentes ({pente:.0f} sujets/jour)"
                    reference_pente = "(< 10 sujets/jour : action commerciale nécessaire)"
                    couleur_pente = "#f87171"
                
            else:
                volume_total = 0
                premier_vente = None
                dernier_vente = None
                nb_jours_vente = 0
                duree_etalement = 0
                pente = 0
                jour_pallier_25 = jour_pallier_50 = jour_pallier_75 = None
                vitesse_vente = "Aucune vente enregistrée"
                reference_vitesse = ""
                etalement_texte = "Données insuffisantes"
                reference_etalement = ""
                pente_texte = "Données insuffisantes"
                reference_pente = ""
                couleur_vitesse = couleur_etalement = couleur_pente = "#6b7280"
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Conteneur 1 : Statistiques générales
                if volume_total > 0:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">📊 Statistiques des ventes</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Volume total : {volume_total:,.0f} sujets<br>
                            • Première vente : J{premier_vente}<br>
                            • Dernière vente : J{dernier_vente}<br>
                            • {nb_jours_vente} jour(s) de vente
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#6b7280;">
                        <div class="metric-label" style="font-size: 16px;">📊 Statistiques des ventes</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Aucune vente enregistrée pour ce cycle
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Conteneur 2 : Rythme des ventes avec référence
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_vitesse};">
                    <div class="metric-label" style="font-size: 16px;">⏱️ Rythme des ventes</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {vitesse_vente}<br>
                         <span style="color: #6b7280; font-size: 11px;">{reference_vitesse}</span><br>
                        • {pente_texte}<br>
                         <span style="color: #6b7280; font-size: 11px;">{reference_pente}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Conteneur 3 : Étalement des ventes avec référence
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_etalement};">
                    <div class="metric-label" style="font-size: 16px;">📅 Étalement des ventes</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {etalement_texte}<br>
                         <span style="color: #6b7280; font-size: 11px;">{reference_etalement}</span><br>
                        • Ventes sur {duree_etalement} jours (J{premier_vente} à J{dernier_vente})
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur 4 : Progression par pallier
                if jour_pallier_25 and jour_pallier_50 and jour_pallier_75:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">🎯 Progression des ventes</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • 25% du volume atteint : J{jour_pallier_25}<br>
                            • 50% du volume atteint : J{jour_pallier_50}<br>
                            • 75% du volume atteint : J{jour_pallier_75}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#6b7280;">
                        <div class="metric-label" style="font-size: 16px;">🎯 Progression des ventes</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Données insuffisantes pour calculer les palliers
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
    
  
    
    # ============================================================
    # DÉPENSES D'EXPLOITATION PAR CYCLE
    # ============================================================
    st.markdown("### 💰 Dépenses d'exploitation par cycle")
    afficher_cascade_exploit = st.checkbox("", value=True, key="check_cascade_exploit")

    if afficher_cascade_exploit:
        # Récupérer les données du cycle
        c_fin = cycles_recap[cycles_recap["cycle_id"] == cycle_finance].iloc[0]
        
        # Définition des postes d'exploitation (avec Autres frais)
        categories = [
            "Aliment", 
            "Poussins", 
            "Médical", 
            "Litière", 
            "Transport", 
            "Salaires", 
            "Loyer", 
            "Eau/Élec",
            "Télécom",
            "Autres frais",
            
        ]
        
        # Valeurs (positives)
        valeurs = [
            c_fin["cout_aliment_fcfa"] if not pd.isna(c_fin["cout_aliment_fcfa"]) else 0,
            c_fin["cout_poussins_fcfa"] if not pd.isna(c_fin["cout_poussins_fcfa"]) else 0,
            c_fin["cout_medical_fcfa"] if not pd.isna(c_fin["cout_medical_fcfa"]) else 0,
            c_fin["cout_litiere_fcfa"] if not pd.isna(c_fin["cout_litiere_fcfa"]) else 0,
            c_fin["cout_transport_fcfa"] if not pd.isna(c_fin["cout_transport_fcfa"]) else 0,
            c_fin["cout_salaires_fcfa"] if not pd.isna(c_fin["cout_salaires_fcfa"]) else 0,
            c_fin["cout_loyer_fcfa"] if not pd.isna(c_fin["cout_loyer_fcfa"]) else 0,
            c_fin["cout_eau_elec_fcfa"] if not pd.isna(c_fin["cout_eau_elec_fcfa"]) else 0,
            c_fin["cout_telecom_fcfa"] if not pd.isna(c_fin["cout_telecom_fcfa"]) else 0,
            c_fin["cout_autres_fcfa"] if not pd.isna(c_fin["cout_autres_fcfa"]) else 0,
            
        ]
        
        # Créer un graphique à barres simple
        fig_depenses = go.Figure()
        fig_depenses.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color="#E2B75F",
            text=[f"{v/1e6:.2f} M" for v in valeurs if v > 0],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} FCFA<extra></extra>"
        ))
        
        # Calculer le total des dépenses
        total_depenses = c_fin["depenses_totales_fcfa"]
        if hasattr(total_depenses, 'iloc'):
            total_depenses = total_depenses.iloc[0]
        
        plotly_light_layout(fig_depenses, f"Dépenses d'exploitation - {cycle_finance} (total : {total_depenses/1e6:.2f} M FCFA)", height=500)
        fig_depenses.update_xaxes(tickangle=-45)
        fig_depenses.update_yaxes(title_text="Montant (FCFA)")
        st.plotly_chart(fig_depenses, use_container_width=True)
        
                # Cartes récapitulatives
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="--accent:#E2B75F">
                <div class="metric-label">📊 Total dépenses exploitation</div>
                <div class="metric-value">{total_depenses/1e6:.2f} M FCFA</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # Répartition par type (variables vs fixes) - GESTION DYNAMIQUE
            variables = (c_fin["cout_aliment_fcfa"] + c_fin["cout_poussins_fcfa"] + 
                        c_fin["cout_medical_fcfa"] + c_fin["cout_litiere_fcfa"] + 
                        c_fin["cout_transport_fcfa"])
            
            # Charges fixes de base (toujours présentes)
            fixes = (c_fin["cout_salaires_fcfa"] + c_fin["cout_loyer_fcfa"] + 
                    c_fin["cout_eau_elec_fcfa"])
            
            # Ajouter Télécom et Autres frais uniquement s'ils existent
            if "cout_telecom_fcfa" in c_fin.index and pd.notna(c_fin["cout_telecom_fcfa"]):
                fixes += c_fin["cout_telecom_fcfa"]
            if "cout_autres_fcfa" in c_fin.index and pd.notna(c_fin["cout_autres_fcfa"]):
                fixes += c_fin["cout_autres_fcfa"]
            
            if hasattr(variables, 'iloc'):
                variables = variables.iloc[0]
                fixes = fixes.iloc[0]
            
            st.markdown(f"""
            <div class="metric-card" style="--accent:#D4A373">
                <div class="metric-label">📈 Répartition</div>
                <div class="metric-value">Coûts variables : {variables/1e6:.2f} M</div>
                <div class="metric-sub">Charges fixes : {fixes/1e6:.2f} M</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================================
        # INTERPRÉTATIONS DYNAMIQUES - DÉPENSES D'EXPLOITATION
        # ============================================================
        with st.expander("📖 Interprétations", expanded=False):
            
            if total_depenses > 0:
                # Calcul des parts
                parts = [(v / total_depenses * 100) for v in valeurs]
                
                # Postes principaux
                postes_principaux = []
                for i, (cat, part) in enumerate(zip(categories, parts)):
                    if part > 10:
                        postes_principaux.append(f"• {cat} : {part:.1f}%")
                
                # Analyse de la structure
                part_aliment = parts[0]
                part_poussins = parts[1]
                part_fixes = (c_fin["cout_salaires_fcfa"] + c_fin["cout_loyer_fcfa"] + c_fin["cout_eau_elec_fcfa"]) / total_depenses * 100
                
                # ALIMENT AVEC RÉFÉRENCE 45%
                if part_aliment > 50:
                    alerte_aliment = "Aliment trop élevé (>50%) → premier levier d'optimisation"
                    couleur_aliment = "#f87171"
                    reference_aliment = "(Réf. : < 45% pour être maîtrisé)"
                elif part_aliment > 45:
                    alerte_aliment = "Aliment correct (45-50%) → à surveiller"
                    couleur_aliment = "#E2B75F"
                    reference_aliment = "(Réf. : < 45% pour être maîtrisé)"
                else:
                    alerte_aliment = "Aliment maîtrisé (<45%)"
                    couleur_aliment = "#34d399"
                    reference_aliment = "(Réf. : < 45% → bonne maîtrise)"
                
                if part_fixes > 30:
                    alerte_fixes = "Charges fixes élevées (>30%) → augmenter le volume"
                    couleur_fixes = "#f87171"
                elif part_fixes > 20:
                    alerte_fixes = "Charges fixes modérées (20-30%)"
                    couleur_fixes = "#E2B75F"
                else:
                    alerte_fixes = "Charges fixes maîtrisées (<20%)"
                    couleur_fixes = "#34d399"
                
            else:
                postes_principaux = []
                part_aliment = 0
                part_fixes = 0
                alerte_aliment = "Données de dépenses manquantes"
                alerte_fixes = "Données insuffisantes"
                reference_aliment = ""
                couleur_aliment = couleur_fixes = "#6b7280"
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Conteneur 1 : Structure des coûts AVEC RÉFÉRENCE
                if postes_principaux:
                    texte_structure = ""
                    for poste in postes_principaux:
                        # Extraire le nom et le pourcentage
                        if "Aliment" in poste:
                            valeur = part_aliment
                            if valeur < 45:
                                reference = "(bon)"
                            elif valeur <= 50:
                                reference = "(acceptable)"
                            else:
                                reference = "(trop élevé)"
                        elif "Poussins" in poste:
                            valeur = part_poussins
                            if valeur < 20:
                                reference = "(bon)"
                            elif valeur <= 25:
                                reference = "(acceptable)"
                            else:
                                reference = "(trop élevé)"
                        elif "Médical" in poste:
                            valeur = parts[categories.index("Médical")] if "Médical" in categories else 0
                            if valeur < 4:
                                reference = "(bon)"
                            elif valeur <= 6:
                                reference = "(acceptable)"
                            else:
                                reference = "(élevé)"
                        elif "Transport" in poste or "Litière" in poste:
                            reference = "(à surveiller)"
                        elif "Salaires" in poste or "Loyer" in poste or "Eau/Élec" in poste:
                            reference = "(charge fixe)"
                        else:
                            reference = ""
                        
                        texte_structure += f"• {poste} {reference}<br>"
                else:
                    texte_structure = "• Données insuffisantes"

                st.markdown(f"""
                <div class="metric-card" style="--accent:#163F36;">
                    <div class="metric-label" style="font-size: 16px;">Structure des coûts</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        {texte_structure}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur 2 : Analyse aliment AVEC RÉFÉRENCE
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_aliment};">
                    <div class="metric-label" style="font-size: 16px;">Poste alimentaire</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • Part de l'aliment : {part_aliment:.1f}% du total<br>
                        • {alerte_aliment}<br>
                        • <span style="color: #6b7280; font-size: 11px;">{reference_aliment}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Conteneur 3 : Charges fixes
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_fixes};">
                    <div class="metric-label" style="font-size: 16px;">Charges fixes</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • Part des charges fixes : {part_fixes:.1f}% du total<br>
                        • {alerte_fixes}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur 4 : Synthèse et recommandation
                if total_depenses > 0:
                    if part_aliment > 50:
                        synthese = "Priorité : réduire le coût alimentaire (négocier les sacs, réduire le gaspillage)"
                    elif part_fixes > 30 and c_fin["volume_vendu"] < 2000:
                        synthese = "Envisager d'augmenter le volume pour diluer les charges fixes"
                    elif part_aliment <= 45 and part_fixes <= 25:
                        synthese = "Structure des coûts maîtrisée → maintenir les bonnes pratiques"
                    else:
                        synthese = "Structure équilibrée → surveillance continue recommandée"
                else:
                    synthese = "Données insuffisantes pour l'analyse"
                
                st.markdown(f"""
                <div class="metric-card" style="--accent:#D4A373;">
                    <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {synthese}<br>
                        • Coût total : {total_depenses/1e6:.2f} M FCFA
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
    
 
    
    # ============================================================
    # INVESTISSEMENTS GLOBAUX (cycles 1 à 3)
    # ============================================================
    st.markdown("### 🏗️ Investissements globaux (cycles passés)")

      
    
    # Récupérer l'investissement du cycle sélectionné
    inv_cycle = c_fin.get("investissements_globaux_fcfa", 0)
    if hasattr(inv_cycle, 'iloc'):
        inv_cycle = inv_cycle.iloc[0]
    
    # Vérifier si le cycle fait partie des 3 premiers
    cycle_num = int(cycle_finance.replace("Cycle", "")) if cycle_finance.startswith("Cycle") else 0
    
    if cycle_num <= 3:
        # Cycles 1, 2, 3 : afficher le total cumulé
        total_inv = cycles_recap[cycles_recap["cycle_id"].isin(["Cycle1", "Cycle2", "Cycle3"])]["investissements_globaux_fcfa"].sum()
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <div class="metric-card" style="--accent:#E2B75F; margin-top: 10px; text-align: center; width: 100%; max-width: 500px;">
                <div class="metric-label" style="text-align: center;">📊 Total investissements (cycles 1 à 3)</div>
                <div class="metric-value" style="text-align: center; font-size: 24px;">{total_inv:,.0f} FCFA</div>
                <div class="metric-sub" style="text-align: center;">{total_inv/1e6:.2f} M FCFA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Cycle 4 ou plus : afficher l'investissement du cycle (montant exact)
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <div class="metric-card" style="--accent:#E2B75F; margin-top: 10px; text-align: center; width: 100%; max-width: 500px;">
                <div class="metric-label" style="text-align: center;">📊 Investissements - {cycle_finance}</div>
                <div class="metric-value" style="text-align: center; font-size: 24px;">{inv_cycle:,.0f} FCFA</div>
                <div class="metric-sub" style="text-align: center;">{inv_cycle/1e6:.2f} M FCFA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # ÉVOLUTION DU COÛT TOTAL PAR JOUR
    # ============================================================
    st.markdown("### 🐣 Évolution du coût total par jour")
    afficher_cout_jour = st.checkbox("", value=True, key="check_cout_jour")

    if afficher_cout_jour:
        if not j_fin.empty:
            # Coût alimentaire par jour (360 FCFA/kg)
            cout_aliment_jour = j_fin["conso_jour"] * 360
            
            # Répartition des autres coûts variables sur la durée du cycle
            couts_variables = (c_fin["cout_poussins_fcfa"] + c_fin["cout_medical_fcfa"] + 
                            c_fin["cout_transport_fcfa"] + c_fin["cout_litiere_fcfa"])
            cout_journalier_variables = couts_variables / len(j_fin) if len(j_fin) > 0 else 0
            
            # Coût total par jour
            cout_total_jour = cout_aliment_jour + cout_journalier_variables
            
            # Coût cumulé
            cout_cumule = cout_total_jour.cumsum()
            
            fig_cout = go.Figure()
            fig_cout.add_trace(go.Scatter(
                x=j_fin["jour"],
                y=cout_total_jour,
                mode="lines+markers",
                name="Coût total par jour",
                line=dict(color="#163F36", width=2.5),
                marker=dict(size=6, color="#E2B75F"),
                fill="tozeroy",
                fillcolor="rgba(78, 124, 255, 0.15)",
                hovertemplate="Jour %{x}<br>Coût journalier : %{y:,.0f} FCFA<extra></extra>"
            ))
            
            # Ajout de la courbe de coût cumulé (axe secondaire)
            fig_cout.add_trace(go.Scatter(
                x=j_fin["jour"],
                y=cout_cumule,
                mode="lines",
                name="Coût cumulé",
                line=dict(color="#E2B75F", width=2, dash="dot"),
                yaxis="y2",
                hovertemplate="Jour %{x}<br>Coût cumulé : %{y:,.0f} FCFA<extra></extra>"
            ))
            
            plotly_light_layout(fig_cout, f"Évolution du coût total par jour - {cycle_finance}", height=400)
            fig_cout.update_layout(
                legend=dict(font=dict(color="#163F36", size=10)),
                yaxis2=dict(
                    overlaying="y",
                    side="right",
                    showgrid=False,
                    tickfont=dict(color="#163F36", size=10),
                    title_font=dict(color="#163F36"),
                    title_text="Coût cumulé (FCFA)"
                )
            )
            fig_cout.update_xaxes(title_text="Jour du cycle")
            fig_cout.update_yaxes(title_text="Coût journalier (FCFA)")
            st.plotly_chart(fig_cout, use_container_width=True)
            
            # ============================================================
            # INTERPRÉTATIONS DYNAMIQUES - COÛT TOTAL PAR JOUR
            # ============================================================
            with st.expander("📖 Interprétations", expanded=False):
                
                # Calculs dynamiques
                cout_moyen_journalier = cout_total_jour.mean()
                cout_max_journalier = cout_total_jour.max()
                
                # CORRECTION : Trouver le jour correspondant au coût maximum
                if not cout_total_jour.empty and cout_max_journalier > 0:
                    # Récupérer l'index de la ligne où le coût est maximum
                    idx_max = cout_total_jour.idxmax()
                    # Récupérer le jour correspondant dans la colonne "jour"
                    jour_max_cout = j_fin.loc[idx_max, "jour"] if idx_max in j_fin.index else 0
                else:
                    jour_max_cout = 0
                    
                cout_cumule_final = cout_cumule.iloc[-1] if not cout_cumule.empty else 0
                
                # Détection de la progression
                if len(j_fin) >= 2:
                    debut = cout_total_jour.iloc[:len(j_fin)//3].mean() if len(j_fin) >= 3 else cout_total_jour.iloc[0]
                    fin = cout_total_jour.iloc[-len(j_fin)//3:].mean() if len(j_fin) >= 3 else cout_total_jour.iloc[-1]
                    progression = (fin - debut) / debut * 100 if debut > 0 else 0
                else:
                    progression = 0
                
                if progression > 50:
                    texte_progression = f"Forte augmentation du coût (+{progression:.0f}%) en fin de cycle"
                    couleur_prog = "#f87171"
                elif progression > 20:
                    texte_progression = f"Augmentation modérée du coût (+{progression:.0f}%)"
                    couleur_prog = "#E2B75F"
                elif progression < -20:
                    texte_progression = f"Baisse significative du coût ({progression:.0f}%)"
                    couleur_prog = "#34d399"
                elif progression < -5:
                    texte_progression = f"Légère baisse du coût ({progression:.0f}%)"
                    couleur_prog = "#34d399"
                else:
                    texte_progression = f"Coût stable tout au long du cycle (variation de {progression:+.0f}%)"
                    couleur_prog = "#34d399"
                
                # === PART DE L'ALIMENT ===
                if cout_total_jour.sum() > 0 and cout_total_jour.mean() > 0:
                    part_aliment_jour = (cout_aliment_jour / cout_total_jour).mean() * 100
                    
                    if part_aliment_jour > 80:
                        alerte_aliment = f"L'aliment représente plus de 80% du coût journalier (très élevé)"
                        couleur_aliment = "#f87171"
                        reference_aliment = "(Réf. : < 45% pour être maîtrisé)"
                    elif part_aliment_jour > 70:
                        alerte_aliment = f"L'aliment représente 70-80% du coût journalier"
                        couleur_aliment = "#E2B75F"
                        reference_aliment = "(Réf. : < 45% pour être maîtrisé)"
                    elif part_aliment_jour > 45:
                        alerte_aliment = f"Part de l'aliment : {part_aliment_jour:.0f}% (au-dessus de la référence)"
                        couleur_aliment = "#E2B75F"
                        reference_aliment = "(Réf. : < 45% pour être maîtrisé)"
                    else:
                        alerte_aliment = f"Part de l'aliment maîtrisée ({part_aliment_jour:.0f}%)"
                        couleur_aliment = "#34d399"
                        reference_aliment = "(< 45% : bonne maîtrise)"
                else:
                    part_aliment_jour = 0
                    alerte_aliment = "Données insuffisantes pour calculer la part de l'aliment"
                    reference_aliment = ""
                    couleur_aliment = "#6b7280"
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Conteneur 1 : Statistiques générales
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Statistiques du coût journalier</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Coût moyen : {cout_moyen_journalier:,.0f} FCFA/jour<br>
                            • Coût maximum : {cout_max_journalier:,.0f} FCFA (J{jour_max_cout})<br>
                            • Coût total cumulé : {cout_cumule_final/1e6:.2f} M FCFA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 2 : Progression du coût
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_prog};">
                        <div class="metric-label" style="font-size: 16px;">Progression du coût</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_progression}<br>
                            • Début cycle : {debut:,.0f} FCFA/jour → Fin cycle : {fin:,.0f} FCFA/jour
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Part de l'aliment
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_aliment};">
                        <div class="metric-label" style="font-size: 16px;">Part de l'aliment</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {alerte_aliment}<br>
                            • Part moyenne : {part_aliment_jour:.0f}% du coût journalier<br>
                            • <span style="color: #6b7280; font-size: 11px;">{reference_aliment}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Synthèse
                    if cout_moyen_journalier > 0:
                        if cout_cumule_final > c_fin["ca_fcfa"]:
                            synthese = "Coût total supérieur au CA → cycle déficitaire"
                        elif cout_cumule_final > c_fin["ca_fcfa"] * 0.9:
                            synthese = "Coût proche du CA → marge faible"
                        else:
                            synthese = "Coût maîtrisé par rapport au CA"
                    else:
                        synthese = "Données insuffisantes pour l'analyse"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {synthese}<br>
                            • Coût journalier moyen : {cout_moyen_journalier:,.0f} FCFA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            st.info("Données journalières insuffisantes pour calculer le coût par jour.")
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")

    # ============================================================
    # SECTION : ÉVOLUTION DU COÛT TOTAL CUMULÉ (poussin + aliment)
    # ============================================================
    st.markdown("### 📦 Coût cumulé (aliment + poussins uniquement)")

    afficher_cout_cumul = st.checkbox("Afficher l'évolution du coût total cumulé", value=True, key="check_cout_cumul")

    if afficher_cout_cumul:
        if not j_fin.empty:
            # Coût d'achat des poussins (montant total)
            cout_poussins_total = c_fin.get("cout_poussins_fcfa", 0)
            if hasattr(cout_poussins_total, 'iloc'):
                cout_poussins_total = cout_poussins_total.iloc[0]
            
            # Coût alimentaire par jour (360 FCFA/kg)
            cout_aliment_par_jour = j_fin["conso_jour"] * 360
            
            # Calcul du coût total cumulé (poussins + aliment cumulé)
            cout_aliment_cumule = cout_aliment_par_jour.cumsum()
            cout_total_cumule = cout_poussins_total + cout_aliment_cumule
            
            # Coût par sujet
            effectif_initial = c_fin.get("effectif_initial", 1)
            if hasattr(effectif_initial, 'iloc'):
                effectif_initial = effectif_initial.iloc[0]
            cout_par_sujet = cout_total_cumule / effectif_initial
            
            # Graphique du coût total cumulé
            fig_cout_cumul = go.Figure()
            fig_cout_cumul.add_trace(go.Scatter(
                x=j_fin["jour"],
                y=cout_total_cumule,
                mode="lines+markers",
                name="Coût total cumulé (lot)",
                line=dict(color="#163F36", width=2.5),
                marker=dict(size=6, color="#E2B75F"),
                fill="tozeroy",
                fillcolor="rgba(78, 124, 255, 0.15)",
                hovertemplate=f"Jour %{{x}}<br>Coût total cumulé : %{{y:,.0f}} FCFA<extra></extra>"
            ))
            
            plotly_light_layout(fig_cout_cumul, f"Évolution du coût total cumulé (poussin + aliment) - {cycle_finance}", height=400)
            fig_cout_cumul.update_layout(
                legend=dict(font=dict(color="#163F36", size=10))
            )
            fig_cout_cumul.update_xaxes(title_text="Jour du cycle")
            fig_cout_cumul.update_yaxes(title_text="Coût total cumulé (FCFA)")
            st.plotly_chart(fig_cout_cumul, use_container_width=True)
            
            # Graphique du coût par sujet
            fig_cout_sujet = go.Figure()
            fig_cout_sujet.add_trace(go.Scatter(
                x=j_fin["jour"],
                y=cout_par_sujet,
                mode="lines+markers",
                name="Coût par sujet",
                line=dict(color="#E2B75F", width=2.5),
                marker=dict(size=6, color="#163F36"),
                fill="tozeroy",
                fillcolor="rgba(226, 183, 95, 0.15)",
                hovertemplate=f"Jour %{{x}}<br>Coût par sujet : %{{y:,.0f}} FCFA<extra></extra>"
            ))
            
            plotly_light_layout(fig_cout_sujet, f"Évolution du coût par sujet (poussin + aliment) - {cycle_finance}", height=400)
            fig_cout_sujet.update_layout(
                legend=dict(font=dict(color="#163F36", size=10))
            )
            fig_cout_sujet.update_xaxes(title_text="Jour du cycle")
            fig_cout_sujet.update_yaxes(title_text="Coût par sujet (FCFA)")
            st.plotly_chart(fig_cout_sujet, use_container_width=True)

            
            # ============================================================
            # INTERPRÉTATIONS DYNAMIQUES - COÛTS CUMULÉS
            # ============================================================
            with st.expander("📖 Interprétations", expanded=False):
                
                # Calculs dynamiques
                cout_total_final = cout_total_cumule.iloc[-1] if not cout_total_cumule.empty else 0
                cout_par_sujet_final = cout_par_sujet.iloc[-1] if not cout_par_sujet.empty else 0
                prix_vente_moyen = c_fin.get("prix_moyen_fcfa", 0)
                if hasattr(prix_vente_moyen, 'iloc'):
                    prix_vente_moyen = prix_vente_moyen.iloc[0]
                
                # Pente du coût cumulé (augmentation moyenne par jour)
                if len(j_fin) >= 2:
                    pente_cout = (cout_total_cumule.iloc[-1] - cout_total_cumule.iloc[0]) / (j_fin["jour"].iloc[-1] - j_fin["jour"].iloc[0])
                else:
                    pente_cout = 0
                
                # Marge par sujet (prix de vente - coût par sujet)
                if prix_vente_moyen > 0 and cout_par_sujet_final > 0:
                    marge_sujet = prix_vente_moyen - cout_par_sujet_final
                    if marge_sujet > 200:
                        texte_marge = f" Marge positive : {marge_sujet:.0f} FCFA/sujet"
                        couleur_marge = "#34d399"
                    elif marge_sujet > 0:
                        texte_marge = f"Marge faible : {marge_sujet:.0f} FCFA/sujet"
                        couleur_marge = "#E2B75F"
                    else:
                        texte_marge = f"Marge négative : {marge_sujet:.0f} FCFA/sujet"
                        couleur_marge = "#f87171"
                else:
                    texte_marge = "Données de prix ou coût manquantes"
                    couleur_marge = "#6b7280"
                
                # Comparaison avec le seuil de rentabilité
                seuil_rentabilite = c_fin.get("seuil_rentabilite_fcfa", 0)
                if hasattr(seuil_rentabilite, 'iloc'):
                    seuil_rentabilite = seuil_rentabilite.iloc[0]
                
                if seuil_rentabilite > 0:
                    if cout_total_final < seuil_rentabilite:
                        texte_seuil = f"Coût total ({cout_total_final/1e6:.1f} M) < seuil ({seuil_rentabilite/1e6:.1f} M)"
                        couleur_seuil = "#f87171"
                    else:
                        texte_seuil = f"Coût total ({cout_total_final/1e6:.1f} M) ≥ seuil ({seuil_rentabilite/1e6:.1f} M)"
                        couleur_seuil = "#34d399"
                else:
                    texte_seuil = " Seuil de rentabilité non disponible"
                    couleur_seuil = "#6b7280"
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Conteneur 1 : Coûts finaux
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#163F36;">
                        <div class="metric-label" style="font-size: 16px;">Coûts finaux</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Coût total cumulé : {cout_total_final/1e6:.2f} M FCFA<br>
                            • Coût par sujet : {cout_par_sujet_final:,.0f} FCFA<br>
                            • Augmentation moyenne : {pente_cout:,.0f} FCFA/jour
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 2 : Comparaison seuil de rentabilité
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_seuil};">
                        <div class="metric-label" style="font-size: 16px;">Seuil de rentabilité</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_seuil}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Marge par sujet (avec VRAI coût)
                    veritable_cout_par_sujet = c_fin["depenses_totales_fcfa"] / c_fin["volume_vendu"] if c_fin["volume_vendu"] > 0 else 0

                    if prix_vente_moyen > 0 and veritable_cout_par_sujet > 0:
                        marge_sujet_reelle = prix_vente_moyen - veritable_cout_par_sujet
                        if marge_sujet_reelle > 200:
                            texte_marge = f"Marge excellente : {marge_sujet_reelle:.0f} FCFA/sujet"
                            couleur_marge = "#34d399"
                        elif marge_sujet_reelle > 0:
                            texte_marge = f"Marge positive : {marge_sujet_reelle:.0f} FCFA/sujet"
                            couleur_marge = "#E2B75F"
                        else:
                            texte_marge = f"🔴 Marge négative : {marge_sujet_reelle:.0f} FCFA/sujet"
                            couleur_marge = "#f87171"
                    else:
                        texte_marge = "Données de prix ou coût manquantes"
                        couleur_marge = "#6b7280"

                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_marge};">
                        <div class="metric-label" style="font-size: 16px;">Marge par sujet</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_marge}<br>
                            • Prix de vente moyen : {prix_vente_moyen:,.0f} FCFA/sujet<br>
                            • Coût réel par sujet : {veritable_cout_par_sujet:,.0f} FCFA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Synthèse
                    # Utiliser le VRAI coût par sujet (toutes dépenses confondues)
                    veritable_cout_par_sujet = c_fin["depenses_totales_fcfa"] / c_fin["volume_vendu"] if c_fin["volume_vendu"] > 0 else 0

                    if prix_vente_moyen > 0 and veritable_cout_par_sujet > 0:
                        marge_reelle = prix_vente_moyen - veritable_cout_par_sujet
                    else:
                        marge_reelle = None

                    if marge_reelle is not None and marge_reelle > 200:
                        synthese = "Cycle très rentable → marge excellente"
                        couleur_synthese = "#34d399"
                    elif marge_reelle is not None and marge_reelle > 0:
                        synthese = "Cycle rentable → marge correcte"
                        couleur_synthese = "#34d399"
                    elif marge_reelle is not None and marge_reelle < 0:
                        synthese = "🔴 Cycle déficitaire → priorité : augmenter le prix ou réduire les coûts"
                        couleur_synthese = "#f87171"
                    else:
                        synthese = "Analyse des coûts disponible pour ce cycle"
                        couleur_synthese = "#D4A373"

                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_synthese};">
                        <div class="metric-label" style="font-size: 16px;">Synthèse</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {synthese}<br>
                            • Coût réel par sujet : {veritable_cout_par_sujet:,.0f} FCFA<br>
                            • Prix de vente moyen : {prix_vente_moyen:,.0f} FCFA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
           
        else:
            st.info("Données journalières insuffisantes pour calculer les coûts cumulés.")
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
            
    # ============================================================
    # CARTES RÉCAPITULATIVES STYLISÉES
    # ============================================================
    st.markdown("#### 📊 Récapitulatif des coûts")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#163F36">
            <div class="metric-label">Coût poussins (total)</div>
            <div class="metric-value">{cout_poussins_total:,.0f} FCFA</div>
            <div class="metric-sub">Achat initial</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#E2B75F">
            <div class="metric-label">Coût aliment total</div>
            <div class="metric-value">{cout_aliment_par_jour.sum():,.0f} FCFA</div>
            <div class="metric-sub">Consommation du cycle</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card" style="--accent:#D4A373">
                <div class="metric-label">Coût total cumulé</div>
                <div class="metric-value">{cout_total_cumule.iloc[-1]:,.0f} FCFA</div>
                <div class="metric-sub">Poussins + aliment</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        prix_vente_moyen = c_fin.get("prix_moyen_fcfa", 0)
        if hasattr(prix_vente_moyen, 'iloc'):
            prix_vente_moyen = prix_vente_moyen.iloc[0]
            
        cout_final = cout_par_sujet.iloc[-1]
        
        st.markdown(f"""
        <div class="metric-card" style="--accent:#D4A373">
            <div class="metric-label">Coût par sujet (final)</div>
            <div class="metric-value">{cout_final:,.0f} FCFA</div>
        </div>
        """, unsafe_allow_html=True)

        # ============================================================
        # EXPLICATION DU CALCUL
        # ============================================================
    with st.expander("📖 Détail du calcul"):
        st.markdown(f"""
            - **Coût d'achat des poussins** : {cout_poussins_total:,.0f} FCFA (ajouté au jour 1)
            - **Coût alimentaire par jour** : consommation (kg) × 360 FCFA/kg
            - **Coût total cumulé** = coût poussins + somme(coût alimentaire des jours précédents)
            - **Coût par sujet** = coût total cumulé / {effectif_initial} sujets
            
            **Rappel** : Le coût alimentaire est calculé sur la base de **360 FCFA/kg** (18 000 FCFA/sac de 50 kg).
            """)

    st.markdown("---")

  
    


    # ============================================================
    # SYNTHÈSE FINANCIÈRE AVEC MÉTRIQUES SUPPLÉMENTAIRES
    # ============================================================

    st.markdown("### 📊 Synthèse financière")

    # Cartes principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(card("CA", f"{c_fin['ca_fcfa']/1e6:.2f} M FCFA", "", "#163F36"), unsafe_allow_html=True)
    
    with col2:
        resultat = c_fin['resultat_net_fcfa']
        couleur_res = "#34d399" if resultat >= 0 else "#f87171"
        st.markdown(card("Résultat net", f"{resultat:+,.0f} FCFA", "", couleur_res), unsafe_allow_html=True)

    # ============================================================
    # INVESTISSEMENTS - adapté selon le cycle
    # ============================================================
    
    # Récupérer le numéro du cycle
    cycle_num = int(cycle_finance.replace("Cycle", "")) if cycle_finance.startswith("Cycle") else 0
    
    if cycle_num <= 3:
        # Cycles 1, 2, 3 : afficher le total cumulé
        total_invest = cycles_recap[cycles_recap["cycle_id"].isin(["Cycle1", "Cycle2", "Cycle3"])]["investissements_globaux_fcfa"].sum()
        if hasattr(total_invest, 'iloc'):
            total_invest = total_invest.iloc[0]
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="--accent:#D4A373;">
                <div class="metric-label">Total investissements</div>
                <div class="metric-value">{total_invest/1e6:.2f} M FCFA</div>
                <div class="metric-sub">cycles 1 à 3</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Cycle 4 ou plus : afficher l'investissement du cycle
        inv_cycle = c_fin.get("investissements_globaux_fcfa", 0)
        if hasattr(inv_cycle, 'iloc'):
            inv_cycle = inv_cycle.iloc[0]
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="--accent:#D4A373;">
                <div class="metric-label">Investissements - {cycle_finance}</div>
                <div class="metric-value">{inv_cycle:,.0f} FCFA</div>
                <div class="metric-sub">{inv_cycle/1e6:.2f} M FCFA</div>
            </div>
            """, unsafe_allow_html=True)

    col_1, col_2, col_3 = st.columns(3)
    # 2. Total dépenses d'exploitation (dépenses totales du cycle sélectionné - investissements du cycle sélectionné)
    total_invest_cycle = c_fin.get("investissements_globaux_fcfa", 0)
    if hasattr(total_invest_cycle, 'iloc'):
        total_invest_cycle = total_invest_cycle.iloc[0]

    total_exploit = c_fin['depenses_totales_fcfa'] - total_invest_cycle
    if hasattr(total_exploit, 'iloc'):
        total_exploit = total_exploit.iloc[0]

    with col_1:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#E2B75F;">
            <div class="metric-label">Dépenses d'exploitation</div>
            <div class="metric-value">{total_exploit/1e6:.2f} M FCFA</div>
            <div class="metric-sub">hors investissements</div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Coûts variables (aliment + poussins + médical + transport + litière)
    couts_variables = (c_fin["cout_aliment_fcfa"] + c_fin["cout_poussins_fcfa"] + 
                    c_fin["cout_medical_fcfa"] + c_fin["cout_transport_fcfa"] + 
                    c_fin["cout_litiere_fcfa"])
    if hasattr(couts_variables, 'iloc'):
        couts_variables = couts_variables.iloc[0]

    with col_2:
        st.markdown(f"""
        <div class="metric-card" style="--accent:#fbbf24;">
            <div class="metric-label">Coûts variables</div>
            <div class="metric-value">{couts_variables/1e6:.2f} M FCFA</div>
            <div class="metric-sub">aliment + poussins + soins</div>
        </div>
        """, unsafe_allow_html=True)

    # Quatrième métrique (coûts fixes)
    couts_fixes = total_exploit - couts_variables
    if hasattr(couts_fixes, 'iloc'):
        couts_fixes = couts_fixes.iloc[0]

    with col_3:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <div class="metric-card" style="--accent:#34d399; text-align: center; max-width: 300px;">
                <div class="metric-label">Charges fixes</div>
                <div class="metric-value">{couts_fixes/1e6:.2f} M FCFA</div>
                <div class="metric-sub">salaires + loyer + eau/élec</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
# ═══════════════════════════════════════════════════
# PAGE 4 : BILAN COMPARATIF
# ═══════════════════════════════════════════════════
elif page == "⚖️ Bilan Comparatif":

    section_header("⚖️ Bilan Comparatif", "Comparaison des performances entre tous les cycles")

    col_r1, col_r2 = st.columns(2)

    # ============================================================
    # COMPARAISON DES CYCLES - PARAMÈTRES CLÉS
    # ============================================================
    st.markdown("### 📊 Comparaison des cycles par paramètre")

    # Récupérer TOUS les cycles disponibles
    cycles_disponibles = sorted(cycles_recap["cycle_id"].unique())
    nb_cycles = len(cycles_disponibles)
    
    # Créer des listes dynamiques pour chaque indicateur
    cycles_noms = []
    cout_par_sujet_list = []
    duree_ventes_list = []
    roi_list = []
    ic_list = []
    poids_list = []
    marge_list = []
    prix_moyen_list = []
    prix_revient_list = []

    for cycle in cycles_disponibles:
        c_data = cycles_recap[cycles_recap["cycle_id"] == cycle].iloc[0]
        cycles_noms.append(cycle)
        
        # Coût par sujet
        cout_sujet = c_data["depenses_totales_fcfa"] / c_data["volume_vendu"] if c_data["volume_vendu"] > 0 else 0
        cout_par_sujet_list.append(cout_sujet)
        
        # Durée des ventes
        ventes_cycle = ventes[ventes["cycle_id"] == cycle]
        duree = ventes_cycle["jour"].max() - ventes_cycle["jour"].min() if not ventes_cycle.empty else 0
        duree_ventes_list.append(duree)
        
        # ROI
        roi_list.append(c_data.get("roi_pct", 0))
        
        # IC
        ic_list.append(c_data.get("ic_calcule", c_data.get("ic_standard", 1.7)))
        
        # Poids final
        poids_list.append(c_data["poids_final_kg"])
        
        # Marge unitaire
        marge_list.append(c_data["marge_unitaire_fcfa"])
        
        # Prix moyen
        prix_moyen_list.append(c_data["prix_moyen_fcfa"])
        
        # Prix de revient unitaire
        prix_revient_list.append(c_data.get("prix_revient_unitaire", 0))

    # ============================================================
    # FONCTION POUR CLASSER LES CYCLES (adaptée à N cycles)
    # ============================================================
    def classer_cycles_dynamique(valeurs, cycles, plus_est_mieux):
        """Classe les cycles et retourne le meilleur, le pire et la moyenne"""
        items = list(zip(cycles, valeurs))
        if plus_est_mieux:
            items.sort(key=lambda x: x[1], reverse=True)
        else:
            items.sort(key=lambda x: x[1])
        
        return {
            "meilleur": items[0][0],
            "meilleur_valeur": items[0][1],
            "pire": items[-1][0],
            "pire_valeur": items[-1][1],
            "moyenne": sum(valeurs) / len(valeurs) if valeurs else 0
        }

    # ============================================================
    # GRAPHIQUE 1 : ROI
    # ============================================================
    st.markdown("#### 📈 1. Retour sur Investissement (ROI)")
    afficher_roi = st.checkbox("", value=True, key="check_roi")

    if afficher_roi:
        roi_classement = classer_cycles_dynamique(roi_list, cycles_noms, plus_est_mieux=True)

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=cycles_noms,
            y=roi_list,
            marker_color=["#163F36", "#E2B75F", "#D4A373", "#a78bfa", "#34d399"][:nb_cycles],
            text=[f"{v:+.1f}%" for v in roi_list],
            textposition="outside"
        ))
        fig1.add_hline(y=0, line_dash="dot", line_color="#f87171")
        plotly_light_layout(fig1, "ROI par cycle", height=350)
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander("📖 Interprétation du ROI"):
            st.markdown(f"""
            - **Meilleur cycle** : {roi_classement["meilleur"]} ({roi_classement["meilleur_valeur"]:+.1f}%)
            - **Moyenne des cycles** : {roi_classement["moyenne"]:+.1f}%
            - **Cycle le moins performant** : {roi_classement["pire"]} ({roi_classement["pire_valeur"]:+.1f}%)
            
            Un ROI positif signifie que l'investissement génère un retour. Un ROI négatif indique une perte.
            """)
    else:
        st.caption("Graphique ROI masqué")

    st.markdown("---")

    # ============================================================
    # GRAPHIQUE 2 : IC
    # ============================================================
    st.markdown("#### 🍗 2. Indice de Consommation (IC)")
    afficher_ic = st.checkbox("", value=True, key="check_ic")

    if afficher_ic:
        ic_classement = classer_cycles_dynamique(ic_list, cycles_noms, plus_est_mieux=False)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=cycles_noms,
            y=ic_list,
            marker_color=["#163F36", "#E2B75F", "#D4A373", "#a78bfa", "#34d399"][:nb_cycles],
            text=[f"{v:.2f}" for v in ic_list],
            textposition="outside"
        ))
        fig2.add_hline(y=1.7, line_dash="dash", line_color="#34d399", annotation_text="Objectif 1.7")
        plotly_light_layout(fig2, "Indice de consommation (IC) par cycle", height=350)
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("📖 Interprétation de l'IC"):
            st.markdown(f"""
            - **Meilleur cycle (IC le plus bas)** : {ic_classement["meilleur"]} ({ic_classement["meilleur_valeur"]:.2f})
            - **Moyenne des cycles** : {ic_classement["moyenne"]:.2f}
            - **Cycle le moins performant (IC le plus élevé)** : {ic_classement["pire"]} ({ic_classement["pire_valeur"]:.2f})
            
            Un IC bas signifie une meilleure efficacité alimentaire. L'objectif est ≤ 1,7.
            """)
    else:
        st.caption("Graphique IC masqué")

    st.markdown("---")

    # ============================================================
    # GRAPHIQUE 3 : Poids final
    # ============================================================
    st.markdown("#### 🥩 3. Poids final moyen")
    afficher_poids = st.checkbox("", value=True, key="check_poids_comp")

    if afficher_poids:
        poids_classement = classer_cycles_dynamique(poids_list, cycles_noms, plus_est_mieux=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=cycles_noms,
            y=poids_list,
            marker_color=["#163F36", "#E2B75F", "#D4A373", "#a78bfa", "#34d399"][:nb_cycles],
            text=[f"{v:.2f} kg" for v in poids_list],
            textposition="outside"
        ))
        fig3.add_hline(y=2.0, line_dash="dash", line_color="#34d399", annotation_text="Objectif 2.0 kg")
        plotly_light_layout(fig3, "Poids final moyen par cycle", height=350)
        st.plotly_chart(fig3, use_container_width=True)
        
        with st.expander("📖 Interprétation du poids final"):
            st.markdown(f"""
            - **Meilleur cycle (poids le plus élevé)** : {poids_classement["meilleur"]} ({poids_classement["meilleur_valeur"]:.2f} kg)
            - **Moyenne des cycles** : {poids_classement["moyenne"]:.2f} kg
            - **Cycle le moins performant (poids le plus faible)** : {poids_classement["pire"]} ({poids_classement["pire_valeur"]:.2f} kg)
            
            Un poids final élevé est généralement meilleur pour la vente (poulet plus lourd).
            """)
    else:
        st.caption("Graphique Poids final masqué")

    st.markdown("---")

    # ============================================================
    # GRAPHIQUE 4 : Coût par sujet
    # ============================================================
    st.markdown("#### 💰 4. Coût par sujet")
    afficher_cout = st.checkbox("", value=True, key="check_cout_sujet")

    if afficher_cout:
        cout_classement = classer_cycles_dynamique(cout_par_sujet_list, cycles_noms, plus_est_mieux=False)

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=cycles_noms,
            y=cout_par_sujet_list,
            marker_color=["#163F36", "#E2B75F", "#D4A373", "#a78bfa", "#34d399"][:nb_cycles],
            text=[f"{v:,.0f} FCFA" for v in cout_par_sujet_list],
            textposition="outside"
        ))
        plotly_light_layout(fig4, "Coût par sujet (poulet produit)", height=350)
        st.plotly_chart(fig4, use_container_width=True)
        
        with st.expander("📖 Interprétation du coût par sujet"):
            st.markdown(f"""
            - **Meilleur cycle (coût le plus bas)** : {cout_classement["meilleur"]} ({cout_classement["meilleur_valeur"]:,.0f} FCFA)
            - **Moyenne des cycles** : {cout_classement["moyenne"]:,.0f} FCFA
            - **Cycle le moins performant (coût le plus élevé)** : {cout_classement["pire"]} ({cout_classement["pire_valeur"]:,.0f} FCFA)
            
            Un coût par sujet bas est essentiel pour la rentabilité.
            """)
    else:
        st.caption("Graphique Coût par sujet masqué")

    st.markdown("---")

    # ============================================================
    # GRAPHIQUE 5 : Durée des ventes
    # ============================================================
    st.markdown("#### 📅 5. Durée des ventes (étalement)")
    afficher_duree = st.checkbox("", value=True, key="check_duree_ventes")

    if afficher_duree:
        duree_classement = classer_cycles_dynamique(duree_ventes_list, cycles_noms, plus_est_mieux=False)

        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=cycles_noms,
            y=duree_ventes_list,
            marker_color=["#163F36", "#E2B75F", "#D4A373", "#a78bfa", "#34d399"][:nb_cycles],
            text=[f"{v:.0f} jours" for v in duree_ventes_list],
            textposition="outside"
        ))
        plotly_light_layout(fig5, "Étalement des ventes (première → dernière vente)", height=350)
        st.plotly_chart(fig5, use_container_width=True)
        
        with st.expander("📖 Interprétation de la durée des ventes"):
            st.markdown(f"""
            - **Meilleur cycle (ventes concentrées)** : {duree_classement["meilleur"]} ({duree_classement["meilleur_valeur"]:.0f} jours)
            - **Moyenne des cycles** : {duree_classement["moyenne"]:.0f} jours
            - **Cycle le moins performant (ventes trop étalées)** : {duree_classement["pire"]} ({duree_classement["pire_valeur"]:.0f} jours)
            
            Des ventes concentrées réduisent les coûts logistiques et améliorent la trésorerie.
            """)
    else:
        st.caption("Graphique Durée des ventes masqué")

    st.markdown("---")

    # ============================================================
    # GRAPHIQUE : Prix moyen vs Prix de revient
    # ============================================================
    st.markdown("<span style='font-size:22px; font-weight:600;'>💰 Prix moyen vs Prix de revient</span>", unsafe_allow_html=True)
    afficher_prix_revient = st.checkbox("", value=True, key="check_prix_revient")

    if afficher_prix_revient:
        fig_pm = make_subplots(
            rows=2, cols=1, 
            subplot_titles=("Prix Moyen vs Prix de Revient (FCFA)", "Marge Unitaire (FCFA)"),
            vertical_spacing=0.18
        )
        
        fig_pm.add_trace(go.Scatter(
            x=cycles_noms, y=prix_moyen_list, 
            mode="lines+markers",
            name="Prix moyen", 
            line=dict(color="#4e7cff", width=2.5),
            marker=dict(size=10)
        ), row=1, col=1)
        
        fig_pm.add_trace(go.Scatter(
            x=cycles_noms, y=prix_revient_list, 
            mode="lines+markers",
            name="Prix revient", 
            line=dict(color="#f87171", width=2.5, dash="dot"),
            marker=dict(size=10)
        ), row=1, col=1)
        
        colors_m = ["#34d399" if m >= 0 else "#f87171" for m in marge_list]
        fig_pm.add_trace(go.Bar(
            x=cycles_noms, y=marge_list, 
            marker_color=colors_m, 
            opacity=0.85, 
            name="Marge"
        ), row=2, col=1)
        
        fig_pm.add_hline(y=0, line_color="#374151", line_dash="dot", row=2, col=1)

        fig_pm.update_layout(
            plot_bgcolor="#EFE2D1", 
            paper_bgcolor="#EFE2D1",
            font=dict(family=FONT_FAMILY, color="#163F36"),
            height=450,
            showlegend=True,
            margin=dict(l=12, r=12, t=60, b=40),
            legend=dict(
                bgcolor="#F4E8D8", 
                bordercolor="#E2B75F", 
                borderwidth=1,
                font=dict(color="#163F36", size=10),
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        
        fig_pm.update_xaxes(title_font=dict(color="#163F36"), tickfont=dict(color="#163F36"), gridcolor="#E2B75F")
        fig_pm.update_yaxes(title_font=dict(color="#163F36"), tickfont=dict(color="#163F36"), gridcolor="#E2B75F")
        
        st.plotly_chart(fig_pm, use_container_width=True)
        
        with st.expander("📖 Interprétation du prix moyen vs prix de revient"):
            # Trouver le meilleur cycle pour la marge
            meilleur_marge_idx = marge_list.index(max(marge_list))
            meilleur_marge_cycle = cycles_noms[meilleur_marge_idx]
            
            st.markdown(f"""
            - **Cycle avec la meilleure marge unitaire** : {meilleur_marge_cycle} ({max(marge_list):+.0f} FCFA/sujet)
            - **Prix de vente moyen le plus élevé** : {cycles_noms[prix_moyen_list.index(max(prix_moyen_list))]} ({max(prix_moyen_list):.0f} FCFA)
            - **Prix de revient le plus bas** : {cycles_noms[prix_revient_list.index(min([p for p in prix_revient_list if p > 0]))]} ({min([p for p in prix_revient_list if p > 0]):.0f} FCFA)
            
            Un écart positif entre le prix de vente et le prix de revient indique une marge bénéficiaire.
            Plus cet écart est grand, plus le cycle est rentable.
            """)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")

        # ============================================================
    # SYNTHÈSE GLOBALE (adaptée à N cycles)
    # ============================================================
    st.markdown("### 🎯 Synthèse globale")

    # Classements pour chaque indicateur
    roi_classement = classer_cycles_dynamique(roi_list, cycles_noms, plus_est_mieux=True)
    ic_classement = classer_cycles_dynamique(ic_list, cycles_noms, plus_est_mieux=False)
    poids_classement = classer_cycles_dynamique(poids_list, cycles_noms, plus_est_mieux=True)
    cout_classement = classer_cycles_dynamique(cout_par_sujet_list, cycles_noms, plus_est_mieux=False)
    duree_classement = classer_cycles_dynamique(duree_ventes_list, cycles_noms, plus_est_mieux=False)
    marge_classement = classer_cycles_dynamique(marge_list, cycles_noms, plus_est_mieux=True)

    # Compter les mentions "meilleur" par cycle
    compteur = {cycle: 0 for cycle in cycles_noms}
    for classement in [roi_classement, ic_classement, poids_classement, cout_classement, duree_classement, marge_classement]:
        compteur[classement["meilleur"]] += 1

    meilleur_cycle = max(compteur, key=compteur.get)

    # Construction du texte des détails des performances (CORRIGÉ)
    details_html = ""
    
    # Liste des indicateurs avec leurs classements
    indicateurs = [
        ("ROI", roi_classement),
        ("IC", ic_classement),
        ("Poids final", poids_classement),
        ("Coût par sujet", cout_classement),
        ("Étalement des ventes", duree_classement),
        ("Marge unitaire", marge_classement)
    ]
    
    for nom, class_dict in indicateurs:
        details_html += f"<div>• {nom} : <strong>{class_dict['meilleur']}</strong></div>"

    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <div class="metric-card" style="--accent:#D4A373; background: #F4E8D8; color: #163F36; text-align: center; max-width: 600px; width: 100%;">
            <div class="metric-label" style="color: #163F36; font-size: 14px;">🏆 CYCLE LE PLUS PERFORMANT</div>
            <div class="metric-value" style="color: #163F36; font-size: 28px;">{meilleur_cycle}</div>
            <div class="metric-sub" style="color: #163F36;">{compteur[meilleur_cycle]}/6 critères</div>
            <div style="margin-top: 15px; border-top: 1px solid #E2B75F; padding-top: 12px;">
                <div style="font-size: 13px; font-weight: 600; margin-bottom: 8px;">📊 DÉTAIL DES PERFORMANCES</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12px; text-align: left;">
                    {details_html}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # TABLEAU SEUIL DE RENTABILITÉ (adapté à N cycles)
    # ============================================================
    st.markdown('<div class="section-header">Seuil de Rentabilité</div>', unsafe_allow_html=True)
    
    # Expander avec les explications
    with st.expander("📖 Comment est calculé le seuil de rentabilité ?"):
        st.markdown("""
        ### 🎯 Méthodologie de calcul du seuil de rentabilité
        
        Le **seuil de rentabilité** est le chiffre d'affaires minimum à atteindre pour couvrir l'ensemble des charges (variables + fixes).
        
        #### Formules utilisées :
        
        | Étape | Formule | Explication |
        |-------|---------|-------------|
        | 1 | **Charges variables (CV)** = Aliment + Poussins + Médical + Transport + Litière | Coûts qui varient avec le volume de production |
        | 2 | **Charges fixes (CF)** = Salaires + Loyer + Eau/Élec + Télécom + Autres frais | Coûts indépendants du volume de production |
        | 3 | **Marge sur coûts variables (MCV)** = CA - CV | Ce qui reste après avoir payé les charges variables |
        | 4 | **Taux de marge sur CV (TMCV)** = MCV / CA | Chaque franc de CA génère ce taux de marge |
        | 5 | **Seuil de rentabilité (SR)** = CF / TMCV | CA minimum à atteindre |
        | 6 | **Point mort (jours)** = (SR / CA) × Durée du cycle | Nombre de jours pour atteindre le seuil |
        
        #### Exemple concret (Cycle 3) :
        
        | Indicateur | Valeur | Calcul |
        |------------|--------|--------|
        | Charges variables | 11 202 401 FCFA | Aliment + Poussins + Médical + Transport |
        | Charges fixes | 1 347 500 FCFA | Salaires + Loyer + Eau/Élec |
        | CA réalisé | 12 250 505 FCFA | |
        | MCV | 1 048 104 FCFA | 12 250 505 - 11 202 401 |
        | TMCV | 8,56% | 1 048 104 / 12 250 505 |
        | **Seuil de rentabilité** | **15 743 458 FCFA** | 1 347 500 / 0,0856 |
        | Point mort | 68 jours | (15 743 458 / 12 250 505) × 53 |
        
        #### Interprétation des résultats :
        
        | Situation | Signification |
        |-----------|---------------|
        | **SR atteint** (CA ≥ SR) | Le cycle est rentable |
        | **SR non atteint** (CA < SR) | Le cycle n'est pas rentable |
        | **Marge négative** (MCV < 0) | Le cycle est structurellement déficitaire |
        | **Point mort < durée cycle** | Le seuil est atteint pendant le cycle |
        | **Point mort > durée cycle** | Le seuil n'est pas atteint dans le temps imparti |
        
        > 💡 **Note** : Si la marge sur coûts variables est négative, le seuil de rentabilité est **non atteignable** car chaque vente supplémentaire génère une perte.
        """)
    
    # Créer des colonnes dynamiquement (max 4 par ligne)
    n_cols = min(4, nb_cycles)
    cols = st.columns(n_cols)
    
    for idx, cid in enumerate(cycles_disponibles):
        col_idx = idx % n_cols
        with cols[col_idx]:
            c = cycles_recap[cycles_recap["cycle_id"] == cid].iloc[0]
            sr = c["seuil_rentabilite_fcfa"]
            ca = c["ca_fcfa"]
            pm_j = c["point_mort_jours"]
            color = COLORS.get(cid, "#4e7cff")
            
            if not pd.isna(sr) and sr > 0:
                gap = ca - sr
                pct_couv = (ca/sr)*100 if sr != 0 else 0
                st.markdown(f"""
                <div class="metric-card" style="--accent:{color}">
                    <div class="metric-label">{cid} · Seuil de Rentabilité</div>
                    <div class="metric-value">{sr/1e6:.2f} M FCFA</div>
                    <div class="metric-sub">CA réalisé : {ca/1e6:.2f} M FCFA</div>
                    <div class="{'metric-delta-pos' if gap>=0 else 'metric-delta-neg'}" style='margin-top:8px'>
                        {"▲" if gap>=0 else "▼"} {abs(gap)/1e6:.2f} M · {pct_couv:.0f}% couvert
                    </div>
                    {"<div style='margin-top:8px;font-size:12px;color:#6b7280'>Point mort : <b style='color:#fbbf24'>"+str(round(pm_j,1))+" j</b></div>" if not pd.isna(pm_j) and pm_j > 0 else ""}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="--accent:{color}">
                    <div class="metric-label">{cid} · Seuil de Rentabilité</div>
                    <div class="metric-value">Non atteignable</div>
                    <div class="metric-sub">Marge sur CV négative</div>
                </div>
                """, unsafe_allow_html=True)


        
    # ============================================================
    # 4. SYNTHÈSE FINALE
    # ============================================================
    st.markdown("---")
    st.markdown("### 🎯 Objectifs pour le Cycle 5")
        
    st.markdown("""
    | Indicateur | Objectif | Justification |
    |------------|----------|---------------|
    | Volume | 6 000 – 8 000 sujets | Poursuivre la montée en volume pour diluer les charges fixes |
    | Prix de vente | ≥ 2 800 FCFA/sujet | Améliorer la marge face à l'augmentation des coûts |
    | Coût de revient | ≤ 2 600 FCFA/sujet | Maîtriser l'inflation des matières premières |
    | Marge unitaire | ≥ 250 FCFA/sujet | Objectif de rentabilité renforcé |
    | IC | ≤ 1,7 | Maintenir l'efficacité alimentaire |
    | Mortalité | ≤ 4% | Maintenir la maîtrise sanitaire |
    | Taux de conformité température | ≥ 85% | Réduire l'impact sur la mortalité |
    | Jours hors norme température | ≤ 5 jours | Limiter le stress thermique des animaux |
    """)
        
    

# ═══════════════════════════════════════════════════
# PAGE 5 : RECOMMANDATIONS DYNAMIQUES
# ═══════════════════════════════════════════════════
elif page == "🎯 Recommandations":

    section_header("🎯 Recommandations & Plan d'Action", "Actions prioritaires basées sur l'analyse des données")

    # Récupérer TOUS les cycles disponibles (dynamique)
    cycles_disponibles = sorted(cycles_recap["cycle_id"].unique())
    nb_cycles = len(cycles_disponibles)
    
    # ============================================================
    # FONCTION POUR CALCULER LE SCORE D'UN CYCLE
    # ============================================================
    def calculer_score_cycle(c_data):
        """Calcule le score de performance pour un cycle donné"""
        
        # 1. Score de Rentabilité (30% du total)
        resultat = c_data["resultat_net_fcfa"]
        if resultat > 0:
            score_renta = 100
        elif resultat > -500000:
            score_renta = 50
        else:
            score_renta = 0
        
        # 2. Score de Mortalité (25% du total)
        mortalite = c_data["taux_mortalite_pct"]
        if mortalite <= 4:
            score_mortalite = 100
        elif mortalite <= 6:
            score_mortalite = 70
        elif mortalite <= 8:
            score_mortalite = 40
        else:
            score_mortalite = 0
        
        # 3. Score de Marge unitaire (20% du total)
        marge = c_data["marge_unitaire_fcfa"]
        if marge > 200:
            score_marge = 100
        elif marge > 0:
            score_marge = 60
        else:
            score_marge = 0
        
        # 4. Score de l'IC (Indice de Consommation) (15% du total)
        ic_val = c_data.get("ic_calcule", c_data.get("ic_standard", 1.7))
        if ic_val <= 1.7:
            score_ic = 100
        elif ic_val <= 1.9:
            score_ic = 70
        elif ic_val <= 2.1:
            score_ic = 40
        else:
            score_ic = 0
        
        # 5. Score du ROI (10% du total)
        roi_val = c_data.get("roi_pct", 0)
        if roi_val > 20:
            score_roi = 100
        elif roi_val > 0:
            score_roi = 60
        else:
            score_roi = 0
        
        # Calcul du score total (pondéré)
        score_total = (score_renta * 0.30) + (score_mortalite * 0.25) + (score_marge * 0.20) + (score_ic * 0.15) + (score_roi * 0.10)
        
        return {
            "total": round(score_total),
            "renta": score_renta,
            "mortalite": score_mortalite,
            "marge": score_marge,
            "ic": score_ic,
            "roi": score_roi
        }
    
    # ============================================================
    # CALCUL DES SCORES POUR TOUS LES CYCLES (UN SEUL BLOC)
    # ============================================================
    scores_cycles = {}
    cycles_data = {}
    for cycle in cycles_disponibles:
        c_data = cycles_recap[cycles_recap["cycle_id"] == cycle].iloc[0]
        scores_cycles[cycle] = calculer_score_cycle(c_data)
        cycles_data[cycle] = c_data

    # Définir le dernier cycle
    dernier_cycle = cycles_disponibles[-1]
    c_dernier = cycles_data[dernier_cycle]
    
    # ============================================================
    # AFFICHAGE DES SCORES PAR CYCLE (DYNAMIQUE)
    # ============================================================
    st.markdown("### 📊 Score de performance par cycle")
    
    # ============================================================
    # EXPLICATION DE LA MÉTHODE DE CALCUL (RÉSUMÉE)
    # ============================================================
    with st.expander("📖 Comment est calculé le score ?"):
        st.markdown("""
        | Indicateur | Pondération | Barème |
        |------------|-------------|--------|
        | Rentabilité | 30% | 100 si bénéfice, 50 si perte < 500k, 0 sinon |
        | Mortalité | 25% | 100 si ≤4%, 70 si ≤6%, 40 si ≤8%, 0 si >8% |
        | Marge unitaire | 20% | 100 si >200 FCFA, 60 si >0, 0 si négative |
        | IC | 15% | 100 si ≤1,7, 70 si ≤1,9, 40 si ≤2,1, 0 si >2,1 |
        | ROI | 10% | 100 si >20%, 60 si >0%, 0 si négatif |
        
        **Couleurs :** 🟢 ≥70 Excellent · 🟡 50-69 Bon · 🟠 30-49 Moyen · 🔴 <30 Critique
        """)
        
        

    # Déterminer le nombre de colonnes par ligne (max 4)
    cols_par_ligne = min(4, nb_cycles)
    
    # Afficher les scores ligne par ligne
    for i in range(0, nb_cycles, cols_par_ligne):
        cycles_ligne = cycles_disponibles[i:i+cols_par_ligne]
        cols = st.columns(len(cycles_ligne))
        
        for idx, cycle in enumerate(cycles_ligne):
            with cols[idx]:
                scores = scores_cycles[cycle]
                
                # Déterminer la couleur et le niveau
                if scores["total"] >= 70:
                    couleur = "#34d399"
                    emoji = "🟢"
                    niveau = "Excellent"
                elif scores["total"] >= 50:
                    couleur = "#fbbf24"
                    emoji = "🟡"
                    niveau = "Bon"
                elif scores["total"] >= 30:
                    couleur = "#f97316"
                    emoji = "🟠"
                    niveau = "Moyen"
                else:
                    couleur = "#f87171"
                    emoji = "🔴"
                    niveau = "Critique"
                
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur}; text-align:center;">
                    <div class="metric-label" style="font-size: 14px;">{emoji} {cycle}</div>
                    <div class="metric-value" style="font-size: 36px;">{scores['total']}</div>
                    <div class="metric-sub">/100 · {niveau}</div>
                </div>
                """, unsafe_allow_html=True)
    
    

    st.markdown("---")
    
    # === OPTIMISATION DU JOUR DE VENTE (AVEC PRIX LIÉ AU POIDS) ===
    with st.expander("📖 Comprendre l'analyse du jour optimal de vente"):
        st.markdown("""
        Cette analyse compare chaque jour :
        - **Dépenses cumulées** depuis le debut du cycle
        - **Valeur estimée du lot** (poids total × prix de vente au kg), avec un **prix qui augmente avec le poids**
        - **Mortalité réelle** (sujets morts)
        - **Sujets vendus** (si deja commence)

        Le **jour optimal** est celui où la **différence (valeur − dépenses) est maximale**.
        Vendre après ce jour réduit la marge.
        """)

    # Selection du cycle
    cycle_opt = st.selectbox("Choisir un cycle pour l'analyse", cycles_disponibles, key="opt_cycle")
    j_opt = journalier[journalier["cycle_id"] == cycle_opt].copy()
    c_opt = cycles_recap[cycles_recap["cycle_id"] == cycle_opt].iloc[0]

    if not j_opt.empty:

        # Parametres fixes
        prix_sac = 18000
        poids_sac = 50
        prix_kg_aliment = prix_sac / poids_sac

        # Modele de prix
        prix_au_kg_min = 1750
        prix_au_kg_max = 3500
        poids_min = 1.5
        poids_max = 2.0

        def prix_au_kg_en_fonction_poids(poids):
            if poids <= poids_min:
                return prix_au_kg_min
            elif poids >= poids_max:
                return prix_au_kg_max
            else:
                return prix_au_kg_min + (prix_au_kg_max - prix_au_kg_min) * (poids - poids_min) / (poids_max - poids_min)

        # Charges fixes quotidiennes
        duree_cycle = c_opt.get("duree_jours", 60)
        charges_fixes_totales = c_opt.get("cout_salaires_fcfa", 0) + c_opt.get("cout_loyer_fcfa", 0)
        charges_fixes_par_jour = charges_fixes_totales / duree_cycle if duree_cycle > 0 else 0

        # Couts initiaux
        couts_initiaux = (
            c_opt.get("cout_poussins_fcfa", 0) +
            c_opt.get("cout_medical_fcfa", 0) +
            c_opt.get("cout_litière_fcfa", 0) +
            c_opt.get("cout_transport_fcfa", 0)
        )

        # Interpolation du poids
        cycle_num = int(cycle_opt.replace("Cycle", "")) if cycle_opt.startswith("Cycle") else 0
        
        if cycle_num >= 4:
            pesees_opt = j_opt[j_opt["poids_g1"].notna()].copy()
            if not pesees_opt.empty:
                jour_poids = []
                for jour in pesees_opt["jour"].unique():
                    ligne = pesees_opt[pesees_opt["jour"] == jour].iloc[0]
                    poids_groupes = [ligne["poids_g1"], ligne["poids_g2"], ligne["poids_g3"], 
                                   ligne["poids_g4"], ligne["poids_g5"]]
                    poids_valides = [p for p in poids_groupes if pd.notna(p)]
                    if poids_valides:
                        jour_poids.append({"jour": jour, "poids": np.mean(poids_valides)})
                
                if len(jour_poids) >= 2:
                    df_poids = pd.DataFrame(jour_poids).sort_values("jour")
                    from scipy import interpolate
                    f_interp = interpolate.interp1d(
                        df_poids["jour"],
                        df_poids["poids"],
                        kind='linear',
                        fill_value='extrapolate'
                    )
                    j_opt["poids_estime"] = j_opt["jour"].apply(lambda x: float(f_interp(x)) if x >= df_poids["jour"].min() else None)
                else:
                    st.warning("Pas assez de pesées pour interpoler la croissance.")
                    st.stop()
            else:
                st.warning("Aucune donnée de poids disponible pour ce cycle.")
                st.stop()
        else:
            pesees_opt = j_opt[j_opt["poids_10plus"].notna()].copy()
            if len(pesees_opt) >= 2:
                from scipy import interpolate
                pesees_opt = pesees_opt.sort_values("jour")
                f_interp = interpolate.interp1d(
                    pesees_opt["jour"],
                    pesees_opt["poids_10plus"],
                    kind='linear',
                    fill_value='extrapolate'
                )
                j_opt["poids_estime"] = j_opt["jour"].apply(lambda x: float(f_interp(x)) if x >= pesees_opt["jour"].min() else None)
            else:
                st.warning("Pas assez de pesées pour interpoler la croissance.")
                st.stop()

        # Calcul des dépenses et valeur
        j_opt["sujets_restants"] = j_opt["effectif_restant"]
        j_opt["cout_aliment_jour"] = j_opt["conso_jour"] * prix_kg_aliment
        j_opt["charges_fixes_jour"] = charges_fixes_par_jour
        j_opt["dépenses_jour"] = j_opt["cout_aliment_jour"] + j_opt["charges_fixes_jour"]
        j_opt["depenses_cumulees"] = couts_initiaux + j_opt["dépenses_jour"].cumsum()
        
        j_opt["prix_au_kg"] = j_opt["poids_estime"].apply(prix_au_kg_en_fonction_poids)
        j_opt["prix_unitaire_estime"] = j_opt["poids_estime"] * j_opt["prix_au_kg"]
        j_opt["valeur_lot"] = j_opt["prix_unitaire_estime"] * j_opt["sujets_restants"]
        
        j_opt["diff_valeur_depenses"] = j_opt["valeur_lot"] - j_opt["depenses_cumulees"]
        j_opt["diff_valeur_depenses"] = j_opt["diff_valeur_depenses"].fillna(0)
        
        # Jour optimal
        df_valide = j_opt[j_opt["valeur_lot"].notna() & (j_opt["valeur_lot"] > 0)]
        if not df_valide.empty:
            idx_opt = df_valide["diff_valeur_depenses"].idxmax()
            jour_optimal = int(j_opt.loc[idx_opt, "jour"])
            diff_max = j_opt.loc[idx_opt, "diff_valeur_depenses"]
            valeur_opt = j_opt.loc[idx_opt, "valeur_lot"]
            depenses_opt = j_opt.loc[idx_opt, "depenses_cumulees"]
            sujets_restants_opt = j_opt.loc[idx_opt, "sujets_restants"]
            poids_opt = j_opt.loc[idx_opt, "poids_estime"]
            prix_au_kg_opt = j_opt.loc[idx_opt, "prix_au_kg"]
        else:
            jour_optimal = None
            diff_max = 0

        # Graphique
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["valeur_lot"],
            name="Valeur estimee du lot", mode="lines+markers",
            line=dict(color="#34d399", width=2)
        ))
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["depenses_cumulees"],
            name="Depenses cumulees", mode="lines+markers",
            line=dict(color="#f87171", width=2)
        ))
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["diff_valeur_depenses"],
            name="Marge (valeur − depenses)", mode="lines+markers",
            line=dict(color="#fbbf24", width=2.5, dash="dot")
        ))
        fig_opt.add_hline(y=0, line_dash="dot", line_color="#6b7280")
        
        if jour_optimal:
            fig_opt.add_vline(x=jour_optimal, line_dash="dash", line_color="#fbbf24",
                            annotation_text=f"Jour optimal : {jour_optimal}",
                            annotation_position="top right")

        fig_opt.update_layout(
            legend=dict(font=dict(color="#163F36", size=11))
        )
        plotly_light_layout(fig_opt, "Valeur du lot vs Depenses cumulees (prix lie au poids)", 450)
        fig_opt.update_yaxes(title_text="FCFA")
        fig_opt.update_xaxes(title_text="Jour du cycle")
        st.plotly_chart(fig_opt, use_container_width=True, key=f"graph_{cycle_opt}")

        # Resultat textuel
        with st.expander("📖 Resultat de l'analyse du jour optimal", expanded=False):
            if jour_optimal:
                st.markdown(f"""
                **Resultat pour le {cycle_opt} (avec prix lie au poids)** :
                - **Jour optimal de vente : J{jour_optimal}**
                - Poids estimé à J{jour_optimal} : **{poids_opt:.2f} kg**
                - Prix au kg à J{jour_optimal} : **{prix_au_kg_opt:.0f} FCFA**
                - Prix unitaire estimé : **{poids_opt * prix_au_kg_opt:.0f} FCFA**
                - Sujets restants : **{sujets_restants_opt:,.0f}** tetes
                - Valeur estimée du lot : **{valeur_opt/1e6:.2f} M FCFA**
                - Dépenses cumulées : **{depenses_opt/1e6:.2f} M FCFA**
                - Marge maximale : **{diff_max/1e6:.2f} M FCFA**
                
                **Interpretation** :  
                - Avant **J{jour_optimal}** : la valeur du lot augmente plus vite que les dépenses  
                - Après **J{jour_optimal}** : les dépenses supplémentaires ne sont plus rentabilisées  
                - **Vendre au plus tard a J{jour_optimal} pour maximiser la marge**
                """)
            else:
                st.markdown(f"""
                **Resultat pour le {cycle_opt}** :
                - Impossible de determiner un jour optimal
                - Vérifiez que les données de pesée et de mortalité sont completes
                """)

        # Simulation interactive
        st.markdown("---")
        st.markdown("<h4 style='color:#163F36;'>Simulation - Impact du jour de vente sur la marge</h4>", unsafe_allow_html=True)

        jour_min = int(j_opt["jour"].min())
        jour_max = int(j_opt["jour"].max())
        jour_defaut = jour_optimal if jour_optimal and jour_min <= jour_optimal <= jour_max else 40
        
        jour_sim = st.slider("Jour de vente simulé", jour_min, jour_max, jour_defaut, key="jour_sim")

        ligne_sim = j_opt[j_opt["jour"] == jour_sim]
        
        if not ligne_sim.empty:
            poids_sim = ligne_sim["poids_estime"].iloc[0] if "poids_estime" in ligne_sim.columns and pd.notna(ligne_sim["poids_estime"].iloc[0]) else None
            sujets_sim = ligne_sim["sujets_restants"].iloc[0] if "sujets_restants" in ligne_sim.columns and pd.notna(ligne_sim["sujets_restants"].iloc[0]) else None
            depenses_sim = ligne_sim["depenses_cumulees"].iloc[0] if "depenses_cumulees" in ligne_sim.columns and pd.notna(ligne_sim["depenses_cumulees"].iloc[0]) else None
            
            # Récupérer la marge au jour optimal pour comparaison
            marge_optimale = None
            if jour_optimal and jour_optimal in j_opt["jour"].values:
                ligne_opt = j_opt[j_opt["jour"] == jour_optimal].iloc[0]
                if "diff_valeur_depenses" in ligne_opt:
                    marge_optimale = ligne_opt["diff_valeur_depenses"]
            
            if poids_sim is not None and sujets_sim is not None and depenses_sim is not None and poids_sim > 0:
                
                # === NOUVELLE FONCTION DE PRIX BASÉE SUR LES VENTES RÉELLES ===
                def prix_unitaire_en_fonction_poids(poids):
                    """
                    Estimation du prix en fonction du poids
                    Basé sur les ventes réelles du Cycle 4:
                    - 1.90 kg → 2100 FCFA (J34)
                    - 2.08 kg → 2900 FCFA (J37)
                    - 2.15 kg → 3116 FCFA (J46)
                    """
                    if poids <= 1.5:
                        return 1800
                    elif poids <= 1.7:
                        return 2000
                    elif poids <= 1.9:
                        return 2200
                    elif poids <= 2.0:
                        return 2500
                    elif poids <= 2.1:
                        return 2800
                    elif poids <= 2.2:
                        return 3100
                    elif poids <= 2.3:
                        return 3300
                    else:
                        return 3500
                
                prix_unitaire_sim = prix_unitaire_en_fonction_poids(poids_sim)
                prix_au_kg_sim = prix_unitaire_sim / poids_sim if poids_sim > 0 else 0
                valeur_sim = prix_unitaire_sim * sujets_sim
                
                marge_sim = valeur_sim - depenses_sim
                marge_unitaire_sim = marge_sim / sujets_sim if sujets_sim > 0 else 0

                # Seuil de poids minimum pour vente
                POIDS_MIN_VENTE = 1.2
                
                if poids_sim >= POIDS_MIN_VENTE:
                    # Affichage des cartes
                    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                    
                    with col_r1:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#163F36; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Poids estimé</div>
                            <div class="metric-value" style="color: #1f2937;">{poids_sim:.2f} kg</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r2:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#163F36; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Prix unitaire estimé</div>
                            <div class="metric-value" style="color: #1f2937;">{prix_unitaire_sim:.0f} FCFA</div>
                            <div class="metric-sub" style="color: #4b5563;">({prix_au_kg_sim:.0f} FCFA/kg)</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r3:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#163F36; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Valeur estimée</div>
                            <div class="metric-value" style="color: #1f2937;">{valeur_sim/1e6:.2f} M FCFA</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r4:
                        if marge_sim >= 0:
                            couleur_accent = "#10b981"
                            couleur_fond = "#d1fae5"
                        else:
                            couleur_accent = "#ef4444"
                            couleur_fond = "#fee2e2"
                        
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:{couleur_accent}; background-color: {couleur_fond};">
                            <div class="metric-label" style="color: #1f2937;">Marge simulée</div>
                            <div class="metric-value" style="color: #1f2937;">{marge_sim:+,.0f} FCFA</div>
                            <div class="metric-sub" style="color: #4b5563;">{marge_unitaire_sim:+.0f} FCFA/sujet</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Message de comparaison avec le jour optimal
                    if jour_optimal and marge_optimale is not None:
                        if jour_sim < jour_optimal:
                            difference_marge = marge_optimale - marge_sim
                            st.markdown(f"""
                            <div style="color: #163F36; background-color: #fef3c7; padding: 12px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-top: 12px;">
                                ⏳ <strong>Vente anticipée</strong> : Vous vendez {jour_optimal - jour_sim} jours avant le jour optimal.<br>
                                💰 En attendant J{jour_optimal}, vous pourriez gagner <strong>{difference_marge:+,.0f} FCFA</strong> supplémentaires.
                            </div>
                            """, unsafe_allow_html=True)
                        elif jour_sim > jour_optimal:
                            difference_marge = marge_sim - marge_optimale
                            st.markdown(f"""
                            <div style="color: #163F36; background-color: #fee2e2; padding: 12px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 12px;">
                                ⚠️ <strong>Vente tardive</strong> : Vous vendez {jour_sim - jour_optimal} jours après le jour optimal.<br>
                                📉 Vous perdez <strong>{difference_marge:+,.0f} FCFA</strong> par rapport à une vente au J{jour_optimal}.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="color: #163F36; background-color: #d1fae5; padding: 12px; border-radius: 10px; border-left: 4px solid #10b981; margin-top: 12px;">
                                ✅ <strong>Jour optimal</strong> : Vous vendez au moment idéal pour maximiser la marge.
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Message de rentabilité
                    if marge_sim > 0:
                        st.markdown(f"""
                        <div style="color: #163F36; background-color: #d1fae5; padding: 12px; border-radius: 10px; border-left: 4px solid #10b981; margin-top: 12px;">
                            ✅ En vendant au <strong>J{jour_sim}</strong> (poids {poids_sim:.2f} kg), le cycle est rentable.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="color: #163F36; background-color: #fee2e2; padding: 12px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 12px;">
                            ⚠️ En vendant au <strong>J{jour_sim}</strong> (poids {poids_sim:.2f} kg), le cycle reste déficitaire.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if poids_sim < 2.2:
                            st.markdown(f"""
                            <div style="color: #163F36; background-color: #fef3c7; padding: 12px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-top: 8px;">
                                💡 <strong>Ajustement possible</strong> : Attendez que le poids atteigne <strong>2.2 kg</strong> pour un meilleur prix (environ 3100 FCFA).
                            </div>
                            """, unsafe_allow_html=True)
                
                else:
                    # Poids insuffisant
                    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                    
                    with col_r1:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#f59e0b; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Poids estimé</div>
                            <div class="metric-value" style="color: #1f2937;">{poids_sim:.2f} kg</div>
                            <div class="metric-sub" style="color: #4b5563;">(< {POIDS_MIN_VENTE} kg)</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r2:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#6b7280; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Prix unitaire estimé</div>
                            <div class="metric-value" style="color: #1f2937;">N/A</div>
                            <div class="metric-sub" style="color: #4b5563;">poids insuffisant</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r3:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#6b7280; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Valeur estimée</div>
                            <div class="metric-value" style="color: #1f2937;">N/A</div>
                            <div class="metric-sub" style="color: #4b5563;">poids insuffisant</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_r4:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#6b7280; background-color: #F4E8D8;">
                            <div class="metric-label" style="color: #1f2937;">Marge simulée</div>
                            <div class="metric-value" style="color: #1f2937;">N/A</div>
                            <div class="metric-sub" style="color: #4b5563;">vendre à partir de {POIDS_MIN_VENTE} kg</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if jour_optimal and jour_optimal > jour_sim:
                        st.info(f"⏳ Poids insuffisant ({poids_sim:.2f} kg). Le jour optimal estimé est J{jour_optimal}. Attendez que les poulets grandissent.")
                    else:
                        st.info(f"⏳ Poids insuffisant ({poids_sim:.2f} kg). Attendez que les poulets atteignent au moins {POIDS_MIN_VENTE} kg.")
            
            else:
                st.warning(f"⚠️ Données insuffisantes pour le jour {jour_sim}.")
        else:
            st.info("Données insuffisantes pour la simulation.")
    else:
        st.info("Donnees insuffisantes pour ce cycle.")

    # ============================================================
    # PLAN D'ACTION DÉTAILLÉ (style unifié)
    # ============================================================
    st.markdown('<div class="section-header">Plan d\'action détaillé</div>', unsafe_allow_html=True)

    # Onglets
    tab_urg, tab_surv, tab_forts = st.tabs(["URGENTES", "À SURVEILLER", "POINTS FORTS"])

    # ============================================================
    # ONGLET 1 : URGENTES
    # ============================================================
    with tab_urg:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #f87171; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                À traiter immédiatement
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        urgence_cards = []
        
        cycles_marge_negative = [cycle for cycle, data in cycles_data.items() if data["marge_unitaire_fcfa"] < 0]
        if cycles_marge_negative:
            urgence_cards.append({
                "titre": "Marge unitaire négative",
                "contenu": f"Cycles concernés : {', '.join(cycles_marge_negative)}",
                "action": "Objectif : atteindre 200 FCFA par sujet",
                "proposition": "Augmenter le prix de vente de 250 FCFA ou réduire le coût alimentaire de 10%",
                "cycle": ", ".join(cycles_marge_negative)
            })
        
        # 2. Prix de vente trop bas (dernier cycle vs meilleur)
        if len(cycles_disponibles) >= 2:
            # Extraire les valeurs numériques correctement
            meilleur_cycle, meilleur_data = max(cycles_data.items(), key=lambda x: x[1]["prix_moyen_fcfa"])
            meilleur_prix = float(meilleur_data["prix_moyen_fcfa"]) if hasattr(meilleur_data["prix_moyen_fcfa"], 'item') else meilleur_data["prix_moyen_fcfa"]
            dernier_prix = float(c_dernier["prix_moyen_fcfa"]) if hasattr(c_dernier["prix_moyen_fcfa"], 'item') else c_dernier["prix_moyen_fcfa"]
            
            if dernier_prix < meilleur_prix - 100:
                urgence_cards.append({
                    "titre": "Prix de vente en baisse",
                    "contenu": f"Dernier cycle : {dernier_prix:.0f} FCFA (max: {meilleur_prix:.0f} FCFA sur {meilleur_cycle})",
                    "action": "Augmenter de 250 à 300 FCFA",
                    "proposition": "Diversifier les circuits de vente et vendre pendant les périodes de fête",
                    "cycle": dernier_cycle
                })
        
        for cycle, data in cycles_data.items():
            if data["depenses_totales_fcfa"] > 0:
                part_aliment = (data["cout_aliment_fcfa"] / data["depenses_totales_fcfa"]) * 100
                if part_aliment > 50:
                    urgence_cards.append({
                        "titre": f"Coût alimentaire trop élevé ({cycle})",
                        "contenu": f"L'aliment représente {part_aliment:.1f}% des charges",
                        "action": "Négocier le prix des sacs, réduire le gaspillage",
                        "proposition": "Comparer les fournisseurs, acheter en plus grande quantité",
                        "cycle": cycle
                    })
                    break
        
        for cycle, data in cycles_data.items():
            if data["taux_mortalite_pct"] > 6:
                urgence_cards.append({
                    "titre": f"Mortalité élevée ({cycle})",
                    "contenu": f"Taux de mortalité : {data['taux_mortalite_pct']:.1f}%",
                    "action": "Revoir les protocoles sanitaires et la régulation température",
                    "proposition": "Renforcer la biosécurité et améliorer le contrôle climatique",
                    "cycle": cycle
                })
                break
        
        for cycle, data in cycles_data.items():
            if data["effectif_initial"] > 0:
                taux_reliquat = (data["effectif_final"] / data["effectif_initial"]) * 100
                if taux_reliquat > 5:
                    urgence_cards.append({
                        "titre": f"Reliquat non vendu ({cycle})",
                        "contenu": f"{data['effectif_final']} sujets non vendus ({taux_reliquat:.1f}%)",
                        "action": "Vendre en plus petits lots en fin de cycle",
                        "proposition": "Proposer une remise sur les derniers lots",
                        "cycle": cycle
                    })
                    break
        
        if urgence_cards:
            for car in urgence_cards[:6]:
                st.markdown(f"""
                <div class="metric-card" style="--accent:#f87171; background: #F4E8D8; margin-bottom: 12px;">
                    <div class="metric-label" style="color: #163F36;">{car['titre']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px;">{car['contenu']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px; font-weight: 500; font-size: 13px">Action : {car['action']}</div>
                    <div class="metric-sub" style="color: #E2B75F; margin-top: 6px; font-size: 13px">Proposition : {car['proposition']}</div>
                    <div class="metric-sub" style="color: #6b7280; margin-top: 6px; font-size: 10px;">Cycle(s) concerné(s) : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Aucune urgence détectée.")

    # ============================================================
    # ONGLET 2 : À SURVEILLER
    # ============================================================
    with tab_surv:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #fbbf24; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                Surveillance reguliere
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        surveillance_cards = []
        
        if len(cycles_disponibles) >= 3:
            prix_list = [(cycle, data["prix_moyen_fcfa"]) for cycle, data in cycles_data.items()]
            if prix_list[0][1] > prix_list[1][1] > prix_list[2][1]:
                surveillance_cards.append({
                    "titre": "Prix de vente en baisse constante",
                    "contenu": "Tendance à la baisse sur les derniers cycles",
                    "action": "Inverser la tendance, cibler 2 700-2 800 FCFA",
                    "proposition": "Fixer un prix plancher et diversifier les acheteurs",
                    "cycle": "Tous"
                })
        
        for cycle, data in cycles_data.items():
            ventes_cycle = ventes[ventes["cycle_id"] == cycle]
            if not ventes_cycle.empty:
                premier_vente = ventes_cycle["jour"].min()
                if premier_vente > 38:
                    surveillance_cards.append({
                        "titre": f"Premier jour de vente tardif ({cycle})",
                        "contenu": f"Première vente : J{premier_vente}",
                        "action": "Anticiper les ventes avant J40",
                        "proposition": "Démarcher les acheteurs dès le jour 30",
                        "cycle": cycle
                    })
                    break
        
        for cycle, data in cycles_data.items():
            if data["volume_vendu"] < 3000 and data["depenses_totales_fcfa"] > 0:
                part_fixes = (data.get("cout_salaires_fcfa", 0) + data.get("cout_loyer_fcfa", 0)) / data["depenses_totales_fcfa"] * 100
                if part_fixes > 25:
                    surveillance_cards.append({
                        "titre": f"Charges fixes lourdes ({cycle})",
                        "contenu": f"Volume : {data['volume_vendu']} sujets, charges fixes : {part_fixes:.0f}%",
                        "action": "Augmenter la taille des cycles",
                        "proposition": "Passer à 5 000-6 000 sujets par cycle",
                        "cycle": cycle
                    })
                    break
        
        for cycle, data in cycles_data.items():
            ic_val = data.get("ic_calcule", data.get("ic_standard", 1.7))
            if ic_val > 1.7:
                surveillance_cards.append({
                    "titre": f"IC à surveiller ({cycle})",
                    "contenu": f"IC = {ic_val:.2f} (cible ≤ 1,7)",
                    "action": "Améliorer l'efficacité alimentaire",
                    "proposition": "Ajuster les phases de croissance",
                    "cycle": cycle
                })
                break
        
        if surveillance_cards:
            for car in surveillance_cards[:5]:
                st.markdown(f"""
                <div class="metric-card" style="--accent:#fbbf24; background: #F4E8D8; margin-bottom: 12px;">
                    <div class="metric-label" style="color: #163F36;">{car['titre']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px;">{car['contenu']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px; font-weight: 500; font-size: 13px">Action : {car['action']}</div>
                    <div class="metric-sub" style="color: #E2B75F; margin-top: 6px; font-size: 13px">Proposition : {car['proposition']}</div>
                    <div class="metric-sub" style="color: #6b7280; margin-top: 6px; font-size: 10px;">Cycle concerne : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun point de vigilance particulier.")

    # ============================================================
    # ONGLET 3 : POINTS FORTS
    # ============================================================
    with tab_forts:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #34d399; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                À capitaliser
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        points_forts = []
        
        meilleur_prix_cycle = max(cycles_data.items(), key=lambda x: x[1]["prix_moyen_fcfa"])
        if meilleur_prix_cycle[1]["prix_moyen_fcfa"] > 2700:
            points_forts.append({
                "titre": "Meilleur prix de vente",
                "contenu": f"{meilleur_prix_cycle[0]} : {meilleur_prix_cycle[1]['prix_moyen_fcfa']:.0f} FCFA par sujet",
                "action": "Objectif à atteindre pour les autres cycles",
                "proposition": "Reproduire la stratégie commerciale de ce cycle",
                "cycle": meilleur_prix_cycle[0]
            })
        
        meilleur_cout_cycle = min(cycles_data.items(), key=lambda x: x[1]["depenses_totales_fcfa"] / x[1]["volume_vendu"] if x[1]["volume_vendu"] > 0 else float('inf'))
        if meilleur_cout_cycle[1]["volume_vendu"] > 0:
            cout_revient = meilleur_cout_cycle[1]["depenses_totales_fcfa"] / meilleur_cout_cycle[1]["volume_vendu"]
            points_forts.append({
                "titre": "Meilleur coût de revient",
                "contenu": f"{meilleur_cout_cycle[0]} : {cout_revient:.0f} FCFA par sujet",
                "action": "Applicable aux autres cycles",
                "proposition": "Appliquer les pratiques de ce cycle (alimentation, densité, suivi sanitaire)",
                "cycle": meilleur_cout_cycle[0]
            })
        
        meilleur_ic_cycle = min(cycles_data.items(), key=lambda x: x[1].get("ic_calcule", x[1].get("ic_standard", 10)))
        ic_val = meilleur_ic_cycle[1].get("ic_calcule", meilleur_ic_cycle[1].get("ic_standard", 0))
        if ic_val <= 1.7:
            points_forts.append({
                "titre": "Indice de consommation maîtrisé",
                "contenu": f"{meilleur_ic_cycle[0]} : IC = {ic_val:.2f}",
                "action": "Maintenir cette efficacité alimentaire",
                "proposition": "Garder le même fournisseur d'aliment et les mêmes phases",
                "cycle": meilleur_ic_cycle[0]
            })
        
        meilleur_mortalite_cycle = min(cycles_data.items(), key=lambda x: x[1]["taux_mortalite_pct"])
        if meilleur_mortalite_cycle[1]["taux_mortalite_pct"] <= 4:
            points_forts.append({
                "titre": "Mortalité maîtrisée",
                "contenu": f"{meilleur_mortalite_cycle[0]} : {meilleur_mortalite_cycle[1]['taux_mortalite_pct']:.2f}%",
                "action": "Maintenir la biosécurité",
                "proposition": "Continuer les protocoles de vaccination",
                "cycle": meilleur_mortalite_cycle[0]
            })
        
        if len(cycles_disponibles) >= 2:
            premier_cycle = cycles_disponibles[0]
            dernier_cycle_vol = cycles_disponibles[-1]
            vol_premier = cycles_data[premier_cycle]["volume_vendu"]
            vol_dernier = cycles_data[dernier_cycle_vol]["volume_vendu"]
            if vol_dernier > vol_premier * 2:
                points_forts.append({
                    "titre": "Montée en volume réussie",
                    "contenu": f"Multiplication par {vol_dernier/vol_premier:.1f} entre {premier_cycle} et {dernier_cycle_vol}",
                    "action": "Capacité opérationnelle prouvée",
                    "proposition": "Capitaliser sur cette expérience",
                    "cycle": f"{premier_cycle}→{dernier_cycle_vol}"
                })
        
        if points_forts:
            for car in points_forts:
                st.markdown(f"""
                <div class="metric-card" style="--accent:#34d399; background: #F4E8D8; margin-bottom: 12px;">
                    <div class="metric-label" style="color: #163F36;">{car['titre']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px;">{car['contenu']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px; font-weight: 500; font-size: 13px">Action : {car['action']}</div>
                    <div class="metric-sub" style="color: #E2B75F; margin-top: 6px; font-size: 13px">Proposition : {car['proposition']}</div>
                    <div class="metric-sub" style="color: #6b7280; margin-top: 6px; font-size: 10px;">Cycle concerne : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Capitalisez sur vos succès pour les cycles futurs.")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px; padding:20px 0; border-top:1px solid #1e2230; text-align:center;
     font-size:11px; color:#374151; letter-spacing:0.06em; text-transform:uppercase;'>
    Dashboard Avicole INIS · Diagnostic Financier · Poulets de Chair
</div>
""", unsafe_allow_html=True)