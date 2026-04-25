import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AgriTech | Vertical Farm Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour une interface plus moderne
st.markdown("""
<style>
    .main { background-color: #f4fcf4; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #1b5e20; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    h1, h2, h3 { color: #1b5e20; }
</style>
""", unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
DATA_FILE = "vertical_farm_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        # Création d'un dataframe vide avec les bonnes colonnes
        df = pd.DataFrame(columns=[
            "Date", "Type_Plante", "Eau_Consommee_L", 
            "Niveau_pH", "Heures_Lumiere", 
            "Rendement_Recolte_kg", "Score_Qualite"
        ])
    
    # Forcer le type numérique pour éviter les erreurs Plotly
    cols_num = ["Eau_Consommee_L", "Niveau_pH", "Heures_Lumiere", "Rendement_Recolte_kg", "Score_Qualite"]
    for col in cols_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Chargement dans la session pour réactivité immédiate
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# --- SIDEBAR: FORMULAIRE DE COLLECTE ---
st.sidebar.title("🌿 AgriTech Input")
st.sidebar.header("📝 Saisie des Données")
st.sidebar.markdown("Enregistrez les métriques journalières ou par cycle de la serre verticale.")

with st.sidebar.form("farm_form"):
    date_input = st.date_input("Date de la mesure", datetime.today())
    plante = st.selectbox("Type de Culture", ["Laitue", "Basilic", "Épinard", "Tomate Cerise", "Coriandre"])
    eau = st.number_input("Eau Consommée (Litres)", min_value=0.0, value=15.5, step=0.5)
    ph = st.slider("Niveau de pH de la Solution", min_value=0.0, max_value=14.0, value=6.0, step=0.1)
    lumiere = st.number_input("Exposition Lumineuse (Heures)", min_value=0.0, max_value=24.0, value=16.0, step=0.5)
    rendement = st.number_input("Rendement Récolte (kg)", min_value=0.0, value=5.0, step=0.1)
    qualite = st.slider("Score de Qualité Visuelle (/10)", min_value=1, max_value=10, value=8)
    
    submitted = st.form_submit_button("🌱 Enregistrer les données")
    
    if submitted:
        new_data = {
            "Date": date_input.strftime("%Y-%m-%d"),
            "Type_Plante": plante,
            "Eau_Consommee_L": eau,
            "Niveau_pH": ph,
            "Heures_Lumiere": lumiere,
            "Rendement_Recolte_kg": rendement,
            "Score_Qualite": qualite
        }
        df = st.session_state.data
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        # Trier par date pour la cohérence des graphiques
        df = df.sort_values(by="Date").reset_index(drop=True)
        st.session_state.data = df
        save_data(df)
        st.success("✅ Données agricoles enregistrées avec succès !")

# --- MAIN PAGE: ANALYSE DESCRIPTIVE ---
st.title("🌿 AgriTech: Dashboard de Ferme Verticale")
st.markdown("**Plateforme d'analyse descriptive et de suivi des rendements pour l'agriculture urbaine intelligente.**")

df = st.session_state.data

# Conversion de sécurité pour la session active
cols_num = ["Eau_Consommee_L", "Niveau_pH", "Heures_Lumiere", "Rendement_Recolte_kg", "Score_Qualite"]
if not df.empty:
    for col in cols_num:
        df[col] = pd.to_numeric(df[col], errors='coerce')

if df.empty:
    st.info("📊 Aucune donnée enregistrée. Veuillez remplir le formulaire dans la barre latérale pour commencer l'analyse.")
else:
    # --- KPIs ---
    st.markdown("### 🎯 Indicateurs de Performance Globaux (KPIs)")
    col1, col2, col3, col4 = st.columns(4)
    
    total_recolte = df["Rendement_Recolte_kg"].sum()
    eau_totale = df["Eau_Consommee_L"].sum()
    score_moyen = df["Score_Qualite"].mean()
    # Efficacité hydrique : litres d'eau nécessaires pour produire 1 kg
    eff_hydrique = eau_totale / total_recolte if total_recolte > 0 else 0

    col1.metric("Récolte Totale", f"{total_recolte:.1f} kg")
    col2.metric("Eau Consommée", f"{eau_totale:.1f} L")
    col3.metric("Qualité Moyenne", f"{score_moyen:.1f} / 10")
    col4.metric("Efficacité Hydrique", f"{eff_hydrique:.2f} L/kg", help="Plus c'est bas, plus le système est efficient !")

    st.markdown("---")
    
    # --- CHARTS ---
    st.markdown("### 📈 Analyses Descriptives et Croisées")
    
    tab1, tab2, tab3 = st.tabs(["Performance par Culture", "Suivi Environnemental", "Base de Données Exploratoire"])
    
    with tab1:
        st.subheader("Rendement et Qualité selon le Type de Plante")
        col_fig1, col_fig2 = st.columns(2)
        
        # Pie chart du rendement
        df_groupe = df.groupby("Type_Plante")["Rendement_Recolte_kg"].sum().reset_index()
        fig1 = px.pie(df_groupe, values='Rendement_Recolte_kg', names='Type_Plante', hole=0.4,
                      title="Répartition des Récoltes", color_discrete_sequence=px.colors.sequential.Greens_r)
        col_fig1.plotly_chart(fig1, use_container_width=True)
        
        # Bar chart de la qualité
        df_qualite = df.groupby("Type_Plante")["Score_Qualite"].mean().reset_index()
        fig2 = px.bar(df_qualite, x='Type_Plante', y='Score_Qualite', 
                      title="Score de Qualité Moyen", color='Score_Qualite',
                      color_continuous_scale='YlGn')
        col_fig2.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Corrélations Environnementales (Variables Multiples)")
        
        # Scatter plot multidimensionnel
        fig3 = px.scatter(df, x="Heures_Lumiere", y="Rendement_Recolte_kg", 
                          size="Eau_Consommee_L", color="Niveau_pH", hover_name="Type_Plante",
                          title="Impact Lumière/pH sur Rendement (Taille de bulle = Eau)",
                          color_continuous_scale='Teal')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Line chart temporel
        fig4 = px.line(df, x="Date", y=["Niveau_pH", "Heures_Lumiere"], markers=True,
                       title="Suivi Temporel de l'Environnement (pH & Lumière)")
        st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("Gestion et Export des Données")
        st.markdown("Tableau brut avec mise en évidence des valeurs maximales.")
        st.dataframe(df.style.highlight_max(axis=0, subset=['Rendement_Recolte_kg', 'Score_Qualite'], color='lightgreen'), use_container_width=True)
        
        # Bouton de téléchargement
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exporter la base de données (CSV)",
            data=csv,
            file_name='vertical_farm_data.csv',
            mime='text/csv',
        )

# Footer
st.markdown("---")
st.caption("Développé avec 💚 en Python & Streamlit pour l'agriculture urbaine de demain.")
