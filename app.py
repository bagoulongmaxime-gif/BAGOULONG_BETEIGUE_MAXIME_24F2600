import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import date

# -----------------------------------------------------------------------------
# CONFIGURATION DE LA PAGE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DevLife Analytics",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

import time

# -----------------------------------------------------------------------------
# SPLASH SCREEN (LOGO AU LANCEMENT)
# -----------------------------------------------------------------------------
if 'splash_shown' not in st.session_state:
    splash = st.empty()
    with splash.container():
        st.markdown("<br>", unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 20px;'>DevLife Analytics</h1>", unsafe_allow_html=True)
            
            # Affichage de l'image de l'équipement informatique (logo)
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
            
            st.markdown("<p style='text-align: center; font-size: 20px; color: #666;'>Chargement de vos données de productivité...</p>", unsafe_allow_html=True)
            
            # Barre de progression animée sur 5 secondes (100 itérations * 0.05s)
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.05)  # 100 * 0.05 = 5 secondes
                progress_bar.progress(percent_complete + 1)
            
    # Vider le conteneur du splash screen une fois terminé
    splash.empty()
    st.session_state.splash_shown = True

# -----------------------------------------------------------------------------
# CONSTANTES ET FICHIER DE DONNÉES
# -----------------------------------------------------------------------------
DATA_FILE = "dev_data.csv"

def load_data():
    """Charge les données depuis le fichier CSV. Si le fichier n'existe pas, crée un DataFrame vide."""
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # S'assurer que la colonne Date est au format datetime
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        # Rétrocompatibilité : si des données existent sans la colonne "Nom de l'étudiant"
        if "Nom de l'étudiant" not in df.columns:
            df.insert(1, "Nom de l'étudiant", "Anonyme")
            
        # S'assurer que les colonnes numériques ont le bon type
        colonnes_numeriques = ["Heures de Code", "Tasses de Café", "Heures de Sommeil", "Niveau de Stress (1-10)", "Bugs Résolus"]
        for col in colonnes_numeriques:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
        return df
    else:
        # Création des colonnes par défaut si aucune donnée
        return pd.DataFrame(columns=[
            "Date", "Nom de l'étudiant", "Heures de Code", "Tasses de Café", 
            "Heures de Sommeil", "Niveau de Stress (1-10)", 
            "Bugs Résolus", "Langage Principal"
        ])

def save_data(df):
    """Sauvegarde le DataFrame dans le fichier CSV."""
    df.to_csv(DATA_FILE, index=False)

# -----------------------------------------------------------------------------
# INITIALISATION DES DONNÉES
# -----------------------------------------------------------------------------
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# -----------------------------------------------------------------------------
# BARRE LATÉRALE (SIDEBAR) - SAISIE ET À PROPOS
# -----------------------------------------------------------------------------
st.sidebar.title("💻 DevLife Analytics")
st.sidebar.markdown("---")
st.sidebar.info(
    "Application conçue pour analyser le lien entre "
    "les habitudes de vie d'un étudiant en informatique "
    "et sa productivité."
)

