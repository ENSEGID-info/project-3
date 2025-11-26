

from laspy import *
import numpy as np
import matplotlib.pyplot as plt

def etape1_main():
    print("Exécution de l'étape 1...")
    # Exemple : lecture d’un fichier ou génération de données
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data



def ouverture_laspy():
    with laspy.open('H:/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:
        
        print('Points from Header:', fh.header.point_count)
        las = fh.read()
        print(las)
        print('Points from data:', len(las.points))
        ground_pts = las.classification == 2
        bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
        print('Ground Point Return Number distribution:')
        for r,c in zip(bins,counts):
            print('    {}:{}'.format(r,c))
        X=las.x
        Y=las.y
        Z=las.z

    print("Exemple de coordonnées :", list(zip(X, Y, Z))[:5])

    if hasattr(las, "red"):
        r = las.red
        g = las.green
        b = las.blue
        print("Couleurs disponibles")
    else:
        print("Pas de couleur dans ce fichier")











