import pybullet as p

def dropMarker(position):
    '''
    Drop a marker in the world
    '''

    visual = p.createVisualShape(
        p.GEOM_BOX, 
        halfExtents = [0.02, 0.02, 0.005],
        #Have the marker be bright red so that it's easily visible
        rgbaColor = [1, 0, 0, 1]
    )

    collision = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents = [0.02, 0.02, 0.005]
    )

    p.createMultiBody(
        baseMass = 0.001,
        baseVisualShapeIndex = visual, 
        baseCollisionShapeIndex = collision,
        basePosition = position
    )

    print(f"Dropped marker at {position}")