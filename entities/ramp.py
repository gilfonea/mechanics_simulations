from vpython import *

class Ramp:


    def __init__(self, LeftAngle, RightAngle, DoubleRamp, RampColor):  # Constructor
        self.LeftAngle = LeftAngle
        self.RightAngle = RightAngle  #right slope angle is negative (below x-axis), but we need it possitive for calculations
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

        linepath = [ vec(0,0,-4), vec(0,0,4) ]
        ramp = extrusion(shape=self.triangleshape, path=linepath, color=self.RampColor,opacity=0.5)


 
    def right_slope_position(self, local_position):
        """
        this method transforms right ramp coordinates to the real original x-y coordinates
        position 0,0 is the top of the slope

        Args:
            local_position          (vector): The local x,y,z coordinates on the ramp. 
                                              x is along the slope, y is perpendicular to the slope.
            
        Returns:
            vector: (x,y,z) global axes coordinates

        Raises:
            ValueError: If the user ID is not found.
        """
            
        Xslope = local_position.x
        Yslope = local_position.y

        # TODO: here add Xslope, Yslope protection against position longer that slope 

        #Xslope_origin = 0 + self.RADIUS * sin(radians(self.RightAngle))
        #Yslope_origin = self.RAMP_HEIGHT + self.RADIUS * cos(radians(self.RightAngle))
        X = ((Yslope * sin(radians(self.RightAngle))) + (Xslope * cos(radians(self.RightAngle))))
        Y = (self.RAMP_HEIGHT - (Xslope * sin(radians(self.RightAngle)))) + (Yslope * cos(radians(self.RightAngle)))


        return vector(X, Y, 0)



    def left_slope_position(self, local_position):
        """
        this method transforms left ramp coordinates to the real original x-y coordinates
        position 0,0 is the top of the slope

        Args:
            local_position          (vector): The local x,y,z coordinates on the ramp. 
                                              x is along the slope, y is perpendicular to the slope.
            
        Returns:
            vector: (x,y,z) global axes coordinates

        Raises:
            ValueError: If the user ID is not found.
        """
            
        Xslope = local_position.x
        Yslope = local_position.y

        # TODO: here add Xslope, Yslope protection against position longer that slope 

        X = - ((Yslope * sin(radians(self.LeftAngle))) + (Xslope * cos(radians(self.LeftAngle))))
        Y = (self.RAMP_HEIGHT - (Xslope * sin(radians(self.LeftAngle)))) + (Yslope * cos(radians(self.LeftAngle)))

        return vector(X, Y, 0)



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