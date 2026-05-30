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
COLORS = {
    "Cycle1": "#163F36",
    "Cycle2": "#E2B75F",
    "Cycle3": "#D4A373",
}
ACCENT = ["#4e7cff", "#a78bfa", "#34d399", "#fbbf24", "#f87171"]
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
GRID_COLOR = "#1e2230"
TEXT_COLOR = "#9ca3af"
FONT_FAMILY = "DM Sans, sans-serif"

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
    <div style='font-size:11px;color:#4b5563;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px'>Totaux 3 cycles</div>

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
        <p>Exploitation Poulets de Chair · 3 Cycles · Diagnostic Financier Complet</p>
    </div>
    """, unsafe_allow_html=True)

    # KPIs row 1
    cols = st.columns(3)
    total_ca  = cr["ca_fcfa"].sum()
    total_dep = cr["depenses_totales_fcfa"].sum()
    total_res = cr["resultat_net_fcfa"].sum()
    total_vol = cr["volume_vendu"].sum()

    
    with cols[0]:
        st.markdown(card("Effectif Vendu", f"{total_vol:,} têtes", "3 cycles cumulés", "#a78bfa"), unsafe_allow_html=True)
    
    

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
            <div class="metric-sub">objectif 1.7</div>
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
                    
                    color = COLORS.get(cid, "#163F36")
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

    # Calcul de l'homogénéité à partir des données du cycle sélectionné
    # Calcul de l'homogénéité
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
            <div class="metric-label">📉 Indice de consommation (IC)</div>
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
                    nb_pics = len(v)
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
                        <div class="metric-label" style="font-size: 16px;">📊 Évolution de l'effectif restant</div>
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
                        <div class="metric-label" style="font-size: 16px;">🔗 Relation entre les courbes</div>
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
                        <div class="metric-label" style="font-size: 16px;">📊 Consommation journalière (barres)</div>
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
                        <div class="metric-label" style="font-size: 16px;">🔗 Analyse de la performance</div>
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
                        <div class="metric-label" style="font-size: 16px;">📈 Consommation cumulée (courbe)</div>
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
                            <div class="metric-label" style="font-size: 16px;">⚠️ Point d'attention</div>
                            <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                                • Pic de consommation anormalement élevé<br>
                                • Vérifier la cohérence des données de saisie
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif conso_totale > 0:
                        st.markdown(f"""
                        <div class="metric-card" style="--accent:#34d399;">
                            <div class="metric-label" style="font-size: 16px;">✅ Synthèse</div>
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

            # Préparer les données de pesée
            pesees_graph = j[j["poids_10plus"].notna() | j["poids_10moins"].notna()].copy()
            pesees_graph = pesees_graph.sort_values("jour")

            if not pesees_graph.empty:
                # Poids des plus lourds (rendu légèrement plus discret/fin si besoin)
                fig_p.add_trace(go.Scatter(
                    x=pesees_graph["jour"], 
                    y=pesees_graph["poids_10plus"],
                    name=">10% poids", 
                    mode="lines+markers",
                    line=dict(color="#34d399", width=2.0), # Légèrement affiné pour faire ressortir le standard
                    marker=dict(size=6, symbol="circle", color="#34d399"),
                    connectgaps=True
                ))
                
                # Poids des plus faibles (rendu légèrement plus discret/fin si besoin)
                fig_p.add_trace(go.Scatter(
                    x=pesees_graph["jour"], 
                    y=pesees_graph["poids_10moins"],
                    name="<10% poids", 
                    mode="lines+markers",
                    line=dict(color="#f87171", width=2.0), # Légèrement affiné
                    marker=dict(size=6, symbol="circle", color="#f87171"),
                    connectgaps=False
                ))
                
                # Poids standard -> MIS EN VALEUR
                pesees_std = j[j["poids_standard"].notna()].copy()
                if not pesees_std.empty:
                    fig_p.add_trace(go.Scatter(
                        x=pesees_std["jour"], 
                        y=pesees_std["poids_standard"],
                        name="Standard", 
                        mode="lines+markers",
                        # Ligne continue, plus épaisse et couleur contrastée (Bleu nuit/Noir)
                        line=dict(color="#1e293b", width=3.0, shape="linear"), 
                        marker=dict(size=10, symbol="diamond", color="#1e293b")
                    ))
                
                # Forcer l'affichage de tous les points en étendant l'axe X
                fig_p.update_xaxes(range=[0, pesees_graph["jour"].max() + 2])

            # Configuration du graphique
            plotly_light_layout(fig_p, "Évolution des Poids lors des Contrôles (kg)", 340)
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
            fig_p.update_yaxes(title_text="Poids moyen (kg)")

            st.plotly_chart(fig_p, use_container_width=True)
            
            # ============================================================
            # INTERPRÉTATIONS DYNAMIQUES AVEC RÉFÉRENCES
            # ============================================================
            with st.expander("📖 Interprétations", expanded=False):
                
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
                    # Conteneur 3 : Gain de poids quotidien AVEC RÉFÉRENCE
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
                            • <span style="color: #6b7280; font-size: 11px;">{reference_gain}</span><br>
                            • Période : du J{jour_debut if jour_debut else '?'} au J{dernier_jour if dernier_jour else '?'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Synthèse et recommandation
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
                nb_ventes = len(v_cycle)
                
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
                        <div class="metric-label" style="font-size: 16px;">📊 Statistiques des prix</div>
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
                        <div class="metric-label" style="font-size: 16px;">📊 Statistiques des prix</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • Aucune donnée de vente disponible
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Conteneur 2 : Niveau de prix et référence
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_prix};">
                    <div class="metric-label" style="font-size: 16px;">💰 Niveau de prix</div>
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
                    <div class="metric-label" style="font-size: 16px;">📈 Tendance des prix</div>
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
                    <div class="metric-label" style="font-size: 16px;">✅ Synthèse</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {synthese}<br>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")
    
    # Graphique : Volume Vendu Cumulé
    st.markdown("<span style='font-size:22px; font-weight:600;'>📦 Volume Vendu Cumulé</span>", unsafe_allow_html=True)
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
                nb_jours_vente = len(v_cycle)
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
                
                for _, row in v_cycle.iterrows():
                    if jour_pallier_25 is None and row["qte_cum"] >= pallier_25:
                        jour_pallier_25 = row["jour"]
                    if jour_pallier_50 is None and row["qte_cum"] >= pallier_50:
                        jour_pallier_50 = row["jour"]
                    if jour_pallier_75 is None and row["qte_cum"] >= pallier_75:
                        jour_pallier_75 = row["jour"]
                
                # Évaluation de la vitesse de vente
                if premier_vente <= 38:
                    vitesse_vente = " Démarrage précoce (avant J40)"
                    couleur_vitesse = "#34d399"
                else:
                    vitesse_vente = f"Démarrage tardif (J{premier_vente})"
                    couleur_vitesse = "#f87171"
                
                # Évaluation de l'étalement
                if duree_etalement <= 7:
                    etalement_texte = " Ventes concentrées (logistique optimisée)"
                    couleur_etalement = "#34d399"
                elif duree_etalement <= 10:
                    etalement_texte = f"Étalement correct ({duree_etalement} jours)"
                    couleur_etalement = "#E2B75F"
                else:
                    etalement_texte = f"Ventes très étalées ({duree_etalement} jours)"
                    couleur_etalement = "#f87171"
                
                # Évaluation de la pente
                if pente > 30:
                    pente_texte = f"Ventes rapides ({pente:.0f} sujets/jour)"
                    couleur_pente = "#34d399"
                elif pente > 15:
                    pente_texte = f"Ventes correctes ({pente:.0f} sujets/jour)"
                    couleur_pente = "#E2B75F"
                else:
                    pente_texte = f"Ventes lentes ({pente:.0f} sujets/jour)"
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
                etalement_texte = "Données insuffisantes"
                pente_texte = "Données insuffisantes"
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
                
                # Conteneur 2 : Rythme des ventes
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_vitesse};">
                    <div class="metric-label" style="font-size: 16px;">⏱️ Rythme des ventes</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {vitesse_vente}<br>
                        • {pente_texte}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Conteneur 3 : Étalement des ventes
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_etalement};">
                    <div class="metric-label" style="font-size: 16px;">📅 Étalement des ventes</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        • {etalement_texte}<br>
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
        
        # Définition des postes d'exploitation
        categories = [
            "Aliment", 
            "Poussins", 
            "Médical", 
            "Litière", 
            "Transport", 
            "Salaires", 
            "Loyer", 
            "Eau/Élec"
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
            c_fin["cout_eau_elec_fcfa"] if not pd.isna(c_fin["cout_eau_elec_fcfa"]) else 0
        ]
        
        # Créer un graphique à barres simple
        fig_depenses = go.Figure()
        fig_depenses.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color="#E2B75F",
            text=[f"{v/1e6:.2f} M" for v in valeurs],
            textposition="outside",
            hovertemplate="%{x}<br>%{y:,.0f} FCFA<extra></extra>"
        ))
        
        # Calculer le total des dépenses
        total_depenses = c_fin["depenses_totales_fcfa"]
        if hasattr(total_depenses, 'iloc'):
            total_depenses = total_depenses.iloc[0]
        
        plotly_light_layout(fig_depenses, f"Dépenses d'exploitation - {cycle_finance} (total : {total_depenses/1e6:.2f} M FCFA)", height=450)
        fig_depenses.update_xaxes(tickangle=-30)
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
            # Répartition par type (variables vs fixes)
            variables = c_fin["cout_aliment_fcfa"] + c_fin["cout_poussins_fcfa"] + c_fin["cout_medical_fcfa"] + c_fin["cout_litiere_fcfa"] + c_fin["cout_transport_fcfa"]
            fixes = c_fin["cout_salaires_fcfa"] + c_fin["cout_loyer_fcfa"] + c_fin["cout_eau_elec_fcfa"]
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
                    <div class="metric-label" style="font-size: 16px;">📊 Structure des coûts</div>
                    <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                        {texte_structure}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Conteneur 2 : Analyse aliment AVEC RÉFÉRENCE
                st.markdown(f"""
                <div class="metric-card" style="--accent:{couleur_aliment};">
                    <div class="metric-label" style="font-size: 16px;">🍗 Poste alimentaire</div>
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
                    <div class="metric-label" style="font-size: 16px;">🏢 Charges fixes</div>
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
                    <div class="metric-label" style="font-size: 16px;">✅ Synthèse</div>
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

    # Carte récapitulative centrée
    total_inv = cycles_recap["investissements_globaux_fcfa"].sum()
    st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <div class="metric-card" style="--accent:#E2B75F; margin-top: 10px; text-align: center; width: 100%; max-width: 500px;">
            <div class="metric-label" style="text-align: center;">📊 Total investissements (cycles 1 à 3)</div>
            <div class="metric-value" style="text-align: center;">{total_inv/1e6:.2f} M FCFA</div>
            <div class="metric-sub" style="text-align: center;">1,26 M identifiés sur Cycle 3</div>
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
                jour_max_cout = cout_total_jour.idxmax() + 1 if not cout_total_jour.empty else 0
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
                
                # === PART DE L'ALIMENT (sécurisée) AVEC RÉFÉRENCE ===
                if cout_total_jour.sum() > 0 and cout_total_jour.mean() > 0:
                    part_aliment_jour = (cout_aliment_jour / cout_total_jour).mean() * 100
                    
                    # Référence : < 45% = maîtrisé
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
                        <div class="metric-label" style="font-size: 16px;">📊 Statistiques du coût journalier</div>
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
                        <div class="metric-label" style="font-size: 16px;">📈 Progression du coût</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_progression}<br>
                            • Début cycle : {debut:,.0f} FCFA/jour → Fin cycle : {fin:,.0f} FCFA/jour
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Part de l'aliment AVEC RÉFÉRENCE
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_aliment};">
                        <div class="metric-label" style="font-size: 16px;">🍗 Part de l'aliment</div>
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
                        <div class="metric-label" style="font-size: 16px;">✅ Synthèse</div>
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
                        <div class="metric-label" style="font-size: 16px;">📊 Coûts finaux</div>
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
                        <div class="metric-label" style="font-size: 16px;">🎯 Seuil de rentabilité</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_seuil}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Conteneur 3 : Marge par sujet
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:{couleur_marge};">
                        <div class="metric-label" style="font-size: 16px;">💰 Marge par sujet</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {texte_marge}<br>
                            • Prix de vente moyen : {prix_vente_moyen:,.0f} FCFA/sujet
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Conteneur 4 : Synthèse
                    if marge_sujet > 0:
                        synthese = " Cycle rentable → maintenir les bonnes pratiques"
                    elif marge_sujet < 0 and abs(marge_sujet) < 100:
                        synthese = "Cycle quasi à l'équilibre → petit ajustement nécessaire"
                    elif marge_sujet < 0:
                        synthese = "Cycle déficitaire → priorité : augmenter le prix ou réduire les coûts"
                    else:
                        synthese = "Analyse des coûts disponible pour ce cycle"
                    
                    st.markdown(f"""
                    <div class="metric-card" style="--accent:#D4A373;">
                        <div class="metric-label" style="font-size: 16px;">✅ Synthèse</div>
                        <div class="metric-sub" style="margin-top: 10px; font-size: 13px; line-height: 1.6;">
                            • {synthese}<br>
                            • Objectif : marge ≥ 200 FCFA/sujet
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
                <div class="metric-label">💰 Coût poussins (total)</div>
                <div class="metric-value">{cout_poussins_total:,.0f} FCFA</div>
                <div class="metric-sub">Achat initial</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="--accent:#E2B75F">
                <div class="metric-label">🍗 Coût aliment total</div>
                <div class="metric-value">{cout_aliment_par_jour.sum():,.0f} FCFA</div>
                <div class="metric-sub">Consommation du cycle</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card" style="--accent:#D4A373">
                <div class="metric-label">📊 Coût total cumulé</div>
                <div class="metric-value">{cout_total_cumule.iloc[-1]:,.0f} FCFA</div>
                <div class="metric-sub">Poussins + aliment</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            # Couleur selon la marge (vert si coût < prix de vente, rouge sinon)
            prix_vente_moyen = c_fin.get("prix_moyen_fcfa", 0)
            if hasattr(prix_vente_moyen, 'iloc'):
                prix_vente_moyen = prix_vente_moyen.iloc[0]
            
            cout_final = cout_par_sujet.iloc[-1]
            if prix_vente_moyen > 0 and cout_final < prix_vente_moyen:
                couleur_cout = "#34d399"  # vert
                sous_texte = "Bon niveau"
            elif prix_vente_moyen > 0 and cout_final > prix_vente_moyen:
                couleur_cout = "#f87171"  # rouge
                sous_texte = "À améliorer"
            else:
                couleur_cout = "#D4A373"
                sous_texte = "Référence"
            
            st.markdown(f"""
            <div class="metric-card" style="--accent:{couleur_cout}">
                <div class="metric-label">🐔 Coût par sujet (final)</div>
                <div class="metric-value">{cout_final:,.0f} FCFA</div>
                <div class="metric-sub">{sous_texte}</div>
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

    


    # 1. Total investissements (somme des 3 cycles)
    total_invest = cycles_recap["investissements_globaux_fcfa"].sum()
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

    section_header("⚖️ Bilan Comparatif", "Comparaison des performances entre les 3 cycles")

    col_r1, col_r2 = st.columns(2)

    # ============================================================
    # COMPARAISON DES CYCLES - 5 PARAMÈTRES CLÉS
    # ============================================================
    st.markdown("### 📊 Comparaison des cycles par paramètre")

    # Récupérer les données des 3 cycles
    c1 = cycles_recap[cycles_recap["cycle_id"] == "Cycle1"].iloc[0]
    c2 = cycles_recap[cycles_recap["cycle_id"] == "Cycle2"].iloc[0]
    c3 = cycles_recap[cycles_recap["cycle_id"] == "Cycle3"].iloc[0]

    # Calculer les indicateurs supplémentaires
    cout_par_sujet_c1 = c1["depenses_totales_fcfa"] / c1["volume_vendu"] if c1["volume_vendu"] > 0 else 0
    cout_par_sujet_c2 = c2["depenses_totales_fcfa"] / c2["volume_vendu"] if c2["volume_vendu"] > 0 else 0
    cout_par_sujet_c3 = c3["depenses_totales_fcfa"] / c3["volume_vendu"] if c3["volume_vendu"] > 0 else 0

    # Durée des ventes (étalement)
    ventes1 = ventes[ventes["cycle_id"] == "Cycle1"]
    ventes2 = ventes[ventes["cycle_id"] == "Cycle2"]
    ventes3 = ventes[ventes["cycle_id"] == "Cycle3"]

    duree_ventes_c1 = ventes1["jour"].max() - ventes1["jour"].min() if not ventes1.empty else 0
    duree_ventes_c2 = ventes2["jour"].max() - ventes2["jour"].min() if not ventes2.empty else 0
    duree_ventes_c3 = ventes3["jour"].max() - ventes3["jour"].min() if not ventes3.empty else 0

    # ROI
    roi_c1 = c1.get("roi_pct", 0)
    roi_c2 = c2.get("roi_pct", 0)
    roi_c3 = c3.get("roi_pct", 0)

    # IC
    ic_c1 = c1.get("ic_calcule", c1.get("ic_standard", 1.7))
    ic_c2 = c2.get("ic_calcule", c2.get("ic_standard", 1.7))
    ic_c3 = c3.get("ic_calcule", c3.get("ic_standard", 1.7))

    # Poids final
    poids_c1 = c1["poids_final_kg"]
    poids_c2 = c2["poids_final_kg"]
    poids_c3 = c3["poids_final_kg"]

    # ============================================================
    # FONCTION POUR CLASSER LES CYCLES
    # ============================================================
    def classer_cycles(valeurs, cycles, plus_est_mieux):
        items = list(zip(cycles, valeurs))
        if plus_est_mieux:
            items.sort(key=lambda x: x[1], reverse=True)
        else:
            items.sort(key=lambda x: x[1])
        
        return {
            "meilleur": items[0][0],
            "moyen": items[1][0],
            "mediocre": items[2][0]
        }

    # ============================================================
    # GRAPHIQUE 1 : ROI
    # ============================================================
    st.markdown("#### 📈 1. Retour sur Investissement (ROI)")
    afficher_roi = st.checkbox("", value=True, key="check_roi")

    if afficher_roi:
        roi_values = [roi_c1, roi_c2, roi_c3]
        roi_classement = classer_cycles(roi_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=True)

        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=["Cycle1", "Cycle2", "Cycle3"],
            y=roi_values,
            marker_color=["#163F36", "#E2B75F", "#D4A373"],
            text=[f"{v:+.1f}%" for v in roi_values],
            textposition="outside"
        ))
        fig1.add_hline(y=0, line_dash="dot", line_color="#f87171")
        plotly_light_layout(fig1, "ROI par cycle", height=350)
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander("📖 Interprétation du ROI"):
            st.markdown(f"""
            - **Meilleur cycle** : {roi_classement["meilleur"]} ({max(roi_values):+.1f}%)
            - **Cycle moyen** : {roi_classement["moyen"]}
            - **Cycle médiocre** : {roi_classement["mediocre"]} ({min(roi_values):+.1f}%)
            
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
        ic_values = [ic_c1, ic_c2, ic_c3]
        ic_classement = classer_cycles(ic_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=False)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=["Cycle1", "Cycle2", "Cycle3"],
            y=ic_values,
            marker_color=["#163F36", "#E2B75F", "#D4A373"],
            text=[f"{v:.2f}" for v in ic_values],
            textposition="outside"
        ))
        fig2.add_hline(y=1.7, line_dash="dash", line_color="#34d399", annotation_text="Objectif 1.7")
        plotly_light_layout(fig2, "Indice de consommation (IC) par cycle", height=350)
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("📖 Interprétation de l'IC"):
            st.markdown(f"""
            - **Meilleur cycle (IC le plus bas)** : {ic_classement["meilleur"]} ({min(ic_values):.2f})
            - **Cycle moyen** : {ic_classement["moyen"]}
            - **Cycle médiocre (IC le plus élevé)** : {ic_classement["mediocre"]} ({max(ic_values):.2f})
            
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
        poids_values = [poids_c1, poids_c2, poids_c3]
        poids_classement = classer_cycles(poids_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=["Cycle1", "Cycle2", "Cycle3"],
            y=poids_values,
            marker_color=["#163F36", "#E2B75F", "#D4A373"],
            text=[f"{v:.2f} kg" for v in poids_values],
            textposition="outside"
        ))
        fig3.add_hline(y=2.0, line_dash="dash", line_color="#34d399", annotation_text="Objectif 2.0 kg")
        plotly_light_layout(fig3, "Poids final moyen par cycle", height=350)
        st.plotly_chart(fig3, use_container_width=True)
        
        with st.expander("📖 Interprétation du poids final"):
            st.markdown(f"""
            - **Meilleur cycle (poids le plus élevé)** : {poids_classement["meilleur"]} ({max(poids_values):.2f} kg)
            - **Cycle moyen** : {poids_classement["moyen"]}
            - **Cycle médiocre (poids le plus faible)** : {poids_classement["mediocre"]} ({min(poids_values):.2f} kg)
            
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
        cout_values = [cout_par_sujet_c1, cout_par_sujet_c2, cout_par_sujet_c3]
        cout_classement = classer_cycles(cout_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=False)

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=["Cycle1", "Cycle2", "Cycle3"],
            y=cout_values,
            marker_color=["#163F36", "#E2B75F", "#D4A373"],
            text=[f"{v:,.0f} FCFA" for v in cout_values],
            textposition="outside"
        ))
        plotly_light_layout(fig4, "Coût par sujet (poulet produit)", height=350)
        st.plotly_chart(fig4, use_container_width=True)
        
        with st.expander("📖 Interprétation du coût par sujet"):
            st.markdown(f"""
            - **Meilleur cycle (coût le plus bas)** : {cout_classement["meilleur"]} ({min(cout_values):,.0f} FCFA)
            - **Cycle moyen**: {cout_classement["moyen"]}
            - **Cycle médiocre (coût le plus élevé)** : {cout_classement["mediocre"]} ({max(cout_values):,.0f} FCFA)
            
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
        duree_values = [duree_ventes_c1, duree_ventes_c2, duree_ventes_c3]
        duree_classement = classer_cycles(duree_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=False)

        fig5 = go.Figure()
        fig5.add_trace(go.Bar(
            x=["Cycle1", "Cycle2", "Cycle3"],
            y=duree_values,
            marker_color=["#163F36", "#E2B75F", "#D4A373"],
            text=[f"{v:.0f} jours" for v in duree_values],
            textposition="outside"
        ))
        plotly_light_layout(fig5, "Étalement des ventes (première → dernière vente)", height=350)
        st.plotly_chart(fig5, use_container_width=True)
        
        with st.expander("📖 Interprétation de la durée des ventes"):
            st.markdown(f"""
            - **Meilleur cycle (ventes concentrées)** : {duree_classement["meilleur"]} ({min(duree_values):.0f} jours)
            - **Cycle moyen** : {duree_classement["moyen"]}
            - **Cycle médiocre (ventes trop étalées)** : {duree_classement["mediocre"]} ({max(duree_values):.0f} jours)
            
            Des ventes concentrées réduisent les coûts logistiques et améliorent la trésorerie.
            """)
    else:
        st.caption("Graphique Durée des ventes masqué")

    st.markdown("---")

    # Graphique : Prix moyen vs Prix de revient (pleine largeur) avec case à cocher
    st.markdown("<span style='font-size:22px; font-weight:600;'>💰 Prix moyen vs Prix de revient</span>", unsafe_allow_html=True)
    afficher_prix_revient = st.checkbox("", value=True, key="check_prix_revient")

    if afficher_prix_revient:
        prix_moy = [c1["prix_moyen_fcfa"], c2["prix_moyen_fcfa"], c3["prix_moyen_fcfa"]]
        prix_rev = [c1.get("prix_revient_unitaire", 0), c2.get("prix_revient_unitaire", 0), c3.get("prix_revient_unitaire", 0)]
        marge_u = [c1["marge_unitaire_fcfa"], c2["marge_unitaire_fcfa"], c3["marge_unitaire_fcfa"]]
        cycs_lbl = ["Cycle 1", "Cycle 2", "Cycle 3"]

        fig_pm = make_subplots(
            rows=2, cols=1, 
            subplot_titles=("Prix Moyen vs Prix de Revient (FCFA)", "Marge Unitaire (FCFA)"),
            vertical_spacing=0.18
        )
        
        fig_pm.add_trace(go.Scatter(
            x=cycs_lbl, y=prix_moy, 
            mode="lines+markers",
            name="Prix moyen", 
            line=dict(color="#4e7cff", width=2.5),
            marker=dict(size=10)
        ), row=1, col=1)
        
        fig_pm.add_trace(go.Scatter(
            x=cycs_lbl, y=prix_rev, 
            mode="lines+markers",
            name="Prix revient", 
            line=dict(color="#f87171", width=2.5, dash="dot"),
            marker=dict(size=10)
        ), row=1, col=1)
        
        colors_m = ["#34d399" if m >= 0 else "#f87171" for m in marge_u]
        fig_pm.add_trace(go.Bar(
            x=cycs_lbl, y=marge_u, 
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
        
        # Mise à jour des axes avec couleurs vert foncé
        fig_pm.update_xaxes(title_font=dict(color="#163F36"), tickfont=dict(color="#163F36"), gridcolor="#E2B75F")
        fig_pm.update_yaxes(title_font=dict(color="#163F36"), tickfont=dict(color="#163F36"), gridcolor="#E2B75F")
        
        st.plotly_chart(fig_pm, use_container_width=True)
        
        # ============================================================
        # INTERPRÉTATION
        # ============================================================
        with st.expander("📖 Interprétation du prix moyen vs prix de revient"):
            # Calcul du meilleur cycle pour la marge
            meilleur_marge = "Cycle1" if marge_u[0] == max(marge_u) else ("Cycle2" if marge_u[1] == max(marge_u) else "Cycle3")
            
            st.markdown(f"""
            - **Cycle avec la meilleure marge unitaire** : {meilleur_marge} ({max(marge_u):+.0f} FCFA/sujet)
            - **Prix de vente moyen le plus élevé** : Cycle1 (2 758 FCFA)
            - **Prix de revient le plus bas** : Cycle3 (2 843 FCFA)
            
            Un écart positif entre le prix de vente et le prix de revient indique une marge bénéficiaire.
            Plus cet écart est grand, plus le cycle est rentable.
            """)
    else:
        st.caption("Graphique masqué. Cochez la case pour l'afficher.")

    # ============================================================
# SYNTHÈSE GLOBALE (conteneur esthétique)
# ============================================================
    st.markdown("### 🎯 Synthèse globale")

    # Classement pour la marge unitaire
    marge_values = [c1["marge_unitaire_fcfa"], c2["marge_unitaire_fcfa"], c3["marge_unitaire_fcfa"]]
    marge_classement = classer_cycles(marge_values, ["Cycle1", "Cycle2", "Cycle3"], plus_est_mieux=True)

    # Compter les mentions "meilleur" par cycle (6 critères)
    compteur = {"Cycle1": 0, "Cycle2": 0, "Cycle3": 0}
    for classement in [roi_classement, ic_classement, poids_classement, cout_classement, duree_classement, marge_classement]:
        compteur[classement["meilleur"]] += 1

    meilleur_cycle = max(compteur, key=compteur.get)

    # Conteneur esthétique (carte) centrée
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <div class="metric-card" style="--accent:#D4A373; background: #F4E8D8; color: #163F36; text-align: center; max-width: 600px; width: 100%;">
            <div class="metric-label" style="color: #163F36; font-size: 14px;">🏆 CYCLE LE PLUS PERFORMANT</div>
            <div class="metric-value" style="color: #163F36; font-size: 28px;">{meilleur_cycle}</div>
            <div class="metric-sub" style="color: #163F36;">{compteur[meilleur_cycle]}/6 critères</div>
            <div style="margin-top: 15px; border-top: 1px solid #E2B75F; padding-top: 12px;">
                <div style="font-size: 13px; font-weight: 600; margin-bottom: 8px;">📊 DÉTAIL DES PERFORMANCES</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12px; text-align: left;">
                    <div>• ROI : <strong>{roi_classement["meilleur"]}</strong></div>
                    <div>• IC : <strong>{ic_classement["meilleur"]}</strong></div>
                    <div>• Poids final : <strong>{poids_classement["meilleur"]}</strong></div>
                    <div>• Coût par sujet : <strong>{cout_classement["meilleur"]}</strong></div>
                    <div>• Étalement des ventes : <strong>{duree_classement["meilleur"]}</strong></div>
                    <div>• Marge unitaire : <strong>{marge_classement["meilleur"]}</strong></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        

    # Tableau seuil rentabilité (gardé identique)
    st.markdown('<div class="section-header">Seuil de Rentabilité</div>', unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns(3)
    for col_w, (i, cid) in zip([col_s1,col_s2,col_s3], enumerate(CYCLES)):
        with col_w:
            c = cycles_recap.iloc[i]
            sr = c["seuil_rentabilite_fcfa"]
            ca = c["ca_fcfa"]
            pm_j = c["point_mort_jours"]
            color = COLORS.get(cid,"#4e7cff")
            if not pd.isna(sr):
                gap = ca - sr
                pct_couv = (ca/sr)*100 if sr != 0 else 0
                st.markdown(f"""
                <div class="metric-card" style="--accent:{color}">
                    <div class="metric-label">{cid} · Seuil de Rentabilité</div>
                    <div class="metric-value">{sr/1e6:.2f} M FCFA</div>
                    <div class="metric-sub">CA réalisé : {ca/1e6:.2f} M FCFA</div>
                    <div class="{'metric-delta-pos' if gap>=0 else 'metric-delta-neg'}" style='margin-top:8px'>
                        {"▲" if gap>=0 else "▼"} {abs(gap)/1e6:.2f} M par rapport au seuil · {pct_couv:.0f}% couvert
                    </div>
                    {"<div style='margin-top:8px;font-size:12px;color:#6b7280'>Point mort : <b style='color:#fbbf24'>"+str(round(pm_j,1))+" j</b> / durée cycle 53 j</div>" if not pd.isna(pm_j) else ""}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="--accent:{color}">
                    <div class="metric-label">{cid} · Seuil de Rentabilité</div>
                    <div class="metric-value">Non calculé</div>
                    <div class="metric-sub">Données insuffisantes pour C1/C2</div>
                </div>
                """, unsafe_allow_html=True)


        
        # ============================================================
        # 4. SYNTHÈSE FINALE
        # ============================================================
    st.markdown("---")
    st.markdown("### 🎯 Objectifs pour le Cycle 4")
        
    st.markdown("""
    | Indicateur | Objectif | Justification |
    |------------|----------|---------------|
    | Volume | 5 000 – 6 800 sujets | Diluer les charges fixes |
    | Prix de vente | ≥ 2 700 FCFA/sujet | Revenir au niveau du Cycle 1 |
    | Coût de revient | ≤ 2 500 FCFA/sujet | Maintenir les performances du Cycle 3 |
    | Marge unitaire | ≥ 200 FCFA/sujet | Atteindre la rentabilité |
    | IC | ≤ 1,7 | Maintenir l'efficacité alimentaire |
    | Mortalité | ≤ 4% | Maintenir la maîtrise sanitaire |
    """)
        
    

# ═══════════════════════════════════════════════════
# PAGE 5 : RECOMMANDATIONS DYNAMIQUES
# ═══════════════════════════════════════════════════
elif page == "🎯 Recommandations":

    section_header("🎯 Recommandations & Plan d'Action", "Actions prioritaires basées sur l'analyse des données")

    # Récupérer les données pour les 3 cycles
    c1 = cycles_recap.iloc[0]
    c2 = cycles_recap.iloc[1]
    c3 = cycles_recap.iloc[2]

    # Score global amélioré avec nos indicateurs
    scores = {
        "Rentabilité": 0 if c3["resultat_net_fcfa"] < 0 else 100,
        "Mortalité": max(0, 100 - int(c3["taux_mortalite_pct"] * 15)),
        "Indice Consommation": max(0, 100 - int((c3.get("ic_calcule", 2.0) - 1.6) * 50)) if c3.get("ic_calcule", 2.0) > 1.6 else 100,
        "Marge unitaire": 0 if c3["marge_unitaire_fcfa"] < 0 else 100,
        "ROI": round(max(0, 50 + c3.get("roi_pct", -100) * 2) if c3.get("roi_pct", -100) > -50 else 0, 2)    }
    score_global = int(sum(scores.values()) / len(scores))

    col_score, col_jauge = st.columns([1, 2])
    with col_score:
        color_score = "#34d399" if score_global >= 70 else ("#fbbf24" if score_global >= 45 else "#f87171")
        st.markdown(f"""
        <div class="metric-card" style="--accent:{color_score}; text-align:center; padding:36px 24px">
            <div class="metric-label">Score de Performance Global</div>
            <div style='font-family:Syne,sans-serif;font-size:64px;font-weight:800;color:{color_score};line-height:1'>{score_global}</div>
            <div style='font-size:18px;color:#6b7280;margin-top:4px'>/100</div>
            <div style='margin-top:16px;font-size:13px;color:#9ca3af'>
                {"🟢 Performance solide" if score_global>=70 else ("🟡 Amélioration possible" if score_global>=45 else "🔴 Action urgente nécessaire")}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_jauge:
        fig_sc = go.Figure(go.Bar(
            x=list(scores.values()), y=list(scores.keys()),
            orientation="h",
            marker=dict(color=[
                "#34d399" if v>=70 else ("#fbbf24" if v>=45 else "#f87171")
                for v in scores.values()
            ], line_width=0),
            text=[f"{v}/100" for v in scores.values()],
            textposition="outside",
            textfont=dict(size=12, color="#163F36")
        ))
        fig_sc.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family=FONT_FAMILY, color="#163F36"),
            height=220, margin=dict(l=12, r=60, t=20, b=12),
            xaxis=dict(range=[0,120], gridcolor=GRID_COLOR, showticklabels=False),
            yaxis=dict(
                gridcolor="rgba(0,0,0,0)",
                tickfont=dict(color="#163F36", size=12)  # ← AJOUT : couleur des noms (Rentabilité, etc.)
            ),
            title=dict(text="Décomposition du Score", font=dict(family="Syne", size=14, color="#163F36"))
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # === OPTIMISATION DU JOUR DE VENTE (AVEC PRIX LIÉ AU POIDS) ===
    with st.expander("Comprendre l'analyse du jour optimal de vente"):
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
    cycle_opt = st.selectbox("Choisir un cycle pour l'analyse", CYCLES, key="opt_cycle")
    j_opt = journalier[journalier["cycle_id"] == cycle_opt].copy()
    c_opt = cycles_recap[cycles_recap["cycle_id"] == cycle_opt].iloc[0]

    if not j_opt.empty:

        # Parametres fixes
        prix_sac = 18000
        poids_sac = 50
        prix_kg_aliment = prix_sac / poids_sac   # 360 FCFA/kg

        # Modele de prix : le prix au kg augmente avec le poids
        # Ajuster ces parametres selon le marche
        prix_au_kg_min = 1750      # Prix au kg pour un petit poulet (1.5 kg)
        prix_au_kg_max = 3500      # Prix au kg pour un gros poulet (2.5 kg)
        poids_min = 1.5
        poids_max = 2.0

        def prix_au_kg_en_fonction_poids(poids):
            """Calcule le prix au kg en fonction du poids (augmentation lineaire)"""
            if poids <= poids_min:
                return prix_au_kg_min
            elif poids >= poids_max:
                return prix_au_kg_max
            else:
                # Interpolation lineaire
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

        # Interpolation du poids entre les pesées
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
            st.warning("Pas assez de pesées pour interpoler la croissance. Ajoutez au moins 2 pesées par cycle.")
            st.stop()

        # === PRISE EN COMPTE DES PERTES REELLES ===
        j_opt["sujets_restants"] = j_opt["effectif_restant"]
        
        # Calcul des depenses cumulees
        j_opt["cout_aliment_jour"] = j_opt["conso_jour"] * prix_kg_aliment
        j_opt["charges_fixes_jour"] = charges_fixes_par_jour
        j_opt["dépenses_jour"] = j_opt["cout_aliment_jour"] + j_opt["charges_fixes_jour"]
        j_opt["depenses_cumulees"] = couts_initiaux + j_opt["dépenses_jour"].cumsum()
        
        # Valeur estimee du lot avec prix lie au poids
        j_opt["prix_au_kg"] = j_opt["poids_estime"].apply(prix_au_kg_en_fonction_poids)
        j_opt["prix_unitaire_estime"] = j_opt["poids_estime"] * j_opt["prix_au_kg"]
        j_opt["valeur_lot"] = j_opt["prix_unitaire_estime"] * j_opt["sujets_restants"]
        
        # Marge
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
            legend=dict(
                font=dict(color="#163F36", size=11)  # ← Légende en vert foncé
            )
        )
        plotly_light_layout(fig_opt, "Valeur du lot vs Depenses cumulees (prix lie au poids)", 450)
        fig_opt.update_yaxes(title_text="FCFA")
        fig_opt.update_xaxes(title_text="Jour du cycle")
        st.plotly_chart(fig_opt, use_container_width=True)

        # Resultat textuel
        with st.expander("Resultat de l'analyse du jour optimal", expanded=False):
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

        # Sélection du jour de vente (seulement)
        jour_sim = st.slider("Jour de vente simulé", int(j_opt["jour"].min()), int(j_opt["jour"].max()), jour_optimal if jour_optimal else 40, key="jour_sim")

        ligne_sim = j_opt[j_opt["jour"] == jour_sim]
        if not ligne_sim.empty:
            poids_sim = ligne_sim["poids_estime"].iloc[0]
            sujets_sim = ligne_sim["sujets_restants"].iloc[0]
            
            # Références de prix (prix unitaire total, pas au kg)
            prix_unitaire_min = 1500   # pour 1.0 kg (poids min pour vendre)
            prix_unitaire_max = 3500   # pour 2.5 kg (poids max pour vendre)
            poids_min = 1.0
            poids_max = 2.5
            
            def prix_unitaire_en_fonction_poids(poids):
                """Calcule le prix unitaire total en fonction du poids (interpolation linéaire)"""
                if poids <= poids_min:
                    return prix_unitaire_min
                elif poids >= poids_max:
                    return prix_unitaire_max
                else:
                    # Interpolation linéaire
                    return prix_unitaire_min + (prix_unitaire_max - prix_unitaire_min) * (poids - poids_min) / (poids_max - poids_min)
            
            prix_unitaire_sim = prix_unitaire_en_fonction_poids(poids_sim)
            prix_au_kg_sim = prix_unitaire_sim / poids_sim if poids_sim > 0 else 0
            valeur_sim = prix_unitaire_sim * sujets_sim
            
            depenses_sim = ligne_sim["depenses_cumulees"].iloc[0]
            marge_sim = valeur_sim - depenses_sim
            marge_unitaire_sim = marge_sim / sujets_sim if sujets_sim > 0 else 0

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
                    <div class="metric-label" style="color: #1f2937;">Prix unitaire</div>
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

            # Recommandation
            if marge_sim > 0:
                st.markdown(f"""
                <div style="color: #163F36; background-color: #d1fae5; padding: 12px; border-radius: 10px; border-left: 4px solid #10b981; margin-top: 12px;">
                    ✅ En vendant au <strong>J{jour_sim}</strong> (poids {poids_sim:.2f} kg, prix {prix_unitaire_sim:.0f} FCFA), le cycle est rentable.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="color: #163F36; background-color: #fee2e2; padding: 12px; border-radius: 10px; border-left: 4px solid #ef4444; margin-top: 12px;">
                    ⚠️ En vendant au <strong>J{jour_sim}</strong> (poids {poids_sim:.2f} kg, prix {prix_unitaire_sim:.0f} FCFA), le cycle reste déficitaire.
                </div>
                """, unsafe_allow_html=True)
                
                # Suggestion d'amélioration
                if prix_unitaire_sim < prix_unitaire_max:
                    st.markdown(f"""
                    <div style="color: #163F36; background-color: #fef3c7; padding: 12px; border-radius: 10px; border-left: 4px solid #f59e0b; margin-top: 8px;">
                        💡 <strong>Ajustement possible</strong> : Attendez que le poids atteigne <strong>{poids_max:.1f} kg</strong> pour un prix unitaire de {prix_unitaire_max:.0f} FCFA.
                    </div>
                    """, unsafe_allow_html=True)

        else:
            st.info("Données insuffisantes pour la simulation.")

    else:
        st.info("Donnees insuffisantes pour ce cycle.")

    # ============================================================
    # PLAN D'ACTION DÉTAILLÉ (style unifié)
    # ============================================================
    st.markdown('<div class="section-header">Plan d\'action détaillé</div>', unsafe_allow_html=True)

    # Récupérer les données des 3 cycles
    c1 = cycles_recap[cycles_recap["cycle_id"] == "Cycle1"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle1"]) > 0 else None
    c2 = cycles_recap[cycles_recap["cycle_id"] == "Cycle2"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle2"]) > 0 else None
    c3 = cycles_recap[cycles_recap["cycle_id"] == "Cycle3"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle3"]) > 0 else None

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
        
        # 1. Marge unitaire négative (tous cycles)
        if c1 is not None and c2 is not None and c3 is not None:
            urgence_cards.append({
                "titre": "Marge unitaire négative",
                "contenu": f"C1 : {c1['marge_unitaire_fcfa']:.0f} FCFA | C2 : {c2['marge_unitaire_fcfa']:.0f} FCFA | C3 : {c3['marge_unitaire_fcfa']:.0f} FCFA",
                "action": "Objectif : atteindre 200 FCFA par sujet pour tous les cycles",
                "proposition": "Augmenter le prix de vente de 250 FCFA ou réduire le coût alimentaire de 10 pour cent",
                "cycle": "Tous"
            })
        
        # 2. Prix de vente trop bas (Cycle 3)
        if c3 is not None and c1 is not None and c3['prix_moyen_fcfa'] < 2600:
            urgence_cards.append({
                "titre": "Prix de vente trop bas",
                "contenu": f"Cycle 3 : {c3['prix_moyen_fcfa']:.0f} FCFA (C1 : {c1['prix_moyen_fcfa']:.0f} FCFA)",
                "action": "Augmenter de 250 à 300 FCFA pour revenir au niveau du Cycle 1",
                "proposition": "Diversifier les circuits de vente (grossiste, detail, HORECA) et vendre pendant les periodes de fete",
                "cycle": "C3"
            })
        
        # 3. Coût alimentaire trop élevé (Cycle 3)
        if c3 is not None and c3['depenses_totales_fcfa'] > 0:
            part_aliment = (c3['cout_aliment_fcfa'] / c3['depenses_totales_fcfa']) * 100
            if part_aliment > 50:
                urgence_cards.append({
                    "titre": "Coût alimentaire trop élevé",
                    "contenu": f"Cycle 3 : l'aliment représente {part_aliment:.1f} pour cent des charges",
                    "action": "Négocier le prix des sacs (18 000 FCFA), réduire le gaspillage",
                    "proposition": "Comparer les prix chez GMD et NMA, acheter en plus grande quantite pour obtenir une remise, et installer des mangeoires anti-gaspillage",
                    "cycle": "C3"
                })
        
        # 4. Seuil de rentabilité non atteint (Cycle 3)
        if c3 is not None:
            seuil_c3 = c3.get('seuil_rentabilite_fcfa', 0)
            if seuil_c3 > 0 and c3['ca_fcfa'] < seuil_c3:
                couverture = (c3['ca_fcfa'] / seuil_c3) * 100
                urgence_cards.append({
                    "titre": "Seuil de rentabilité non atteint",
                    "contenu": f"Cycle 3 : CA = {c3['ca_fcfa']/1e6:.1f} M FCFA | Seuil = {seuil_c3/1e6:.1f} M FCFA ({couverture:.0f} pour cent)",
                    "action": "Augmenter le CA de 37 pour cent ou réduire les charges fixes",
                    "proposition": "Augmenter le volume à 6 800 sujets ou augmenter le prix de vente de 300 FCFA par sujet",
                    "cycle": "C3"
                })
        
        # 5. Point mort trop tardif (Cycle 3)
        if c3 is not None:
            point_mort = c3.get('point_mort_jours', 0)
            if point_mort > 53:
                urgence_cards.append({
                    "titre": "Point mort trop tardif",
                    "contenu": f"Cycle 3 : point mort à {point_mort:.0f} jours (cycle = 53 jours)",
                    "action": "Le cycle n'est jamais rentable → réduire les charges fixes",
                    "proposition": "Réduire les salaires ou le loyer, ou augmenter le volume à 6 000 sujets pour diluer les charges fixes",
                    "cycle": "C3"
                })
        
        # 6. Reliquat non vendu (C1 et C2)
        for cycle, nom in [(c1, "C1"), (c2, "C2")]:
            if cycle is not None and cycle['effectif_initial'] > 0:
                taux_reliquat = (cycle['effectif_final'] / cycle['effectif_initial']) * 100
                if taux_reliquat > 5:
                    urgence_cards.append({
                        "titre": f"Reliquat non vendu ({nom})",
                        "contenu": f"{cycle['effectif_final']} sujets non vendus ({taux_reliquat:.1f} pour cent)",
                        "action": "Vendre en plus petits lots en fin de cycle",
                        "proposition": "Proposer une remise de 5 pour cent sur les derniers lots ou contacter des acheteurs de proximite",
                        "cycle": nom
                    })
        
        # 7. Résultat net déficitaire (C2)
        if c2 is not None and c2['resultat_net_fcfa'] < 0:
            urgence_cards.append({
                "titre": "Résultat net très déficitaire",
                "contenu": f"Cycle 2 : {c2['resultat_net_fcfa']:,.0f} FCFA de perte",
                "action": "Revoir la stratégie commerciale et les coûts avant le prochain cycle",
                "proposition": "Augmenter le prix de vente de 200 FCFA et réduire le coût alimentaire de 5 pour cent",
                "cycle": "C2"
            })
        
        # Affichage des cartes (style unifié)
        if urgence_cards:
            for car in urgence_cards[:6]:
                st.markdown(f"""
                <div class="metric-card" style="--accent:#f87171; background: #F4E8D8; margin-bottom: 12px;">
                    <div class="metric-label" style="color: #163F36;">{car['titre']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px;">{car['contenu']}</div>
                    <div class="metric-sub" style="color: #163F36; margin-top: 8px; font-weight: 500; font-size: 13px">Action : {car['action']}</div>
                    <div class="metric-sub" style="color: #E2B75F; margin-top: 6px; font-size: 13px">Proposition : {car['proposition']}</div>
                    <div class="metric-sub" style="color: #6b7280; margin-top: 6px; font-size: 10px;">Cycle concerne : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("Aucune urgence détectee.")

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
        
        # 1. Prix en baisse constante
        if c1 is not None and c2 is not None and c3 is not None:
            if c1['prix_moyen_fcfa'] > c2['prix_moyen_fcfa'] > c3['prix_moyen_fcfa']:
                surveillance_cards.append({
                    "titre": "Prix de vente en baisse constante",
                    "contenu": f"C1: {c1['prix_moyen_fcfa']:.0f} → C2: {c2['prix_moyen_fcfa']:.0f} → C3: {c3['prix_moyen_fcfa']:.0f} FCFA",
                    "action": "Inverser la tendance, cibler 2 700-2 800 FCFA",
                    "proposition": "Fixer un prix plancher a 2 700 FCFA et diversifier les acheteurs",
                    "cycle": "Tous"
                })
        
        # 2. Premier jour de vente tardif
        for cycle, nom, jour_vente in [(c1, "C1", 34), (c2, "C2", 38), (c3, "C3", 36)]:
            if cycle is not None and jour_vente > 38:
                surveillance_cards.append({
                    "titre": f"Premier jour de vente tardif ({nom})",
                    "contenu": f"Première vente : J{jour_vente}",
                    "action": "Anticiper les ventes avant J40",
                    "proposition": "Demarcher les acheteurs des le jour 30 et proposer des pre-reservations",
                    "cycle": nom
                })
                break
        
        # 3. Charges fixes lourdes (C1 et C2)
        for cycle, nom in [(c1, "C1"), (c2, "C2")]:
            if cycle is not None and cycle['volume_vendu'] < 2000:
                part_fixes = (cycle.get('cout_salaires_fcfa', 0) + cycle.get('cout_loyer_fcfa', 0)) / cycle['depenses_totales_fcfa'] * 100 if cycle['depenses_totales_fcfa'] > 0 else 0
                if part_fixes > 30:
                    surveillance_cards.append({
                        "titre": f"Charges fixes lourdes ({nom})",
                        "contenu": f"Volume : {cycle['volume_vendu']} sujets, charges fixes : {part_fixes:.0f} pour cent",
                        "action": "Augmenter la taille des cycles (3 000-5 000 sujets)",
                        "proposition": "Passer a 3 000 ou 5 000 sujets par cycle pour diluer les charges fixes",
                        "cycle": nom
                    })
        
        # 4. Lot hétérogène (C3)
        if c3 is not None and c3['poids_final_kg'] > 0:
            df_c3 = journalier[journalier["cycle_id"] == "Cycle3"]
            poids_faible = df_c3[df_c3["poids_10moins"].notna()]["poids_10moins"].iloc[-1] if not df_c3[df_c3["poids_10moins"].notna()].empty else 0
            if poids_faible > 0:
                ecart = c3['poids_final_kg'] - poids_faible
                if ecart > 0.6:
                    surveillance_cards.append({
                        "titre": "Lot heterogene",
                        "contenu": f"Cycle 3 : écart de {ecart:.2f} kg entre plus lourds et plus faibles",
                        "action": "Trier les sujets par poids, ajuster la densité",
                        "proposition": "Installer des barrières de tri dans le poulailler et ajuster la densité à 12-15 sujets par metre carre",
                        "cycle": "C3"
                    })
        
        # 5. IC à surveiller (C3)
        if c3 is not None:
            ic_c3 = c3.get('ic_calcule', 0) or c3.get('ic_standard', 0)
            if ic_c3 > 1.7:
                surveillance_cards.append({
                    "titre": "Indice de consommation à surveiller",
                    "contenu": f"Cycle 3 : IC = {ic_c3:.2f} (cible ≤ 1,7)",
                    "action": "Améliorer l'efficacité alimentaire",
                    "proposition": "Changer de fournisseur d'aliment ou ajuster les phases de croissance",
                    "cycle": "C3"
                })
        
        # 6. Étalement des ventes (C3)
        surveillance_cards.append({
            "titre": "Eetalement des ventes",
            "contenu": "Cycle 3 : ventes étalées sur plusieurs jours",
            "action": "Regrouper les livraisons pour réduire les coûts de transport",
            "proposition": "Planifier des tournees de livraison fixes (mardi, jeudi, samedi) pour mutualiser les transports",
            "cycle": "C3"
        })
        
        # Affichage des cartes (style unifié)
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
        
        # 1. Meilleur prix (C1)
        if c1 is not None and c1['prix_moyen_fcfa'] > 2700:
            points_forts.append({
                "titre": "Meilleur prix de vente",
                "contenu": f"Cycle 1 : {c1['prix_moyen_fcfa']:.0f} FCFA par sujet",
                "action": "Objectif à atteindre pour les cycles suivants",
                "proposition": "Reproduire la strategie commerciale du Cycle 1 (clients, periode de vente)",
                "cycle": "C1"
            })
        
        # 2. Meilleur coût de revient (C3)
        if c3 is not None and c3['depenses_totales_fcfa'] > 0 and c3['volume_vendu'] > 0:
            cout_revient = c3['depenses_totales_fcfa'] / c3['volume_vendu']
            points_forts.append({
                "titre": "Meilleur coût de revient",
                "contenu": f"Cycle 3 : {cout_revient:.0f} FCFA par sujet",
                "action": "Applicable aux cycles 1 et 2",
                "proposition": "Appliquer les pratiques du Cycle 3 (alimentation, densite, suivi sanitaire) aux petits cycles",
                "cycle": "C3"
            })
        
        # 3. Montée en volume réussie
        if c1 is not None and c3 is not None and c3['volume_vendu'] > c1['volume_vendu'] * 4:
            points_forts.append({
                "titre": "Montee en volume réussie",
                "contenu": f"Multiplication par {c3['volume_vendu']/c1['volume_vendu']:.1f} entre C1 et C3",
                "action": "Capacité opérationnelle prouvée",
                "proposition": "Capitaliser sur cette experience pour passer a 6 000 ou 8 000 sujets",
                "cycle": "C1→C3"
            })
        
        # 4. IC maîtrisé (C3)
        if c3 is not None:
            ic_c3 = c3.get('ic_calcule', 0) or c3.get('ic_standard', 0)
            if ic_c3 <= 1.7:
                points_forts.append({
                    "titre": "Indice de consommation maîtrisé",
                    "contenu": f"Cycle 3 : IC = {ic_c3:.2f} (cible ≤ 1,7)",
                    "action": "Maintenir cette efficacité alimentaire",
                    "proposition": "Garder le meme fournisseur d'aliment et les memes phases de croissance",
                    "cycle": "C3"
                })
        
        # 5. Mortalité maîtrisée (C3)
        if c3 is not None and c3['taux_mortalite_pct'] <= 4:
            points_forts.append({
                "titre": "Mortalité maîtrisée",
                "contenu": f"Cycle 3 : {c3['taux_mortalite_pct']:.2f} pour cent",
                "action": "Maintenir la biosécurité",
                "proposition": "Continuer les protocoles de vaccination et le controle de temperature",
                "cycle": "C3"
            })
        
        # 6. Trésorerie disponible (C3)
        if c3 is not None:
            treso = c3.get('tresorerie_disponible_fcfa', 0)
            if treso > 0:
                points_forts.append({
                    "titre": "Trésorerie disponible",
                    "contenu": f"{treso/1e6:.1f} M FCFA",
                    "action": "Capacité à financer le Cycle 4",
                    "proposition": "Utiliser cette tresorerie pour acheter en gros (aliment, poussins) et obtenir des remises",
                    "cycle": "C3"
                })
        
        # 7. Reliquat nul (C2)
        if c2 is not None and c2['effectif_final'] == 0:
            points_forts.append({
                "titre": "Reliquat nul",
                "contenu": "Cycle 2 : tous les sujets ont été vendus",
                "action": "Bonne gestion commerciale à reproduire",
                "proposition": "Reproduire la strategie de vente du Cycle 2 (calendrier, prix, clients)",
                "cycle": "C2"
            })
        
        # Affichage des cartes (style unifié)
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
    Dashboard Avicole INIS · Diagnostic Financier 3 Cycles · Poulets de Chair
</div>
""", unsafe_allow_html=True)