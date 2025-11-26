
import laspy
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

# === Chemin vers le fichier LAS ===
fichier_las = "C:/Alice/2504_SEGO_NewMorvan_subset_filtered_30_percent.las"
fichier_las="H:/Données projet info/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_30_percent.las"

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

# ============================================================
# 1) Chargement des points (exemple : fichier ou tableau)
# ============================================================

# Exemple : chargement depuis un fichier texte "points.xyzrgb"
# Chaque ligne : x y z r g b
points = np.loadtxt("las")

coords = points[:, :3]     # X, Y, Z
colors = points[:, 3:]     # R, G, B

# Normalisation si données entre 0 et 255
if colors.max() > 1.0:
    colors = colors / 255.0


# ============================================================
# 2) Visualisation 3D du nuage de points coloré (Matplotlib)
# ============================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
           c=colors, s=5)

ax.set_title("Nuage de points 3D coloré")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()

# ============================================================
# 3) Détection automatique des couches géologiques
#    à partir des changements de couleur
# ============================================================

# On suppose que les couches ont des couleurs relativement homogènes.
# On applique un clustering KMeans sur les couleurs pour détecter les couches.

# Ajustez ce nombre selon vos données :
n_layers = 4

kmeans = KMeans(n_clusters=n_layers)
labels = kmeans.fit_predict(colors)

# Palette pour affichage
unique_labels = np.unique(labels)
layer_colors = plt.cm.tab10(unique_labels % 10)[:, :3]

colored_by_layer = layer_colors[labels]


# ============================================================
# 4) Visualisation des couches détectées
# ============================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
           c=colored_by_layer, s=5)

ax.set_title(f"Couches géologiques détectées (KMeans, {n_layers} couches)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()

