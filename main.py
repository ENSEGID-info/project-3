# ===============================
# Projet Informatique
# Structure du programme principal
# ===============================

# Import des modules écrits par les sous-groupes
import etape1
import etape2
import etape3

def main():
    print("=== Début du programme ===")
    
    # Étape 1 – Préparation ou lecture de données
    print("\n--- Étape 1 : Lecture ou préparation ---")
    data = etape1.etape1_main()
    data = etape1.ouverture_laspy()
    data = etape1.co()
    data = etape1.exemple()
    data = etape1.couleur_arbre()
    data = etape1.liste_couleur()
    data = etape1.sup_points()
    data = etape1.affichage()
    # Étape 2 – Traitement ou analyse
    print("\n--- Étape 2 : Traitement principal ---")
    result = etape2.etape2_main(data)
    result = etape2.compute_normals(coords, k=30)
    result = etape2.compute_features(coords, Z, normals, k=20)
    result = etape2.cluster_and_plot(coords_clean, features_clean, n_layers=5, sample_size=200000)
    result = etape2.execution( X, Y, Z)
    # Étape 3 – Résultats ou affichage final
    print("\n--- Étape 3 : Résultats ou sortie ---")
    etape3.etape3_main(result)
    
    print("\n=== Fin du programme ===")

if __name__ == "__main__":
    main()

