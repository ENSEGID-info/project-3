# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 11:56:02 2025

@author: lfinet
"""

import laspy
import numpy as np
import matplotlib.pyplot as plt

def etape1_main():
    """
    Exécute l'étape 1 du programme.

    Cette fonction affiche un message indiquant l'exécution de l'étape,
    génère une liste de données simples et la retourne.

    :return: Une liste de données d'exemple [1, 2, 3].
    :rtype: list
    """
    print("Exécution de l'étape 1...")
    # Exemple : lecture d’un fichier ou génération de données
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data


# Fonction d'ouverture d'un fichier LAS via LasPy
# Elle lit les points, affiche des informations du header
# et retourne l'objet LAS pour une utilisation ultérieure


def ouverture_laspy():
    """
   Ouvre un fichier LAS et affiche plusieurs informations utiles.

   La fonction utilise la bibliothèque LasPy pour lire un fichier LAS.
   Elle affiche :
     - Le nombre total de points selon l'en-tête,
     - Les données générales du fichier,
     - Le nombre réel de points lus,
     - La distribution des retours (return number) des points classés comme sol.

   :return: L'objet LAS contenant toutes les données du fichier.
   :rtype: laspy.LasData
   """
    with laspy.open('H:/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:
        las = fh.read()
        # Affichage du nombre total de points dans le fichier
        print('Points from Header:', fh.header.point_count)
# Affichage du nombre de points réellement lus
        print(las)
        print('Points from data:', len(las.points))
# Extraction des points classés comme "sol" (classification = 2)
        ground_pts = las.classification == 2
        bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
        print('Ground Point Return Number distribution:')
        for r,c in zip(bins,counts):
            print('    {}:{}'.format(r,c))
    return las

# Lecture du fichier LAS pour extraire ses données

with laspy.open('H:/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:
      las = fh.read()          
#liste des cordonnée, récupération des coordonnées XYZ de chaque point
X=las.x
Y=las.y
Z=las.z
#liste couleur RGB #couleur via lidar  /256 ( Divisées par 256 car souvent codées sur 16 bits )
R=las.red/256
B=las.blue/256
G=las.green/256
#plt.plot(X,Y,Z)
#plt.show()


    
# Affichage d’un exemple de point (coordonnées + couleurs)
        

print("Exemple de coordonnées :", list(zip(X, Y, Z,R,B,G))[:1])
   
#couleur disponible

if hasattr(las, "red"):
    r = las.red
    g = las.green
    b = las.blue
    print("Couleurs disponibles")
else:
    print("Pas de couleur dans ce fichier")

#formt d'un point
with laspy.open('H:/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:
     las = fh.read()
        
point_format = las.point_format
print(list(point_format.dimension_names))


# Calcul du NDVI sur chaque point :
# NDVI = (Green - Red) / (Green + Red - Blue)
# Puis recoloration : si NDVI > 0.1, on colore le point en rouge
#NDVI==(Green - Red)/(Green + Red - Blue)

for k in range (len(X)):
    NDVI=(G[k]-R[k])/(G[k]+R[k]-B[k])
    if NDVI>0.1:#valeur de référence pour une végétation moderer 
        G[k]=255
        R[k]=0
        B[k]=0
    else :
         None
         
# Construction de la liste des couleurs RGB normalisées (0-1)
# Utilisées par Matplotlib pour l'affichage
         
C=[]
for i in range(len(X)):
    d=[]
    d.append(R[i]/255)
    d.append(G[i]/255)
    d.append(B[i]/255)
    C.append(d)
         
# Affichage 3D du nuage de points avec coloration NDVI
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(X, Y, Z,c=C, cmap='terrain', s=1)  # scatter 3D
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title("Nuage de points 3D")
plt.show()

         
            
# import numpy as np
# import matplotlib.pyplot as plt

# # Créer des données pour les axes x, y et z
# z = Z
# x = X
# y = Y

# # Créer un objet Axes3D pour le graphique 3D
# plt.figure("Exemple de courbe en 3D")
# axes = plt.axes(projection="3d")
# print(axes, type(axes))

# # Tracer les lignes en 3D
# axes.plot(x, y, z)

# # Ajouter des étiquettes pour les axes
# axes.set_xlabel("X")
# axes.set_ylabel("Y")
# axes.set_zlabel("Z")

# # Afficher le graphique en 3D
# plt.show()





