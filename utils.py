from pathlib import Path

import pandas as pd


def traiter_csv(file_path):
    file_path = Path(file_path)

    lignes = file_path.read_text(encoding="ISO-8859-1").splitlines()

    nouveau_format = any(
        ligne.startswith("Date comptable;") for ligne in lignes
    )

    if nouveau_format:
        ligne_fin = next(
            ligne for ligne in lignes if ligne.startswith("Solde en fin")
        )
        ligne_debut = next(
            ligne for ligne in lignes if ligne.startswith("Solde en d")
        )

        solde_fin_banque = float(
            ligne_fin.split(";")[3].strip().replace(",", ".")
        )
        solde_debut_banque = float(
            ligne_debut.split(";")[3].strip().replace(",", ".")
        )

        ligne_entete = next(
            index
            for index, ligne in enumerate(lignes)
            if ligne.startswith("Date comptable;")
        )

        df = pd.read_csv(
            file_path,
            encoding="ISO-8859-1",
            sep=";",
            decimal=",",
            skiprows=ligne_entete,
        )

        df = df[
            [
                "Date comptable",
                "Libelle simplifie",
                "Informations complementaires",
                "Reference",
                "Date operation",
                "Date de valeur",
                "Debit",
                "Credit",
            ]
        ].copy()

        df.columns = [
            "Date_Compta",
            "Libelle",
            "Informations complementaires",
            "Reference",
            "Date_Op",
            "Date_Valeur",
            "Debit",
            "Credit",
        ]

    else:
        solde_debut_banque = None
        solde_fin_banque = None

        df = pd.read_csv(
            file_path,
            encoding="ISO-8859-1",
            sep=";",
            decimal=",",
            usecols=range(6),
        )

        df.columns = [
            "Date_Compta",
            "Date_Op",
            "Libelle",
            "Reference",
            "Date_Valeur",
            "Montant",
        ]

        df["Informations complementaires"] = ""

        df["Debit"] = df["Montant"].where(df["Montant"] < 0, 0)
        df["Credit"] = df["Montant"].where(df["Montant"] > 0, 0)

    for colonne in ["Date_Compta", "Date_Op", "Date_Valeur"]:
        df[colonne] = pd.to_datetime(
            df[colonne],
            format="%d/%m/%Y",
            errors="coerce",
        ).dt.date

    df = df.dropna(subset=["Date_Compta"])

    df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0)
    df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce").fillna(0)

    df["Montant"] = df["Debit"] + df["Credit"]
    df["recette"] = df["Montant"].clip(lower=0)
    df["dépense"] = df["Montant"].clip(upper=0)

    total_recette = df["recette"].sum()
    total_depense = df["dépense"].sum()
    solde_calcule = (
        solde_debut_banque + total_recette + total_depense
        if solde_debut_banque is not None
        else None
    )

    resultat = df[
        [
            "Date_Compta",
            "Date_Op",
            "Libelle",
            "Informations complementaires",
            "Reference",
            "Date_Valeur",
            "Montant",
            "recette",
            "dépense",
        ]
    ].copy()

    resultat.loc[len(resultat)] = [
        "Total",
        "",
        "",
        "",
        "",
        "",
        total_recette + total_depense,
        total_recette,
        total_depense,
    ]

    date_min = resultat["Date_Compta"].iloc[:-1].min()
    date_max = resultat["Date_Compta"].iloc[:-1].max()

    dossier_sortie = Path("fichiers clean")
    dossier_sortie.mkdir(exist_ok=True)

    output_path = dossier_sortie / f"Mouvements_{date_min}_{date_max}.csv"
    resultat.to_csv(output_path, index=False)

    return {
        "df": resultat,
        "solde_debut": solde_debut_banque,
        "solde_fin": solde_fin_banque,
        "solde_calcule": solde_calcule,
        "total_recette": total_recette,
        "total_depense": total_depense,
        "output_path": output_path,
    }