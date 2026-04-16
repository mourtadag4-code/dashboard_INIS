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
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
            
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
            

/* Carte unique d'interprétation */
.interp-card {
    background: linear-gradient(135deg, #141720 0%, #1a1e2a 100%);
    border: 1px solid #242838;
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
    opacity: 0.06;
    pointer-events: none;
}
.interp-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #f0ece4;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid #242838;
}
.interp-card-content {
    font-size: 13px;
    color: #9ca3af;
    line-height: 1.7;
}
.interp-card-content strong {
    color: #fbbf24;
}
.interp-card-content ul {
    margin: 8px 0;
    padding-left: 20px;
}
.interp-card-content li {
    margin: 6px 0;
}

/* Fond global */
.stApp {
    background: #0d0f14;
    color: #e8e4dc;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid #1e2230;
}
[data-testid="stSidebar"] * {
    color: #c8c4bc !important;
}

/* Titres */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Cards métriques custom */
.metric-card {
    background: linear-gradient(135deg, #141720 0%, #1a1e2a 100%);
    border: 1px solid #242838;
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: #3d4a6e;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #4e7cff);
    border-radius: 16px 16px 0 0;
}
.metric-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: #f0ece4;
    line-height: 1.1;
}
.metric-sub {
    font-size: 12px;
    color: #6b7280;
    margin-top: 6px;
}
.metric-delta-pos { color: #34d399; font-size: 13px; font-weight: 500; }
.metric-delta-neg { color: #f87171; font-size: 13px; font-weight: 500; }

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #f0ece4;
    letter-spacing: -0.02em;
    margin: 32px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e2230;
}

/* Badge cycle */
.cycle-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.05em;
}

