from vpython import *

class Mass(box):
    def __init__(self, name, tilted_degrees, **kwargs):

        self.name = name
        # 5. Initialize the parent VPython box with the calculated values
        super().__init__(
            **kwargs 
        )

        self.tilted_degrees = tilted_degrees

    def mass_position(self, bottom_center):

        """
        position a box where the 'bottom_center' is exactly on the specified 
        coordinate, tilted around the Z-axis by 'tilt_degrees'.
        """
        # 1. Convert the tilt angle from degrees to radians
        tilt_rad = radians(self.tilted_degrees)
        z_axis = vector(0, 0, 1)

        # 2. Default orientation vectors for a flat box
        default_axis = vector(1, 0, 0) # Points right
        default_up = vector(0, 1, 0)   # Points up

        # 3. Rotate the orientation vectors by the given angle around the Z-axis
        new_axis = default_axis.rotate(angle=tilt_rad, axis=z_axis)
        new_up = default_up.rotate(angle=tilt_rad, axis=z_axis)

        # 4. Calculate the true center of the box
        # The geometric center is half the height away from the bottom, 
        # in the direction of the new tilted "up" vector.
        offset = (self.height/2) * hat(new_up)
        true_center = bottom_center + offset

        self.pos = true_center
        self.axis = new_axis
        self.up = new_up
