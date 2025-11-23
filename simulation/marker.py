import pybullet as p

class Needle:
    '''
    This class represents a needle-like object in the simulation world
    '''

    def __init__(self, position):

        #Visual shape: yellow cylinder
        visual = p.createVisualShape(
            #It's a cylinder
            p.GEOM_CYLINDER,
            radius = 0.004,
            length = 0.1,
            #It has a yellow color
            rgbaColor = [1, 1, 0, 1]
        )
        
        #Collision shape is the same as the visual shape
        collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius = 0.004,
            height = 0.1
        )

        #Create the object in simulation
        self.body = p.createMultiBody(
            baseMass = 0.01,
            baseCollisionShapeIndex = collision,
            baseVisualShapeIndex = visual,
            basePosition = position
        )

