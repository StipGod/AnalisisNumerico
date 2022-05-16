import numpy as np
import trimesh as tm
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay as dl

mesh = tm.load("lowlaurana.obj", file_type='obj')
fm = dl(mesh.vertices[:,(0,1)])
mesh = tm.Trimesh(vertices=mesh.vertices, faces=fm.simplices)
AreaMesh = mesh.area

class gen:
    def __init__(self, ngenerations = 100, npopulation = 20, nselection = 5, sizeindividuo = len(mesh.vertices), mutaprob = 0.1, verbose = False):
        self.ngenerations = ngenerations
        self.npopulation = npopulation
        self.sizeindividuo = sizeindividuo
        self.mutaprob = mutaprob
        self.verbose = verbose
        self.nselection = nselection
            
    def createindividuo(self):
        return [np.random.randint(2) for i in range(self.sizeindividuo)]
    
    def createpopulation(self):
        return [self.createindividuo() for i in range(self.npopulation)]

    def fitness(self, individuo):
        v = mesh.vertices 
        index = np.where(np.array(individuo) == 1)
        v = np.delete(v, index, axis=0)
        f = dl(v[:,(0,1)])
        nmesh = tm.Trimesh(vertices=v, faces=f.simplices)
        nArea = nmesh.area
        return np.sqrt((np.abs(nArea - AreaMesh)**2 + len(f.simplices)**2))
    
    def selection(self, population):
        selection = [[self.fitness(population[i]),population[i]] for i in range(len(population))]
        st = sorted(selection)[:self.nselection]
        return [st[i][1] for i in range(len(st))]
    
    def cross(self,selection):
        newgeneration = []
        ns = [i[1] for i in selection]
        for i in range(len(selection)):
            for j in range(i+1,len(selection)):
                newgeneration.append([selection[i][k] if np.random.rand() < 0.5 else selection[j][k] for k in range(self.sizeindividuo)])
        return newgeneration + selection
    
    def mutation(self,population):
        for i in range(len(population)):
            population[i] = [np.random.randint(2) if np.random.rand() < self.mutaprob else population[i][j] for j in range(len(population[i]))]
        return population
    
    def generations(self):
        population = self.createpopulation()
        for i in range(self.ngenerations):
            population = self.mutation(self.cross(self.selection(population)))
        return population
            
test = gen()
# print(test.cross(test.selection(test.createpopulation())))

best = test.selection(test.generations())[0]

vo = mesh.vertices
index = np.where(np.array(best) == 1)
vb = np.delete(vo, index, axis=0)
fb = dl(vb[:,(0,1)])
nmesh = tm.Trimesh(vertices=vb, faces=fb.simplices)
print(f"Original vertices number: {len(vo)} \n Vertices number: {len(vb)} \n Triangles number: {len(fb.simplices)} \n Error: {np.abs(AreaMesh - nmesh.area)}")
nmesh.show()
nmesh.visual = tm.visual.ColorVisuals()
# asd = nmesh.export("lowlaurana.obj", file_type="obj")