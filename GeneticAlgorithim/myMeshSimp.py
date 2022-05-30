import numpy as np
import trimesh as tm
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay as dl

def my_triangulation(points):
    return (dl(points[:,(0,1)]).simplices)

def my_mesh_builder(points, triangles):
    return tm.Trimesh(vertices=points, faces=triangles)
    
class Individual:

    def __init__(self, original_number_of_points, original_points, original_area, keep_or_leave = None):

        self.keep_or_leave = keep_or_leave

        if(keep_or_leave == None):
            self.generate_keep_or_leave(original_number_of_points)
        
        self.number_of_points = None
        self.generate_number_of_points()

        self.points = []
        self.generate_points(original_number_of_points, original_points)

        self.area = my_mesh_builder(self.points, my_triangulation(self.points)).area

        self.error = np.abs(original_area - self.area)

        self.distance = 0 #!!

    def generate_keep_or_leave(self, original_number_of_points):
        self.keep_or_leave = [np.random.randint(2) for _ in range(original_number_of_points)]

    def generate_number_of_points(self):
        self.number_of_points = sum(self.keep_or_leave)

        while(self.number_of_points <= 2):
            i = 0
            if(self.keep_or_leave[i] == 0):
                self.keep_or_leave[i] = 1
                self.number_of_points = self.number_of_points + 1
            i = i + 1

    def generate_points(self, original_number_of_points, original_points):
        for i in range(original_number_of_points):
            if(self.keep_or_leave[i] == 1):
                self.points.append(original_points[i])
        self.points = np.array(self.points)
    
    def dominates(self, individual):
        if((self.error <= individual.error and self.number_of_points <= individual.number_of_points) 
        and (self.error < individual.error or self.number_of_points < individual.number_of_points)):
            return True
        else:
            return False
    
    def __str__(self):
        return "NP_"+ str(self.number_of_points) + "_Er_" + str(self.error)
    
    def __repr__(self):
        return self.__str__()

    def print_info(self):
        show_k_or_l = "Keep or leave: \n" + str(self.keep_or_leave) + "\n"
        show_number_of_points = "Number of points: \n" + str(self.number_of_points) + "\n"
        show_points = "Points: \n" + str(self.points) + "\n"
        show_area = "Area: \n" + str(self.area) + "\n"
        show_error = "Error: \n" + str(self.error) + "\n"
        show_distance = "Distance: \n" + str(self.distance) + "\n"

        print(show_k_or_l + show_number_of_points + show_points + show_area + show_error + show_distance)

