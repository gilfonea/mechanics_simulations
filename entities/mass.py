from vpython import *

class Mass(box):
    def __init__(self, name, bottom_center, tilt_degrees, tilt_axis, length, height, width, **boxargs):
        """
        Creates a Mass body (inherits from box) where the given position 
        is the center of its bottom face.
        """
        self.name = name

        # 1. Convert the tilt angle from degrees to radians
        tilt_rad = radians(tilt_degrees)

        # 2. Define the default orientation vectors
        default_axis = vector(1, 0, 0) # Defines the length direction
        default_up = vector(0, 1, 0)   # Defines the height direction

        # 3. Rotate the orientation vectors by the given angle and axis
        new_axis = default_axis.rotate(angle=tilt_rad, axis=tilt_axis)
        new_up = default_up.rotate(angle=tilt_rad, axis=tilt_axis)

        print(self.name, "new_axis:", new_axis)
        print(self.name, "new_up:", new_up)


        # 4. Calculate the true center of the box
        true_box_center = bottom_center #+ (new_up * (height / 2))

        # 5. Initialize the Parent (box) with the calculated values
        # We pass **boxargs at the end so it catches things like color=color.red
        super().__init__(
            pos=true_box_center, 
            axis=new_axis, 
            up=new_up, 
            length=length, 
            height=height, 
            width=width, 
            **boxargs 
        )