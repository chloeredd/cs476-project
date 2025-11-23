import pybullet as p
import pybullet_data
import time

#connect to physics server
p.connect(p.GUI)



#insert models and other things here TODO


#running simulation
p.setGravity(0,0,-9.8)
while(True):
    p.stepSimulation()
    #time sleep

#disconnect may not be needed
p.disconnect()