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
        
        #direction = norm(vector(cos(radians(self.tilt_angle)), sin(radians(self.tilt_angle)), 0))
        #self.axis = direction * self.size.x
        # Generate the box
        my_box = create_tilted_box(
                    bottom_center=my_bottom_position,
                    tilt_degrees=my_tilt_angle,
                    tilt_axis=my_tilt_axis,
                    length=4,
                    height=2,
                    width=2,
                    box_color=color.cyan
)


    def create_tilted_box(bottom_center, tilt_degrees, tilt_axis, length, height, width, box_color=color.white):
        """
        Creates a box where the given position is the center of its bottom face.

        :param bottom_center: vector() representing the center of the bottom face
        :param tilt_degrees: Angle in degrees to tilt the box
        :param tilt_axis: vector() representing the axis to rotate around
        :param length: Box length (x-dimension before rotation)
        :param height: Box height (y-dimension before rotation)
        :param width: Box width (z-dimension before rotation)
        """
        # 1. Convert the tilt angle from degrees to radians
        tilt_rad = radians(tilt_degrees)

        # 2. Define the default orientation vectors (before any tilt)
        default_axis = vector(1, 0, 0) # Defines the length direction
        default_up = vector(0, 1, 0)   # Defines the height direction

        # 3. Rotate the orientation vectors by the given angle and axis
        new_axis = default_axis.rotate(angle=tilt_rad, axis=tilt_axis)
        new_up = default_up.rotate(angle=tilt_rad, axis=tilt_axis)

        # 4. Calculate the true center of the box
        # Since we want the bottom face at 'bottom_center', the true center 
        # is exactly half the height 'up' from the bottom center.
        true_box_center = bottom_center + (new_up * (height / 2))

        # 5. Create and return the box
        return box(pos=true_box_center, 
                   axis=new_axis, 
                   up=new_up, 
                   length=length, 
                   height=height, 
                   width=width, 
                   color=box_color)
