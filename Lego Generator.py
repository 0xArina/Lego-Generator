import maya.cmds as cmds
import random as rnd

if 'myWin' in globals():
    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin, window=True)

# Window Title       
myWin = cmds.window(title="Lego Blocks", menuBar=True)

# Collapsible Menu with options to create New Scene and Delete Selected
cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

#          UI: adjust and create a Standard Block               #
#################################################################
cmds.frameLayout(collapsable=True, label="Standard Block", width=475, height=140)

cmds.columnLayout()

cmds.intSliderGrp('height',l="Height", f=True, min=1, max=20, value=3)
cmds.intSliderGrp('blockWidth', l="Width", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('blockLength', l="Length", f=True, min=1, max=20, value=8)
cmds.colorSliderGrp('blockColour', label="Colour", hsv=(120, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Basic Block", command=('basicBlock()'))

# Level Up in Hierarchy
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

#      UI: adjust and create a Standard Block With Holes        #
#################################################################
cmds.frameLayout(collapsable=True, label="Standard Block with Holes", width=475, height=90)

cmds.columnLayout()

cmds.intSliderGrp('blockWithHolesLength', l="Length", f=True, min=1, max=20, value=8)
cmds.colorSliderGrp('blockWithHolesColour', label="Colour", hsv=(120, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Basic Block With Holes", command=('basicBlockWithHoles()'))

# Level Up in Hierarchy
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

#       UI: adjust and create a Rounded Block With Holes        #
#################################################################
cmds.frameLayout(collapsable=True, label="Rounded Block with Holes")

cmds.columnLayout()

cmds.intSliderGrp('roundedBlockWithHolesLength', l="Length", f=True, min=1, max=20, value=8)
cmds.colorSliderGrp('roundedBlockWithHolesColour', label="Colour", hsv=(120, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Rounded Block With Holes", command=('roundedBlockWithHoles()'))

# Level Up in Hierarchy
cmds.setParent( '..' )
cmds.setParent( '..' )
cmds.setParent( '..' )

#   UI: adjust and create a Rounded Block With Holes and Angle  #
#################################################################
#function for syncing UI 
def checkBend60deg(isOn):
    if(isOn):
      # disable adjusting length feauture for bend at 60 deg (had little time left)
      bendLength = cmds.intSliderGrp('roundedBlockWithHolesAngleBendLength', edit=True, en=False)
      length = cmds.intSliderGrp('roundedBlockWithHolesAngleLength', edit=True, en=False)
    else:
        bendLength = cmds.intSliderGrp('roundedBlockWithHolesAngleBendLength', edit=True, en=True)
        length = cmds.intSliderGrp('roundedBlockWithHolesAngleLength', edit=True, en=True)

cmds.frameLayout(collapsable=True, label="Rounded Block with Holes and Angle")

cmds.columnLayout()

cmds.intSliderGrp('roundedBlockWithHolesAngleLength', l="Base Part Length", f=True, min=1, max=20, value=4)
cmds.intSliderGrp('roundedBlockWithHolesAngleBendLength', l="Bended Part Length", f=True, min=2, max=20, value=3)
cmds.radioButtonGrp('roundedBlockWithHolesBendAngle', label="Bend Angle", labelArray2=["90 deg", "60 deg"], numberOfRadioButtons=2, sl=1,cc2=checkBend60deg)
#cmds.radioButton( label='roundedBlockWithHolesBendAngle90', label="Bend at 90 degrees")
#cmds.radioButton( label='roundedBlockWithHolesBendAngle135', label="Bend at 135 degrees")
cmds.colorSliderGrp('roundedBlockWithHolesAngleColour', label="Colour", hsv=(120, 1, 1))

cmds.columnLayout()
cmds.button(label="Create Rounded Block With Holes and Angle", command=('roundedBlockWithHolesAngle()'))

# Level Up in Hierarchy

# show UI window
cmds.showWindow( myWin )

#################################################################
#               Basic Block Without Holes                       #
#################################################################
def basicBlock():
    # query values from UI sliders
    height = cmds.intSliderGrp('height', q=True, v=True)
    width = cmds.intSliderGrp('blockWidth', q=True, v=True)
    length = cmds.intSliderGrp('blockLength', q=True, v=True)   
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    
    # name
    nsTmp = "Block" + str(rnd.randint(1000,9999))
    
    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    # define a cube's size
    cubeSizeX = width * 0.8
    cubeSizeZ = length * 0.8
    cubeSizeY = height * 0.32
    
    # create a cube
    cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    
    # move block half size up on Y axis
    cmds.move((cubeSizeY/2.0), moveY=True)
    
    # loop through width and length (in bumps)
    for i in range(width):
        for j in range(length):
            # create cylinder
            cmds.polyCylinder(r=0.25, h=0.20)
            # move it on Y axis
            cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
            # move it on X axis
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            # move it on Z axis
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
    
    # add material        
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], type='double3')
    
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    
    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)
    
#################################################################
#                    Basic Block With Holes                     #
#################################################################
def basicBlockWithHoles():
    # set up block dimensions
    height = 3
    width = 1 #bump
    length = cmds.intSliderGrp('blockWithHolesLength', q=True, v=True)
    rgb = cmds.colorSliderGrp('blockWithHolesColour', q=True, rgbValue=True)
    
    # name
    nsTmp = "BlockWithHoles" + str(rnd.randint(1000,9999))
    
    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    # define cube's size 
    cubeSizeX = width * 0.8
    cubeSizeZ = length * 0.8
    cubeSizeY = height * 0.32
    
    # create a cube
    cube = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    
    # move it up
    cmds.move((cubeSizeY/2.0), moveY=True)
    
    # create bumps
    for i in range(width):
        for j in range(length):
            # create cylinder
            cmds.polyCylinder(r=0.25, h=0.20)
            # move it
            cmds.move((cubeSizeY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
            
    # create holes
    for i in range(width):
        for j in range(length):
            # create cylinder in the place of a hole
            hole = cmds.polyCylinder(r=0.25, h=height/2.0)
            
            # rotate and position it
            cmds.rotate(90, rotateX=True, a=True)
            cmds.rotate(90, rotateY=True, a=True)
            
            cmds.move((cubeSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0) + 0.4), moveZ=True, a=True)
            
            # remove it from the base block
            cube = cmds.polyCBoolOp(cube, hole, op=2, caching=False, ch=False)
    
    # add material        
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], type='double3')
    
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    
    cmds.hyperShade(assign=(nsTmp+":blckMat"))  
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)
    
#################################################################
#                Rounded Block  With Holes                      #
#################################################################
def roundedBlockWithHoles():
    # set up block dimensions
    height = 3
    width = 1 #bump
    length = cmds.intSliderGrp('roundedBlockWithHolesLength', q=True, v=True)
    rgb = cmds.colorSliderGrp('roundedBlockWithHolesColour', q=True, rgbValue=True)
    
    # name
    nsTmp = "RoundedBlockWithHoles" + str(rnd.randint(1000,9999))
    
    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    # define cube's size 
    cubeSizeX = width * 0.8
    cubeSizeZ = length * 0.8
    cubeSizeY = height * 0.32
    
    # create a cube
    cube = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    
    # move it up 
    cmds.move((cubeSizeY/2.0), moveY=True)
    
    # create holes
    for i in range(width):
        for j in range(length):
            # create cylinder in the place of a hole
            hole = cmds.polyCylinder(r=0.25, h=height/2.0)
            
            # rotate and position it
            cmds.rotate(90, rotateX=True, a=True)
            cmds.rotate(90, rotateY=True, a=True)
            
            cmds.move((cubeSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
            
            # remove it from the base block
            cube = cmds.polyCBoolOp(cube, hole, op=2, caching=False, ch=False)    
    
    # add cylinders to round corners
    # right side 
    rCylind = cmds.polyCylinder(r=cubeSizeY*0.5, h=cubeSizeX)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)
    cmds.move((cubeSizeX/2.0 + 0.079), moveY=True, a=True)
    cmds.move((-cubeSizeZ * 0.5), moveZ=True, a=True) 
    # create a hole in it 
    rHole = cmds.polyCylinder(r=0.25, h=height/2.0)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)       
    cmds.move((cubeSizeY/2.0), moveY=True, a=True)
    cmds.move(((0 * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
    cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
    rCylind = cmds.polyCBoolOp(rCylind, rHole, op=2, caching=False, ch=False)
    
    # left side 
    lCylind = cmds.polyCylinder(r=cubeSizeY*0.5, h=cubeSizeX)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)
    cmds.move((cubeSizeX/2.0 + 0.079), moveY=True, a=True)
    cmds.move((cubeSizeZ * 0.5), moveZ=True, a=True)
    # create a hole in it 
    lHole = cmds.polyCylinder(r=0.25, h=height/2.0)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)       
    cmds.move((cubeSizeY/2.0), moveY=True, a=True)
    cmds.move(((width * 0.8) - cubeSizeX), moveX=True, a=True) 
    cmds.move(((length * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
    lCylind = cmds.polyCBoolOp(lCylind, lHole, op=2, caching=False, ch=False)
    
    # subtract a cylinder from left side of the cube
    lCubeHole = cmds.polyCylinder(r=0.25, h=height/2.0)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)       
    cmds.move((cubeSizeY/2.0), moveY=True, a=True)
    cmds.move(((width * 0.8) - cubeSizeX), moveX=True, a=True) 
    cmds.move(((length * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
    cube = cmds.polyCBoolOp(cube, lCubeHole, op=2, caching=False, ch=False)
    
    # add material        
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], type='double3')
    
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    
    cmds.hyperShade(assign=(nsTmp+":blckMat"))  
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)
    
#################################################################
#             Rounded Block With Holes and Angle                #
#################################################################
def roundedBlockWithHolesAngle():
    # set up block dimensions
    height = 3
    width = 1 #bump
    bendAngle = cmds.radioButtonGrp('roundedBlockWithHolesBendAngle', q=True, sl=True)
    if(bendAngle == 1):
        length = cmds.intSliderGrp('roundedBlockWithHolesAngleLength', q=True, v=True)
        bendLength = cmds.intSliderGrp('roundedBlockWithHolesAngleBendLength', q=True, v=True)
    if(bendAngle == 2):
        length = 4
        bendLength = 3
    rgb = cmds.colorSliderGrp('roundedBlockWithHolesAngleColour', q=True, rgbValue=True)
    
    # name
    nsTmp = "RoundedBlockWithHolesAngle" + str(rnd.randint(1000,9999))
    
    cmds.select(clear=True)
    cmds.namespace(add=nsTmp)
    cmds.namespace(set=nsTmp)
    
    # define cubes size 
    cubeSizeX = width * 0.8
    cubeSizeZ = length * 0.8
    cubeSizeY = height * 0.32
    bendSizeZ = bendLength * 0.8
    
    # create a cube
    cube = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    
    # move it up 
    cmds.move((cubeSizeY/2.0), moveY=True) 
    
    # create holes
    for i in range(width):
        for j in range(length):
            # create cylinder in the place of a hole
            hole = cmds.polyCylinder(r=0.25, h=height/2.0)
    
            # rotate and position it
            cmds.rotate(90, rotateX=True, a=True)
            cmds.rotate(90, rotateY=True, a=True)
            
            cmds.move((cubeSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
            cmds.move(((j * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
            
            # remove it from the base block
            cube = cmds.polyCBoolOp(cube, hole, op=2, caching=False, ch=False)     
    
    # add cylinders to round corners
    # right side 
    rCylind = cmds.polyCylinder(r=cubeSizeY*0.5, h=cubeSizeX)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)
    cmds.move((cubeSizeX/2.0 + 0.079), moveY=True, a=True)
    cmds.move((-cubeSizeZ * 0.5), moveZ=True, a=True)
    # merge right cylinder with cube
    cube = cmds.polyCBoolOp(cube, rCylind, op=1, caching=False, ch=False)
    # add a hole
    rHole = cmds.polyCylinder(r=0.25, h=height/2.0)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)       
    cmds.move((cubeSizeY/2.0), moveY=True, a=True)
    cmds.move(((0 * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
    cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
    cube = cmds.polyCBoolOp(cube, rHole, op=2, caching=False, ch=False)
    
    # left side 
    lCylind = cmds.polyCylinder(r=cubeSizeY*0.5, h=cubeSizeX)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)
    cmds.move((cubeSizeX/2.0 + 0.079), moveY=True, a=True)
    cmds.move((cubeSizeZ * 0.5), moveZ=True, a=True)
    # merge left cylinder with cube
    cube = cmds.polyCBoolOp(cube, lCylind, op=1, caching=False, ch=False)
    # create a hole 
    lHole = cmds.polyCylinder(r=0.25, h=height/2.0)
    cmds.rotate(90, rotateX=True, a=True)
    cmds.rotate(90, rotateY=True, a=True)       
    cmds.move((cubeSizeY/2.0), moveY=True, a=True)
    cmds.move(((width * 0.8) - cubeSizeX), moveX=True, a=True) 
    cmds.move(((length * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
    cube = cmds.polyCBoolOp(cube, lHole, op=2, caching=False, ch=False)
    
    # create a second cube for bend 
    if(bendAngle == 1): # at 90 degrees
        cubeBend = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=bendSizeZ)
        cmds.rotate(90, rotateX=True, a=True)
        
        # move it up 
        cmds.move((bendSizeZ/2.0), moveY=True)
        
        # add cylinder to its end
        endCylind = cmds.polyCylinder(r=cubeSizeY*0.5, h=cubeSizeX)
        cmds.rotate(90, rotateX=True, a=True)
        cmds.rotate(90, rotateY=True, a=True)
        cmds.move((bendSizeZ), moveY=True, a=True)    
         
        # merge cube with cylinder 
        cubeBend = cmds.polyCBoolOp(cubeBend, endCylind, op=1, caching=False, ch=False)
        
        # move bended cube to cube's end
        cmds.move((-cubeSizeZ/2), moveZ=True, a=True)
        
        # move it up a bit
        cmds.move(0.5, moveY=True)
        
        # add holes to bended part
        # create holes
        for i in range(width):
            for j in range(bendLength):
                # create cylinder in the place of a hole
                bHole = cmds.polyCylinder(r=0.25, h=height/2.0)        
                # rotate and position it
                cmds.rotate(90, rotateX=True, a=True)
                cmds.rotate(90, rotateY=True, a=True)
                cmds.move((cubeSizeY/2.0), moveY=True, a=True)
                cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
                cmds.move(((0 * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
                cmds.move(((j * 0.8) + (cubeSizeY/2.0)), moveY=True, a=True)
                # remove it from the base block
                cubeBend = cmds.polyCBoolOp(cubeBend, bHole, op=2, caching=False, ch=False)     
        
        # create the last hole
        endHole = cmds.polyCylinder(r=0.25, h=height/2.0)
        # rotate and position it
        cmds.rotate(90, rotateX=True, a=True)
        cmds.rotate(90, rotateY=True, a=True)
        cmds.move((cubeSizeY/2.0), moveY=True, a=True)
        cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
        cmds.move((((bendLength) * 0.8) + (cubeSizeY/2.0)), moveY=True, a=True)
        # remove it from end cylinder
        cubeBend = cmds.polyCBoolOp(cubeBend, endHole, op=2, caching=False, ch=False) 
        
    if(bendAngle == 2):    # bend at 60 degrees
        # create a cube for bend
        cubeBend = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=bendSizeZ)
        # move & rotate
        cmds.move((cubeSizeY), moveY=True)
        cmds.rotate(60, rotateX=True, a=True)
        cmds.move(( 0 -(cubeSizeZ/2.0) + 1.04), moveZ=True, a=True)   
            
        # add cylinder to its end
        endCylind = cmds.polyCylinder(r=cubeSizeY*0.5+0.01, h=cubeSizeX)
        cmds.rotate(90, rotateX=True, a=True)
        cmds.rotate(90, rotateY=True, a=True)
        cmds.move((bendSizeZ - 0.4), moveY=True, a=True) 
        cmds.move((-bendSizeZ/2 + 0.04), moveZ=True, a=True)    
         
        # merge cube with cylinder 
        cubeBend = cmds.polyCBoolOp(cubeBend, endCylind, op=1, caching=False, ch=False)
        
        # move bended cube to cube's end
        cmds.move((-cubeSizeZ/2), moveZ=True, a=True)
        
        # move it up a bit
        cmds.move(0.5, moveY=True)
        
        # add holes to bended part
        # create holes
        for i in range(width):
            for j in range(bendLength):
                # create cylinder in the place of a hole
                bHole = cmds.polyCylinder(r=0.25, h=height/2.0)        
                # rotate and position it
                cmds.rotate(90, rotateX=True, a=True)
                cmds.rotate(90, rotateY=True, a=True)
                cmds.move((cubeSizeY/2.0), moveY=True, a=True)
                cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
                cmds.move(((0 * 0.8) - (cubeSizeX/2.0) + 0.4), moveX=True, a=True) 
                cmds.move(((j * 0.8) + (cubeSizeY/2.0)), moveY=True, a=True)
                # remove it from the base block
                cubeBend = cmds.polyCBoolOp(cubeBend, bHole, op=2, caching=False, ch=False)     
        
        # create the last hole
        endHole = cmds.polyCylinder(r=0.25, h=height/2.0)
        # rotate and position it
        cmds.rotate(90, rotateX=True, a=True)
        cmds.rotate(90, rotateY=True, a=True)
        cmds.move((cubeSizeY/2.0), moveY=True, a=True)
        cmds.move(((0 * 0.8) - (cubeSizeZ/2.0)), moveZ=True, a=True)
        cmds.move((((bendLength) * 0.8) + (cubeSizeY/2.0)), moveY=True, a=True)
        # remove it from end cylinder
        cubeBend = cmds.polyCBoolOp(cubeBend, endHole, op=2, caching=False, ch=False)    
       
    # add material       
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")
    cmds.setAttr(nsTmp+":blckMat.color",rgb[0],rgb[1],rgb[2], type='double3')
    
    cmds.polyUnite((nsTmp+":*"), n=nsTmp, ch=False)
    cmds.delete(ch=True)
    
    cmds.hyperShade(assign=(nsTmp+":blckMat"))  
    cmds.namespace(removeNamespace=":"+nsTmp,mergeNamespaceWithParent=True)