from config import * 


class Sphere:

    def __init__(self,center,radius,color,roughness,reflectivity):
        self.type = 1
        self.center = np.array(center,dtype = np.float32)
        self.radius = radius
        self.color = np.array(color,dtype = np.float32)
        self.roughness = roughness
        self.reflectivity = reflectivity