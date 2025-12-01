
import laspy
import matplotlib as plt

# --- Chemin vers ton fichier LAS ---
fichier1_las = "H:\TD info\p3\image1.las"

fichier2_las = "H:\TD info\p3\image2.las"
# --- Ouvrir le fichier LAS ---
las1 = laspy.read(fichier1_las)
las2 = laspy.read(fichier2_las)

# --- Afficher quelques infos ---
print("Nombre de points :", len(las1.points))
print("Système de coordonnées :", las1.header.parse_crs())
print("Dimensions disponibles :", las1.point_format.dimension_names)

# --- Accéder aux coordonnées x, y, z ---
x = las1.x
y = las1.y
z = las1.z

print("Quelques points exemple :")
X=[]
Y=[]

for i in range(10,20):
    print(f"({x[i]}, {y[i]}, {z[i]})")
    X.append(x[i])
    Y.append(y[i])
    



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # nécessaire pour les tracés 3D

fig = plt.figure()
ax 
= fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c=z, cmap='terrain', s=1)  # scatter 3D
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title("Nuage de points 3D")
plt.show()

# --- Si tu veux tout convertir en un tableau NumPy ---
import numpy as np
points = np.vstack((x, y, z)).T  # tableau Nx3
print("Forme du tableau :", points.shape)

def  profil_ero():
    L=[]  
    Y2=[]
    Z2=[]
    Y3=[]
    Z3=[]
    Zf=[]
    Yf=[]
    for k in range(len(x)):
        if x[k]==x[2]:
            L.append(k)
            Y2.append(y[k])
            Z2.append(z[k])
        if x[k]==x[3]:
            L.append(k)
            Y3.append(y[k])
            Z3.append(z[k])
                 
    # for k in range(len(Y2)):
    #     Yf.append((Y3[k]+Y2[k])/2)
    #     Zf.append((Z3[k]+Z2[k])/2)
    T=[]
    for i in range(len(x)):
        for k in range(len(x)):
            if x[k]==x[i]:
                T.append(k)
                L.append(k)
                Yf.append(y[k])
                Zf.append(z[k])  
                plt.scatter(Yf,Zf)
                plt.scatter(Yf, Zf,s=80,marker='^', alpha=0.7,edgecolor='black')
        Zf=[]
        Yf=[]
    plt.show()



















































def etape3_main(result):
    print("Exécution de l'étape 3...")
    # Exemple : display of the result
    print("Maximum is " + str(result) + ".")

