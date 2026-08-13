from vpython import *

#parameters
RIM_THICKNESS = 0.08
RIM_RADIUS = 0.3

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
        rim_radius = RIM_RADIUS
        rim_thickness = RIM_THICKNESS
        hub_radius = 0.1
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
        # --- Create Complete Wheel Assembly ---
        self.wheel = compound([rim, hub] + spokes + [self.fork], origin=self.center_position)


    def get_top_wheel_position(self):
        """
        מחזירה וקטור של המיקום של הנקודה העליונה ביותר של קצה גלגל הגלגלת.
        """
        # המשתנים מהבנאי (אפשר גם להפוך אותם למשתני מחלקה self.rim_radius וכו')
        rim_radius = RIM_RADIUS
        rim_thickness = RIM_THICKNESS
        
        # הרדיוס החיצוני המוחלט של הגלגל הוא רדיוס הטבעת ועוד חצי מהעובי שלה
        outer_radius = rim_radius + (rim_thickness / 2)
        
        # self.wheel.pos יושב עכשיו בדיוק במרכז הגלגל (בזכות ה-origin שהוספנו)
        # hat(self.wheel.up) מחזיר וקטור יחידה המצביע כלפי מעלה ביחס לזווית הנוכחית של הגלגלת
        top_pos = self.wheel.pos + outer_radius * hat(self.wheel.up)
        
        return top_pos
        