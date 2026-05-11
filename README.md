# Flight Pricing Analysis : Décrypter la stratégie tarifaire aérienne

> **Pourquoi le même vol Paris → Madrid coûte 54€ un mardi matin et 310€ le vendredi soir ?**  
> Ce projet analyse les mécanismes du pricing aérien à partir de ~300 000 billets réels pour en extraire des recommandations concrètes pour les voyageurs comme pour les compagnies aériennes.

---

## Objectifs

- Identifier les **facteurs clés** qui font varier le prix d'un billet
- Quantifier l'impact de chaque variable : délai de réservation, escales, compagnie, créneau horaire
- Construire un **modèle prédictif interprétable** (Random Forest)
- Formuler des **recommandations actionnables** pour voyageurs et yield managers

---

## Dataset

**Source :** [Ease My Trip — Flight Price Prediction](https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction) (Kaggle)  
**Volume :** ~300 000 billets de vols domestiques indiens (2022)  
**Variables clés :**

| Variable | Description |
|----------|-------------|
| `airline` | Compagnie aérienne |
| `source_city` | Ville de départ |
| `destination_city` | Ville d'arrivée |
| `departure_time` | Créneau horaire de départ |
| `stops` | Nombre d'escales |
| `arrival_time` | Créneau horaire d'arrivée |
| `class` | Classe (Economy / Business) |
| `duration` | Durée du vol (heures) |
| `days_left` | Jours restants avant le départ |
| `price` | Prix du billet (INR) |

---

## Structure du projet

```
Analyse-pricing-avion/
│
├── README.md
├── requirements.txt
├── streamlit_app.py                    <- Dashboard interactif
│
├── 01_eda_exploration.ipynb            <- Exploration & nettoyage
├── 02_pricing_analysis.ipynb          <- Analyse des facteurs de prix
├── 03_model_prediction.ipynb          <- Modèle prédictif + feature importance
└── 04_recommendations.ipynb           <- Synthèse & recommandations
```

---

## Insights clés

- **Réserver J-46+ permet d'économiser 57.7%** par rapport au last-minute (J-1 à J-7)
- **Les vols directs sont 43% moins chers** que les vols avec escale — mais 10h de trajet en moins
- **La classe Business est le facteur n°1** du prix : elle explique à elle seule 89.7% de la variance
- **Les vols tôt le matin** sont systématiquement moins chers que les vols du soir

---

## Résultats du modèle

| Modèle | R² | RMSE | MAE |
|--------|----|------|-----|
| Baseline (médiane) | -0.35 | 26 398 INR | 16 155 INR |
| Random Forest | **0.9786** | **3 321 INR** | **1 715 INR** |

Le Random Forest explique **97.9% de la variance du prix** — amélioration de 87.4% vs baseline.

---

## Feature Importance — Ce qui explique vraiment le prix

| Rang | Facteur | Importance |
|------|---------|-----------|
| 1 | Classe Business | 89.7% |
| 2 | Durée du vol | 5.2% |
| 3 | Jours avant le départ | 1.3% |
| 4 | Compagnie | 1.1% |
| 5 | Ville de départ | 1.0% |

---

## Recommandations

### Pour les voyageurs
1. **Réserver au moins 46 jours à l'avance** — économie moyenne de 57.7% vs last-minute
2. **Privilégier les vols directs** sur les courts trajets (médiane à 4 499 INR vs 7 959 INR avec escale)
3. **Choisir un départ tôt le matin** — créneau systématiquement moins cher

### Pour les compagnies (yield management)
1. **La classe est le levier n°1** — 89.7% de la variance du prix, à optimiser en priorité
2. **Affiner la grille tarifaire J-8 à J-21** — forte élasticité, segments non capturés
3. **Re-pricer les créneaux early morning** — fort volume mais prix sous la moyenne du marché

---

## Stack technique

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange?logo=scikit-learn)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple?logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)

---

## Lancer le projet

```bash
# 1. Cloner le repo
git clone https://github.com/apiraamikrs/Analyse-pricing-avion.git
cd Analyse-pricing-avion

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Télécharger le dataset sur Kaggle
# https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction
# Placer Clean_Dataset.csv dans le même dossier

# 4. Lancer les notebooks dans l'ordre
jupyter notebook

# 5. Lancer le dashboard
streamlit run streamlit_app.py
```

---

## Auteur

**Apiraami Karuneswaran** — Data Analyst  
[LinkedIn](https://www.linkedin.com/in/apiraami-karuneswaran-5699a91b8/) · [GitHub](https://github.com/apiraamikrs/Analyse-pricing-avion)

---

*Projet réalisé dans le cadre d'un portfolio Data Analyst — 2026*
