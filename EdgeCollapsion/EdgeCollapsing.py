from math import sqrt
from operator import truediv
from pickle import FALSE, TRUE
import trimesh as tm
import numpy as np

mesh = tm.load("lowlaurana.obj", file_type = 'obj')

tm.viewer.SceneViewer(mesh)

#E = mesh.edges_unique
E = mesh.edges
V = mesh.vertices 


def calculateLoss(i):
    x = V[E[i,0],0] - V[E[i,1],0]
    y = V[E[i,0],1] - V[E[i,1],1]
    z = V[E[i,0],2] - V[E[i,1],2]

    return sqrt(pow(x,2)+pow(y,2)+pow(z,2))

def deleteVertix(i,j):
    # i tiene que ser menor que j
    V[i,0] = (V[i,0] + V[j,0])/2
    V[i,1] = (V[i,1] + V[j,1])/2
    V[i,2] = (V[i,2] + V[j,2])/2
    
    V = np.delete(V,j,0)

    for e in E:
        if (E[e,0] == i & E[e,0] == j) | (E[e,0] == j & E[e,0] == i): 
            E = np.delete(E,e,0)
            break
    
    deletedEdges = np.array
    nonDeletedEdges = np.array
    for e in E:
        if (E[e,0] == j | E[e,1] == j):
            if E[e,0] < j: E[e,0] -= 1
            if E[e,1] < j: E[e,1] -= 1
            np.append(deletedEdges,E[e])
            E = np.delete(E, e, 0)
            e -= 1
        elif (E[e,0] == i | E[e,1] == i):
            if E[e,0] < j: E[e,0] -= 1
            if E[e,1] < j: E[e,1] -= 1
            np.append(nonDeletedEdges,E[e])
        else:
            if E[e,0] < j: E[e,0] -= 1
            if E[e,1] < j: E[e,1] -= 1

    for idxD in deletedEdges:
        posD = 1
        if deletedEdges[idxD,1] == j: posD = 0
        same = FALSE
        for idxN in nonDeletedEdges:
            posN = 1
            if nonDeletedEdges[idxN,1] == i: posN = 0
            if deletedEdges[idxD,posD] == nonDeletedEdges[idxN,posN]:
                same = TRUE
                break
        if same == FALSE:
            np.append(E,[i,deletedEdges[posD]])

def collapse(n):
    for i in range(n):
    #iteramos para saber cual es el error mas bajo para juntar los vertices n veces
        lowErrorIndex = 0 
        lowError = calculateLoss(i)
        for e in E:
            lowErrorAux = calculateLoss(e)
            if(lowErrorAux<lowError): 
                lowError = lowErrorAux
                lowErrorIndex = e
        deleteVertix(np.minimum(E[lowErrorIndex,0],E[lowErrorIndex,1]),np.maximum(E[lowErrorIndex,0],E[lowErrorIndex,1]))

def render():
    pass

#collapse(10)