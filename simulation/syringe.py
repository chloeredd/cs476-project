import pybullet as p

class Syringe:
    def __init__(self, position):
        """
        Creates a yellow cylinder to represent a syringe.
        Returns the created body id as self.body
        """
        # visual
        visual = p.createVisualShape(
            p.GEOM_CYLINDER,
            radius=0.004,
            length=0.1,
            rgbaColor=[1, 1, 0, 1]
        )
        # collision
        collision = p.createCollisionShape(
            p.GEOM_CYLINDER,
            radius=0.004,
            height=0.1
        )
        self.body = p.createMultiBody(
            baseMass=0.01,
            baseCollisionShapeIndex=collision,
            baseVisualShapeIndex=visual,
            basePosition=position
        )

    def getPosition(self):
        pos, _ = p.getBasePositionAndOrientation(self.body)
        return pos
