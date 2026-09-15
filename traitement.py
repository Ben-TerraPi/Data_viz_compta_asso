from utils import traiter_csv


file_path = "fichiers_brut/operations_01092025_31082026.csv"

resultat = traiter_csv(file_path)

print(f"Recettes : {resultat['total_recette']:.2f} EUR")
print(f"Dépenses : {resultat['total_depense']:.2f} EUR")
if resultat["solde_debut"] is not None:
	print(f"Solde initial : {resultat['solde_debut']:.2f} EUR")
	print(f"Solde calculé : {resultat['solde_calcule']:.2f} EUR")
	print(f"Solde bancaire : {resultat['solde_fin']:.2f} EUR")
	print(
		f"Écart : {resultat['solde_calcule'] - resultat['solde_fin']:.2f} EUR"
	)
else:
	print("Soldes bancaires : non disponibles dans cet ancien format")
print(f"Fichier créé : {resultat['output_path']}")