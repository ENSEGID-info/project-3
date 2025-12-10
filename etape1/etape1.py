

import laspy
import numpy as np
import matplotlib.pyplot as plt

def etape1_main():
    print("Exécution de l'étape 1...")            # Exemple : lecture d’un fichier ou génération de données
    data = [1, 2, 3]
    print("Input data is " + str(data) + ".")
    return data



def ouverture_laspy():
    """
    

    Returns
    -------
    las : TYPE
        DESCRIPTION.

    """
    with laspy.open('H:\Données de la prof/2504_SEGO_NewMorvan_subset_filtered_03_percent.las') as fh:    
        las = fh.read()
        print('Points from Header:', fh.header.point_count)
        point_format = las.point_format
        print(list(point_format.dimension_names))
        print(las)
        print('Points from data:', len(las.points))
        ground_pts = las.classification == 2
        bins, counts = np.unique(las.return_number[ground_pts], return_counts=True)
        print('Ground Point Return Number distribution:')
        for r,c in zip(bins,counts):
            print('    {}:{}'.format(r,c))
    return las 

def co():
    las =ouverture_laspy()
    #liste des cordonnée
    X=las.x
    Y=las.y
    Z=las.z
    #liste couleur RGB #couleur via lidar  /256
    R=las.red/256
    B=las.blue/256
    G=las.green/256
    
    return X,Y,Z,R,G,B
def exemple():
    return("Exemple de coordonnées :", list(zip(co()))[:1])
   
#NDVI==(Green - Red)/(Green + Red - Blue)
def couleur_arbre():
    X,Y,Z,R,G,B=co()
    for k in range (len(X)):
        NDVI=(G[k]-R[k])/(G[k]+R[k]-B[k])
        if Z[k]>1792:
            if NDVI>0.1:#valeur de référence pour une végétation moderer 
                G[k]=255
                R[k]=0
                B[k]=0
            else :
                None
        else:
            None 
    return G,R,B
            
def liste_couleur():

    G,R,B= couleur_arbre()
    C=[]
    for i in range(len(G)):
        d=[]
        d.append(R[i]/255)
        d.append(G[i]/255)
        d.append(B[i]/255)
        C.append(d)
    return C

def sup_points():
    return 
        
def affichage(): 
    X,Y,Z,R,G,B=co()       
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    C=liste_couleur()

    ax.scatter(X, Y, Z,c=C, cmap='terrain', s=1)     # scatter 3D
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    elevation_angle = 25            # modifie angle de vue verticalement
    azimuthal_angle = -130            # modifie angle de vue horizontalement
    ax.view_init(elevation_angle, azimuthal_angle)
    plt.title("Nuage de points 3D")
    plt.show()
    return None

         
            