/* Reco cards */
.reco-card {
    border-radius: 12px;
    padding: 18px 20px;
    margin: 10px 0;
    border-left: 4px solid;
    background: #141720;
}
.reco-urgente  { border-color: #f87171; background: #1a1015; }
.reco-attention{ border-color: #fbbf24; background: #1a1810; }
.reco-positive { border-color: #34d399; background: #101a15; }
.reco-titre { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.reco-texte { font-size: 13px; color: #9ca3af; line-height: 1.6; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #141720 0%, #0f1520 50%, #141720 100%);
    border: 1px solid #1e2230;
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
    opacity: 0.15;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    color: #f0ece4 !important;
    margin: 0 !important;
    letter-spacing: -0.03em;
}
.hero p {
    color: #6b7280;
    font-size: 14px;
    margin-top: 8px;
}

/* Alert */
.alert-box {
    background: #1a1015;
    border: 1px solid #f87171;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 13px;
    color: #fca5a5;
}
.success-box {
    background: #101a15;
    border: 1px solid #34d399;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 13px;
    color: #6ee7b7;
}
            
/* ========== RESPONSIVE DESIGN ========== */

/* Grand écran (défaut) */
@media screen and (min-width: 1200px) {
    .metric-value {
        font-size: 26px !important;
    }
    .hero h1 {
        font-size: 32px !important;
    }
    .section-header {
        font-size: 22px !important;
    }
}

/* Écran moyen (tablette) */
@media screen and (max-width: 992px) {
    .metric-value {
        font-size: 20px !important;
    }
    .metric-card {
        padding: 16px 18px !important;
    }
    .hero {
        padding: 24px 28px !important;
    }
    .hero h1 {
        font-size: 26px !important;
    }
    .hero::after {
        font-size: 48px !important;
        right: 20px !important;
    }
    .section-header {
        font-size: 18px !important;
    }
    .reco-card {
        padding: 14px 16px !important;
    }
}

/* Petit écran (mobile) */
@media screen and (max-width: 768px) {
    .metric-value {
        font-size: 16px !important;
    }
    .metric-label {
        font-size: 9px !important;
    }
    .metric-sub {
        font-size: 9px !important;
    }
    .metric-card {
        padding: 12px 14px !important;
    }
    .hero {
        padding: 20px 24px !important;
    }
    .hero h1 {
        font-size: 20px !important;
    }
    .hero p {
        font-size: 11px !important;
    }
    .hero::after {
        font-size: 36px !important;
        right: 15px !important;
    }
    .section-header {
        font-size: 16px !important;
        margin: 20px 0 12px 0 !important;
    }
    .reco-titre {
        font-size: 12px !important;
    }
    .reco-texte {
        font-size: 11px !important;
    }
    .cycle-badge {
        font-size: 10px !important;
        padding: 2px 10px !important;
    }
    [data-testid="stSidebar"] {
        min-width: 200px !important;
    }
}

/* Très petit écran */
@media screen and (max-width: 480px) {
    .metric-value {
        font-size: 13px !important;
    }
    .metric-label {
        font-size: 8px !important;
    }
    .hero h1 {
        font-size: 16px !important;
    }
    .hero p {
        font-size: 9px !important;
    }
    .hero::after {
        font-size: 28px !important;
    }
    .section-header {
        font-size: 14px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PALETTES & CONSTANTES
# ─────────────────────────────────────────────
COLORS = {
    "Cycle1": "#4e7cff",
    "Cycle2": "#a78bfa",
    "Cycle3": "#34d399",
}
ACCENT = ["#4e7cff", "#a78bfa", "#34d399", "#fbbf24", "#f87171"]
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
GRID_COLOR = "#1e2230"
TEXT_COLOR = "#9ca3af"
FONT_FAMILY = "DM Sans, sans-serif"

def plotly_dark_layout(fig, title="", height=380, legend_orientation="v"):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=16, color="#f0ece4"), x=0, pad=dict(l=4)),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        height=height,
        margin=dict(l=12, r=12, t=44, b=12),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(size=11)),
        legend=dict(
            orientation=legend_orientation,
            yanchor="bottom" if legend_orientation == "h" else "top",
            y=1.02 if legend_orientation == "h" else 1,
            xanchor="center" if legend_orientation == "h" else "right",
            x=0.5 if legend_orientation == "h" else 1,
            bgcolor="rgba(20,23,32,0.8)",
            bordercolor="#242838",
            borderwidth=1,
            font=dict(size=11)
        )
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

# ─────────────────────────────────────────────
# FONCTIONS DE CALCUL
# ─────────────────────────────────────────────
def calculer_ic(row):
    """Calcule l'Indice de Consommation si possible"""
    if row.get("conso_totale_kg") and row.get("poids_final_kg") and row.get("volume_vendu"):
        poids_total = row["poids_final_kg"] * row["volume_vendu"]
        if poids_total > 0:
            return row["conso_totale_kg"] / poids_total
    return None

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
        ["🏠 Vue d'ensemble", "📊 Analyse par Cycle", "💰 Ventes & Prix", "⚖️ Bilan Comparatif", "🎯 Recommandations"],
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
    cols = st.columns(4)
    total_ca  = cr["ca_fcfa"].sum()
    total_dep = cr["depenses_totales_fcfa"].sum()
    total_res = cr["resultat_net_fcfa"].sum()
    total_vol = cr["volume_vendu"].sum()

    with cols[1]:
        st.markdown(card("CA Total", f"{total_ca/1e6:.2f} M FCFA", f"{len(selected_cycles)} cycles", "#4e7cff"), unsafe_allow_html=True)
    with cols[0]:
        st.markdown(card("Effectif Vendu", f"{total_vol:,} têtes", "3 cycles cumulés", "#a78bfa"), unsafe_allow_html=True)
    with cols[2]:
        st.markdown(card("Dépenses Totales", f"{total_dep/1e6:.2f} M FCFA", "Charges visibles", "#fbbf24"), unsafe_allow_html=True)
    with cols[3]:
        color = "#34d399" if total_res >= 0 else "#f87171"
        sign = "+" if total_res >= 0 else ""
        st.markdown(card("Résultat Net", f"{sign}{total_res/1e6:.2f} M FCFA", "Cumulé", color), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # KPIs row 2 - Indicateurs clés par cycle
    col_a, col_b, col_c, col_d = st.columns(4)
    
    # Mortalité moyenne
    mort_moy = cr["taux_mortalite_pct"].mean()
    with col_d:
        st.markdown(card("Mortalité Moy.", f"{mort_moy:.1f}%", "Tous cycles", "#f87171" if mort_moy > 4 else "#34d399"), unsafe_allow_html=True)
    
    # IC moyen (calculé)
    ic_moy = cr["ic_calcule"].mean()
    with col_b:
        color_ic = "#34d399" if ic_moy <= 1.7 else ("#fbbf24" if ic_moy <= 1.9 else "#f87171")
        st.markdown(card("IC Moyen", f"{ic_moy:.2f}", "Indice consommation", color_ic), unsafe_allow_html=True)
    
    # ROI global
    roi_global = (total_res / total_dep) * 100 if total_dep > 0 else 0
    with col_c:
        color_roi = "#34d399" if roi_global >= 0 else "#f87171"
        st.markdown(card("ROI Global", f"{roi_global:+.1f}%", "Retour sur invest.", color_roi), unsafe_allow_html=True)
    
    # Prix de revient moyen
    prix_revient_moy = cr["prix_revient_unitaire"].mean()
    prix_moyen = cr["prix_moyen_fcfa"].mean()
    delta_marge = prix_moyen - prix_revient_moy
    with col_a:
        color_delta = "#34d399" if delta_marge >= 0 else "#f87171"
        st.markdown(card("Marge nette/sujet", f"{delta_marge:+.0f} FCFA", f"Prix: {prix_moyen:.0f} / Revient: {prix_revient_moy:.0f}", color_delta), unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    # Graphiques overview
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # CA vs Dépenses vs Résultat par cycle
        fig = go.Figure()
        cycs = cr["cycle_id"].tolist()
        ca_vals  = cr["ca_fcfa"].tolist()
        dep_vals = cr["depenses_totales_fcfa"].tolist()
        res_vals = cr["resultat_net_fcfa"].tolist()

        fig.add_trace(go.Bar(name="CA", x=cycs, y=ca_vals,
                             marker_color="#0145ff",
                             marker_line_width=0, opacity=0.9))
        fig.add_trace(go.Bar(name="Dépenses", x=cycs, y=dep_vals,
                             marker_color="#374151", marker_line_width=0, opacity=0.9))
        fig.add_trace(go.Scatter(name="Résultat Net", x=cycs, y=res_vals,
                                 mode="lines+markers",
                                 line=dict(color="#fbbf24", width=2.5, dash="dot"),
                                 marker=dict(size=9, symbol="diamond")))
        fig.update_layout(barmode="group")
        plotly_dark_layout(fig, "CA · Dépenses · Résultat par Cycle", height=340)
        st.plotly_chart(fig, use_container_width=True)
    
    # Résultat net des cycles
    with col_right:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=cr["cycle_id"],
            y=cr["resultat_net_fcfa"],
            marker_color=["#4e7cff", "#a78bfa", "#34d399"],
            text=cr["resultat_net_fcfa"].apply(lambda x: f"{x:+,.0f}"),
            textposition="outside"
        ))
        fig2.add_hline(y=0, line_color="#f87171", line_dash="dash")
        plotly_dark_layout(fig2, "Résultat Net par Cycle", height=340)
        fig2.update_yaxes(title_text="FCFA")
        st.plotly_chart(fig2, use_container_width=True)

    # Évolution effectifs & mortalité
    st.markdown('<div class="section-header">📈 Dynamique des Effectifs</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        fig3 = go.Figure()
        for cid in selected_cycles:
            j = jf[jf["cycle_id"] == cid]
            color = COLORS.get(cid, "#4e7cff")
            
            # Convertir hex en rgb
            hex_color = color.lstrip('#')
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            rgba_color = f"rgba({r}, {g}, {b}, 0.15)"
            
            fig3.add_trace(go.Scatter(
                x=j["jour"], y=j["effectif_restant"],
                name=cid, mode="lines",
                line=dict(color=color, width=2),
                fill="tozeroy",
                fillcolor=rgba_color,
                hovertemplate=f"<b>{cid}</b> J%{{x}}<br>Effectif : %{{y:,}}<extra></extra>"
            ))
        plotly_dark_layout(fig3, "Évolution de l'Effectif Restant (jour par jour)", height=300)
        fig3.update_xaxes(title_text="Jour du cycle")
        fig3.update_yaxes(title_text="Têtes")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        fig4 = go.Figure()
        for cid in selected_cycles:
            j = jf[jf["cycle_id"] == cid]
            fig4.add_trace(go.Scatter(
                x=j["jour"], y=j["mortalite_cumulee"],
                name=cid, mode="lines",
                line=dict(color=COLORS.get(cid, "#fff"), width=2),
                hovertemplate=f"<b>{cid}</b> J%{{x}}<br>Morts cumulés : %{{y}}<extra></extra>"
            ))
        plotly_dark_layout(fig4, "Mortalité Cumulée par Cycle", height=300)
        fig4.update_xaxes(title_text="Jour du cycle")
        fig4.update_yaxes(title_text="Morts cumulés")
        st.plotly_chart(fig4, use_container_width=True)



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

    # KPIs cycle avec nos indicateurs
    # Première ligne : 7 indicateurs
    cols = st.columns(5)

    # Calcul des indicateurs
    roi = c.get("roi_pct", 0)
    ic_val = c.get("ic_calcule", 0)
    prix_revient = c.get("prix_revient_unitaire", 0)
    marge_nette = c.get("marge_unitaire_fcfa", 0)  # Résultat net / volume

    metrics = [
        ("Effectif Initial", f"{c['effectif_initial']:,}", "têtes", color),
        ("Effectif Vendu", f"{c['volume_vendu']:,}", "têtes", "#34d399"),
        ("Chiffre d'Affaire (CA)", f"{c['ca_fcfa']/1e6:.2f} M", "FCFA", color),
        ("Dépenses totales", f"{c['depenses_totales_fcfa']/1e6:.2f} M", "FCFA", "#fbbf24"),
        ("Dépenses total", f"{prix_revient:,.0f}", "FCFA/sujet", "#a78bfa"),
        
        
    ]

    for col_w, (lbl, val, sub, acc) in zip(cols, metrics):
        with col_w:
            st.markdown(card(lbl, val, sub, acc), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Deuxième ligne : 3 indicateurs (mortalité, IC, ROI)
    cols2 = st.columns(5)

    metrics2 = [
        ("Résultat Net", f"{c['resultat_net_fcfa']:+,.0f}", "FCFA", "#34d399" if c['resultat_net_fcfa']>=0 else "#f87171"),
        ("Marge Nette/sujet", f"{marge_nette:+.0f}", "FCFA/sujet", "#34d399" if marge_nette >= 0 else "#f87171"),
        ("Mortalité", f"{c['taux_mortalite_pct']:.2f}%", f"{c['mortalite_totale']:.0f} têtes", "#f87171" if c['taux_mortalite_pct']>4 else "#34d399"),
        ("Indice de Consommation (IC)", f"{ic_val:.2f}", "kg consommé / kg produit", "#fbbf24" if ic_val <= 1.9 else "#f87171"),
        ("ROI (Retour sur Invest.)", f"{roi:+.1f}%", "Résultat / Dépenses", "#34d399" if roi >= 0 else "#f87171"),
        
    ]

    for col_w, (lbl, val, sub, acc) in zip(cols2, metrics2):
        with col_w:
            st.markdown(card(lbl, val, sub, acc), unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


    # Graphiques détaillés
    tab1, tab2, tab3 = st.tabs(["📈 Journalier", "🥩 Pesées & Poids", "💸 Finances"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Effectif + ventes
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=j["jour"], y=j["effectif_restant"], name="Effectif restant",
                                     line=dict(color=color, width=2), fill="tozeroy",
                                     fillcolor=hex_to_rgba(color, 0.15)), secondary_y=False)
            if not v.empty:
                fig.add_trace(go.Bar(x=v["jour"], y=v["quantite"], name="Ventes/jour",
                                     marker_color="#fbbf24", opacity=0.7), secondary_y=True)
            plotly_dark_layout(fig, "Effectif & Ventes Journalières", 320)
            fig.update_yaxes(title_text="Effectif", secondary_y=False, gridcolor=GRID_COLOR)
            fig.update_yaxes(title_text="Qté vendue", secondary_y=True, showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Consommation journalière
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=j["jour"], y=j["conso_jour"], name="Conso/jour",
                                  marker_color=color, opacity=0.8))
            fig2.add_trace(go.Scatter(x=j["jour"], y=j["conso_cumulee"], name="Conso cumulée",
                                      line=dict(color="#fbbf24", width=2), yaxis="y2"))
            plotly_dark_layout(fig2, "Consommation Aliment (kg/jour)", 320)
            fig2.update_layout(yaxis2=dict(overlaying="y", side="right", showgrid=False,
                                           tickfont=dict(size=10), color=TEXT_COLOR))
            st.plotly_chart(fig2, use_container_width=True)

        # Morts journaliers
        fig3 = go.Figure()
        # Barres de mortalité
        fig3.add_trace(go.Bar(x=j["jour"], y=j["morts_jour"],
                            marker_color="#f87171", opacity=0.85, 
                            name="Morts/jour"))
        
        # Filtrer les actions (exclure Nettoyage si tu veux)
        actions = j[j["action"].notna()].copy()
        
        if not actions.empty:
            # Définir les couleurs par type d'action
            action_colors = {
                "Vaccin": "#34d399",
                "Changement alimentation": "#fbbf24",
                "Control pesée": "#60a5fa"
            }
            
            def get_action_color(action):
                for key, color in action_colors.items():
                    if key in action:
                        return color
                return "#f87171"
            
            actions["color"] = actions["action"].apply(get_action_color)
            
            # Ajouter chaque type d'événement avec sa couleur
            for action_type in actions["action"].unique():
                df_action = actions[actions["action"] == action_type]
                color = get_action_color(action_type)
                
                fig3.add_trace(go.Scatter(
                    x=df_action["jour"], 
                    y=df_action["morts_jour"] + 0.5,
                    mode="markers",
                    marker=dict(color=color, size=10, symbol="star"),
                    name=action_type,
                    hovertemplate=f"<b>{action_type}</b><br>Jour %{{x}}<extra></extra>"
                ))
        
        # Configuration de la légende
        plotly_dark_layout(fig3, "Mortalité Journalière & Événements Clés", 280)
        fig3.update_layout(
            legend=dict(
                orientation="h",           # Légende horizontale
                yanchor="top",             # Ancrage en haut de la légende
                y=-0.25,                   # Position sous le graphique (négatif = en bas)
                xanchor="center",          # Centrée horizontalement
                x=0.5,                     # Position centrée
                bgcolor="rgba(20,23,32,0.8)",
                bordercolor="#242838",
                borderwidth=1,
                font=dict(size=9)
            ),
            margin=dict(b=60)              # Augmente la marge du bas pour accueillir la légende
        )
        st.plotly_chart(fig3, use_container_width=True)

        # === INTERPRÉTATIONS ET RECOMMANDATIONS - JOURNALIER ===
        st.markdown("---")

        # Vérifier que les données existent
        if not j.empty and not v.empty:
            
            # Construction du texte HTML
            texte_html = ""
            
            # 1. PREMIER JOUR DE VENTE
            jours_vente = v["jour"].unique()
            if len(jours_vente) > 0:
                premier_vente = min(jours_vente)
                
                if premier_vente <= 38:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Premier jour de vente</strong><br>
                    ✅ J{premier_vente} — Bon rythme, vente précoce<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce rythme de vente précoce<br><br>
                    """
                elif premier_vente <= 42:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Premier jour de vente</strong><br>
                    ⚠️ J{premier_vente} — Acceptable, mais pourrait être amélioré<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Anticiper la commercialisation de 2-3 jours<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Premier jour de vente</strong><br>
                    ❌ J{premier_vente} — Trop tardif, risque de perte de marge<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Contacter les acheteurs plus tôt, prospecter avant la fin du cycle<br><br>
                    """
            
            # 2. PIC DE MORTALITÉ
            max_morts = j["morts_jour"].max() if not j.empty else 0
            effectif_init = j["effectif_restant"].iloc[0] if not j.empty else 1
            seuil_mortalite_5 = effectif_init * 0.05
            seuil_mortalite_10 = effectif_init * 0.10
            
            if max_morts > seuil_mortalite_10:
                jour_max = j[j["morts_jour"] == max_morts]["jour"].iloc[0]
                texte_html += f"""
                <strong style="color: #60a5fa;">⚠️ Pic de mortalité</strong><br>
                ❌ {max_morts} morts au J{jour_max} — Dépasse 10% du lot<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Consulter un vétérinaire, réviser le protocole vaccinal<br><br>
                """
            elif max_morts > seuil_mortalite_5:
                jour_max = j[j["morts_jour"] == max_morts]["jour"].iloc[0]
                texte_html += f"""
                <strong style="color: #60a5fa;">⚠️ Pic de mortalité</strong><br>
                ⚠️ {max_morts} morts au J{jour_max} — Dépasse 5% du lot<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Renforcer la biosécurité, vérifier la température et l'humidité<br><br>
                """
            else:
                texte_html += f"""
                <strong style="color: #60a5fa;">⚠️ Pic de mortalité</strong><br>
                ✅ Pic de mortalité maîtrisé — Maximum {max_morts} morts sur un jour<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Surveillance maintenue, pas d'action urgente<br><br>
                """
            
            # 3. RELIQUAT NON VENDU
            effectif_final = j["effectif_restant"].iloc[-1] if not j.empty else 0
            taux_reliquat = (effectif_final / effectif_init) * 100 if effectif_init > 0 else 0
            
            if taux_reliquat > 10:
                texte_html += f"""
                <strong style="color: #60a5fa;">📦 Reliquat non vendu</strong><br>
                ❌ {effectif_final} sujets ({taux_reliquat:.1f}%) — Perte économique importante<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Revoir la stratégie commerciale, diversifier les circuits de vente<br><br>
                """
            elif taux_reliquat > 5:
                texte_html += f"""
                <strong style="color: #60a5fa;">📦 Reliquat non vendu</strong><br>
                ⚠️ {effectif_final} sujets ({taux_reliquat:.1f}%) — À améliorer<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Proposer une remise de fin de cycle ou trouver des acheteurs de proximité<br><br>
                """
            elif taux_reliquat > 0:
                texte_html += f"""
                <strong style="color: #60a5fa;">📦 Reliquat non vendu</strong><br>
                🟢 Reliquat faible : {effectif_final} sujets ({taux_reliquat:.1f}%) — Acceptable<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Organiser des tournées de vente plus tôt pour libérer le bâtiment<br><br>
                """
            else:
                texte_html += f"""
                <strong style="color: #60a5fa;">📦 Reliquat non vendu</strong><br>
                ✅ Reliquat nul — Tous les sujets ont été vendus<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Capitaliser sur cette bonne organisation commerciale<br><br>
                """
            
            # 4. ÉTALEMENT DES VENTES
            if len(jours_vente) >= 2:
                premier_vente = min(jours_vente)
                dernier_vente = max(jours_vente)
                etalement = dernier_vente - premier_vente
                
                if etalement <= 7:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Étalement des ventes</strong><br>
                    ✅ {etalement} jours — Logistique optimisée<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir cette organisation logistique<br><br>
                    """
                elif etalement <= 10:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Étalement des ventes</strong><br>
                    🟡 {etalement} jours — Correct, peut être amélioré<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Regrouper certaines livraisons pour réduire les coûts de transport<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Étalement des ventes</strong><br>
                    ⚠️ {etalement} jours — Très étalé, perte d'efficacité<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Planifier des ventes par lots (2 à 3 créneaux fixes par semaine)<br><br>
                    """
          

            # Afficher la carte unique
            afficher_interpretation("📋 Journalier - Interprétations et Recommandations", texte_html)

        else:
            st.info("Données insuffisantes pour générer des interprétations")
    

    with tab2:
        # Graphique des poids
        fig_p = go.Figure()

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
                line=dict(color="#34d399", width=2.5),
                marker=dict(size=8, symbol="circle", color="#34d399"),
                connectgaps=True  # connecter les trous
            ))
            
            # Poids des plus faibles
            fig_p.add_trace(go.Scatter(
                x=pesees_graph["jour"], 
                y=pesees_graph["poids_10moins"],
                name="<10% poids", 
                mode="lines+markers",
                line=dict(color="#f87171", width=2.5),
                marker=dict(size=8, symbol="circle", color="#f87171"),
                connectgaps=False
            ))
            
            # Poids standard (toutes les lignes avec valeur)
            pesees_std = j[j["poids_standard"].notna()].copy()
            if not pesees_std.empty:
                fig_p.add_trace(go.Scatter(
                    x=pesees_std["jour"], 
                    y=pesees_std["poids_standard"],
                    name="Standard", 
                    mode="lines+markers",
                    line=dict(color="#6b7280", width=1.5, dash="dash"),
                    marker=dict(size=6, symbol="diamond", color="#6b7280")
                ))
            
            # Forcer l'affichage de tous les points en étendant l'axe X
            fig_p.update_xaxes(range=[0, pesees_graph["jour"].max() + 2])

        # Configuration du graphique
        plotly_dark_layout(fig_p, "Évolution des Poids lors des Contrôles (kg)", 340)
        fig_p.update_layout(
            legend=dict(
                orientation="v",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.8,
                bgcolor="rgba(20,23,32,0.8)",
                bordercolor="#242838",
                borderwidth=1,
                font=dict(size=9)
            ),
            margin=dict(b=70)
        )
        fig_p.update_xaxes(title_text="Jour du cycle", dtick=5)
        fig_p.update_yaxes(title_text="Poids moyen (kg)")

        st.plotly_chart(fig_p, use_container_width=True)

        # Tableau des pesées (amélioré)
        st.markdown("<div style='font-size:13px;color:#6b7280;margin:16px 0 8px'>Données des Contrôles de Pesée</div>", unsafe_allow_html=True)

        # Récupérer toutes les lignes avec au moins une valeur de poids
        pesees_display = j[
            j["poids_10plus"].notna() | 
            j["poids_10moins"].notna() | 
            j["poids_standard"].notna()
        ].copy()

        if not pesees_display.empty:
            # Sélectionner les colonnes à afficher
            cols_display = ["jour", "date", "poids_10plus", "poids_10moins", "poids_standard"]
            pesees_display = pesees_display[cols_display]
            pesees_display.columns = ["Jour", "Date", "Poids >10%", "Poids <10%", "Standard"]
                
            # Trier par jour
            pesees_display = pesees_display.sort_values("Jour")
                
            # Afficher le tableau
            st.dataframe(
                pesees_display.style.format({
                    "Poids >10%": "{:.3f}",
                    "Poids <10%": "{:.3f}",
                    "Standard": "{:.3f}"
                }).set_properties(**{'text-align': 'center'}),
                use_container_width=True,
                hide_index=True
            )
            

        # === INTERPRÉTATIONS ET RECOMMANDATIONS - PESÉES & POIDS ===
        st.markdown("---")

        # Vérifier que les données de pesée existent
        if not pesees_graph.empty:
            
            texte_html = ""
            
            # 1. POIDS FINAL PAR RAPPORT À LA CIBLE
            poids_final = None
            if "poids_10plus" in pesees_graph.columns:
                poids_final_values = pesees_graph[pesees_graph["poids_10plus"].notna()]
                if not poids_final_values.empty:
                    poids_final = poids_final_values["poids_10plus"].iloc[-1]
                    jour_final = poids_final_values["jour"].iloc[-1]
            
            if poids_final:
                if poids_final >= 2.2:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">🍗 Poids final</strong><br>
                    ✅ J{jour_final} : {poids_final:.2f} kg — Excellent poids, poulet lourd valorisable<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Vendre comme poulet lourd (prix potentiellement plus élevé)<br><br>
                    """
                elif poids_final >= 1.8:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">🍗 Poids final</strong><br>
                    ✅ J{jour_final} : {poids_final:.2f} kg — Poids standard pour le marché<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir cette performance<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">🍗 Poids final</strong><br>
                    ⚠️ J{jour_final} : {poids_final:.2f} kg — Poids insuffisant<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Prolonger le cycle de 3 à 5 jours ou améliorer l'alimentation de finition<br><br>
                    """
            else:
                texte_html += """
                <strong style="color: #60a5fa;">🍗 Poids final</strong><br>
                ⚠️ Données de poids final manquantes<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Ajouter des pesées en fin de cycle<br><br>
                """
            
            # 2. ÉCART ENTRE POIDS DES PLUS LOURDS ET DES PLUS FAIBLES
            poids_faible = None
            if "poids_10moins" in pesees_graph.columns:
                poids_faible_values = pesees_graph[pesees_graph["poids_10moins"].notna()]
                if not poids_faible_values.empty:
                    poids_faible = poids_faible_values["poids_10moins"].iloc[-1]
            
            if poids_final and poids_faible:
                ecart = poids_final - poids_faible
                uniformite = (poids_faible / poids_final) * 100 if poids_final > 0 else 0
                
                if ecart <= 0.3:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Uniformité du lot</strong><br>
                    ✅ Écart lourds/faibles : {ecart:.2f} kg — Lot très homogène (uniformité {uniformite:.0f}%)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir cette homogénéité<br><br>
                    """
                elif ecart <= 0.6:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Uniformité du lot</strong><br>
                    🟢 Écart lourds/faibles : {ecart:.2f} kg — Homogénéité acceptable (uniformité {uniformite:.0f}%)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Surveiller l'alimentation et la densité<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📊 Uniformité du lot</strong><br>
                    ⚠️ Écart lourds/faibles : {ecart:.2f} kg — Lot hétérogène (uniformité {uniformite:.0f}%)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Trier les sujets par poids, ajuster la densité dans le poulailler<br><br>
                    """
            
            # 3. COURBE DE CROISSANCE PAR RAPPORT AU STANDARD
            pesees_std = j[j["poids_standard"].notna()]
            if not pesees_std.empty and not pesees_graph.empty:
                poids_std_final = pesees_std["poids_standard"].iloc[-1] if not pesees_std["poids_standard"].isna().all() else None
                jour_std = pesees_std["jour"].iloc[-1] if not pesees_std.empty else None
                
                if poids_final and poids_std_final and jour_std:
                    ecart_standard = poids_final - poids_std_final
                    
                    if ecart_standard > 0.1:
                        texte_html += f"""
                        <strong style="color: #60a5fa;">📈 Croissance vs standard</strong><br>
                        ✅ J{jour_std} : +{ecart_standard:.2f} kg — Croissance rapide<br>
                        <span style="color: #60a5fa;">🎯 Recommandation :</span> Capitaliser sur cette performance<br><br>
                        """
                    elif ecart_standard >= -0.1:
                        texte_html += f"""
                        <strong style="color: #60a5fa;">📈 Croissance vs standard</strong><br>
                        ✅ J{jour_std} : {ecart_standard:+.2f} kg — Conforme aux attentes<br>
                        <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir les pratiques actuelles<br><br>
                        """
                    else:
                        texte_html += f"""
                        <strong style="color: #60a5fa;">📈 Croissance vs standard</strong><br>
                        ⚠️ J{jour_std} : {ecart_standard:+.2f} kg — Retard de croissance<br>
                        <span style="color: #60a5fa;">🎯 Recommandation :</span> Vérifier la qualité de l'aliment et les conditions d'élevage<br><br>
                        """
            
            # 4. PROGRESSION DU POIDS (GAIN QUOTIDIEN)
            if not pesees_graph.empty and len(pesees_graph) >= 2:
                premiers_jours = pesees_graph[pesees_graph["poids_10plus"].notna()].sort_values("jour")
                if len(premiers_jours) >= 2:
                    poids_debut = premiers_jours["poids_10plus"].iloc[0]
                    poids_fin_periode = premiers_jours["poids_10plus"].iloc[-1]
                    jours_debut = premiers_jours["jour"].iloc[0]
                    jours_fin_periode = premiers_jours["jour"].iloc[-1]
                    
                    if jours_fin_periode > jours_debut:
                        gain_quotidien = (poids_fin_periode - poids_debut) / (jours_fin_periode - jours_debut)
                        
                        if gain_quotidien >= 0.055:
                            texte_html += f"""
                            <strong style="color: #60a5fa;">📈 Gain quotidien</strong><br>
                            ✅ {gain_quotidien:.3f} kg/jour — Excellente progression<br>
                            <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce rythme de croissance<br><br>
                            """
                        elif gain_quotidien >= 0.045:
                            texte_html += f"""
                            <strong style="color: #60a5fa;">📈 Gain quotidien</strong><br>
                            🟢 {gain_quotidien:.3f} kg/jour — Bonne progression<br>
                            <span style="color: #60a5fa;">🎯 Recommandation :</span> Surveiller l'alimentation de finition<br><br>
                            """
                        else:
                            texte_html += f"""
                            <strong style="color: #60a5fa;">📈 Gain quotidien</strong><br>
                            ⚠️ {gain_quotidien:.3f} kg/jour — Progression lente<br>
                            <span style="color: #60a5fa;">🎯 Recommandation :</span> Améliorer la qualité de l'aliment, vérifier l'absence de stress<br><br>
                            """
                
                # Vérifier le ralentissement en fin de cycle
                if len(premiers_jours) >= 4:
                    milieu = len(premiers_jours) // 2
                    debut = premiers_jours.head(milieu)
                    fin = premiers_jours.tail(milieu)
                    
                    if len(debut) >= 2 and len(fin) >= 2:
                        gain_debut = (debut["poids_10plus"].iloc[-1] - debut["poids_10plus"].iloc[0]) / (debut["jour"].iloc[-1] - debut["jour"].iloc[0])
                        gain_fin = (fin["poids_10plus"].iloc[-1] - fin["poids_10plus"].iloc[0]) / (fin["jour"].iloc[-1] - fin["jour"].iloc[0])
                        
                        if gain_fin < gain_debut * 0.5:
                            texte_html += f"""
                            <strong style="color: #60a5fa;">⚠️ Ralentissement en fin de cycle</strong><br>
                            Gain réduit de {gain_debut:.3f} à {gain_fin:.3f} kg/jour<br>
                            <span style="color: #60a5fa;">🎯 Recommandation :</span> Renforcer l'alimentation de finition<br><br>
                            """
            
            # 5. NOMBRE DE PESÉES EFFECTUÉES
            nb_pesees = len(pesees_graph[pesees_graph["poids_10plus"].notna()])
            
            if nb_pesees >= 7:
                texte_html += f"""
                <strong style="color: #60a5fa;">⚖️ Fréquence des pesées</strong><br>
                ✅ {nb_pesees} pesées — Suivi rigoureux, excellente pratique<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Continuer ce suivi régulier<br><br>
                """
            elif nb_pesees >= 5:
                texte_html += f"""
                <strong style="color: #60a5fa;">⚖️ Fréquence des pesées</strong><br>
                🟢 {nb_pesees} pesées — Suivi correct<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Idéalement 6-8 pesées par cycle pour un meilleur suivi<br><br>
                """
            elif nb_pesees >= 3:
                texte_html += f"""
                <strong style="color: #60a5fa;">⚖️ Fréquence des pesées</strong><br>
                🟡 {nb_pesees} pesées — Suivi minimal acceptable<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Augmenter la fréquence des pesées (au moins 5 par cycle)<br><br>
                """
            else:
                texte_html += f"""
                <strong style="color: #60a5fa;">⚖️ Fréquence des pesées</strong><br>
                ⚠️ {nb_pesees} pesées — Suivi insuffisant<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Programmer des pesées régulières (tous les 5-7 jours)<br><br>
                """
            
            # 6. ESPACEMENT ENTRE LES PESÉES
            if nb_pesees >= 2:
                jours_pesees = sorted(pesees_graph[pesees_graph["poids_10plus"].notna()]["jour"].unique())
                ecarts = [jours_pesees[i+1] - jours_pesees[i] for i in range(len(jours_pesees)-1)]
                ecart_moyen = sum(ecarts) / len(ecarts) if ecarts else 0
                
                if ecart_moyen <= 5:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Espacement des pesées</strong><br>
                    ✅ {ecart_moyen:.0f} jours en moyenne — Très bon suivi<br><br>
                    """
                elif ecart_moyen <= 7:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Espacement des pesées</strong><br>
                    🟢 {ecart_moyen:.0f} jours en moyenne — Suivi correct<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📅 Espacement des pesées</strong><br>
                    ⚠️ {ecart_moyen:.0f} jours en moyenne — Trop espacé<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Rapprocher les pesées (tous les 5-7 jours max)<br><br>
                    """
            
            # Afficher la carte unique
            afficher_interpretation("🥩 Pesées & Poids - Interprétations et Recommandations", texte_html)

        else:
            st.info("Données de pesée insuffisantes pour générer des interprétations")


    with tab3:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            # Waterfall CA → Dépenses → Résultat
            cats = ["CA", "Poussins", "Aliment", "Médical", "Transport", "Litière", "Salaires", "Loyer", "Eau/Élec", "Résultat"]
            vals_wf = [c["ca_fcfa"],
                       -c["cout_poussins_fcfa"] if not pd.isna(c["cout_poussins_fcfa"]) else 0,
                       -c["cout_aliment_fcfa"] if not pd.isna(c["cout_aliment_fcfa"]) else 0,
                       -c["cout_medical_fcfa"] if not pd.isna(c["cout_medical_fcfa"]) else 0,
                       -c["cout_transport_fcfa"] if not pd.isna(c["cout_transport_fcfa"]) else 0,
                       -c["cout_litiere_fcfa"] if not pd.isna(c["cout_litiere_fcfa"]) else 0,
                       -c["cout_salaires_fcfa"] if not pd.isna(c["cout_salaires_fcfa"]) else 0,
                       -c["cout_loyer_fcfa"] if not pd.isna(c["cout_loyer_fcfa"]) else 0,
                       -c["cout_eau_elec_fcfa"] if not pd.isna(c["cout_eau_elec_fcfa"]) else 0,
                       c["resultat_net_fcfa"]]
            measures = ["absolute"] + ["relative"] * (len(cats)-2) + ["total"]
            fig_wf = go.Figure(go.Waterfall(
                name="Résultat", orientation="v",
                measure=measures, x=cats, y=vals_wf,
                connector=dict(line=dict(color="#242838", width=1)),
                increasing=dict(marker=dict(color="#34d399")),
                decreasing=dict(marker=dict(color="#f87171")),
                totals=dict(marker=dict(color="#fbbf24")),
                texttemplate="%{y:+,.0f}", textposition="outside",
                textfont=dict(size=9, color="#9ca3af")
            ))
            plotly_dark_layout(fig_wf, "Cascade Financière", 400)
            fig_wf.update_xaxes(tickangle=-30)
            st.plotly_chart(fig_wf, use_container_width=True)

        with col_f2:
            # Tableau financier
            fin_data = {
                "Poste": ["CA", "Coût Poussins", "Coût Aliment", "Coût Médical", "Transport",
                          "Litière", "Salaires", "Loyer", "Eau/Élec", "━ DÉPENSES TOTALES", "━ RÉSULTAT NET",
                          "━ ROI", "━ IC", "━ Prix de Revient"],
                "Montant (FCFA)": [
                    c["ca_fcfa"], c["cout_poussins_fcfa"], c["cout_aliment_fcfa"],
                    c["cout_medical_fcfa"], c["cout_transport_fcfa"], c["cout_litiere_fcfa"],
                    c["cout_salaires_fcfa"], c["cout_loyer_fcfa"], c["cout_eau_elec_fcfa"],
                    c["depenses_totales_fcfa"], c["resultat_net_fcfa"],
                    f"{c.get('roi_pct', 0):+.1f}%",
                    f"{c.get('ic_calcule', 0):.2f}",
                    f"{c.get('prix_revient_unitaire', 0):,.0f}"
                ]
            }
            df_fin = pd.DataFrame(fin_data)
            st.markdown("<div style='font-size:13px;color:#6b7280;margin:0px 0 8px'>Récapitulatif Financier</div>", unsafe_allow_html=True)
            st.dataframe(df_fin, use_container_width=True, hide_index=True, height=400)

        # === INTERPRÉTATIONS ET RECOMMANDATIONS - FINANCES ===
        st.markdown("---")

        # Vérifier que les données financières existent
        if c.get("ca_fcfa", 0) > 0:

            # Récupération des données
            ca = c.get("ca_fcfa", 0)
            depenses = c.get("depenses_totales_fcfa", 0)
            resultat = c.get("resultat_net_fcfa", 0)
            marge = c.get("marge_unitaire_fcfa", 0)
            volume = c.get("volume_vendu", 0)
            cout_aliment = c.get("cout_aliment_fcfa", 0)
            cout_poussins = c.get("cout_poussins_fcfa", 0)
            cout_salaires = c.get("cout_salaires_fcfa", 0)
            cout_loyer = c.get("cout_loyer_fcfa", 0)
            prix_vente = c.get("prix_moyen_fcfa", 0)
            seuil = c.get("seuil_rentabilite_fcfa", 0)
            point_mort = c.get("point_mort_jours", 0)
            roi = c.get("roi_pct", 0)
            
            texte_html = ""
            
            # 1. RENTABILITÉ GLOBALE
            if resultat > 0:
                texte_html += f"""
                <strong style="color: #60a5fa;">💰 Rentabilité globale</strong><br>
                ✅ Résultat net : {resultat:+,.0f} FCFA — Cycle rentable<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Capitaliser sur les bonnes pratiques de ce cycle<br><br>
                """
            elif resultat < 0:
                texte_html += f"""
                <strong style="color: #60a5fa;">💰 Rentabilité globale</strong><br>
                ❌ Résultat net : {resultat:+,.0f} FCFA — Cycle déficitaire<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Identifier et réduire les postes de coûts les plus élevés<br><br>
                """
            else:
                texte_html += f"""
                <strong style="color: #60a5fa;">💰 Rentabilité globale</strong><br>
                🟡 Résultat net : équilibre — Cycle à l'équilibre<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Améliorer la marge pour dégager du bénéfice<br><br>
                """
            
            # 2. MARGE UNITAIRE
            if marge > 200:
                texte_html += f"""
                <strong style="color: #60a5fa;">💵 Marge unitaire</strong><br>
                ✅ {marge:+.0f} FCFA/sujet — Bonne rentabilité par tête<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce niveau de marge<br><br>
                """
            elif marge > 0:
                texte_html += f"""
                <strong style="color: #60a5fa;">💵 Marge unitaire</strong><br>
                🟡 {marge:+.0f} FCFA/sujet — Faible, risque en cas de variation des prix<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Augmenter le prix de vente ou réduire les coûts variables (aliment, poussins)<br><br>
                """
            elif marge < 0:
                texte_html += f"""
                <strong style="color: #60a5fa;">💵 Marge unitaire</strong><br>
                ❌ {marge:+.0f} FCFA/sujet — Perte par sujet vendu<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Action prioritaire, revoir la stratégie commerciale<br><br>
                """
            else:
                texte_html += f"""
                <strong style="color: #60a5fa;">💵 Marge unitaire</strong><br>
                🟡 Marge unitaire : équilibre<br>
                <span style="color: #60a5fa;">🎯 Recommandation :</span> Viser au moins 200 FCFA de marge par sujet<br><br>
                """
            
            # 3. STRUCTURE DES COÛTS
            if depenses > 0:
                part_aliment = (cout_aliment / depenses) * 100
                part_poussins = (cout_poussins / depenses) * 100
                part_fixes = ((cout_salaires + cout_loyer) / depenses) * 100
                
                texte_html += f"""
                <strong style="color: #60a5fa;">📊 Structure des coûts</strong><br>
                • Aliment : {part_aliment:.1f}% des dépenses<br>
                • Poussins : {part_poussins:.1f}% des dépenses<br>
                • Salaires + Loyer : {part_fixes:.1f}% des dépenses<br>
                """
                
                if part_aliment > 50:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> ⚠️ Aliment trop élevé — Renégocier le prix des sacs (18 000 FCFA), réduire le gaspillage<br><br>"""
                elif part_aliment > 45:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> 🟡 Aliment correct — Surveiller ce poste<br><br>"""
                else:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> ✅ Aliment maîtrisé — Maintenir la qualité tout en surveillant les prix<br><br>"""
                
                if part_fixes > 30 and volume < 2000:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> ⚠️ Charges fixes lourdes pour ce volume — Envisager d'augmenter la taille des cycles<br><br>"""
                elif part_fixes > 30:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> 🟡 Charges fixes élevées — Optimiser l'organisation (mutualisation, sous-traitance)<br><br>"""
                elif part_fixes < 20:
                    texte_html += f"""<span style="color: #60a5fa;">🎯 Recommandation :</span> ✅ Charges fixes maîtrisées<br><br>"""
            
            # 4. PRIX DE VENTE VS PRIX DE REVIENT
            prix_revient = depenses / volume if volume > 0 else 0
            
            if prix_vente > 0 and prix_revient > 0:
                ecart_prix = prix_vente - prix_revient
                
                if ecart_prix > 300:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">💰 Prix de vente vs Prix de revient</strong><br>
                    ✅ Marge Nette : {ecart_prix:.0f} FCFA/sujet — Bonne valorisation<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce positionnement prix<br><br>
                    """
                elif ecart_prix > 0:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">💰 Prix de vente vs Prix de revient</strong><br>
                    🟢 Marge Nette : {ecart_prix:.0f} FCFA/sujet — Marge Nette insuffisante<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Augmenter le prix ou réduire les coûts de production<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">💰 Prix de vente vs Prix de revient</strong><br>
                    ❌ Marge Nette négative — Prix de vente ({prix_vente:.0f} FCFA) inférieur au prix de revient ({prix_revient:.0f} FCFA)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Priorité absolue : revoir le positionnement prix<br><br>
                    """
            
            # 5. SEUIL DE RENTABILITÉ (si disponible)
            if seuil > 0:
                if ca >= seuil:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">🎯 Seuil de rentabilité</strong><br>
                    ✅ Atteint — CA ({ca/1e6:.1f} M FCFA) ≥ Seuil ({seuil/1e6:.1f} M FCFA)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce niveau d'activité<br><br>
                    """
                else:
                    ecart_seuil = seuil - ca
                    texte_html += f"""
                    <strong style="color: #60a5fa;">🎯 Seuil de rentabilité</strong><br>
                    ⚠️ Non atteint — Manque {ecart_seuil/1e6:.1f} M FCFA<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Augmenter le volume ou la marge unitaire<br><br>
                    """
            
            # 6. POINT MORT (si disponible)
            if point_mort > 0:
                if point_mort <= 53:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">⏱️ Point mort</strong><br>
                    ✅ J{point_mort:.0f} — Rentabilité atteinte pendant le cycle<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Bonne performance, maintenir<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">⏱️ Point mort</strong><br>
                    ⚠️ J{point_mort:.0f} — Jamais rentable sur la durée du cycle (53j)<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Réduire les charges fixes ou améliorer la marge<br><br>
                    """
            
            # 7. ROI (si disponible)
            if roi != 0:
                if roi > 10:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📈 ROI (Retour sur Investissement)</strong><br>
                    ✅ {roi:+.1f}% — Très bon retour sur investissement<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Capitaliser sur cette performance<br><br>
                    """
                elif roi > 0:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📈 ROI (Retour sur Investissement)</strong><br>
                    🟢 {roi:+.1f}% — Retour faible mais positif<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Améliorer la rentabilité<br><br>
                    """
                else:
                    texte_html += f"""
                    <strong style="color: #60a5fa;">📈 ROI (Retour sur Investissement)</strong><br>
                    ❌ {roi:+.1f}% — Investissement non rentable<br>
                    <span style="color: #60a5fa;">🎯 Recommandation :</span> Avant tout nouveau cycle, revoir les coûts ou le prix de vente<br><br>
                    """
            
            # 8. RÉCAPITULATIF DES ACTIONS PRIORITAIRES
            texte_html += """
            <strong style="color: #60a5fa;">🎯 Actions prioritaires</strong><br>
            """
            
            actions = []
            
            if resultat < 0:
                actions.append("🔴 Rétablir la rentabilité (priorité absolue)")
            if 'part_aliment' in locals() and part_aliment > 50:
                actions.append("🟠 Réduire le coût alimentaire (18 000 FCFA/sac est élevé)")
            if prix_vente < 2600:
                actions.append("🟠 Augmenter le prix de vente (cibler 2 700-2 800 FCFA/sujet)")
            if 'part_fixes' in locals() and part_fixes > 30 and volume < 2000:
                actions.append("🟡 Augmenter le volume pour diluer les charges fixes")
            if marge < 0:
                actions.append("🟡 Améliorer la marge unitaire (agir sur prix ou coûts)")
            
            if actions:
                for action in actions:
                    texte_html += f"• {action}<br>"
            else:
                texte_html += "✅ Tous les indicateurs sont dans le vert — Félicitations !<br>"
            
            texte_html += "<br>"
            
            # Afficher la carte unique
            afficher_interpretation("💸 Finances - Interprétations et Recommandations", texte_html)

        else:
            st.info("Données financières insuffisantes pour générer des interprétations")
        

# ═══════════════════════════════════════════════════
# PAGE 3 : VENTES & PRIX (identique, à garder)
# ═══════════════════════════════════════════════════
elif page == "💰 Ventes & Prix":

    section_header("💰 Analyse des Ventes & Structure des Prix", "Évolution des prix, volumes et chiffre d'affaires")

    col1, col2 = st.columns(2)

    with col1:
        # Prix unitaire dans le temps - tous cycles
        fig = go.Figure()
        for cid in selected_cycles:
            v = vf[vf["cycle_id"] == cid]
            fig.add_trace(go.Scatter(
                x=v["jour"], y=v["prix_unitaire"], name=cid,
                mode="lines+markers",
                line=dict(color=COLORS.get(cid,"#fff"), width=2),
                marker=dict(size=7),
                hovertemplate=f"<b>{cid}</b> J%{{x}}<br>Prix : %{{y:,}} FCFA<extra></extra>"
            ))
        plotly_dark_layout(fig, "Évolution du Prix Unitaire par Cycle (FCFA/sujet)", 340)
        fig.update_xaxes(title_text="Jour du cycle")
        fig.update_yaxes(title_text="Prix unitaire (FCFA)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Volume vendu cumulé par cycle
        fig2 = go.Figure()
        for cid in selected_cycles:
            v = vf[vf["cycle_id"] == cid].sort_values("jour")
            v = v.copy()
            v["qte_cum"] = v["quantite"].cumsum()
            
            # Convertir la couleur hex en rgba
            color = COLORS.get(cid, "#4e7cff")
            hex_color = color.lstrip('#')
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            rgba_color = f"rgba({r}, {g}, {b}, 0.15)"
            
            fig2.add_trace(go.Scatter(
                x=v["jour"], y=v["qte_cum"], name=cid,
                mode="lines+markers",
                line=dict(color=color, width=2),
                fill="tozeroy",
                fillcolor=rgba_color,  # ← Utilisation du format rgba
                hovertemplate=f"<b>{cid}</b> J%{{x}}<br>Cumulé : %{{y:,}} têtes<extra></extra>"
            ))
        plotly_dark_layout(fig2, "Volume Vendu Cumulé par Cycle", 340)
        fig2.update_xaxes(title_text="Jour du cycle")
        fig2.update_yaxes(title_text="Têtes vendues cumulées")
        st.plotly_chart(fig2, use_container_width=True)

    # CA journalier
    fig3 = go.Figure()
    for cid in selected_cycles:
        v = vf[vf["cycle_id"] == cid]
        v_grp = v.groupby("jour")["prix_total"].sum().reset_index()
        fig3.add_trace(go.Bar(
            x=v_grp["jour"], y=v_grp["prix_total"], name=cid,
            marker_color=COLORS.get(cid,"#fff"), opacity=0.85,
            hovertemplate=f"<b>{cid}</b> J%{{x}}<br>CA : %{{y:,.0f}} FCFA<extra></extra>"
        ))
    plotly_dark_layout(fig3, "CA par Jour de Vente (FCFA)", 300)
    fig3.update_layout(barmode="group")
    fig3.update_xaxes(title_text="Jour du cycle")
    st.plotly_chart(fig3, use_container_width=True)

    # CA cumulé par jour de vente
    fig_ca_cumul = go.Figure()
    for cid in selected_cycles:
        v = vf[vf["cycle_id"] == cid].sort_values("jour")
        v = v.copy()
        v["ca_cumul"] = v["prix_total"].cumsum()
        
        color = COLORS.get(cid, "#4e7cff")
        fig_ca_cumul.add_trace(go.Scatter(
            x=v["jour"], y=v["ca_cumul"], name=cid,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor=f"rgba({int(color[1:3],16)}, {int(color[3:5],16)}, {int(color[5:7],16)}, 0.15)",
            hovertemplate=f"<b>{cid}</b> J%{{x}}<br>CA cumulé : %{{y:,.0f}} FCFA<extra></extra>"
        ))

    plotly_dark_layout(fig_ca_cumul, "Chiffre d'Affaires Cumulé par Cycle", 340)
    fig_ca_cumul.update_xaxes(title_text="Jour du cycle")
    fig_ca_cumul.update_yaxes(title_text="CA cumulé (FCFA)")
    st.plotly_chart(fig_ca_cumul, use_container_width=True)

    # Tableau détail ventes
    st.markdown('<div class="section-header">Détail des Transactions</div>', unsafe_allow_html=True)
    tab_c1, tab_c2, tab_c3 = st.tabs(["Cycle 1", "Cycle 2", "Cycle 3"])

    for tab, cid in zip([tab_c1, tab_c2, tab_c3], ["Cycle1", "Cycle2", "Cycle3"]):
        with tab:
            v = ventes[ventes["cycle_id"] == cid][["jour", "date", "quantite", "prix_unitaire", "prix_total"]].copy()
            v.columns = ["Jour", "Date", "Quantité", "Prix Unit.", "Prix Total"]
            tot = v["Prix Total"].sum()
            vol = v["Quantité"].sum()
            
            col_s, col_v = st.columns([3, 1])
            with col_s:
                st.dataframe(
                    v.style.format({"Prix Unit.": "{:,.0f}", "Prix Total": "{:,.0f}", "Quantité": "{:,}"}),
                    use_container_width=True, hide_index=True
                )
            with col_v:
                st.markdown(f"""
                <div class="metric-card" style="--accent:{COLORS.get(cid, '#4e7cff')}; margin-top:0">
                    <div class="metric-label">Total {cid}</div>
                    <div class="metric-value">{vol:,}</div>
                    <div class="metric-sub">Têtes vendues</div>
                </div>
                <div class="metric-card" style="--accent:{COLORS.get(cid, '#4e7cff')}; margin-top:12px">
                    <div class="metric-label">CA Total</div>
                    <div class="metric-value">{tot/1e6:.2f} M</div>
                    <div class="metric-sub">FCFA</div>
                </div>
                """, unsafe_allow_html=True)
            
            # === INTERPRÉTATIONS ET RECOMMANDATIONS ===
            st.markdown("---")

            # Récupérer les données du cycle
            v_cycle = ventes[ventes["cycle_id"] == cid].copy()
            c_cycle = cycles_recap[cycles_recap["cycle_id"] == cid].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == cid]) > 0 else None

            if not v_cycle.empty and c_cycle is not None:
                
                texte_html = ""
                
                # 1. ANALYSE DU PRIX UNITAIRE
                prix_min = v_cycle["prix_unitaire"].min()
                prix_max = v_cycle["prix_unitaire"].max()
                prix_moy = v_cycle["prix_unitaire"].mean()
                
                texte_html += '<strong style="color: #60a5fa;">💰 Évolution du prix unitaire</strong><br>'
                
                if prix_max - prix_min < 200:
                    texte_html += f'✅ Prix stable ({prix_moy:.0f} FCFA) — bonne stratégie commerciale<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir cette stratégie<br><br>'
                elif prix_max - prix_min < 400:
                    texte_html += f'🟡 Prix en légère variation ({prix_min:.0f} → {prix_max:.0f} FCFA)<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Surveiller les baisses de prix en fin de cycle<br><br>'
                else:
                    texte_html += f'⚠️ Forte variation de prix ({prix_min:.0f} → {prix_max:.0f} FCFA)<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Analyser les causes (client, période, qualité)<br><br>'
                
                if prix_moy < 2600:
                    texte_html += f'⚠️ Prix moyen bas ({prix_moy:.0f} FCFA) : Négocier avec les acheteurs, diversifier les débouchés<br><br>'
                elif prix_moy > 2700:
                    texte_html += f'✅ Bon prix moyen ({prix_moy:.0f} FCFA) : Maintenir cette stratégie<br><br>'
                
                # 2. ANALYSE DU VOLUME VENDU
                v_sort = v_cycle.sort_values("jour").copy()
                premier_vente = v_sort["jour"].min()
                dernier_vente = v_sort["jour"].max()
                volume_total = v_sort["quantite"].sum()
                
                if dernier_vente > premier_vente:
                    pente = volume_total / (dernier_vente - premier_vente)
                else:
                    pente = volume_total
                
                texte_html += '<strong style="color: #60a5fa;">📊 Dynamique des ventes</strong><br>'
                texte_html += f'• Premier jour de vente : <strong>J{premier_vente}</strong><br>'
                texte_html += f'• Dernier jour de vente : <strong>J{dernier_vente}</strong><br>'
                texte_html += f'• Volume total vendu : <strong>{volume_total}</strong> sujets<br>'
                
                if pente > 30:
                    texte_html += f'✅ Ventes rapides ({pente:.0f} sujets/jour) — bonne demande<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Capitaliser sur cette dynamique<br><br>'
                elif pente > 15:
                    texte_html += f'🟡 Ventes correctes ({pente:.0f} sujets/jour) — écoulement acceptable<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Améliorer la prospection<br><br>'
                else:
                    texte_html += f'⚠️ Ventes lentes ({pente:.0f} sujets/jour) — démarchage à renforcer<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Contacter les acheteurs plus tôt dans le cycle<br><br>'
                
                # 3. ANALYSE DU CA
                ca_total = v_cycle["prix_total"].sum()
                ca_par_jour = ca_total / len(v_cycle) if len(v_cycle) > 0 else 0
                
                texte_html += '<strong style="color: #60a5fa;">💵 Progression du chiffre d\'affaires</strong><br>'
                texte_html += f'CA total : <strong>{ca_total/1e6:.2f} M FCFA</strong><br>'
                
                if premier_vente <= 38:
                    texte_html += f'✅ Démarrage précoce des ventes (J{premier_vente}) — bonne trésorerie<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir ce rythme<br><br>'
                else:
                    texte_html += f'⚠️ Démarrage tardif des ventes (J{premier_vente}) — risque de tension de trésorerie<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Anticiper les ventes<br><br>'
                
                if ca_par_jour > 500000:
                    texte_html += f'✅ CA moyen élevé par jour de vente : {ca_par_jour/1e3:.0f} K FCFA<br><br>'
                elif ca_par_jour < 200000:
                    texte_html += f'⚠️ CA moyen faible par jour de vente : {ca_par_jour/1e3:.0f} K FCFA<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Regrouper les livraisons ou augmenter les volumes par vente<br><br>'
                
                # 4. ANALYSE DES PICS DE VENTE
                max_vente = v_cycle["quantite"].max()
                jour_max = v_cycle[v_cycle["quantite"] == max_vente]["jour"].iloc[0]
                ratio_max = (max_vente / volume_total) * 100 if volume_total > 0 else 0
                
                texte_html += '<strong style="color: #60a5fa;">📈 Pics de vente et concentration</strong><br>'
                texte_html += f'• Plus gros pic : <strong>{max_vente}</strong> sujets au <strong>J{jour_max}</strong> ({ratio_max:.0f}% du total)<br>'
                
                if ratio_max > 40:
                    texte_html += f'⚠️ Forte dépendance à un seul pic — risque commercial<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Diversifier les clients pour réduire le risque<br><br>'
                elif ratio_max > 25:
                    texte_html += f'🟡 Concentration modérée<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Éviter de trop dépendre d\'un seul acheteur<br><br>'
                else:
                    texte_html += f'✅ Ventes bien réparties — clientèle diversifiée<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Maintenir cette diversification<br><br>'
                
                # 5. RELIQUAT ET FIN DE CYCLE
                effectif_final = c_cycle["effectif_final"]
                effectif_initial = c_cycle["effectif_initial"]
                taux_reliquat = (effectif_final / effectif_initial) * 100 if effectif_initial > 0 else 0
                
                texte_html += '<strong style="color: #60a5fa;">🏁 Fin de cycle</strong><br>'
                texte_html += f'Reliquat non vendu : <strong>{effectif_final}</strong> sujets ({taux_reliquat:.1f}%)<br>'
                
                if taux_reliquat > 5:
                    texte_html += f'⚠️ Reliquat élevé — perte économique<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Vendre en plus petits lots en fin de cycle<br><br>'
                elif taux_reliquat > 0:
                    texte_html += f'🟡 Reliquat faible mais existant<br>'
                    texte_html += f'<span style="color: #60a5fa;">🎯 Recommandation :</span> Écouler les derniers sujets avec une remise légère<br><br>'
                else:
                    texte_html += f'✅ Aucun reliquat — bonne gestion commerciale<br><br>'
                
                # 6. SYNTHÈSE DES ACTIONS PRIORITAIRES
                texte_html += '<strong style="color: #60a5fa;">🎯 Actions prioritaires</strong><br>'
                
                actions = []
                
                if prix_moy < 2600:
                    actions.append(f"🟠 Prix de vente : Augmenter le prix (actuellement {prix_moy:.0f} FCFA)")
                elif prix_moy > 2700:
                    actions.append(f"✅ Prix de vente : Bon niveau ({prix_moy:.0f} FCFA) — à maintenir")
                
                if premier_vente > 40:
                    actions.append(f"🟠 Première vente : Anticiper la commercialisation (J{premier_vente})")
                elif premier_vente <= 38:
                    actions.append(f"✅ Première vente : Bon rythme (J{premier_vente}) — à reproduire")
                
                if taux_reliquat > 5:
                    actions.append(f"🟡 Reliquat : Réduire les invendus ({effectif_final} sujets)")
                elif taux_reliquat == 0:
                    actions.append(f"✅ Reliquat : Aucun invendu — excellente gestion commerciale")
                
                if ratio_max > 40:
                    actions.append(f"🟡 Concentration : Diversifier les clients (pic de {max_vente} sujets)")
                elif ratio_max <= 25:
                    actions.append(f"✅ Diversification : Clientèle bien répartie — à maintenir")
                
                # Recommandations essentielles
                actions.append(f"📊 Suivi technique : Maintenir l'IC ≤ 1,7 et la mortalité < 4%")
                actions.append(f"💰 Optimisation financière : Viser une marge unitaire ≥ 200 FCFA/sujet")
                actions.append(f"📅 Planification : Programmer les cycles pour coïncider avec les périodes de forte demande")
                
                for action in actions:
                    texte_html += f"• {action}<br>"
                
                texte_html += "<br>"
                
                # Afficher la carte unique
                afficher_interpretation(f"💰 {cid} - Interprétations et Recommandations", texte_html)

            else:
                st.info("Données de ventes insuffisantes pour générer des interprétations")

    
# ═══════════════════════════════════════════════════
# PAGE 4 : BILAN COMPARATIF
# ═══════════════════════════════════════════════════
elif page == "⚖️ Bilan Comparatif":

    section_header("⚖️ Bilan Comparatif", "Comparaison des performances entre les 3 cycles")

    # Tableau de synthèse enrichi
    metrics_bilan = {
        "Indicateur": ["Effectif initial", "Effectif vendu", "Mortalité (%)", "CA (FCFA)",
                       "Dépenses totales (FCFA)", "Résultat net (FCFA)", "Prix moyen/sujet (FCFA)",
                       "Marge unitaire (FCFA)", "IC (indice conso)", "ROI (%)", "Prix de revient (FCFA)"],
        "Cycle 1": [
            cycles_recap.iloc[0]["effectif_initial"],
            cycles_recap.iloc[0]["volume_vendu"],
            cycles_recap.iloc[0]["taux_mortalite_pct"],
            cycles_recap.iloc[0]["ca_fcfa"],
            cycles_recap.iloc[0]["depenses_totales_fcfa"],
            cycles_recap.iloc[0]["resultat_net_fcfa"],
            cycles_recap.iloc[0]["prix_moyen_fcfa"],
            cycles_recap.iloc[0]["marge_unitaire_fcfa"],
            cycles_recap.iloc[0].get("ic_calcule", 0),
            cycles_recap.iloc[0].get("roi_pct", 0),
            cycles_recap.iloc[0].get("prix_revient_unitaire", 0),
        ],
        "Cycle 2": [
            cycles_recap.iloc[1]["effectif_initial"],
            cycles_recap.iloc[1]["volume_vendu"],
            cycles_recap.iloc[1]["taux_mortalite_pct"],
            cycles_recap.iloc[1]["ca_fcfa"],
            cycles_recap.iloc[1]["depenses_totales_fcfa"],
            cycles_recap.iloc[1]["resultat_net_fcfa"],
            cycles_recap.iloc[1]["prix_moyen_fcfa"],
            cycles_recap.iloc[1]["marge_unitaire_fcfa"],
            cycles_recap.iloc[1].get("ic_calcule", 0),
            cycles_recap.iloc[1].get("roi_pct", 0),
            cycles_recap.iloc[1].get("prix_revient_unitaire", 0),
        ],
        "Cycle 3": [
            cycles_recap.iloc[2]["effectif_initial"],
            cycles_recap.iloc[2]["volume_vendu"],
            cycles_recap.iloc[2]["taux_mortalite_pct"],
            cycles_recap.iloc[2]["ca_fcfa"],
            cycles_recap.iloc[2]["depenses_totales_fcfa"],
            cycles_recap.iloc[2]["resultat_net_fcfa"],
            cycles_recap.iloc[2]["prix_moyen_fcfa"],
            cycles_recap.iloc[2]["marge_unitaire_fcfa"],
            cycles_recap.iloc[2].get("ic_calcule", 0),
            cycles_recap.iloc[2].get("roi_pct", 0),
            cycles_recap.iloc[2].get("prix_revient_unitaire", 0),
        ],
    }
    df_bilan = pd.DataFrame(metrics_bilan)
    st.dataframe(df_bilan, use_container_width=True, hide_index=True)

    # Radar chart comparatif
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        # Radar (normalisé)
        cats_r = ["CA (norm.)", "Vol. vendu", "Mortalité inv.", "Prix moy.", "Marge unit.", "IC inv.", "ROI"]
        c1r = cycles_recap.iloc[0]
        c2r = cycles_recap.iloc[1]
        c3r = cycles_recap.iloc[2]

        def norm(vals, inv=False):
            mn, mx = min(vals), max(vals)
            if mx == mn: return [0.5]*len(vals)
            n = [(v - mn)/(mx - mn) for v in vals]
            return [1-x for x in n] if inv else n

        ca_n = norm([c1r["ca_fcfa"], c2r["ca_fcfa"], c3r["ca_fcfa"]])
        vol_n = norm([c1r["volume_vendu"], c2r["volume_vendu"], c3r["volume_vendu"]])
        mort_n = norm([c1r["taux_mortalite_pct"], c2r["taux_mortalite_pct"], c3r["taux_mortalite_pct"]], inv=True)
        prix_n = norm([c1r["prix_moyen_fcfa"], c2r["prix_moyen_fcfa"], c3r["prix_moyen_fcfa"]])
        marge_n = norm([c1r["marge_unitaire_fcfa"], c2r["marge_unitaire_fcfa"], c3r["marge_unitaire_fcfa"]])
        ic_n = norm([c1r.get("ic_calcule", 2.0), c2r.get("ic_calcule", 2.0), c3r.get("ic_calcule", 2.0)], inv=True)
        roi_n = norm([c1r.get("roi_pct", -100), c2r.get("roi_pct", -100), c3r.get("roi_pct", -100)])

        fig_r = go.Figure()
        
        for i, (cid, vals, color) in enumerate(zip(
            ["Cycle1","Cycle2","Cycle3"],
            [[ca_n[0],vol_n[0],mort_n[0],prix_n[0],marge_n[0],ic_n[0],roi_n[0]],
            [ca_n[1],vol_n[1],mort_n[1],prix_n[1],marge_n[1],ic_n[1],roi_n[1]],
            [ca_n[2],vol_n[2],mort_n[2],prix_n[2],marge_n[2],ic_n[2],roi_n[2]]],
            [COLORS["Cycle1"],COLORS["Cycle2"],COLORS["Cycle3"]]
        )):
            if cid in selected_cycles:
                # Convertir la couleur hex en rgba
                hex_color = color.lstrip('#')
                r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                rgba_color = f"rgba({r}, {g}, {b}, 0.15)"
                
                fig_r.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]], theta=cats_r + [cats_r[0]],
                    name=cid, mode="lines+markers",
                    line=dict(color=color, width=2),
                    fill="toself",
                    fillcolor=rgba_color,  # ← Utilisation du format rgba
                    marker=dict(size=7)
                ))

        fig_r.update_layout(
            polar=dict(
                bgcolor="#141720",
                radialaxis=dict(visible=True, range=[0,1], color=TEXT_COLOR, gridcolor=GRID_COLOR),
                angularaxis=dict(color=TEXT_COLOR, gridcolor=GRID_COLOR)
            ),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
            height=380,
            title=dict(text="Radar Comparatif (valeurs normalisées)", font=dict(family="Syne", size=15, color="#f0ece4")),
            margin=dict(l=60,r=60,t=60,b=20),
            legend=dict(bgcolor="#141720", bordercolor="#242838", borderwidth=1)
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with col_r2:
        # Évolution prix moyen vs prix de revient
        prix_moy = [c1r["prix_moyen_fcfa"], c2r["prix_moyen_fcfa"], c3r["prix_moyen_fcfa"]]
        prix_rev = [c1r.get("prix_revient_unitaire", 0), c2r.get("prix_revient_unitaire", 0), c3r.get("prix_revient_unitaire", 0)]
        marge_u = [c1r["marge_unitaire_fcfa"], c2r["marge_unitaire_fcfa"], c3r["marge_unitaire_fcfa"]]
        cycs_lbl = ["Cycle 1","Cycle 2","Cycle 3"]

        fig_pm = make_subplots(rows=2, cols=1, subplot_titles=("Prix Moyen vs Prix de Revient (FCFA)", "Marge Unitaire (FCFA)"),
                                vertical_spacing=0.18)
        fig_pm.add_trace(go.Scatter(x=cycs_lbl, y=prix_moy, mode="lines+markers",
                                     name="Prix moyen", line=dict(color="#4e7cff", width=2.5),
                                     marker=dict(size=10)), row=1, col=1)
        fig_pm.add_trace(go.Scatter(x=cycs_lbl, y=prix_rev, mode="lines+markers",
                                     name="Prix revient", line=dict(color="#f87171", width=2.5, dash="dot"),
                                     marker=dict(size=10)), row=1, col=1)
        colors_m = ["#34d399" if m >= 0 else "#f87171" for m in marge_u]
        fig_pm.add_trace(go.Bar(x=cycs_lbl, y=marge_u, marker_color=colors_m, opacity=0.85, name="Marge"), row=2, col=1)
        fig_pm.add_hline(y=0, line_color="#374151", line_dash="dot", row=2, col=1)

        fig_pm.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
            height=380, showlegend=True,
            margin=dict(l=12,r=12,t=44,b=12),
            legend=dict(bgcolor="#141720", bordercolor="#242838", borderwidth=1)
        )
        for axis in ["xaxis","xaxis2","yaxis","yaxis2"]:
            fig_pm.update_layout(**{axis: dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)})
        st.plotly_chart(fig_pm, use_container_width=True)

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

    # === INTERPRÉTATIONS ET RECOMMANDATIONS - BILAN COMPARATIF ===
    st.markdown("---")

    # Récupérer les données des 3 cycles
    c1 = cycles_recap[cycles_recap["cycle_id"] == "Cycle1"].iloc[0] if len(cycles_recap) > 0 else None
    c2 = cycles_recap[cycles_recap["cycle_id"] == "Cycle2"].iloc[0] if len(cycles_recap) > 1 else None
    c3 = cycles_recap[cycles_recap["cycle_id"] == "Cycle3"].iloc[0] if len(cycles_recap) > 2 else None

    if c1 is not None and c2 is not None and c3 is not None:
        
        texte_html = ""
        
        # ============================================================
        # 1. ANALYSE DU RADAR COMPARATIF
        # ============================================================
        texte_html += '<strong style="color: #60a5fa;">📡 Radar comparatif des performances</strong><br><br>'
        
        # Analyse synthétique
        texte_html += '<strong style="color: #60a5fa;">📌 Analyse synthétique du radar</strong><br>'
        
        # Utilisation de colonnes HTML pour les 3 cycles
        texte_html += """
        <div style="display: flex; gap: 16px; margin: 12px 0;">
            <div style="flex: 1; background: rgba(78, 124, 255, 0.08); border-radius: 12px; padding: 12px;">
                <strong style="color: #60a5fa;">Cycle 1</strong><br>
                ✅ Meilleur prix (2 758 FCFA)<br>
                ❌ Volume trop faible<br>
                ❌ Marge négative
            </div>
            <div style="flex: 1; background: rgba(78, 124, 255, 0.08); border-radius: 12px; padding: 12px;">
                <strong style="color: #60a5fa;">Cycle 2</strong><br>
                ✅ Volume correct<br>
                ❌ Prix en baisse<br>
                ❌ Marge très négative
            </div>
            <div style="flex: 1; background: rgba(78, 124, 255, 0.08); border-radius: 12px; padding: 12px;">
                <strong style="color: #60a5fa;">Cycle 3</strong><br>
                ✅ Meilleur volume (×4,6)<br>
                ❌ Prix le plus bas<br>
                ❌ Marge négative
            </div>
        </div>
        """
        
        texte_html += """
        <strong style="color: #60a5fa;">🎯 Priorité pour le Cycle 4</strong><br>
        Combiner le volume du Cycle 3 (5 000 sujets) avec le prix du Cycle 1 (2 758 FCFA)<br>
        → Objectif de marge unitaire : +200 à 300 FCFA/sujet<br><br>
        """
        
        # Récupérer les données pour l'évaluation
        prix_c1, prix_c2, prix_c3 = c1["prix_moyen_fcfa"], c2["prix_moyen_fcfa"], c3["prix_moyen_fcfa"]
        marge_c1, marge_c2, marge_c3 = c1["marge_unitaire_fcfa"], c2["marge_unitaire_fcfa"], c3["marge_unitaire_fcfa"]
        ic_c1 = c1.get("ic_calcule", c1.get("ic_standard", 1.7))
        ic_c2 = c2.get("ic_calcule", c2.get("ic_standard", 1.7))
        ic_c3 = c3.get("ic_calcule", c3.get("ic_standard", 1.7))
        mort_c1, mort_c2, mort_c3 = c1["taux_mortalite_pct"], c2["taux_mortalite_pct"], c3["taux_mortalite_pct"]
        vol_c1, vol_c2, vol_c3 = c1["volume_vendu"], c2["volume_vendu"], c3["volume_vendu"]
        
        # Points forts
        axes_forts = []
        if ic_c1 <= 1.7 and ic_c2 <= 1.7 and ic_c3 <= 1.7:
            axes_forts.append("✅ Indice de consommation : maîtrisé (≤ 1,7) pour tous les cycles")
        if mort_c1 <= 4 and mort_c2 <= 4 and mort_c3 <= 4:
            axes_forts.append("✅ Mortalité : maîtrisée (< 4%) pour tous les cycles")
        if vol_c3 > vol_c1 * 4:
            axes_forts.append(f"📊 Volume : montée en puissance réussie (×{vol_c3/vol_c1:.1f} entre C1 et C3)")
        
        # Points à améliorer
        axes_faibles = []
        if marge_c1 < 0 and marge_c2 < 0 and marge_c3 < 0:
            axes_faibles.append("🔴 Marge unitaire : négative pour tous les cycles")
        if prix_c1 > prix_c2 > prix_c3:
            axes_faibles.append("📉 Prix de vente : en baisse constante (C1 → C2 → C3)")
        elif prix_c3 <= prix_c1:
            axes_faibles.append("🟡 Prix de vente : stable mais bas")
        
        if axes_forts:
            texte_html += '<strong style="color: #60a5fa;">✅ Points forts</strong><br>'
            for axe in axes_forts:
                texte_html += f"• {axe}<br>"
            texte_html += "<br>"
        
        if axes_faibles:
            texte_html += '<strong style="color: #60a5fa;">⚠️ Points à améliorer</strong><br>'
            for axe in axes_faibles:
                texte_html += f"• {axe}<br>"
            texte_html += "<br>"
        
        # ============================================================
        # 2. ANALYSE PRIX MOYEN VS PRIX DE REVIENT
        # ============================================================
        texte_html += '<strong style="color: #60a5fa;">💰 Prix de vente vs Prix de revient</strong><br>'
        
        prix_revient_c1 = c1["depenses_totales_fcfa"] / c1["volume_vendu"] if c1["volume_vendu"] > 0 else 0
        prix_revient_c2 = c2["depenses_totales_fcfa"] / c2["volume_vendu"] if c2["volume_vendu"] > 0 else 0
        prix_revient_c3 = c3["depenses_totales_fcfa"] / c3["volume_vendu"] if c3["volume_vendu"] > 0 else 0
        
        meilleur_prix = "C1" if prix_c1 == max(prix_c1, prix_c2, prix_c3) else ("C2" if prix_c2 == max(prix_c1, prix_c2, prix_c3) else "C3")
        meilleur_cout = "C1" if prix_revient_c1 == min(prix_revient_c1, prix_revient_c2, prix_revient_c3) else ("C2" if prix_revient_c2 == min(prix_revient_c1, prix_revient_c2, prix_revient_c3) else "C3")
        
        texte_html += f"""
        • Meilleur prix : <strong>{meilleur_prix}</strong> ({max(prix_c1, prix_c2, prix_c3):.0f} FCFA)<br>
        • Meilleur coût de revient : <strong>{meilleur_cout}</strong> ({min(prix_revient_c1, prix_revient_c2, prix_revient_c3):.0f} FCFA)<br>
        • Écart C1 vs C3 : prix −{prix_c1 - prix_c3:.0f} FCFA, coût −{prix_revient_c1 - prix_revient_c3:.0f} FCFA<br>
        """
        
        if meilleur_prix == "C1" and meilleur_cout == "C3":
            texte_html += f"✅ Combinaison gagnante à viser : prix du C1 + coût du C3 → marge potentielle de <strong>+{prix_c1 - prix_revient_c3:.0f} FCFA/sujet</strong><br>"
        
        texte_html += """
        <br><strong style="color: #60a5fa;">🎯 Recommandation</strong><br>
        • Cycle 1 : réduire le coût de revient (appliquer les pratiques de C3)<br>
        • Cycle 3 : augmenter le prix de vente (retour au niveau C1)<br>
        • Objectif C4 : prix ≥ 2 700 FCFA, coût de revient ≤ 2 500 FCFA → marge ≥ 200 FCFA/sujet<br><br>
        """
        
        # ============================================================
        # 3. ANALYSE DU SEUIL DE RENTABILITÉ
        # ============================================================
        texte_html += '<strong style="color: #60a5fa;">🎯 Seuil de rentabilité</strong><br>'
        
        ca_c3 = c3["ca_fcfa"] if c3 is not None else 0
        seuil_c3 = c3.get("seuil_rentabilite_fcfa", 0)
        point_mort_c3 = c3.get("point_mort_jours", 0)
        
        if seuil_c3 > 0:
            couverture = (ca_c3 / seuil_c3) * 100
            ecart = seuil_c3 - ca_c3
            augmentation_necessaire = ((seuil_c3 - ca_c3) / ca_c3) * 100 if ca_c3 > 0 else 0
            
            texte_html += f"""
            <strong>Cycle 3 uniquement</strong> (données disponibles) :<br>
            • Seuil de rentabilité : <strong>{seuil_c3/1e6:.1f} M FCFA</strong><br>
            • CA réalisé : <strong>{ca_c3/1e6:.1f} M FCFA</strong><br>
            • Couverture : <strong>{couverture:.0f}%</strong> du seuil<br>
            • Écart à combler : <strong>{ecart/1e6:.1f} M FCFA</strong><br>
            • Point mort : <strong>{point_mort_c3:.0f} jours</strong> (cycle = 53 jours)<br>
            """
            
            if ca_c3 < seuil_c3:
                texte_html += f"""
                <br><strong>Analyse</strong> :<br>
                • Le CA est insuffisant pour atteindre le seuil de rentabilité<br>
                • Le cycle n'est <strong>jamais rentable</strong> sur sa durée (point mort > 53 jours)<br>
                • Il faudrait augmenter le CA de <strong>{augmentation_necessaire:.0f}%</strong> pour atteindre l'équilibre<br>
                <br><strong style="color: #60a5fa;">🎯 Recommandations</strong> (leviers pour C4) :<br>
                • Augmenter le prix de vente de <strong>+250 FCFA/sujet</strong> (gain ≈ +1,2 M FCFA)<br>
                • Ou augmenter le volume de <strong>+1 800 sujets</strong> (à 6 800 sujets)<br>
                • Ou réduire les charges fixes de <strong>−1,0 M FCFA</strong><br>
                • Ou combiner plusieurs leviers (prix + volume + coûts)<br>
                """
            else:
                texte_html += "<br>✅ Cycle rentable : le seuil de rentabilité est atteint<br>"
        else:
            texte_html += """
            <strong>Cycles 1 et 2</strong> : seuil de rentabilité non calculé (données insuffisantes)<br>
            → Pour les prochains cycles, estimer le seuil à partir du ratio charges fixes / marge sur coûts variables<br>
            """
        
        texte_html += "<br>"
        
        # Afficher la carte unique
        afficher_interpretation("⚖️ Bilan Comparatif - Synthèse", texte_html)

    else:
        st.info("Données insuffisantes pour générer l'analyse comparative")
        
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
        "ROI": max(0, 50 + c3.get("roi_pct", -100) * 2) if c3.get("roi_pct", -100) > -50 else 0,
    }
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
            textfont=dict(size=12, color="#9ca3af")
        ))
        fig_sc.update_layout(
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
            height=220, margin=dict(l=12,r=60,t=20,b=12),
            xaxis=dict(range=[0,120], gridcolor=GRID_COLOR, showticklabels=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
            title=dict(text="Décomposition du Score", font=dict(family="Syne",size=14,color="#f0ece4"))
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # === OPTIMISATION DU JOUR DE VENTE (AVEC PERTES RÉELLES) ===
    st.markdown("---")
    st.markdown("### ⏱️ Analyse du jour optimal de vente")
    st.markdown("""
    Cette analyse compare chaque jour :
    - **Dépenses cumulées** depuis le début du cycle
    - **Valeur estimée du lot** (poids total × prix de vente au kg), en tenant compte :
    - **Mortalité réelle** (sujets morts)
    - **Sujets vendus** (si déjà commencé)

    👉 Le **jour optimal** est celui où la **différence (valeur − dépenses) est maximale**.
    Vendre après ce jour réduit la marge.
    """)

    # Sélection du cycle
    cycle_opt = st.selectbox("Choisir un cycle pour l'analyse", CYCLES, key="opt_cycle")
    j_opt = journalier[journalier["cycle_id"] == cycle_opt].copy()
    c_opt = cycles_recap[cycles_recap["cycle_id"] == cycle_opt].iloc[0]

    if not j_opt.empty:

        # Paramètres fixes
        prix_sac = 18000          # FCFA
        poids_sac = 50            # kg
        prix_kg_aliment = prix_sac / poids_sac   # 360 FCFA/kg

        # Prix de vente moyen au kg (constant sur le cycle)
        if c_opt["poids_final_kg"] > 0 and c_opt["prix_moyen_fcfa"] > 0:
            prix_vente_kg = c_opt["prix_moyen_fcfa"] / c_opt["poids_final_kg"]
        else:
            prix_vente_kg = 0

        # Charges fixes quotidiennes (salaires + loyer) / durée du cycle
        duree_cycle = c_opt.get("duree_jours", 60)
        charges_fixes_totales = c_opt.get("cout_salaires_fcfa", 0) + c_opt.get("cout_loyer_fcfa", 0)
        charges_fixes_par_jour = charges_fixes_totales / duree_cycle if duree_cycle > 0 else 0

        # Coûts initiaux (poussins, médical, litière, transport)
        couts_initiaux = (
            c_opt.get("cout_poussins_fcfa", 0) +
            c_opt.get("cout_medical_fcfa", 0) +
            c_opt.get("cout_litiere_fcfa", 0) +
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
            st.warning("⚠️ Pas assez de pesées pour interpoler la croissance. Ajoutez au moins 2 pesées par cycle.")
            st.stop()

        # === PRISE EN COMPTE DES PERTES RÉELLES ===
        # Nombre de sujets restants (effectif restant)
        j_opt["sujets_restants"] = j_opt["effectif_restant"]
        
        # Calcul des dépenses cumulées
        j_opt["cout_aliment_jour"] = j_opt["conso_jour"] * prix_kg_aliment
        j_opt["charges_fixes_jour"] = charges_fixes_par_jour
        j_opt["depenses_jour"] = j_opt["cout_aliment_jour"] + j_opt["charges_fixes_jour"]
        j_opt["depenses_cumulees"] = couts_initiaux + j_opt["depenses_jour"].cumsum()
        
        # Valeur estimée du lot avec prise en compte des pertes
        # = poids estimé × prix au kg × nombre de sujets restants (pas seulement le volume vendu)
        j_opt["valeur_lot"] = j_opt["poids_estime"] * prix_vente_kg * j_opt["sujets_restants"]
        
        # Marge (différence entre valeur du lot et dépenses cumulées)
        j_opt["diff_valeur_depenses"] = j_opt["valeur_lot"] - j_opt["depenses_cumulees"]
        
        # Remplacer les valeurs NaN (début de cycle) par 0
        j_opt["diff_valeur_depenses"] = j_opt["diff_valeur_depenses"].fillna(0)
        
        # Trouver le jour optimal (différence maximale, en excluant les jours sans valeur)
        df_valide = j_opt[j_opt["valeur_lot"].notna() & (j_opt["valeur_lot"] > 0)]
        if not df_valide.empty:
            idx_opt = df_valide["diff_valeur_depenses"].idxmax()
            jour_optimal = int(j_opt.loc[idx_opt, "jour"])
            diff_max = j_opt.loc[idx_opt, "diff_valeur_depenses"]
            valeur_opt = j_opt.loc[idx_opt, "valeur_lot"]
            depenses_opt = j_opt.loc[idx_opt, "depenses_cumulees"]
            sujets_restants_opt = j_opt.loc[idx_opt, "sujets_restants"]
        else:
            jour_optimal = None
            diff_max = 0

        # Graphique
        fig_opt = go.Figure()
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["valeur_lot"],
            name="Valeur estimée du lot (avec pertes)", mode="lines+markers",
            line=dict(color="#34d399", width=2)
        ))
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["depenses_cumulees"],
            name="Dépenses cumulées", mode="lines+markers",
            line=dict(color="#f87171", width=2)
        ))
        fig_opt.add_trace(go.Scatter(
            x=j_opt["jour"], y=j_opt["diff_valeur_depenses"],
            name="Marge (valeur − dépenses)", mode="lines+markers",
            line=dict(color="#fbbf24", width=2.5, dash="dot")
        ))
        fig_opt.add_hline(y=0, line_dash="dot", line_color="#6b7280")
        
        if jour_optimal:
            fig_opt.add_vline(x=jour_optimal, line_dash="dash", line_color="#fbbf24",
                            annotation_text=f"Jour optimal : {jour_optimal}",
                            annotation_position="top right")

        plotly_dark_layout(fig_opt, "Comparaison : Valeur du lot (avec pertes) vs Dépenses cumulées", 450)
        fig_opt.update_yaxes(title_text="FCFA")
        fig_opt.update_xaxes(title_text="Jour du cycle")
        st.plotly_chart(fig_opt, use_container_width=True)

        # Résultat textuel
        if jour_optimal:
            st.markdown(f"""
            **📌 Résultat pour le {cycle_opt} (avec prise en compte des pertes)** :
            - **Jour optimal de vente : J{jour_optimal}**
            - Sujets restants à J{jour_optimal} : **{sujets_restants_opt:,.0f}** têtes
            - Valeur estimée du lot à J{jour_optimal} : **{valeur_opt/1e6:.2f} M FCFA**
            - Dépenses cumulées à J{jour_optimal} : **{depenses_opt/1e6:.2f} M FCFA**
            - Marge maximale : **{diff_max/1e6:.2f} M FCFA**
            
            💡 **Interprétation** :  
            - Avant **J{jour_optimal}** : la valeur du lot augmente plus vite que les dépenses  
            - Après **J{jour_optimal}** : les dépenses supplémentaires ne sont plus rentabilisées  
            ✅ **Vendre au plus tard à J{jour_optimal} pour maximiser la marge**
            """)
        else:
            st.markdown(f"""
            **⚠️ Résultat pour le {cycle_opt}** :
            - Impossible de déterminer un jour optimal
            - Vérifiez que les données de pesée et de mortalité sont complètes
            """)

        # Simulation interactive
        st.markdown("---")
        st.markdown("### 🔮 Simulation - Impact du jour de vente sur la marge")

        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            jour_sim = st.slider("Jour de vente simulé", int(j_opt["jour"].min()), int(j_opt["jour"].max()), jour_optimal if jour_optimal else 40, key="jour_sim")
        with col_sim2:
            prix_sim = st.number_input("Prix de vente unitaire (FCFA)", value=int(c_opt["prix_moyen_fcfa"]), step=50, key="prix_sim")

        ligne_sim = j_opt[j_opt["jour"] == jour_sim]
        if not ligne_sim.empty:
            poids_sim = ligne_sim["poids_estime"].iloc[0]
            sujets_sim = ligne_sim["sujets_restants"].iloc[0]
            valeur_sim = poids_sim * (prix_sim / c_opt["poids_final_kg"]) * sujets_sim if c_opt["poids_final_kg"] > 0 else 0
            depenses_sim = ligne_sim["depenses_cumulees"].iloc[0]
            marge_sim = valeur_sim - depenses_sim
            marge_unitaire_sim = marge_sim / sujets_sim if sujets_sim > 0 else 0

            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            with col_r1:
                st.metric("Poids estimé", f"{poids_sim:.2f} kg")
            with col_r2:
                st.metric("Sujets restants", f"{sujets_sim:,.0f}")
            with col_r3:
                st.metric("Valeur estimée", f"{valeur_sim/1e6:.2f} M FCFA")
            with col_r4:
                st.metric("Marge simulée", f"{marge_sim:+,.0f} FCFA", delta=f"{marge_unitaire_sim:+.0f} FCFA/sujet")

            if marge_sim > 0:
                st.success(f"✅ En vendant au **J{jour_sim}** à **{prix_sim} FCFA**, le cycle est rentable.")
            else:
                st.warning(f"⚠️ En vendant au **J{jour_sim}** à **{prix_sim} FCFA**, le cycle reste déficitaire.")
                
                # Afficher l'ajustement nécessaire
                if prix_sim < 2800:
                    st.info(f"💡 **Ajustement possible** : Augmentez le prix de vente à 2 800 FCFA ou réduisez le coût alimentaire.")
        else:
            st.info("Données insuffisantes pour la simulation.")

    else:
        st.info("Données insuffisantes pour ce cycle.")

    # === PLAN D'ACTION DÉTAILLÉ ===
    st.markdown('<div class="section-header">📋 Plan d\'action détaillé</div>', unsafe_allow_html=True)

    # Récupérer les données des 3 cycles
    c1 = cycles_recap[cycles_recap["cycle_id"] == "Cycle1"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle1"]) > 0 else None
    c2 = cycles_recap[cycles_recap["cycle_id"] == "Cycle2"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle2"]) > 0 else None
    c3 = cycles_recap[cycles_recap["cycle_id"] == "Cycle3"].iloc[0] if len(cycles_recap[cycles_recap["cycle_id"] == "Cycle3"]) > 0 else None

    # Onglets
    tab_urg, tab_surv, tab_forts = st.tabs(["🔴 URGENTES", "🟡 À SURVEILLER", "🟢 POINTS FORTS"])

    # ============================================================
    # ONGLET 1 : URGENTES
    # ============================================================
    with tab_urg:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #f87171; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                ⚠️ À traiter immédiatement
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        urgence_cards = []
        
        # 1. Marge unitaire négative (tous cycles)
        if c1 is not None and c2 is not None and c3 is not None:
            urgence_cards.append({
                "titre": "📉 Marge unitaire négative",
                "contenu": f"C1 : {c1['marge_unitaire_fcfa']:.0f} FCFA | C2 : {c2['marge_unitaire_fcfa']:.0f} FCFA | C3 : {c3['marge_unitaire_fcfa']:.0f} FCFA",
                "action": "Objectif : atteindre ≥ 200 FCFA/sujet pour tous les cycles",
                "cycle": "Tous"
            })
        
        # 2. Prix de vente trop bas (Cycle 3)
        if c3 is not None and c1 is not None and c3['prix_moyen_fcfa'] < 2600:
            urgence_cards.append({
                "titre": "💰 Prix de vente trop bas",
                "contenu": f"Cycle 3 : {c3['prix_moyen_fcfa']:.0f} FCFA (C1 : {c1['prix_moyen_fcfa']:.0f} FCFA)",
                "action": "Augmenter de +250 à 300 FCFA pour revenir au niveau du Cycle 1",
                "cycle": "C3"
            })
        
        # 3. Coût alimentaire trop élevé (Cycle 3)
        if c3 is not None and c3['depenses_totales_fcfa'] > 0:
            part_aliment = (c3['cout_aliment_fcfa'] / c3['depenses_totales_fcfa']) * 100
            if part_aliment > 50:
                urgence_cards.append({
                    "titre": "🍗 Coût alimentaire trop élevé",
                    "contenu": f"Cycle 3 : l'aliment représente {part_aliment:.1f}% des charges",
                    "action": "Négocier le prix des sacs (18 000 FCFA), réduire le gaspillage",
                    "cycle": "C3"
                })
        
        # 4. Seuil de rentabilité non atteint (Cycle 3)
        if c3 is not None:
            seuil_c3 = c3.get('seuil_rentabilite_fcfa', 0)
            if seuil_c3 > 0 and c3['ca_fcfa'] < seuil_c3:
                couverture = (c3['ca_fcfa'] / seuil_c3) * 100
                urgence_cards.append({
                    "titre": "🎯 Seuil de rentabilité non atteint",
                    "contenu": f"Cycle 3 : CA = {c3['ca_fcfa']/1e6:.1f} M FCFA | Seuil = {seuil_c3/1e6:.1f} M FCFA ({couverture:.0f}%)",
                    "action": "Augmenter le CA de 37% ou réduire les charges fixes",
                    "cycle": "C3"
                })
        
        # 5. Point mort trop tardif (Cycle 3)
        if c3 is not None:
            point_mort = c3.get('point_mort_jours', 0)
            if point_mort > 53:
                urgence_cards.append({
                    "titre": "⏱️ Point mort trop tardif",
                    "contenu": f"Cycle 3 : point mort à {point_mort:.0f} jours (cycle = 53 jours)",
                    "action": "Le cycle n'est jamais rentable → réduire les charges fixes",
                    "cycle": "C3"
                })
        
        # 6. Reliquat non vendu (C1 et C2)
        for cycle, nom in [(c1, "C1"), (c2, "C2")]:
            if cycle is not None and cycle['effectif_initial'] > 0:
                taux_reliquat = (cycle['effectif_final'] / cycle['effectif_initial']) * 100
                if taux_reliquat > 5:
                    urgence_cards.append({
                        "titre": f"📦 Reliquat non vendu ({nom})",
                        "contenu": f"{cycle['effectif_final']} sujets non vendus ({taux_reliquat:.1f}%)",
                        "action": "Vendre en plus petits lots en fin de cycle",
                        "cycle": nom
                    })
        
        # 7. Résultat net déficitaire (C2)
        if c2 is not None and c2['resultat_net_fcfa'] < 0:
            urgence_cards.append({
                "titre": "📉 Résultat net très déficitaire",
                "contenu": f"Cycle 2 : {c2['resultat_net_fcfa']:,.0f} FCFA de perte",
                "action": "Revoyer la stratégie commerciale et les coûts avant le prochain cycle",
                "cycle": "C2"
            })
        
        # Affichage des cartes
        if urgence_cards:
            for car in urgence_cards[:6]:
                st.markdown(f"""
                <div class="reco-card reco-urgente" style="margin-bottom: 12px;">
                    <div class="reco-titre" style='color:#fca5a5'>{car['titre']}</div>
                    <div class="reco-texte">{car['contenu']}</div>
                    <div class="reco-texte" style='color:#fbbf24; margin-top: 8px;'>🎯 {car['action']}</div>
                    <div class="reco-texte" style='color:#6b7280; margin-top: 6px; font-size: 10px;'>📌 Cycle concerné : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Aucune urgence détectée.")

    # ============================================================
    # ONGLET 2 : À SURVEILLER
    # ============================================================
    with tab_surv:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #fbbf24; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                👁️ Surveillance régulière
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        surveillance_cards = []
        
        # 1. Prix en baisse constante
        if c1 is not None and c2 is not None and c3 is not None:
            if c1['prix_moyen_fcfa'] > c2['prix_moyen_fcfa'] > c3['prix_moyen_fcfa']:
                surveillance_cards.append({
                    "titre": "📉 Prix de vente en baisse constante",
                    "contenu": f"C1: {c1['prix_moyen_fcfa']:.0f} → C2: {c2['prix_moyen_fcfa']:.0f} → C3: {c3['prix_moyen_fcfa']:.0f} FCFA",
                    "action": "Inverser la tendance, cibler 2 700-2 800 FCFA",
                    "cycle": "Tous"
                })
        
        # 2. Premier jour de vente tardif
        for cycle, nom, jour_vente in [(c1, "C1", 34), (c2, "C2", 38), (c3, "C3", 36)]:
            if cycle is not None and jour_vente > 38:
                surveillance_cards.append({
                    "titre": f"📅 Premier jour de vente tardif ({nom})",
                    "contenu": f"Première vente : J{jour_vente}",
                    "action": "Anticiper les ventes avant J40",
                    "cycle": nom
                })
                break
        
        # 3. Charges fixes lourdes (C1 et C2)
        for cycle, nom in [(c1, "C1"), (c2, "C2")]:
            if cycle is not None and cycle['volume_vendu'] < 2000:
                part_fixes = (cycle.get('cout_salaires_fcfa', 0) + cycle.get('cout_loyer_fcfa', 0)) / cycle['depenses_totales_fcfa'] * 100 if cycle['depenses_totales_fcfa'] > 0 else 0
                if part_fixes > 30:
                    surveillance_cards.append({
                        "titre": f"🏢 Charges fixes lourdes ({nom})",
                        "contenu": f"Volume : {cycle['volume_vendu']} sujets, charges fixes : {part_fixes:.0f}%",
                        "action": "Augmenter la taille des cycles (3 000-5 000 sujets)",
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
                        "titre": "📊 Lot hétérogène",
                        "contenu": f"Cycle 3 : écart de {ecart:.2f} kg entre plus lourds et plus faibles",
                        "action": "Trier les sujets par poids, ajuster la densité",
                        "cycle": "C3"
                    })
        
        # 5. IC à surveiller (C3)
        if c3 is not None:
            ic_c3 = c3.get('ic_calcule', 0) or c3.get('ic_standard', 0)
            if ic_c3 > 1.7:
                surveillance_cards.append({
                    "titre": "📊 Indice de consommation à surveiller",
                    "contenu": f"Cycle 3 : IC = {ic_c3:.2f} (cible ≤ 1,7)",
                    "action": "Améliorer l'efficacité alimentaire",
                    "cycle": "C3"
                })
        
        # 6. Étalement des ventes (C3)
        surveillance_cards.append({
            "titre": "📦 Étalement des ventes",
            "contenu": "Cycle 3 : ventes étalées sur plusieurs jours",
            "action": "Regrouper les livraisons pour réduire les coûts de transport",
            "cycle": "C3"
        })
        
        # Affichage
        if surveillance_cards:
            for car in surveillance_cards[:5]:
                st.markdown(f"""
                <div class="reco-card reco-attention" style="margin-bottom: 12px;">
                    <div class="reco-titre" style='color:#fde68a'>{car['titre']}</div>
                    <div class="reco-texte">{car['contenu']}</div>
                    <div class="reco-texte" style='color:#fbbf24; margin-top: 8px;'>🎯 {car['action']}</div>
                    <div class="reco-texte" style='color:#6b7280; margin-top: 6px; font-size: 10px;'>📌 Cycle concerné : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Aucun point de vigilance particulier.")

    # ============================================================
    # ONGLET 3 : POINTS FORTS
    # ============================================================
    with tab_forts:
        st.markdown("""
        <div style='margin-bottom: 16px;'>
            <span style='background-color: #34d399; color: #0d0f14; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                🌟 À capitaliser
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        points_forts = []
        
        # 1. Meilleur prix (C1)
        if c1 is not None and c1['prix_moyen_fcfa'] > 2700:
            points_forts.append({
                "titre": "💰 Meilleur prix de vente",
                "contenu": f"Cycle 1 : {c1['prix_moyen_fcfa']:.0f} FCFA/sujet",
                "action": "Objectif à atteindre pour les cycles suivants",
                "cycle": "C1"
            })
        
        # 2. Meilleur coût de revient (C3)
        if c3 is not None and c3['depenses_totales_fcfa'] > 0 and c3['volume_vendu'] > 0:
            cout_revient = c3['depenses_totales_fcfa'] / c3['volume_vendu']
            points_forts.append({
                "titre": "🏭 Meilleur coût de revient",
                "contenu": f"Cycle 3 : {cout_revient:.0f} FCFA/sujet",
                "action": "Appliquable aux cycles 1 et 2",
                "cycle": "C3"
            })
        
        # 3. Montée en volume réussie
        if c1 is not None and c3 is not None and c3['volume_vendu'] > c1['volume_vendu'] * 4:
            points_forts.append({
                "titre": "📈 Montée en volume réussie",
                "contenu": f"×{c3['volume_vendu']/c1['volume_vendu']:.1f} entre C1 et C3",
                "action": "Capacité opérationnelle prouvée",
                "cycle": "C1→C3"
            })
        
        # 4. IC maîtrisé (C3)
        if c3 is not None:
            ic_c3 = c3.get('ic_calcule', 0) or c3.get('ic_standard', 0)
            if ic_c3 <= 1.7:
                points_forts.append({
                    "titre": "✅ Indice de consommation maîtrisé",
                    "contenu": f"Cycle 3 : IC = {ic_c3:.2f} (cible ≤ 1,7)",
                    "action": "Maintenir cette efficacité alimentaire",
                    "cycle": "C3"
                })
        
        # 5. Mortalité maîtrisée (C3)
        if c3 is not None and c3['taux_mortalite_pct'] <= 4:
            points_forts.append({
                "titre": "🩺 Mortalité maîtrisée",
                "contenu": f"Cycle 3 : {c3['taux_mortalite_pct']:.2f}%",
                "action": "Maintenir la biosécurité",
                "cycle": "C3"
            })
        
        # 6. Trésorerie disponible (C3)
        if c3 is not None:
            treso = c3.get('tresorerie_disponible_fcfa', 0)
            if treso > 0:
                points_forts.append({
                    "titre": "💰 Trésorerie disponible",
                    "contenu": f"{treso/1e6:.1f} M FCFA",
                    "action": "Capacité à financer le Cycle 4",
                    "cycle": "C3"
                })
        
        # 7. Reliquat nul (C2)
        if c2 is not None and c2['effectif_final'] == 0:
            points_forts.append({
                "titre": "✅ Reliquat nul",
                "contenu": "Cycle 2 : tous les sujets ont été vendus",
                "action": "Bonne gestion commerciale à reproduire",
                "cycle": "C2"
            })
        
        # Affichage
        if points_forts:
            for car in points_forts:
                st.markdown(f"""
                <div class="reco-card reco-positive" style="margin-bottom: 12px;">
                    <div class="reco-titre" style='color:#6ee7b7'>{car['titre']}</div>
                    <div class="reco-texte">{car['contenu']}</div>
                    <div class="reco-texte" style='color:#34d399; margin-top: 8px;'>💡 {car['action']}</div>
                    <div class="reco-texte" style='color:#6b7280; margin-top: 6px; font-size: 10px;'>📌 Cycle concerné : {car['cycle']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Capitalisez sur vos succès pour les cycles futurs.")

    
st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:48px; padding:20px 0; border-top:1px solid #1e2230; text-align:center;
     font-size:11px; color:#374151; letter-spacing:0.06em; text-transform:uppercase;'>
    Dashboard Avicole INIS · Diagnostic Financier 3 Cycles · Poulets de Chair
</div>
""", unsafe_allow_html=True)