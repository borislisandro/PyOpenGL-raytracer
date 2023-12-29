from config import *

class Light:
    
    
    def __init__(self, position, color, strength,radius, point_count):
        self.position = np.array(position, dtype = np.float32)
        self.color = np.array(color, dtype = np.float32)
        self.strength = strength
        self.radius = radius
        self.points = []
        """ points = [
            (radius+position[0], 0 ,0),
            (-radius+position[0], 0 ,0),
            (0, radius+position[1], 0),
            (0, -radius+position[1], 0),
            (0,0, radius+position[2]),
            (0, 0, -radius+position[2])
        ] """
        
        for i in range(point_count):
            self.points.append((position[0]+ radius * np.random.uniform(low = 0.0, high = 1.0),
                                position[1]+ radius * np.random.uniform(low = 0.0, high = 1.0),
                                position[2]+ radius * np.random.uniform(low = 0.0, high = 1.0)))

        """ for i in range(len(points)):
            points[i][0] = position[0] + points[i][0]
            points[i][1] = position[0] + points[i][1]
            points[i][2] = position[0] + points[i][2] """
        point_num = point_count
        