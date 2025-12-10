from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt

# ======================= Fonctions =======================

def compute_normals(coords, k=30):
    """Calcule les normales pour chaque point du nuage."""
    neigh = NearestNeighbors(n_neighbors=k).fit(coords)
    _, idx = neigh.kneighbors(coords)

    normals = np.zeros_like(coords)
    for i in range(len(coords)):
        pts = coords[idx[i]]
        pts_centered = pts - pts.mean(axis=0)
        cov = pts_centered.T @ pts_centered
        U, _, _ = np.linalg.svd(cov)
        normals[i] = U[:, -1]

    norms = np.linalg.norm(normals, axis=1)
    normals[norms == 0] = [0,0,1]
    normals /= np.maximum(np.linalg.norm(normals, axis=1)[:, None], 1e-9)
    return normals

def compute_features(coords, Z, normals, k=20):
    """Calcule les features pour le clustering: Z_norm, dip, azimut, dZ_local."""
    Nx, Ny, Nz = normals[:,0], normals[:,1], normals[:,2]
    dip = np.arccos(np.clip(np.abs(Nz),0,1))
    azimut = np.arctan2(Ny, Nx)

    # Variation verticale locale
    neigh = NearestNeighbors(n_neighbors=k).fit(coords)
    _, idx = neigh.kneighbors(coords)
    dZ_local = np.array([np.max(Z[idx[i]]) - np.min(Z[idx[i]]) for i in range(len(coords))])

    # Normalisation robuste
    def safe_norm(arr):
        rng = np.ptp(arr)
        return (arr - np.min(arr)) / rng if rng > 1e-9 else np.zeros_like(arr)

    Z_norm = safe_norm(Z)
    dip_norm = safe_norm(dip)
    dZ_norm = safe_norm(dZ_local)
    azimut_norm = (azimut + np.pi) / (2*np.pi)

    features = np.column_stack((Z_norm, dip_norm, azimut_norm, dZ_norm))
    mask = ~np.isnan(features).any(axis=1)
    return features[mask], coords[mask]

def cluster_and_plot(coords_clean, features_clean, n_layers=5, sample_size=200000):
    """Effectue le clustering et affiche le résultat."""
    print("Clustering…")
    kmeans = MiniBatchKMeans(n_clusters=n_layers, batch_size=5000)
    labels = kmeans.fit_predict(features_clean)

    # Échantillonnage pour affichage
    sample = min(sample_size, len(coords_clean))
    idx_s = np.random.choice(len(coords_clean), sample, replace=False)
    coords_s = coords_clean[idx_s]
    labels_s = labels[idx_s]

    palette = plt.cm.tab10(np.unique(labels_s) % 10)
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords_s[:,0], coords_s[:,1], coords_s[:,2], c=palette[labels_s], s=2)
    ax.set_title("Strates géologiques détectées (géométrie + variation verticale)")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.view_init(elev=25, azim=-130)
    plt.show()

# ======================= Exécution =======================
def execution(X,Y,Z):
    coords = np.column_stack((X, Y, Z))
    normals = compute_normals(coords)
    features_clean, coords_clean = compute_features(coords, Z, normals)
    cluster_and_plot(coords_clean, features_clean)
print("Calcul des normales…")


