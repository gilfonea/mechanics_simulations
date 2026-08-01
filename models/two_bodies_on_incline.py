#two_bodies_on_incline.py


from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley

#simulation parameters
LEFT_SLOPE = 20
RIGHT_SLOPE = 60


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
        myRamp = Ramp(LeftAngle=LEFT_SLOPE, 
                  RightAngle=RIGHT_SLOPE, 
                  DoubleRamp=True, 
                  RampColor=color.blue)

        points(pos=myRamp.right_slope_position(0,0), radius=5, color=color.red)


        #create masses
        m1 = Mass(name="m1",
                   tilted_degrees=-RIGHT_SLOPE,    #negative cause its a negative slope in relate to +x axis
                   tilt_axis=vector(0, 0, 1),    #tilt around z axis
                   length=2,
                   height=1,
                   width=1,
                   color = color.white,
                   )

        m1.mass_position(bottom_center = myRamp.right_slope_position(0.1,0))

        
        points(pos=myRamp.right_slope_position(0.1,0), radius=5, color=color.red)
        points(pos=m1.pos, radius=5, color=color.green)

       
        #create masses
        m2 = Mass( name="m2",
                    tilted_degrees=LEFT_SLOPE,
                    tilt_axis=vector(0, 0, 1),    #tilt around z axis
                    length=2,
                    height=1,
                    width=1,
                    color = color.white,
                    )

               
        m2.mass_position(bottom_center = myRamp.left_slope_position(0.1,0))

        #create pulley
        Mypulley = Pulley(base_position=myRamp.left_slope_position(0,0)) 






        # main simulation:
        xleft, xright = myRamp.get_ramp_base_vertices()  #run until end of slope


        dx_left=0 
        dx_right=0 

        while True:
            #if m1 got to the end of the slope
            if myRamp.right_slope_position(dx_right,0).x < xright and myRamp.right_slope_position(dx_right,0).y > 0:
                dx_right += 0.1
                m1.mass_position(myRamp.right_slope_position(dx_right,0))


            #if m2 got to the end of the slope
            if myRamp.left_slope_position(dx_left,0).x < xleft and myRamp.left_slope_position(dx_left,0).y > 0:
                dx_left += 0.1
                m2.mass_position(myRamp.left_slope_position(dx_left,0))



            sleep(0.1)                 
        
