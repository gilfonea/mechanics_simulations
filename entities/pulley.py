from vpython import *


class Pulley:

    def __init__(self, base_position):  # Constructor
        """
        this method constracts a pulley wheel with base of two rods attached to its pivot.

        Args:
            base_position           : vector for locating the bottom of the base of the pulley

        Returns:
            none                    

        Raises:
            ValueError: none
        """ 


        fork_length = 1.0     # Length extending along y-axis from the hub
        self.base_position = base_position

        # Compute center of wheel based on fork height
        self.center_position = vector(base_position.x, base_position.y + fork_length, base_position.z)

        # --- Wheel Parameters ---
        rim_radius = 0.5
        rim_thickness = 0.1
        hub_radius = 0.2
        hub_length = 0.4
        num_spokes = 20
        spoke_thickness = 0.02

        # --- Create Rim ---
        rim = ring(pos=self.center_position,
                   axis=vector(0, 0, 1),
                   radius=rim_radius,
                   thickness=rim_thickness,
                   color=color.orange)

        # --- Create Hub ---
        hub = cylinder(pos=vector(self.center_position.x, self.center_position.y, -hub_length/2),
                       axis=vector(0, 0, hub_length),
                       radius=hub_radius,
                       color=color.gray(0.6))

        # --- Create Spokes ---
        spokes = []
        for i in range(num_spokes):
            angle = i * (2 * pi / num_spokes)
            hub_pos = vector(hub_radius * cos(angle), hub_radius * sin(angle), 0)
            rim_vector = vector((rim_radius - hub_radius) * cos(angle), (rim_radius - hub_radius) * sin(angle), 0)
            spoke = cylinder(
                pos=self.center_position + hub_pos,
                axis=rim_vector,
                radius=spoke_thickness,
                color=color.gray(0.4)
            )
            spokes.append(spoke)

        # --- Create Fork ---
        fork_thickness = 0.05
        fork_offset = hub_radius + 0.05

        self.fork_left = box(
            pos=vector(self.center_position.x, self.center_position.y - (fork_length / 2), -(hub_length / 2)),
            axis=vector(0, 1, 0),
            length=fork_length,
            height=0.15,
            width=0.15,
            color=color.white
        )

        self.fork_right = box(
            pos=vector(self.center_position.x, self.center_position.y - (fork_length / 2), (hub_length / 2)),
            axis=vector(0, 1, 0),
            length=fork_length,
            height=0.15,
            width=0.15,
            color=color.white
        )

        # Save fork as an attribute for later rotation
        self.fork = compound([self.fork_left, self.fork_right])

        # --- Create Complete Wheel Assembly (including fork, but separately stored) ---
        self.wheel = compound([rim, hub] + spokes + [self.fork])
        
    def pulley_top_of_wheel_coordinates(self):  # Constructor
        """
        this method calculates what is the coordinate of the 
        top of the wheel for the purpose of connecting strings to the pulley

        Args:
            none         : vector for locating the bottom of the base of the pulley

        Returns:
            none                    

        Raises:
            ValueError: none
        """
        return(vector(0,self.center_position.y,0)) 

'''     
# Animation loop
dt = 0.01
while True:
    rate(100)
    wheel.rotate(angle=omega * dt, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
'''
        