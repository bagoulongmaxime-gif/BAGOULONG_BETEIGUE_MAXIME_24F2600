# 🌿 AgriTech - Dashboard de Ferme Verticale

Cette application web construite avec **Python et Streamlit** permet la collecte et l'analyse descriptive de données issues d'une ferme d'agriculture urbaine verticale. 

## Fonctionnalités
1. **Collecte robuste** : Formulaire dans le menu latéral pour ajouter les variables liées à une récolte (Eau, pH, Lumière, etc.). Les données sont automatiquement enregistrées dans un fichier CSV.
2. **Analyse Descriptive** :
    - KPIs dynamiques calculant l'efficience hydrique et le rendement total.
    - Graphiques d'analyse croisée grâce à `Plotly` (corrélations multidimensionnelles, répartition en camembert, suivi temporel).
3. **Export** : Fonctionnalité de téléchargement des données brutes en un clic.

---

## 💻 1. Comment exécuter localement

1. Naviguez dans le dossier du projet :
```bash
cd /home/maxius/bagoulong_beteigue_maxime_24f2600/agritech_app
```
2. Installez les dépendances nécessaires :
```bash
pip install -r requirements.txt
```
3. Lancez l'application :
```bash
streamlit run app.py
```
*(Votre navigateur devrait s'ouvrir automatiquement sur `http://localhost:8501`)*

---

## 🌐 2. Comment la mettre en ligne GRATUITEMENT (Déploiement)

La meilleure façon de déployer une application Streamlit de façon robuste, gratuite et permanente est d'utiliser **Streamlit Community Cloud**.

**Étapes à suivre :**
1. **Publier sur GitHub** : 
   - Créez un compte sur [GitHub.com](https://github.com/) (si ce n'est pas déjà fait).
   - Créez un nouveau *Repository* (dépôt) public.
   - Uploadez-y vos fichiers `app.py` et `requirements.txt`.
2. **Déployer sur Streamlit** :
   - Allez sur [share.streamlit.io](https://share.streamlit.io/) et connectez-vous avec votre compte GitHub.
   - Cliquez sur **"New app"**.
   - Sélectionnez votre repository GitHub contenant l'application, choisissez la branche `main` et tapez `app.py` comme *Main file path*.
   - Cliquez sur **"Deploy"** !

*Et voilà ! En quelques minutes, Streamlit va configurer le serveur, installer vos dépendances et vous donnera une URL publique (ex: `https://votre-app-agritech.streamlit.app`) que vous pourrez partager.*