class My_Mesh_Simp:

    def __init__(self,original_mesh, population_size, mutation_rate):

        self.original_points = original_mesh.vertices
        self.original_number_of_points = len(self.original_points)
        self.original_area = original_mesh.area

        self.population_size = population_size
        self.population = []
        self.generate_first_population(self.original_number_of_points, self.original_points, self.original_area)

        self.fronts_size = 0
        self.fronts = []

        self.mutation_rate = mutation_rate
        
        self.graph_individuals = [self.population[0]]
    
    def generate_first_population(self, original_number_of_points, original_points, original_area):
        
        for _ in range(2*self.population_size):
            self.population.append(Individual(original_number_of_points, original_points, original_area))

    def calculate_front(self):

        front = []
        front.append(self.population.pop(0))
        
        p = 0
        f = 0
        is_p_dominated = False

        while(p < len(self.population)):
            while(f < len(front)):
                
                if(front[f].dominates(self.population[p])):
                    # print(front[f], "from the front, dominates", self.population[p])
                    is_p_dominated = True
                
                if(self.population[p].dominates(front[f])):
                    # print(self.population[p], "dominates", front[f])
                    # print("We remove", front[f], "from the front")
                    self.population.append(front.pop(f))
                    f = f-1

                f = f+1
            if(not is_p_dominated):
                front.append(self.population.pop(p))
                p = p -1
            
            is_p_dominated = False
            p = p +1
            f = 0
        
        return front
    
    def calculate_all_fronts(self):

        while(self.fronts_size < self.population_size):
            front = self.calculate_front()
            self.fronts_size = self.fronts_size + len(front)
            self.fronts.append(front)

    def calculate_distances(self):
        for individual in self.population:
            individual.distance = 0 #!!
        
        self.fronts[-1].sort(key= lambda individual: individual.number_of_points, reverse = False)

        self.fronts[-1][0].distance = np.inf
        self.fronts[-1][-1].distance = np.inf

        for i in range(1,len(self.fronts[-1])-1):
            self.fronts[-1][i].distance = \
            self.fronts[-1][i].distance + \
            (self.fronts[-1][i+1].number_of_points - self.fronts[-1][i-1].number_of_points)/ \
            (self.fronts[-1][-1].number_of_points - self.fronts[-1][0].number_of_points)

        
        self.fronts[-1].sort(key= lambda individual: individual.error, reverse = False)
        
        self.fronts[-1][0].distance = np.inf
        self.fronts[-1][-1].distance = np.inf

        for i in range(1,len(self.fronts[-1])-1):
            self.fronts[-1][i].distance = \
            self.fronts[-1][i].distance + \
            (self.fronts[-1][i+1].error - self.fronts[-1][i-1].error)/ \
            (self.fronts[-1][-1].error - self.fronts[-1][0].error)
        
        self.fronts[-1].sort(key= lambda individual: individual.distance, reverse = True)

    def select_the_fittest(self):
        self.population = []
        for i in range(len(self.fronts)-1):
            self.population += self.fronts[i]
        
        cut = len(self.fronts[-1]) - (self.fronts_size - self.population_size)

        if(cut < len(self.fronts[-1])):
            self.calculate_distances()

        self.population += self.fronts[-1][0:cut]
        
        s = [(self.population[i].number_of_points + self.population[i].error, self.population[i]) for i in range(len(self.population))]
        st = sorted(s)
    
        self.graph_individuals.append(st[0][1])

        self.fronts_size = 0
        self.fronts = [] 

    def generate_offspring(self):
            offspring = []
            for _ in range(len(self.population)):
                i,j = np.random.choice(range(0,len(self.population)),size=2, replace=False)
                
                new_keep_or_leave = self.mutation([self.population[i].keep_or_leave[k] if np.random.rand() < 0.5 
                                    else self.population[j].keep_or_leave[k] 
                                    for k in range(self.original_number_of_points)])

                offspring.append(Individual(self.original_number_of_points, self.original_points, self.original_area, new_keep_or_leave))

            self.population += offspring
        
    def mutation(self, keep_or_leave):
        mutated_keep_or_leave =  [(1 if keep_or_leave[k] == 0 else 0) if np.random.rand() < self.mutation_rate
                                    else keep_or_leave[k] for k in range(self.original_number_of_points)]
        return mutated_keep_or_leave
        
    def run_iteration(self, number_of_iterations):

        for _ in range(number_of_iterations-1):
            self.calculate_all_fronts()
            self.select_the_fittest()
            all_number_of_points = [individual.number_of_points for individual in self.population]
            all_errors = [individual.error for individual in self.population]
            plt.plot(all_number_of_points,all_errors, '+', color="black", ms=5, mec="black")
            self.generate_offspring()

        self.calculate_all_fronts()
        self.select_the_fittest()
        all_number_of_points = [individual.number_of_points for individual in self.population]
        all_errors = [individual.error for individual in self.population]
        plt.plot(all_number_of_points,all_errors, 'o', color="red", ms=5, mec="red")
        plt.xlabel("Número de puntos")
        plt.ylabel("Error")
        plt.show()
   
np.random.seed(1)
# mesh = tm.load("lowlaurana.obj", file_type='obj')
mesh = tm.load("face_2.obj", file_type='obj')
my_mesh_simp = My_Mesh_Simp(original_mesh=mesh, population_size=20, mutation_rate=0.01)
my_mesh_simp.run_iteration(500)