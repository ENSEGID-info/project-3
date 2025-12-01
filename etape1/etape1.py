

import laspy
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
        las = fh.read()
        print('Points from Header:', fh.header.point_count)
       
        print(las)
        print('Points from data:', len(las.points))
        ground_pts = las.classification == 2
        bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
        print('Ground Point Return Number distribution:')
        for r,c in zip(bins,counts):
            print('    {}:{}'.format(r,c))
    return las
with laspy.open('H:/Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:
      las = fh.read()          
#liste des cordonnée
X=las.x
Y=las.y
Z=las.z
#liste couleur RGB #couleur via lidar  /256
R=las.red/256
B=las.blue/256
G=las.green/256
#plt.plot(X,Y,Z)
#plt.show()
        

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

#NDVI==(Green - Red)/(Green + Red - Blue)

for k in range (len(X)):
    NDVI=(G[k]-R[k])/(G[k]+R[k]-B[k])
    if NDVI>0.2:#valeur de référence pour une végétation moderer 
        G[k]=255
        R[k]=0
        B[k]=0
    else :
         None
            
            
    






