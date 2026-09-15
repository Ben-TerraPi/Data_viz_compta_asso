import streamlit as st
import pandas as pd
from utils import traiter_csv


# streamlit run streamlit_app.py


def main():

#>>>>>>>>>>>>>>>>>>>>> Config page
    st.set_page_config(
        page_title="LVR compta",
        page_icon="🧾",
        layout="wide",
        initial_sidebar_state="expanded",
    )

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> En tête

    col1, col2, col3 = st.columns([1,3,1])

    with col1:
        st.image("images/Logo_LVR_blanc_fond_transparent.png", width=300)

    with col2:
        st.title('La Vilaine Compta ')

        st.header("Outil de Data Viz pour les comptes de l'association")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>< Upload

        uploaded_file = st.file_uploader(
            "Importer un relevé bancaire BPO",
            type=["csv"],
        )

        if uploaded_file is None:
            return

        resultat = traiter_csv(uploaded_file)
        df = resultat["df"].iloc[:-1].copy()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Gestion des dates début et fin

        date_debut = resultat.get("date_debut_document")
        date_fin = resultat.get("date_fin_document")

        label_solde_debut = (
            f"Solde bancaire au {date_debut.strftime('%d/%m/%Y')}"
            if date_debut is not None
            else "Solde bancaire à la date de début du document"
        )
        label_solde_fin = (
            f"Solde bancaire au {date_fin.strftime('%d/%m/%Y')}"
            if date_fin is not None
            else "Solde bancaire à la date de fin du document"
        )

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Blocs calcul

    if resultat["solde_debut"] is not None:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            label_solde_debut,
            f"{resultat['solde_debut']:.2f} EUR",
        )
        col2.metric(
            "Recettes sur la période",
            f"{resultat['total_recette']:.2f} EUR",
        )
        col3.metric(
            "Dépenses sur la période",
            f"{abs(resultat['total_depense']):.2f} EUR",
        )
        col4.metric(
            label_solde_fin,
            f"{resultat['solde_fin']:.2f} EUR",
        )
    else:
        st.info("Les soldes bancaires ne sont pas disponibles pour cet ancien format.")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>< Téléchargement du fichier traité

    output_path = resultat["output_path"]

    st.download_button(
        label="Télécharger le fichier traité",
        data=output_path.read_bytes(),
        file_name=output_path.name,
        mime="text/csv",
    )

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Line chart

    st.subheader("Recettes et dépenses sur la période")

    df["Date_Compta"] = pd.to_datetime(df["Date_Compta"])

    evolution = (
        df.groupby("Date_Compta")[["recette", "dépense"]]
        .sum()
        .sort_index()
    )

    st.line_chart(evolution,
                  color=["#0db500", "#FF0000"])

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Bar chart

    df["Mois"] = df["Date_Compta"].dt.to_period("M").astype(str)

    repartition_mensuelle = (
        df.assign(dépense=df["dépense"].abs())
        .groupby("Mois")[["recette", "dépense"]]
        .sum()
        .sort_index()
    )

    st.subheader("Recettes et dépenses par mois")
    st.bar_chart(
        repartition_mensuelle,
        color=["#0db500", "#FF0000"],
    )

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Mouvements

    st.subheader("Mouvements")
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()