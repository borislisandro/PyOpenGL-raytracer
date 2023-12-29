from config import * 

class Camera:


    def __init__(self, position):
        

        self.position = np.array(position,dtype = np.float32)

        self.theta = 0
        self.phi = 0
        self.recalculateVectors()

    def recalculateVectors(self):
        
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ], dtype = np.float32
        )

        self.right = pyrr.vector3.cross(self.forwards, np.array([0,0,1],dtype = np.float32))

        self.up = pyrr.vector3.cross(self.right,self.forwards)