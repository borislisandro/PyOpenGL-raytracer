def ObjParser(modelpath: str = ''):
    
    file = open(modelpath,"r", encoding='utf-8')

    # get only lines that start with v/vn/vt/f
    cleanFile = []
    DirtyObjectNames = []

    with open(modelpath, 'r') as file:
        for line in file:
            if not line:
                break
            elif line[0] in ['v', 'f']:
                cleanFile.append(line)
            elif line[0] == 'o':
                DirtyObjectNames.append(line)
            
    objectNames = []
    objectNames = [obj.strip('o \n') for obj in DirtyObjectNames]

    # divide into multiple objects
    i = 0
    objects = [[]]
    newObject = False
    ignoreFirstObject = True
    for line in cleanFile:
        if line[0] == 'v' and not newObject :
            newObject = True
            if not ignoreFirstObject:
                objects.append([])
                i += 1
            else:
                ignoreFirstObject = False

        elif line[0] == 'f' and newObject:
            newObject = False
        objects[i].append(line)


    #reformat each object to vt vt vn vn vn v v v
    #                        f v[i]/vt[i]/vn[i]
    parcedObjects = []
    vs = []
    vts = []
    i = 0
    for object in objects:
        fs = []
        for line in object:
            tokens = line.split()
            if tokens[0] == 'v':
                vs.append(tokens[1:4])
            elif tokens[0] == 'vt':
                vts.append(tokens[1:3])
            elif tokens[0] == 'vn':
                continue
            else:
                fs_temp = [item.split('/') for item in tokens[1:5]]
                fs.append(fs_temp)
                
        temp = []
        faces = []
        for f in fs:
            temp2 = []
            if len(f) == 4:     #when f declares 2 triangles
                temp2 = []
                for f_temp in [f[0],f[1],f[2]]:
                    for item in vts[int(f_temp[1])-1]:
                        temp.append(float(item))
                    for item in vs[int(f_temp[0])-1]:
                        temp.append(float(item))
                    temp2.append(int(f_temp[0])-1) 
                faces.append(temp2)
                temp2 = []
                for f_temp in [f[3],f[0],f[2]]:
                    for item in vts[int(f_temp[1])-1]:
                        temp.append(float(item))
                    for item in vs[int(f_temp[0])-1]:
                        temp.append(float(item))
                    temp2.append(int(f_temp[0])-1)
                faces.append(temp2)  
            elif len(f) == 3:   #when f declares 1 triangle
                temp2 = []
                for f_temp in f:
                    for item in vts[int(f_temp[1])-1]:
                        temp.append(float(item))
                    for item in vs[int(f_temp[0])-1]:
                        temp.append(float(item))
                    temp2.append(int(f_temp[0])-1) 
                faces.append(temp2)
            else: 
                print("TERMINAL ERROR ( F = X//X) EXITING")
                exit() 
        concant= [objectNames[i],temp,faces]
        parcedObjects.append(concant)  
        i += 1
    return parcedObjects