with st.sidebar.expander("✍️ Saisir des Données", expanded=False):
    st.markdown("Enregistrez vos statistiques du jour.")

    with st.form("data_entry_form", clear_on_submit=True):
        nom_etudiant = st.text_input("Nom de l'étudiant", placeholder="Ex: Maxime")
        jour = st.date_input("Date", date.today())
        heures_code = st.number_input("Heures de Code", min_value=0.0, max_value=24.0, value=2.0, step=0.5)
        sommeil = st.number_input("Heures de Sommeil", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        cafe = st.number_input("Tasses de Café", min_value=0, max_value=20, value=1, step=1)
        stress = st.slider("Niveau de Stress (1-10)", 1, 10, 5)
        bugs = st.number_input("Bugs Résolus / Fonctionnalités terminées", min_value=0, max_value=100, value=0, step=1)
        langage = st.selectbox("Langage Principal", ["Python", "Java", "C++", "C", "JavaScript", "HTML/CSS", "Autre"])

        submit_button = st.form_submit_button(label="💾 Enregistrer", use_container_width=True)

        if submit_button:
            if not nom_etudiant.strip():
                st.sidebar.error("❌ Le nom de l'étudiant est obligatoire !")
            else:
                new_data = {
                    "Date": jour,
                    "Nom de l'étudiant": nom_etudiant.strip(),
                    "Heures de Code": heures_code,
                    "Tasses de Café": cafe,
                    "Heures de Sommeil": sommeil,
                    "Niveau de Stress (1-10)": stress,
                    "Bugs Résolus": bugs,
                    "Langage Principal": langage
                }
                # Ajout des nouvelles données au DataFrame
                new_df = pd.DataFrame([new_data])
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                
                # Sauvegarde persistante
                save_data(st.session_state.df)
                
                st.sidebar.success("✅ Données enregistrées !")
                st.balloons()

with st.sidebar.expander("⚙️ À Propos de ce projet"):
    st.markdown("""
    ### 🎯 Objectif du Projet
    Conçu comme un projet de niveau **L2 Informatique**, il démontre :
    1. **La collecte de données** interactives.
    2. **Le stockage persistant** (CSV).
    3. **L'analyse descriptive** de l'impact du mode de vie sur la productivité.
    
    ### 🛠️ Technologies
    Python, Streamlit, Pandas, Plotly.
    """)

# -----------------------------------------------------------------------------
# MISE EN PAGE PRINCIPALE : TABLEAU DE BORD
# -----------------------------------------------------------------------------
st.header("📊 Tableau de Bord")

df_complet = st.session_state.df

# S'assurer que la colonne existe pour la session en cours (rétrocompatibilité)
if not df_complet.empty and "Nom de l'étudiant" not in df_complet.columns:
    df_complet.insert(1, "Nom de l'étudiant", "Anonyme")

# Conversion de sécurité pour la session en cours
colonnes_numeriques = ["Heures de Code", "Tasses de Café", "Heures de Sommeil", "Niveau de Stress (1-10)", "Bugs Résolus"]
for col in colonnes_numeriques:
    if col in df_complet.columns:
        df_complet[col] = pd.to_numeric(df_complet[col], errors='coerce').fillna(0)

if df_complet.empty:
    st.warning("⚠️ Aucune donnée disponible. Veuillez d'abord cliquer sur '✍️ Saisir des Données' dans le menu à gauche.")
else:
    # --- FILTRE PAR ÉTUDIANT ---
    st.markdown("### 👤 Filtre Étudiant")
    col_filtre, _ = st.columns([1, 2])
    with col_filtre:
        etudiants_uniques = sorted(df_complet["Nom de l'étudiant"].unique().tolist())
        etudiant_selectionne = st.selectbox(
            "Sélectionnez les résultats à afficher :", 
            ["Tous les étudiants"] + etudiants_uniques
        )
    
    # Filtrer le DataFrame selon le choix
    if etudiant_selectionne == "Tous les étudiants":
        df = df_complet.copy()
    else:
        df = df_complet[df_complet["Nom de l'étudiant"] == etudiant_selectionne].copy()

    if df.empty:
        st.warning(f"Aucune donnée à afficher pour {etudiant_selectionne}.")
    else:
        # Tri par date
        df = df.sort_values(by="Date")

        # --- KPIs (Indicateurs clés de performance) ---
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="Total Heures Codées", value=f"{df['Heures de Code'].sum()} h")
        kpi2.metric(label="Moyenne de Sommeil", value=f"{df['Heures de Sommeil'].mean():.1f} h")
        kpi3.metric(label="Bugs Résolus (Total)", value=int(df['Bugs Résolus'].sum()))
        kpi4.metric(label="Stress Moyen", value=f"{df['Niveau de Stress (1-10)'].mean():.1f} / 10")
        
        st.markdown("---")

        # --- Visualisations avec Onglets (Tabs) pour une meilleure lisibilité ---
        tab1, tab2, tab3 = st.tabs(["Évolution dans le temps", "Corrélations (Café/Bugs/Stress)", "Langages & Corrélation Globale"])

        with tab1:
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(x=df['Date'], y=df['Heures de Code'], mode='lines+markers', name='Heures de Code', line=dict(color='blue')))
            fig_time.add_trace(go.Scatter(x=df['Date'], y=df['Heures de Sommeil'], mode='lines+markers', name='Heures de Sommeil', line=dict(color='green')))
            fig_time.update_layout(xaxis_title="Date", yaxis_title="Heures", margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_time, use_container_width=True)

        with tab2:
            # S'il n'y a qu'un seul point de donnée, le scatter plot peut ne pas bien marcher
            if len(df) > 0:
                fig_scatter = px.scatter(
                    df, x="Tasses de Café", y="Bugs Résolus", 
                    size="Heures de Code", color="Niveau de Stress (1-10)",
                    hover_data=["Date", "Langage Principal", "Nom de l'étudiant"],
                    color_continuous_scale="reds",
                    title="Café vs Bugs (Taille = Heures de Code, Couleur = Stress)"
                )
                fig_scatter.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_scatter, use_container_width=True)
            
        with tab3:
            col_t3_1, col_t3_2 = st.columns(2)
            with col_t3_1:
                lang_counts = df['Langage Principal'].value_counts().reset_index()
                lang_counts.columns = ['Langage Principal', 'Compte']
                if not lang_counts.empty:
                    fig_pie = px.pie(lang_counts, names='Langage Principal', values='Compte', hole=0.4, title="Langages Préférés")
                    fig_pie.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_t3_2:
                numeric_df = df.select_dtypes(include=['float64', 'int64'])
                if len(numeric_df.columns) > 1 and len(numeric_df) > 1:
                    corr = numeric_df.corr()
                    fig_corr = px.imshow(
                        corr, text_auto=".2f", aspect="auto", 
                        color_continuous_scale="RdBu_r", origin='lower',
                        title="Matrice de Corrélation"
                    )
                    fig_corr.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("Plus de données requises pour afficher la matrice de corrélation.")

    st.markdown("---")
    with st.expander("🔍 Voir et gérer les données brutes"):
        st.dataframe(df.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)
        
        # Bouton pour effacer les données avec rechargement
        if st.button("🗑️ Effacer toutes les données", type="primary"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.session_state.df = pd.DataFrame(columns=df_complet.columns)
            st.rerun() # Force le rafraîchissement immédiat de la page
