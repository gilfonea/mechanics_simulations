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
                  RightAngle=60, 
                  DoubleRamp=True, 
                  RampColor=color.blue)

        #create masses
        #m1 = Mass(tilt_angle=-60, 
        #          pos=myRamp.right_slope_position(5,0),                   
        #          opacity=1, 
        #          length=1, 
        #          height=1, 
        #          widht=2)


        #m2 = Mass(tilt_angle=200, 
        #          pos=myRamp.left_slope_position(5,0),                   
        #          opacity=1, 
        #          length=2,  #was 1
        #          height=1, 
        #          widht=2)
    
        point1 = sphere(pos=myRamp.right_slope_position(1,0), radius=0.1, color=color.red, make_trail=True, retain=50)
        point2 = sphere(pos=myRamp.left_slope_position(1,0), radius=0.1, color=color.yellow, make_trail=True, retain=50)

        #create pulley
        Mypulley = Pulley(base_position=myRamp.left_slope_position(0,0)) 

        # main simulation:
        xleft, xright = myRamp.get_ramp_base_vertices()  #run until end of slope



        dt=0       
        while dt < 10 :
            #if m1 got to the end of the slope
            if point1.pos.x < xleft:
                point1.pos =  myRamp.right_slope_position(0.5+dt,0)

            #if m2 got to the end of the slope
            if point2.pos.x < xright:
                point2.pos =  myRamp.left_slope_position(0.5+dt,0)

            dt += 0.1
            sleep(0.1)                 
        
