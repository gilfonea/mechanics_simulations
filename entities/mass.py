from vpython import *


class Mass(box):
    
    def __init__(self, tilt_angle, **boxargs):  # Constructor
        """
        this method constracts a mass body

        Args:
            tilt_angle              : angle of the mass tilt relative to positive x axis (sometimes used as ramp angle)

        Returns:
            none                    : a mass is located in the designated coordinates

        Raises:
            ValueError: none
        """        
        super().__init__(**boxargs)  # Initialize Parent
        self.tilt_angle = tilt_angle
        
        #box.axis is a vector that modifies box.size vector. its direction is set from origin and only 
        #states the portions between x,y,z coordinates to give a pointing direction
        direction = norm(vector(cos(radians(self.tilt_angle)), sin(radians(self.tilt_angle)), 0))
        self.axis = direction * self.size.x


