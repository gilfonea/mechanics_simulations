from vpython import *

class Ramp:


    def __init__(self, LeftAngle, RightAngle, DoubleRamp, RampColor):  # Constructor
        self.LeftAngle = LeftAngle
        self.RightAngle = -RightAngle  #right slope angle is negative (below x-axis), but we need it possitive for calculations
        self.DoubleRamp = DoubleRamp
        self.RampColor = RampColor

        #constants
        self.RAMP_HEIGHT = 4
        self.RADIUS = 1


        self.Xleft = self.RAMP_HEIGHT/tan(radians(self.RightAngle))    #opposite to axises - dont know why
        self.Xright = self.RAMP_HEIGHT/tan(radians(self.LeftAngle))    #opposite to axises - dont know why 

        if self.DoubleRamp == True:
            self.triangleshape = [ [self.Xright,0], [0,self.RAMP_HEIGHT], [-self.Xleft,0], [self.Xright,0]]
        else:
            self.triangleshape = [ [self.Xright,0], [0,self.RAMP_HEIGHT], [0,0], [self.Xright,0]]

        outer_circle = shapes.circle(radius=self.RADIUS, pos=[0,self.RAMP_HEIGHT],thickness=0.2)


        linepath = [ vec(0,0,-4), vec(0,0,4) ]
        ramp = extrusion(shape=self.triangleshape, path=linepath, color=self.RampColor,opacity=1)


 
    def right_slope_position(self, Xslope, Yslope, height_above_slope):
        """
        this method transforms right ramp coordinates to the real original x-y coordinates
        position 0,0 is the top of the slope

        Args:
            Xslope                  (float): The x coordinates on ramp x axis.
            Yslope                  (float): The y coordinates on ramp y axis (currently unavilable)
            height_above_slope      (float): height above the ramp: 0 < height_above_slope < ...

        Returns:
            vector: (x,y,z) global axes coordinates

        Raises:
            ValueError: If the user ID is not found.
        """
            

        # TODO: here add Xslope, Yslope protection against position longer that slope 

        # TODO: add support to calculate x,y in case Yslope is not zero


        #Xslope_origin = 0 + self.RADIUS * sin(radians(self.RightAngle))
        #Yslope_origin = self.RAMP_HEIGHT + self.RADIUS * cos(radians(self.RightAngle))
        Xslope_origin = 0 + height_above_slope * sin(radians(self.RightAngle))
        Yslope_origin = self.RAMP_HEIGHT + height_above_slope * cos(radians(self.RightAngle))



        return(vector(Xslope_origin+(Xslope*cos(radians(self.RightAngle))),Yslope_origin-(Xslope*sin(radians(self.RightAngle))),0))



    def left_slope_position(self, Xslope, Yslope, height_above_slope):
        """
        this method transforms left ramp coordinates to the real original x-y coordinates
        position 0,0 is the top of the slope

        Args:
            Xslope                  (float): The x coordinates on ramp x axis.
            Yslope                  (float): The y coordinates on ramp y axis (currently unavilable)
            height_above_slope      (float): height above the ramp: 0 < height_above_slope < ...

        Returns:
            vector: (x,y,z) global axes coordinates

        Raises:
            ValueError: If the user ID is not found.
        """
            

        # TODO: here add Xslope, Yslope protection against position longer that slope 

        # TODO: add support to calculate x,y in case Yslope is not zero
        

        Xslope_origin = 0 - (height_above_slope * sin(radians(self.LeftAngle)))
        Yslope_origin = self.RAMP_HEIGHT + height_above_slope * cos(radians(self.LeftAngle))

        return(vec(Xslope_origin-(Xslope*cos(radians(self.LeftAngle))),Yslope_origin-(Xslope*sin(radians(self.LeftAngle))),0))



    def get_ramp_base_vertices(self):
        """
        this method returns the x coordinates of the base of the ramp on the x-axis as related to origin 
        (the base sits on the x-axis)

        Args:
            none

        Returns:
            Xleft, Xright

        Raises:
            ValueError: If the user ID is not found.
        """        
        return self.Xleft, self.Xright


    def get_ramp_top_vertex(self):
        """
        this method returns the x,y coordinates of the vertex of the top of the ramp

        Args:
            none

        Returns:
            x,y,z vector

        Raises:
            ValueError: If the user ID is not found.
        """        
        return vector(0, self.RAMP_HEIGHT,  0)