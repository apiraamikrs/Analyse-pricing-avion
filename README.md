# Flight Pricing Analysis — Décrypter la stratégie tarifaire aérienne

> **Pourquoi le même vol Paris → Madrid coûte 54€ un mardi matin et 310€ le vendredi soir ?**  
> Ce projet analyse les mécanismes du pricing aérien à partir de ~300 000 billets réels pour en extraire des recommandations concrètes — pour les voyageurs comme pour les compagnies.

---

## Objectifs

- Identifier les **facteurs clés** qui font varier le prix d'un billet
- Quantifier l'impact de chaque variable : délai de réservation, escales, compagnie, jour de la semaine
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
flight-pricing/
│
├── README.md
├── requirements.txt
│
├── notebooks/
│   ├── 01_eda_exploration.ipynb        ← Exploration & nettoyage
│   ├── 02_pricing_analysis.ipynb       ← Analyse des facteurs de prix
│   ├── 03_model_prediction.ipynb       ← Modèle prédictif + feature importance
│   └── 04_recommendations.ipynb        ← Synthèse & recommandations
│
├── data/
│   └── README.md                       ← Instructions téléchargement dataset
│
└── dashboard/
    └── app.py                          ← Dashboard Streamlit (optionnel)
```

---

## Insights clés

> *(à compléter après analyse)*

- **Réserver X jours à l'avance** permet d'économiser en moyenne **XX%**
- **Les vols avec escale** sont XX% moins chers mais allongent le trajet de Xh en moyenne
- **Les vols du matin** sont systématiquement moins chers que les vols du soir
- **Les 3 facteurs les plus prédictifs** du prix : `days_left`, `class`, `stops`

---

## Résultats du modèle

| Modèle | R² | RMSE |
|--------|----|------|
| Baseline (moyenne) | — | — |
| Random Forest | — | — |

---

## Recommandations

### Pour les voyageurs
1. **Réserver entre J-30 et J-45** pour le meilleur rapport qualité/prix
2. **Éviter les vols du vendredi soir et dimanche soir** (pics tarifaires systématiques)
3. **Privilégier 1 escale courte** sur les longues distances : économie moyenne de XX%

### Pour les compagnies (yield management)
1. **Augmenter la granularité tarifaire** sur les créneaux J-7 à J-15 (forte élasticité)
2. **Sous-tarifer les vols early morning** pour améliorer le taux de remplissage
3. **Revoir le pricing Business** sur les routes secondaires (ratio Business/Economy anormalement bas)

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
git clone https://github.com/[ton-username]/flight-pricing.git
cd flight-pricing

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Télécharger le dataset (voir data/README.md)

# 4. Lancer les notebooks dans l'ordre
jupyter notebook notebooks/
```

---

## Auteur

**[Apiraami Karuneswaran]** — Data Analyst  
[LinkedIn](https://www.linkedin.com/in/apiraami-karuneswaran-5699a91b8/) · [GitHub](https://github.com/apiraamikrs/Analyse-pricing-avion)

---

*Projet réalisé dans le cadre d'un portfolio Data Analyst — Mars 2026*
