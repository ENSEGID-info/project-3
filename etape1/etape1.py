
import math
import laspy
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
#        ♥   OUVERTURE DES FICHIERS LASPY   ♥
# ==================================================

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
    with laspy.open('H:\Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:    
        las = fh.read()
# Affichage du nombre total de points dans le fichier
        print('Points from Header:', fh.header.point_count)
        point_format = las.point_format
        print(list(point_format.dimension_names))
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

def co():
    las=ouverture_laspy()
    X=list(las.x)              #liste des cordonnées
    Y=list(las.y) 
    Z=list(las.z)           
    R=list(las.red/256)        #liste couleur RGB   #couleur via lidar  /256
    B=list(las.blue/256)
    G=list(las.green/256)
    return X,Y,Z,R,G,B


def couleur_arbre():
    X,Y,Z,R,G,B=co()
    for k in range (len(X)):
        NDVI=(G[k]-R[k])/(G[k]+R[k]-B[k])#NDVI==(Green - Red)/(Green + Red - Blue)
        if Z[k]>1792:
            if NDVI>0.1:#valeur de référence pour une végétation moderer 
                G[k]=255
                R[k]=0
                B[k]=0
            else :
                None
        else:
            None 
    return R,G,B

        
def exemple():
    return("Exemple de coordonnées :", list(zip(co()))[:1])# Affichage d’un exemple de point (coordonnées + couleurs)
   

def couleur_arbre1():
    X,Y,Z,R,G,B=co()
    x=[]
    y=[]
    z=[]
    r=[]
    g=[]
    b=[]
    for k in range (len(X)):
        NDVI=(G[k]-R[k])/(G[k]+R[k]-B[k])#NDVI==(Green - Red)/(Green + Red - Blue)
        if Z[k]>1792 and NDVI>-0.015:
            None
        else:
            x.append(X[k])
            y.append(Y[k])
            z.append(Z[k])
            r.append(R[k])
            g.append(G[k])
            b.append(B[k]) 
    return x,y,z,r,g,b
            
def liste_couleur():

    R,G,B= couleur_arbre()
    C=[]                         #construit une liste c contenant pour chaque point un triplet [R,G,B] normalisé entre 0 et 1
    for i in range(len(G)):
        d=[]
        d.append(R[i]/255)#/255 --> affiche couleur LIDAR
        d.append(G[i]/255)
        d.append(B[i]/255)
        C.append(d)
    return C
def liste_couleur1():

    x,y,z,R,G,B= couleur_arbre1()
    C=[]                         #construit une liste c contenant pour chaque point un triplet [R,G,B] normalisé entre 0 et 1
    for i in range(len(G)):
        d=[]
        d.append(R[i]/255)#/255 --> affiche couleur LIDAR
        d.append(G[i]/255)
        d.append(B[i]/255)
        C.append(d)
    return C



   



def affichage(): 
    X,Y,Z,R,G,B=co()  # Affichage 3D du nuage de points avec coloration NDVI
    fig = plt.figure()# créer une figure 3D : contient un seul graphique dans la figure
    ax = fig.add_subplot(111, projection='3d') #trace 1 ligne, 1 colonne, 1 figure
    # C=[sup_points()[3],sup_points()[4],sup_points()[5]]
    C=liste_couleur()
# Calcul du NDVI sur chaque point :
# NDVI = (Green - Red) / (Green + Red - Blue)
# Puis recoloration : si NDVI > 0.1, on colore le point en rouge
    ax.scatter(X, Y, Z,c=C, cmap='terrain', s=1)    # scatter 3D, 'c' définit la couleur de chaque point, 'cmap' donne couleur proche de la topographie (image réelle relief), 's' détermine taille des points : ici '1'-> petits points
    ax.set_xlabel('X') 
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    elevation_angle = 25            # modifie angle de vue verticalement
    azimuthal_angle = -130            # modifie angle de vue horizontalement
    ax.view_init(elevation_angle, azimuthal_angle)# affichage des modifications
    plt.title("Nuage de points 3D")
    plt.show()
    return None

def affichage1(): 
    X,Y,Z,R,G,B=couleur_arbre1()  # Affichage 3D du nuage de points avec coloration NDVI
    fig = plt.figure()# créer une figure 3D : contient un seul graphique dans la figure
    ax = fig.add_subplot(111, projection='3d') #trace 1 ligne, 1 colonne, 1 figure
    # C=[sup_points()[3],sup_points()[4],sup_points()[5]]
    C=liste_couleur1()
# Calcul du NDVI sur chaque point :
# NDVI = (Green - Red) / (Green + Red - Blue)
# Puis recoloration : si NDVI > 0.1, on colore le point en rouge
    ax.scatter(X, Y, Z,c=C, cmap='terrain', s=1)    # scatter 3D, 'c' définit la couleur de chaque point, 'cmap' donne couleur proche de la topographie (image réelle relief), 's' détermine taille des points : ici '1'-> petits points
    ax.set_xlabel('X') 
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    elevation_angle = 25            # modifie angle de vue verticalement
    azimuthal_angle = -130            # modifie angle de vue horizontalement
    ax.view_init(elevation_angle, azimuthal_angle)# affichage des modifications
    plt.title("Nuage de points 3D")
    plt.show()
    return None


 

            
         
            







