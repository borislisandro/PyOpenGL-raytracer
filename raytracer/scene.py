from config import *
import sphere
import camera
import plane
import light
import triangle
from objparser import *

class Scene:
    """
        Holds pointers to all objects in the scene
    """


    def __init__(self):
        """
            Set up scene objects.
        """

        self.spheres = [
            sphere.Sphere(
                center = [
                    np.random.uniform(low = -1.0, high = 1.0),
                    np.random.uniform(low = -2.0, high = 2.0),
                    np.random.uniform(low = -1.0, high = 1.0)
                ],
                radius = np.random.uniform(low = 0.3, high = 0.3),
                color = [
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0),
                    np.random.uniform(low = 0.3, high = 1.0)
                ],
                roughness=np.random.uniform(low = 0.3, high = 1.0),
                reflectivity=0.8
            ) for i in range(12)
        ]
    
        self.obj_name = ["couchfixed.obj",
                         "cubone.obj",
                         "tvstand.obj",
                         "lamp.obj",
                         "tv.obj",
                         "window.obj",
                         "human.obj"]
        
        self.model_ratio = [2,
                            2,
                            1.5,
                            1.5,
                            0.14,
                            1.5,
                            2]
        self.color= [[0.7,0.7,0.7],
                     [0.827,0.4,0.0],
                     [0.54,0.27,0.07],
                     [0.27,0.27,0.24],
                     [0.05,0.05,0.05],
                     [0.827,0.827,0.827],
                     [0.2,0.8,0.2]]
        self.position = [[0.0, 3.3, 2.65], 
                        [-0.3, 0, 2.15],
                        [-0.1, -3.6, 2.98],
                        [1.8, 3.29, 3.02],
                        [-0.09, -3.54, 2.44],
                        [1.95, 0, 2.07],
                        [-6.3, -1.7, 1.7]]
        self.reflectivity = [0.0,
                             0.6,
                             0.0,
                             0.4,
                             0.2,
                             0.0,
                             0.4]
        self.roughness = [0.0,
                          0.0,
                          0.0,
                          0.0,
                          0.0,
                          0.0,
                          0.0]

        self.triangles = self.defTriangles()

        self.planes = self.defPlanes()

        self.light_position = (0, 0, 0)
        self.light_strength = 1
        self.light_radius = 0.15
        self.lights = self.defLight() 

        self.objectCounts = np.array([len(self.spheres), len(self.planes), len(self.lights), len(self.triangles)], dtype = np.int32)
        print(self.objectCounts)
        self.camera = camera.Camera(
            position = [-5, 0, 1]
        )

        self.outDated = True

    def changeObj(self,number,pos,light_strength,light_radius):
        self.light_strength += light_strength
        self.light_radius += light_radius
        print(self.light_strength,self.light_radius)
        self.position[int(number)][0] +=  pos[0]
        self.position[int(number)][1] +=  pos[1]
        self.position[int(number)][2] +=  pos[2]
        print(self.position)
        self.triangles = self.defTriangles()
        self.planes = self.defPlanes()
        self.lights = self.defLight()

        self.objectCounts = np.array([len(self.spheres), len(self.planes), len(self.lights), len(self.triangles)], dtype = np.int32)
        print(self.objectCounts)

    def defTriangles(self):


        triangles = []
        temp = []

        for i,obj in enumerate(self.obj_name):
            objects = ObjParser("models/"+obj)
            triangle_temp  = []
            for _object in objects:
                # _object [0] = nome do objeto ||  _object[1] = info dos triangulos
                corners= []
                if(True):
                    print("Loading object: "+ _object[0])
                    for value in _object[1]:
                        temp.append(value)
                        if len(temp) == 5:
                            corners.append([temp[2]*self.model_ratio[i],temp[3]*self.model_ratio[i],temp[4]*self.model_ratio[i]])
                            temp = []
                        if len(corners) == 3:
                            triangle_temp.append(corners)
                            corners= []

                for triangle_corners in triangle_temp:
                    triangle_t =[]
                    for corner in triangle_corners:
                        triangle_t.append([corner[0]+self.position[i][0],corner[1]+self.position[i][1],corner[2]+self.position[i][2]])
                    triangles.append(triangle.Triangle(corners = triangle_t , color = self.color[i],roughness=self.roughness[i],reflectivity=self.reflectivity[i]))

        return triangles

    def defLight(self):
        lights = []
        lights.append(
            light.Light(
                position = self.light_position,
                strength = self.light_strength,#np.random.uniform(low = 1.0, high = 200.0),
                color = [
                    np.random.uniform(low = 1, high = 1.0),
                    np.random.uniform(low = 1, high = 1.0),
                    np.random.uniform(low = 1, high = 1.0)
                ],
                radius = self.light_radius,
                point_count  = 16
            )
        )
        return lights
        

    def defPlanes(self):
        planes = []
        planes.append( # top
            plane.Plane(
                normal = [0, 0, 1],
                tangent = [0, 1, 0],
                bitangent = [1, 0, 0],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 8,
                center = [0, 0, -1],
                material_index = 1
            )
        )
        planes.append( # left
            plane.Plane(
                normal = [0, 1, 0],
                tangent = [0, 0, 1],
                bitangent = [1, 0, 0],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 8,
                center = [0, 4, 1],
                material_index = 2
            )
        )
        planes.append( # right
            plane.Plane(
                normal = [0, -1, 0],
                tangent = [0, 0, 1],
                bitangent = [1, 0, 0],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 8,
                center = [0, -4, 1],
                material_index = 2
            )
        )
        planes.append( # bottom
            plane.Plane(
                normal = [0, 0, -1],
                tangent = [0, 1, 0],
                bitangent = [1, 0, 0],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 2,
                center = [0, 0, 3],
                material_index = 0
            )
        )
        planes.append( # fundo
            plane.Plane(
                normal = [-1, 0, 0],
                tangent = [0, 1, 0],
                bitangent = [0, 0, 1],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 8,
                center = [2, 0, 1],
                material_index = 2
            )
        )
        
        planes.append( # tr'as
            plane.Plane(
                normal = [1, 0, 0],
                tangent = [0, 1, 0],
                bitangent = [0, 0, 1],
                uMin = -8,
                uMax = 8,
                vMin = -8,
                vMax = 8,
                center = [-8, 0, 1],
                material_index = 2
            )
        )         
        
        planes.append( # fundo
            plane.Plane(
                normal = [-1, 0, 0],
                tangent = [0, 1, 0],
                bitangent = [0, 0, 1],
                uMin = -4,
                uMax = 4,
                vMin = -2,
                vMax = 2,
                center = [2, 0, 1],
                material_index = 2
            )
        )

        planes.append( # janela
            plane.Plane(
                normal = [-1, 0, 0],
                tangent = [0, 1, 0],
                bitangent = [0, 0, 1],
                uMin = -1.3,
                uMax = 1.3,
                vMin = -1.18,
                vMax = 1.18,
                center = [1.93, 0, 0.75],
                material_index = 1
            )
        )
        
        return planes
    
    def move_player(self, forward,side):

        dPos = forward * self.camera.forwards + side * self.camera.right

        self.camera.position[0] += dPos[0]
        self.camera.position[1] += dPos[1]

    def spin_player(self, dAngle):



        self.camera.theta += dAngle[0]

        if(self.camera.theta < 0):
            self.camera.theta += 360
        if(self.camera.theta > 360):
            self.camera.theta -= 360

        self.camera.phi += dAngle[1]

        if(self.camera.theta < (-1000*360)):
            self.camera.theta = 0
        elif(self.camera.theta > (1000*360)):
            self.camera.theta = 0

        self.camera.recalculateVectors()