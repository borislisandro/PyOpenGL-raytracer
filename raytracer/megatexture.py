from config import *

class MegaTexture:

    def __init__(self, filenames):
        
        texture_size = 1024
        texture_count = len(filenames)
        #print(f"texture_count = {texture_count}")
        
        height = texture_size

        image_types = ("Color", "Displacement", "Normal", "Roughness","Metalness","Specular","Emission","AO")

        width = texture_size * len(image_types)
        
        textureLayers = [Image.new(mode = "RGBA", size = (width, height)) for _ in range(texture_count)]
        
        for i in range(texture_count):
            print(f"Loading textures\{filenames[i]}")
            for j, image_type in enumerate(image_types):
                with Image.open(f"textures\{filenames[i]}\{filenames[i]}_{image_type}.png", mode = "r") as img:
                    img = img.convert("RGBA")
                    #img.save(f"intermediate_{i}_{j}.png")
                    textureLayers[i].paste(img, (j * texture_size, 0))
                    
            textureLayers[i].save(f"intermediate_{i}.png")

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_RGBA32F,width, height,texture_count)
        #glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, width, height, texture_count, 0, GL_RGBA, GL_UNSIGNED_BYTE, None);

        for i in range(texture_count):
            img_data = bytes(textureLayers[i].tobytes())
            glTexSubImage3D(GL_TEXTURE_2D_ARRAY,0,0,0,i,width, height, 1,GL_RGBA,GL_UNSIGNED_BYTE,img_data)
    
        glActiveTexture(GL_TEXTURE3)
        glBindImageTexture(3,self.texture,0,GL_FALSE,0,GL_READ_ONLY, GL_RGBA32F)

    def destroy(self):
        glDeleteTextures(1, self.texture)