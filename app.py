"""
✈️ Flight Price Analyzer — Dashboard Streamlit
Déploiement : streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Config page ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✈️ Flight Price Analyzer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .metric-card {
        background: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #1B4F8A;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    .insight-box {
        background: #1a3a5c;
        border: 1px solid #2e6da4;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #ffffff !important;
    }
    .insight-box b { color: #7ec8f7 !important; }
    .reco-box {
        background: #1a3d2b;
        border: 1px solid #2e7d4f;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #ffffff !important;
    }
    .reco-box b { color: #7ef7b0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Chargement données ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/flights_clean.csv')
    except FileNotFoundError:
        # Génération de données synthétiques pour la démo
        np.random.seed(42)
        n = 5000
        airlines = ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'GO FIRST', 'AirAsia']
        cities   = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad']
        times    = ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night']
        stops    = ['zero', 'one', 'two_or_more']
        classes  = ['Economy', 'Business']

        days_left  = np.random.randint(1, 50, n)
        stop_arr   = np.random.choice(stops, n, p=[0.4, 0.45, 0.15])
        class_arr  = np.random.choice(classes, n, p=[0.8, 0.2])
        stop_num   = np.where(stop_arr == 'zero', 0, np.where(stop_arr == 'one', 1, 2))
        is_biz     = (class_arr == 'Business').astype(int)

        base_price = (
            5000
            + (50 - days_left) * 120
            + stop_num * (-800)
            + is_biz * 18000
            + np.random.normal(0, 1500, n)
        )
        base_price = np.clip(base_price, 1500, 60000)

        df = pd.DataFrame({
            'airline': np.random.choice(airlines, n),
            'source_city': np.random.choice(cities, n),
            'destination_city': np.random.choice(cities, n),
            'departure_time': np.random.choice(times, n),
            'arrival_time': np.random.choice(times, n),
            'stops': stop_arr,
            'class': class_arr,
            'duration': np.random.uniform(1.5, 8, n).round(2),
            'days_left': days_left,
            'price': base_price.round(0).astype(int)
        })
        st.info("Données de démo (dataset synthétique). Placez `flights_clean.csv` dans `/data` pour les données réelles.")
    return df

df = load_data()

# Calcul booking window
bins   = [0, 7, 14, 21, 30, 45, 100]
labels = ['J-1→7', 'J-8→14', 'J-15→21', 'J-22→30', 'J-31→45', 'J-46+']
df['booking_window'] = pd.cut(df['days_left'], bins=bins, labels=labels)

PALETTE = ['#1B4F8A', '#E8903A', '#2ECC71', '#E74C3C', '#9B59B6', '#1ABC9C']

# ── Sidebar filtres ────────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1px-s.jpg", width=1)
st.sidebar.title("Filtres")

selected_class = st.sidebar.selectbox("Classe", ["Toutes", "Economy", "Business"])
selected_airlines = st.sidebar.multiselect(
    "Compagnies", df['airline'].unique().tolist(),
    default=df['airline'].unique().tolist()
)
days_range = st.sidebar.slider("Jours avant le départ", 1, 49, (1, 49))

# Application des filtres
dff = df[
    (df['airline'].isin(selected_airlines)) &
    (df['days_left'].between(*days_range))
]
if selected_class != "Toutes":
    dff = dff[dff['class'] == selected_class]

# ── En-tête ────────────────────────────────────────────────────────────────────
st.title("✈️ Flight Price Analyzer")
st.markdown("*Décrypter la stratégie tarifaire aérienne — Portfolio Data Analyst*")
st.divider()

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Prix médian", f"{dff['price'].median():,.0f} INR", f"{len(dff):,} billets")
k2.metric("Prix minimum", f"{dff['price'].min():,.0f} INR")
k3.metric("Prix maximum", f"{dff['price'].max():,.0f} INR")
k4.metric("Écart-type", f"{dff['price'].std():,.0f} INR")

st.divider()

# ── Ligne 1 : Délai + Escales ──────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Prix selon le délai de réservation")
    price_by_days = dff.groupby('days_left')['price'].median().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_by_days['days_left'], y=price_by_days['price'],
        mode='lines', fill='tozeroy',
        line=dict(color='#1B4F8A', width=2.5),
        fillcolor='rgba(27,79,138,0.12)',
        name='Prix médian'
    ))
    fig.update_layout(
        xaxis=dict(autorange='reversed', title='Jours avant le départ'),
        yaxis_title='Prix médian (INR)',
        plot_bgcolor='white',
        height=320,
        margin=dict(t=20, b=40, l=40, r=20)
    )
    fig.add_vline(x=15, line_dash='dot', line_color='#E74C3C',
                  annotation_text='Last-minute', annotation_position='top right')
    st.plotly_chart(fig, use_container_width=True)

    window_stats = dff.groupby('booking_window', observed=True)['price'].median()
    cheapest_window = window_stats.idxmin()
    ref = window_stats.max()
    saving = (ref - window_stats.min()) / ref * 100
    st.markdown(f"""<div class='insight-box'>
    💡 <b>Insight :</b> Réserver dans la fenêtre <b>{cheapest_window}</b> permet d'économiser 
    jusqu'à <b>{saving:.0f}%</b> par rapport au last-minute.
    </div>""", unsafe_allow_html=True)

with col2:
    st.subheader("Impact des escales")
    stops_analysis = dff.groupby('stops').agg(
        prix_median=('price', 'median'),
        duree_mediane=('duration', 'median')
    ).reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=stops_analysis['stops'], y=stops_analysis['prix_median'],
        name='Prix médian',
        marker_color=PALETTE[:len(stops_analysis)],
        text=stops_analysis['prix_median'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside'
    ))
    fig2.update_layout(
        xaxis_title='Nombre d\'escales',
        yaxis_title='Prix médian (INR)',
        plot_bgcolor='white',
        height=320,
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=20)
    )
    st.plotly_chart(fig2, use_container_width=True)

    if 'zero' in stops_analysis['stops'].values and 'one' in stops_analysis['stops'].values:
        p_direct = stops_analysis[stops_analysis['stops'] == 'zero']['prix_median'].values[0]
        p_one    = stops_analysis[stops_analysis['stops'] == 'one']['prix_median'].values[0]
        eco_stop = (p_direct - p_one) / p_direct * 100
        dur_direct = stops_analysis[stops_analysis['stops'] == 'zero']['duree_mediane'].values[0]
        dur_one    = stops_analysis[stops_analysis['stops'] == 'one']['duree_mediane'].values[0]
        tps_sup = dur_one - dur_direct
        st.markdown(f"""<div class='insight-box'>
        <b>Arbitrage :</b> 1 escale = <b>-{eco_stop:.0f}%</b> sur le prix 
        mais <b>+{tps_sup:.1f}h</b> de trajet.
        </div>""", unsafe_allow_html=True)

# ── Ligne 2 : Compagnies + Horaires ───────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("✈️ Prix par compagnie")
    airline_order = dff.groupby('airline')['price'].median().sort_values().index
    fig3 = px.box(dff, x='airline', y='price',
                  category_orders={'airline': list(airline_order)},
                  color='airline',
                  color_discrete_sequence=PALETTE,
                  labels={'price': 'Prix (INR)', 'airline': ''})
    fig3.update_layout(showlegend=False, plot_bgcolor='white', height=320,
                       margin=dict(t=20, b=40, l=40, r=20))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🕐 Prix par créneau horaire")
    time_order = ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night']
    time_labels = ['Très tôt', 'Matin', 'Après-midi', 'Soir', 'Nuit', 'Nuit tardive']
    time_price = dff.groupby('departure_time')['price'].median().reindex(time_order).reset_index()
    time_price.columns = ['time', 'price']
    time_price['label'] = time_labels

    fig4 = go.Figure(go.Bar(
        x=time_price['label'], y=time_price['price'],
        marker_color=[PALETTE[2] if v == time_price['price'].min() else
                      PALETTE[3] if v == time_price['price'].max() else
                      PALETTE[0] for v in time_price['price']],
        text=time_price['price'].apply(lambda x: f'{x:,.0f}' if pd.notna(x) else ''),
        textposition='outside'
    ))
    fig4.update_layout(
        xaxis_title='Créneau de départ',
        yaxis_title='Prix médian (INR)',
        plot_bgcolor='white', height=320,
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Recommandations ────────────────────────────────────────────────────────────
st.divider()
st.subheader("💡 Recommandations")

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("""<div class='reco-box'>
    <b>Pour voyager moins cher</b><br><br>
    Réserver <b>31–45 jours à l'avance</b><br>
    Choisir un départ <b>tôt le matin</b><br>
    Accepter <b>1 escale</b> sur les longs trajets
    </div>""", unsafe_allow_html=True)

with r2:
    st.markdown("""<div class='reco-box'>
    <b>🏢 Pour les compagnies (Yield)</b><br><br>
    📈 Affiner les tarifs <b>J-8 à J-21</b><br>
    📈 Re-pricer les créneaux <b>Early Morning</b><br>
    📈 Revoir le ratio <b>Business/Éco</b>
    </div>""", unsafe_allow_html=True)

with r3:
    st.markdown("""<div class='reco-box'>
    <b>Modèle prédictif</b><br><br>
    Top 3 features :<br>
    Jours avant le départ<br>
    Classe Business/Économique<br>
    Nombre d'escales
    </div>""", unsafe_allow_html=True)

st.divider()
st.caption("Portfolio Data Analyst · Projet Flight Pricing · [GitHub](https://github.com)")
