
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


def compute_normals(points, k=30):
    """Calcule des normales robustes pour chaque point."""
    neigh = NearestNeighbors(n_neighbors=k).fit(points)
    _, idx = neigh.kneighbors(points)
    normals = np.zeros_like(points)
    for i in range(points.shape[0]):
        pts = points[idx[i]]
        pts_centered = pts - pts.mean(axis=0)
        cov = pts_centered.T @ pts_centered
        U, _, _ = np.linalg.svd(cov)
        normals[i] = U[:, -1]
    norms = np.linalg.norm(normals, axis=1)
    normals[norms == 0] = [0, 0, 1]
    normals /= np.maximum(norms[:, None], 1e-9)
    return normals

def compute_features(coords, Z, normals, k=20):
    Nx, Ny, Nz = normals[:,0], normals[:,1], normals[:,2]
    dip = np.arccos(np.clip(np.abs(Nz), 0, 1))
    azimut = np.arctan2(Ny, Nx)

    # Normalisations sécurisées
    Z_range = np.ptp(Z)
    Z_norm = (Z - np.min(Z)) / Z_range if Z_range > 1e-9 else np.zeros_like(Z)

    dip_range = np.ptp(dip)
    dip_norm = dip / dip_range if dip_range > 1e-9 else np.zeros_like(dip)

    azimut_norm = (azimut + np.pi) / (2*np.pi)  # toujours sûr

    neigh = NearestNeighbors(n_neighbors=k).fit(coords)
    _, idx = neigh.kneighbors(coords)
    dZ_local = np.array([np.max(Z[idx[i]]) - np.min(Z[idx[i]]) for i in range(len(coords))])
    dZ_range = np.ptp(dZ_local)
    dZ_norm = dZ_local / dZ_range if dZ_range > 1e-9 else np.zeros_like(dZ_local)

    features = np.column_stack((Z_norm, dip_norm, azimut_norm, dZ_norm))
    mask = ~np.isnan(features).any(axis=1)
    return features[mask], coords[mask]


def perform_clustering(features_clean, n_layers=5, batch_size=5000):
    """Effectue le clustering MiniBatchKMeans."""
    kmeans = MiniBatchKMeans(n_clusters=n_layers, batch_size=batch_size)
    labels = kmeans.fit_predict(features_clean)
    return labels

def plot_3d_points(coords, labels=None, colors=None, title="3D Points", elev=25, azim=-130, sample_size=200000):
    """Affiche un nuage de points 3D, avec labels ou couleurs."""
    sample = min(sample_size, len(coords))
    idx_s = np.random.choice(len(coords), sample, replace=False)
    coords_s = coords[idx_s]
    if labels is not None:
        labels_s = labels[idx_s]
        palette = plt.cm.tab10(np.unique(labels_s) % 10)
        c = palette[labels_s]
    elif colors is not None:
        c = colors[idx_s]
    else:
        c = 'b'

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords_s[:,0], coords_s[:,1], coords_s[:,2], c=c, s=2)
    ax.set_title(title)
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.view_init(elev=elev, azim=azim)
    plt.show()

# ---------------------- Main ----------------------

def main(X, Y, Z, R=None, G=None, B=None, n_layers=5):
    coords = np.column_stack((X, Y, Z))
    
    print("Calcul des normales…")
    normals = compute_normals(coords)

    print("Calcul des features…")
    features_clean, coords_clean = compute_features(coords, Z, normals)

    print("Clustering…")
    labels = perform_clustering(features_clean, n_layers=n_layers)

    print("Affichage du nuage original…")
    if R is not None and G is not None and B is not None:
        colors = np.column_stack((R/255, G/255, B/255))
        plot_3d_points(coords, colors=colors, title="Nuage original coloré")
    
    print("Affichage des strates détectées…")
    plot_3d_points(coords_clean, labels=labels, title="Strates géologiques détectées (géométrie + variation verticale)")

# ---------------------- Exemple d'utilisation ----------------------
# X, Y, Z, R, G, B = ... (tes données LAS ici)
# main(X, Y, Z, R, G, B, n_layers=5)