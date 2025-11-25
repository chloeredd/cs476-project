import pybullet as p

def drop_marker(x, y, z):
    """
    Drops a simple red sphere marker at (x, y, z) in the simulation.
    """
    radius = 0.02
    visual = p.createVisualShape(p.GEOM_SPHERE, radius=radius, rgbaColor=[1, 0, 0, 1])
    body = p.createMultiBody(baseMass=0, baseVisualShapeIndex=visual, basePosition=[x, y, z])
    return body
