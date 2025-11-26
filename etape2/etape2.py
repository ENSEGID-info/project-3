
import laspy
import numpy
import matplotlib

# === Chemin vers le fichier LAS ===
fichier_las = "C:/Alice/2504_SEGO_NewMorvan_subset_filtered_30_percent.las"


# === Lecture du fichier ===
las = laspy.read(fichier_las)

# === Extraire les coordonnées des points ===
x = las.x
y = las.y
z = las.z

print("Nombre de points :", len(x))
print("Exemple de coordonnées :", list(zip(x, y, z))[:5])

if hasattr(las, "red"):
    r = las.red
    g = las.green
    b = las.blue
    print("Couleurs disponibles")
else:
    print("Pas de couleur dans ce fichier")

def etape2_main(data):
    

    print("Exécution de l'étape 2...")
    
    # Exemple : traitement de la donnée
    result = max(data)
    return result

