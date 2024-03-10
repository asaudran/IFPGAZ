#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# In[17]:


# Utiliser le CSS personnalisé pour styler les sections
st.markdown("""
    <style>
    .box {
        border: 2px solid #e6e9ef;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f8f9fa; /* Gris très clair */
    }
    .header {
        text-align: center;
        padding: 5px; /* Plus mince */
        background-color: #ffffff; /* Blanc pour un look plus épuré */
        color: #333; /* Texte sombre pour contraste */
        font-size: 18px; /* Taille de police ajustée */
        border-bottom: 2px solid #e6e9ef; /* Ligne de séparation fine */
    }
    .section-header {
        color: #333;
        font-size: 20px;
        margin-bottom: 15px;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #f1f3f6;
        border-top: 1px solid #e6e9ef;
    }
    </style>
    """, unsafe_allow_html=True)


# In[14]:


# Ajouter un en-tête
st.markdown("<div class='header'><h1>PROJET MASSOL : ECONOMIE DU GAZ</h1></div>", unsafe_allow_html=True)

# Création des onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contexte Européen et Chinois", "Prédiction Prix", "Production", "Contexte YAMAL", "Onglet 5"])


# In[15]:


import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Contenu de l'Onglet 2
with tab2.container():
    st.markdown("""
    <div class='box'>
        <p>Voici le graphique des prédictions des prix du gaz naturel :</p>
        <p>Ces données sont issues de l'Energy Institute. La prédiction est réalisée avec une régression linéaire à partir des données de l'année 2010. L'année 2022 a été supprimée des données d'entraînement car considérée comme anormale. Pour le prix 'Japan CIF', les données utilisées pour la régression sont prises à partir de l'année 2016. Sélectionnez une 'Année de paix en Europe' pour ajuster les prédictions de prix TTF.</p>
    </div>
    """, unsafe_allow_html=True)

    peace_year = st.number_input('ANNEE DE PAIX EN EUROPE', min_value=2024, max_value=2050, value=2035, step=1)

    # Définition des données
    years = np.arange(2009, 2024).reshape(-1, 1)
    future_years = np.arange(2024, 2050).reshape(-1, 1)
    prices = {
        'Japan_CIF': [30.90, 37.30, 50.40, 57.16, 55.19, 55.72, 35.03, 23.66, 27.63, 34.35, 33.93, 26.55, 34.37, 45.00, 25.00],
        'JKM': [18.00, 26.34, 47.84, 51.58, 56.49, 47.28, 25.42, 19.53, 24.32, 33.30, 18.75, 14.97, 63.45, 115.94, 60.00],
        'Netherlands_TTF': [16.92, 23.10, 31.59, 32.24, 33.28, 27.79, 21.96, 15.49, 19.52, 26.96, 15.18, 10.47, 54.65, 127.87, 33.00]
    }

    # Définition des couleurs pour chaque série
    colors = {
        'Japan_CIF': 'red',
        'JKM': 'green',
        'Netherlands_TTF': 'blue'
    }

    # Initialisation de la figure Plotly
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # Tracé des données et prédictions pour chaque série
    for market, actual_prices in prices.items():
        actual_years = np.arange(2009 if market != 'Japan_CIF' else 2016, 2023).reshape(-1, 1)
        model = LinearRegression()
        model.fit(actual_years, actual_prices[:len(actual_years)])
        predicted_prices = model.predict(future_years)

        # Courbes des données actuelles
        fig.add_trace(
            go.Scatter(x=actual_years.flatten(), y=actual_prices[:len(actual_years)], mode='markers+lines', name=f'{market} Actual', line=dict(color=colors[market]))
        )

        if market == 'Netherlands_TTF':
            peace_index = np.searchsorted(future_years.flatten(), peace_year)
            predicted_prices[peace_index:] *= 0.85  # Apply the 15% reduction from the peace year onwards
            # Making the adjustment more pronounced and logarithmic
            adjusted_prices = np.empty_like(predicted_prices)
            adjusted_prices[:peace_index] = predicted_prices[:peace_index]
            # Apply a logarithmic growth rate based on the reduced price
            adjusted_prices[peace_index:] = predicted_prices[peace_index] + np.log(1 + np.arange(0, len(predicted_prices) - peace_index)) * (predicted_prices[-1] - predicted_prices[peace_index]) / np.log(len(predicted_prices) - peace_index)

            predicted_prices = adjusted_prices

        # Courbes des prédictions
        fig.add_trace(
            go.Scatter(x=future_years.flatten(), y=predicted_prices, mode='markers+lines', name=f'{market} Predicted', line=dict(color=colors[market], dash='dash'))
        )

    # Configuration du graphique
    fig.update_layout(
        title_text='Natural Gas Price Predictions with Consistent Colors',
        xaxis_title='Year',
        yaxis_title='Price (USD per MWh)',
        legend_title="Legend",
        hovermode="closest"
    )

    # Affichage du graphique dans Streamlit
    st.plotly_chart(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# In[ ]:





# In[19]:


with tab1.container():
    # Vue d'ensemble et contexte 2023
    st.markdown(f"<div class='box' style='background-image: url(\"/Users/audran/Desktop/Data_MASSOL_GAZ_Russie/PAGE_MASSOL/capture1.png\"); background-size: cover; padding:20px; border-radius:10px;'>            <h2 style='color:#333; text-align:center; background-color: rgba(245, 245, 245, 0.8); padding: 10px; border-radius:5px;'><b>VUE D'ENSEMBLE ET CONTEXTE</b></h2>            <div style='background-color:rgba(255, 255, 255, 0.8); padding:10px; border-radius:5px;'>            <p style='color:#666; font-size:14px; text-align:center;'>Vue de l'ensemble ci-dessous</p>            </div>            </div>", unsafe_allow_html=True)
    st.image("/Users/audran/Desktop/Data_MASSOL_GAZ_Russie/PAGE_MASSOL/capture1.png", caption='Vue de l ensemble', width=700)


    # EUROPE
    st.markdown("""
        <div style='background-color:#f0f2f5; padding:20px; border-radius:10px;'>
            <h2 style='color:#333; text-align:center;'><b>EUROPE</b></h2>
            <p><b>Contexte Général et Ressources :</b> En 2022, le marché du gaz naturel mondial a subi un choc majeur, principalement dû aux réductions des livraisons de gaz par pipeline de la Russie vers l'Europe, entraînant une pression sans précédent sur l'approvisionnement et déclenchant une crise énergétique mondiale. L'Europe a cependant réussi à remplir ses sites de stockage de gaz souterrain bien au-dessus des moyennes historiques grâce à une combinaison de mesures politiques ciblées, un afflux record de gaz naturel liquéfié (GNL) et une forte baisse de la consommation, notamment dans les industries à forte intensité énergétique.</p>
            <p><b>Importations et Dépendance :</b> L'Europe a vu une augmentation significative des importations de GNL, particulièrement en provenance des États-Unis, pour remplacer le gaz de pipeline russe. Les stocks de gaz de l'UE à la fin du deuxième trimestre de 2023 étaient supérieurs à 70% dans tous les États membres sauf trois et étaient à des niveaux record par rapport aux années précédentes.</p>
            <p><b>Politiques Énergétiques et Objectifs :</b> L'Europe a adopté de fortes mesures politiques pour augmenter sa résilience énergétique et réduire sa dépendance au gaz naturel face à la crise actuelle. Les gouvernements européens ont œuvré pour diversifier les sources d'énergie et renforcer la sécurité énergétique, en réaction à la baisse des livraisons de gaz russe.</p>
            <p><b>Prix du Gaz et Facteurs d'Influence :</b> Les prix du gaz européens ont continué à baisser au deuxième trimestre de 2023, avec un prix spot moyen (mesuré par le Dutch Title Transfer Facility, TTF) de 35.2 €/MWh, ce qui représente une baisse de 34% par rapport au trimestre précédent et une baisse de 64% en glissement annuel.</p>
            <p><b>Enjeux Géopolitiques :</b> La crise énergétique mondiale de 2022, exacerbée par les coupures de gaz russes, a mis en évidence la vulnérabilité des marchés du gaz face aux enjeux géopolitiques. L'Europe a réagi en cherchant à diversifier ses sources d'approvisionnement et à réduire sa dépendance envers le gaz russe.</p>
            <p><b>Transitions et Innovations Énergétiques :</b> La crise actuelle a accéléré la transition vers des sources d'énergie alternatives en Europe. Les gouvernements européens continuent d'encourager les politiques favorisant les énergies renouvelables et l'efficacité énergétique afin de réduire leur dépendance aux combustibles fossiles.</p>
            <p><b>Prévisions et Perspectives :</b> Bien que la pression sur les marchés européen et mondial du gaz se soit atténuée depuis le début de 2023, l'approvisionnement mondial en gaz reste tendu et est soumis à un large éventail d'incertitudes, notamment les conditions météorologiques défavorables et la disponibilité plus faible du GNL.</p>
        </div>
    """, unsafe_allow_html=True)

# Espacement
    st.write("")

    
    # CHINE
    st.markdown("<div class='box' style='background-color:#f5f5f5; padding:20px; border-radius:10px;'>            <h2 style='color:#333; text-align:center;'><b>CHINE</b></h2>            <p style='color:#666; font-size:16px;'><b>Consommation et Croissance de la Demande :</b> La consommation de gaz naturel en Chine devrait augmenter de 5,5% à 7% en 2023, une inversion par rapport au déclin de 1,2% enregistré en 2022. Cette croissance est attribuée à la reprise économique et à la baisse des prix mondiaux du gaz. Le total de la demande de gaz pourrait atteindre entre 385 et 390 milliards de mètres cubes (Bcm) en 2023.</p>            <p style='color:#666; font-size:16px;'><b>Production et Importations :</b> En 2022, la Chine a produit 220,1 Bcm de gaz naturel, marquant une augmentation de 6% par rapport à l'année précédente, couvrant ainsi 59% de ses besoins intérieurs. Les importations de GNL sont attendues en hausse de 10,9% par rapport à l'année dernière, tandis que les importations de gaz via pipeline devraient augmenter d'environ 10,7%, principalement du fait des approvisionnements russes. Cela fait suite à une baisse des importations en 2022, où les importations totales de gaz naturel ont chuté de 9,9%.</p>            <p style='color:#666; font-size:16px;'><b>Infrastructures et Investissements :</b> La Chine continue d'élargir son \"réseau national\" d'infrastructures gazières, en augmentant la longueur des pipelines de gaz naturel et la capacité de stockage. Ces développements sont en ligne avec le \"14e Plan quinquennal\" qui vise une production annuelle de gaz naturel dépassant les 230 Bcm d'ici 2025, avec un accent mis sur la sécurité de la chaîne d'approvisionnement et la transition verte.</p>            <p style='color:#666; font-size:16px;'><b>Politiques Énergétiques :</b> Les politiques énergétiques de la Chine soulignent l'importance de sécuriser la chaîne d'approvisionnement par la production domestique tout en promouvant la transition vers une énergie verte. La Chine vise également à standardiser les méthodes de tarification pour les services de gazéification des terminaux de GNL pour encourager une plus grande uniformité des prix.</p>            <p style='color:#666; font-size:16px;'><b>Prévisions et Tendances Futures :</b> Les prévisions suggèrent que la demande de gaz naturel en Chine continuera de croître dans les années à venir, avec une estimation que la demande totale pourrait atteindre 700 Bcm d'ici 2040. Cette croissance est attribuée à l'expansion des secteurs industriels et à l'augmentation des besoins en énergie propre.</p>            <p style='color:#666; font-size:16px;'><b>Défis et Perspectives :</b> Malgré la croissance prévue, le marché du gaz naturel en Chine fait face à des défis, notamment la sensibilité des utilisateurs industriels aux fluctuations des prix du gaz. Les politiques et les investissements futurs seront essentiels pour maintenir la stabilité de l'approvisionnement tout en répondant à la croissance de la demande.</p>              </div>", unsafe_allow_html=True)



# Assuming the DataFrame 'df' is structured with rows for each country and columns for each year
data_energy = {
    'Year': list(range(1985, 2023)),  # Years from 1985 to 2022
    'Russian Federation': [424.9, 462.6, 500.5, 542.4, 566.3, 599.6, 591.3, 592.2, 568.6, 558.5, 541.2, 552.3, 523.5, 541.3, 544.4, 537.1, 534.8, 547.5, 570.6, 582.6, 589.5, 604.8, 601.6, 611.5, 536.2, 598.4, 616.8, 601.9, 614.5, 591.2, 584.4, 589.3, 635.6, 669.1, 679, 638.4, 702.1, 618.4],
    'US': [447.9, 436.3, 452, 464.2, 470.7, 483.4, 480.8, 484.7, 490.2, 510.3, 503.3, 510.2, 511.5, 517.3, 510.1, 518.6, 531.9, 511.2, 517.9, 503.1, 489.4, 501.7, 521.9, 546.1, 557.6, 575.2, 617.4, 649.1, 655.7, 704.7, 740.3, 727.4, 746.2, 840.9, 928.1, 916.1, 944.1, 978.6],
    'EU': [267.7, 258.4, 259.9, 245.5, 247.6, 243.2, 251.4, 247.9, 257.9, 258, 266.3, 299.9, 295.5, 294.5, 302.5, 309.9, 313.9, 322.7, 326.1, 337.4, 327.6, 320.4, 306.3, 320.4, 303.6, 310.1, 284.8, 287.5, 280, 266.1, 260.8, 259.9, 262.7, 251.5, 234.8, 218.9, 211, 220.4]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data_energy)

# Streamlit code for the tab
with tab3.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.text_area("Espace de commentaires et de texte", "Votre texte ici...", key="text_area3")
    st.header("Production BCM")

    # Plotting the data using Plotly
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(title_text='Gas Production Over the Years')

    # Add traces for each country/region
    for country in ['Russian Federation', 'US', 'EU']:
        fig.add_trace(go.Scatter(x=df['Year'], y=df[country], name=country), secondary_y=False)

    # Set x-axis title
    fig.update_xaxes(title_text='Year')

    # Set y-axes titles
    fig.update_yaxes(title_text='BCM (Billion Cubic Meters)', secondary_y=False)

    # Display the interactive figure in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
    st.write("Sources : Enery Institute")
 
    
with tab4.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.text_area("Espace de commentaires et de texte", "Votre texte ici...", key="text_area4")
    st.markdown("</div>", unsafe_allow_html=True)

with tab5.container():
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.text_area("Espace de commentaires et de texte", "Votre texte ici...", key="text_area5")
    st.markdown("</div>", unsafe_allow_html=True)

# Ajouter un bas de page
st.markdown("<div class='footer'>Projet Économie du Gaz : Audran - Marc - Aymeric - Raymond</div>", unsafe_allow_html=True)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




