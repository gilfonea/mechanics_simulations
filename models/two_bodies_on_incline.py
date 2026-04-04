#two_bodies_on_incline.py


from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley


class Two_bodies_on_incline():


    def __init__(self):  # Constructor
        """
        this method constracts a simulation of Two_bodies_on_incline

        Args:
            base_position           : vector for locating the bottom of the base of the pulley

        Returns:
            none                    

        Raises:
            ValueError: none
        """     


    def start():

        #create scene
        scene.title = "2 Masses move on Double Ramp"
        scene.background = color.black
        scene.width = 800
        scene.height = 600 

        #create ramp
        myRamp = Ramp(LeftAngle=20, 
                  RightAngle=-60, 
                  DoubleRamp=True, 
                  RampColor=color.blue)

        #create masses
        m1 = Mass(tilt_angle=-60, 
                  pos=myRamp.right_slope_position(0.5,0,0.25),                   
                  opacity=1, 
                  length=1, 
                  height=2, 
                  widht=2)


        m2 = Mass(tilt_angle=200, 
                  pos=myRamp.left_slope_position(0.5,0,0.25),                   
                  opacity=1, 
                  length=1, 
                  height=2, 
                  widht=2)
    

        #create pulley
        Mypulley = Pulley(base_position=myRamp.get_ramp_top_vertex())                  

