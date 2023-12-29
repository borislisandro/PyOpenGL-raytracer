from config import *
import sphere
import plane
import light
import triangle

class Buffer:

    def __init__(self, size: int, binding: int, floatCount: int):

        self.size = size
        self.binding = binding
        self.floatCount = floatCount

        # (cx cy cz r) (r g b _)
        self.hostMemory = np.zeros(floatCount * size, dtype=np.float32)

        self.deviceMemory = glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMemory)
        glBufferStorage(
            GL_SHADER_STORAGE_BUFFER, self.hostMemory.nbytes, 
            self.hostMemory, GL_DYNAMIC_STORAGE_BIT)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, binding, self.deviceMemory)
        self.elements_written = 0

    def recordLight(self, i: int, light: light.Light) -> None:
        """
            Record the given light sourc ein position i. If it exceeds the buffer size, 
            the light is not recorded
        """
        if i >= self.size:
            return
        # p0 p1 p2 str c0 c1 c2 r
        baseIndex = self.floatCount * i
        self.hostMemory[baseIndex : baseIndex + 3] = light.position[:]
        self.hostMemory[baseIndex + 3] = light.strength
        self.hostMemory[baseIndex + 4: baseIndex + 7] = light.color[:]
        self.elements_written += 1
    
    def recordSphere(self, i: int, _sphere: sphere.Sphere) -> None:
        """
            Record the given sphere in position i, if this exceeds the buffer size,
            the sphere is not recorded.
        """

        if i >= self.size:
            return
        # c0 c1 c2 r c0 c1 c2 r r x x x
        baseIndex = self.floatCount * i
        self.hostMemory[baseIndex : baseIndex + 3] = _sphere.center[:]
        self.hostMemory[baseIndex + 3] = _sphere.radius
        self.hostMemory[baseIndex + 4 : baseIndex + 7] = _sphere.color[:]
        self.hostMemory[baseIndex + 7] = _sphere.roughness
        self.hostMemory[baseIndex + 8] = _sphere.reflectivity
        self.elements_written += 1
    
    def recordPlane(self, i: int, _plane: plane.Plane) -> None:
        """
            Record the given sphere in position i, if this exceeds the buffer size,
            the sphere is not recorded.
        """

        if i >= self.size:
            return

        baseIndex = self.floatCount * i
        # plane: (cx cy cz umin) (tx ty tz umax) (bx by bz vmin) (nx ny nz vmax) (material - - -)

        self.hostMemory[baseIndex : baseIndex + 3]  = _plane.center[:]
        self.hostMemory[baseIndex + 3]              = _plane.uMin

        self.hostMemory[baseIndex + 4 : baseIndex + 7]  = _plane.tangent[:]
        self.hostMemory[baseIndex + 7]                  = _plane.uMax

        self.hostMemory[baseIndex + 8 : baseIndex + 11] = _plane.bitangent[:]
        self.hostMemory[baseIndex + 11]                 = _plane.vMin

        self.hostMemory[baseIndex + 12 : baseIndex + 15]    = _plane.normal[:]
        self.hostMemory[baseIndex + 15]                     = _plane.vMax

        self.hostMemory[baseIndex + 16] = _plane.material_index
        self.elements_written += 1

    def recordTriangle(self, i: int, _triangle: triangle.Triangle) -> None:
        """
            Record the given sphere in position i, if this exceeds the buffer size,
            the sphere is not recorded.
        """
        #xxxx xxxx xxxx xxxxx
        if i >= self.size:
            return

        baseIndex = self.floatCount * i

        for j in range(3):
            self.hostMemory[baseIndex + 4*j : baseIndex + 4*j + 3] =\
                _triangle.corners[j][:]
        
        self.hostMemory[baseIndex + 12 : baseIndex + 15] = _triangle.normal[:]

        self.hostMemory[baseIndex + 3] = _triangle.color[0]
        self.hostMemory[baseIndex + 7] = _triangle.color[1]
        self.hostMemory[baseIndex + 11] = _triangle.color[2]
        self.hostMemory[baseIndex + 15] = _triangle.roughness
        self.hostMemory[baseIndex + 16] = _triangle.reflectivity

        self.elements_written += 1
    
    def readFrom(self) -> None:
        """
            Upload the CPU data to the buffer, then arm it for reading.
        """

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.deviceMemory)
        glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self.floatCount * 4 * self.elements_written, self.hostMemory)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, self.binding, self.deviceMemory)
        self.elements_written = 0
    
    def destroy(self) -> None:
        """
            Free the memory.
        """

        glDeleteBuffers(1, (self.deviceMemory,))