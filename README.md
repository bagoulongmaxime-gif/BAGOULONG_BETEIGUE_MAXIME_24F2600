# 💻 DevLife Analytics

Une application web Python interactive (Streamlit) pour collecter, analyser et visualiser les habitudes de vie et la productivité d'un étudiant en informatique.

## 🌟 Fonctionnalités (Niveau L2 Info)
- **Collecte de données :** Formulaire interactif pour saisir les statistiques quotidiennes (heures de code, sommeil, stress, tasses de café, bugs résolus).
- **Stockage local :** Les données sont sauvegardées de manière persistante dans un fichier `dev_data.csv`.
- **Tableau de Bord Dynamique (Analyse descriptive) :** 
  - Graphique linéaire comparant le temps de code et le temps de sommeil.
  - Nuage de points analysant la relation entre le café consommé, le stress et les bugs résolus.
  - Graphique circulaire pour la répartition des langages de programmation.
  - Matrice de corrélation automatique générée avec Plotly.

## 🚀 Comment lancer le projet en local ?

1. Assurez-vous d'avoir Python installé (idéalement Python 3.8+).
2. Installez les dépendances nécessaires en tapant cette commande dans le terminal :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancez l'application avec Streamlit :
   ```bash
   streamlit run app.py
   ```

## 🌍 Comment mettre l'application en ligne gratuitement ?

Pour qu'elle soit accessible à tout le monde, vous pouvez la déployer gratuitement sur **Streamlit Community Cloud** :

1. **GitHub :** Créez un compte sur [GitHub](https://github.com/) et créez un nouveau dépôt public (repository).
2. **Ajouter les fichiers :** Uploadez les fichiers `app.py` et `requirements.txt` dans votre dépôt GitHub. *(Ne pas uploader dev_data.csv s'il est vide, l'app le créera automatiquement)*.
3. **Streamlit Cloud :** Allez sur [Streamlit Community Cloud](https://share.streamlit.io/), connectez-vous avec votre compte GitHub.
4. **Déployer :** Cliquez sur "New app", sélectionnez votre dépôt GitHub, la branche (généralement `main`), et le fichier principal (`app.py`).
5. **C'est en ligne !** Streamlit vous donnera une URL publique (ex: `https://votre-app.streamlit.app`) que vous pourrez partager à votre professeur.

*Note de conception :*
*Le choix de ce sujet (Self-Analytics du développeur) montre une créativité et une application directe de l'informatique au profil de l'étudiant, tout en mobilisant des compétences clés en analyse de données (Pandas) et dataviz (Plotly).*
