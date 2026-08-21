from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley
from utils.physics import *
from constants import g

# simulation parameters
LEFT_SLOPE = 30
RIGHT_SLOPE = 20
PULLEY_POSITION = 0.5
M1_STARTING_POSITION = 1     # must be greater than PULLEY_POSITION
M2_STARTING_POSITION = 4     # must be greater than PULLEY_POSITION
M1_MASS = 2 #kg
M2_MASS = 1 #kg
SLOPES = 2

dt = 0.01

class Two_bodies_on_incline():

    def __init__(self):
        # 1. מצב המערכת ומשתני זמן
        self.state = "SETUP"  # מצבים אפשריים: "SETUP", "RUNNING", "FINISHED"
        self.t = 0
        self.has_rope = True
        
        # משתנים שנשלטים על ידי הממשק
        self.m1_mass_val = M1_MASS
        self.m2_mass_val = M2_MASS

        # 2. בניית הסביבה הוויזואלית והממשק (מתבצע פעם אחת)
        self.build_scene()
        self.build_ui()
        
        # 3. איפוס והחלת פרמטרים התחלתיים
        self.reset_sim()

    def build_scene(self):
        # יצירת הבמה
        scene.title = "2 Masses move on Double Ramp"
        scene.background = color.black
        scene.width = 800
        scene.height = 600 

        # מסילה
        self.myRamp = Ramp(LeftAngle=LEFT_SLOPE, RightAngle=RIGHT_SLOPE, num_slopes=SLOPES, RampColor=color.blue)
        self.xleft, self.xright = self.myRamp.get_ramp_base_vertices()

        # מסה 1
        self.m1 = Mass(name="m1", mass=self.m1_mass_val, tilted_degrees=-RIGHT_SLOPE, tilt_axis=vector(0, 0, 1), 
                       length=2, height=1, width=self.m1_mass_val, color=color.white)
        self.label_m1 = label(text='m1', box=False, opacity=0, line=False, height=14, yoffset=15)
        
        # אתחול משתנים למסה 2 וחוט כדי למנוע שגיאות Reference
        self.m2 = None
        self.label_m2 = None
        self.Mypulley = None
        self.rope = None
        self.top_pulley_pos = None

        if SLOPES > 1:
            # מסה 2
            self.m2 = Mass(name="m2", mass=self.m2_mass_val, tilted_degrees=LEFT_SLOPE, tilt_axis=vector(0, 0, 1), 
                           length=2, height=1, width=self.m2_mass_val, color=color.white)
            self.label_m2 = label(text='m2', box=False, opacity=0, line=False, height=14, yoffset=15)
            
            # גלגלת וחוט
            self.Mypulley = Pulley(base_position=self.myRamp.left_slope_position(vector(0,0,0))) 
            self.top_pulley_pos = self.Mypulley.get_top_wheel_position()
            self.rope = curve(color=color.white, radius=0.02)
            
        # תוויות קבועות במסך (זוויות ותאוצה)
        label(pos=vector(-self.xleft, 0, 0), text=f'{LEFT_SLOPE}°', xoffset=30, yoffset=10, box=False, line=False, height=16, color=color.white)
        label(pos=vector(self.xright, 0, 0), text=f'{RIGHT_SLOPE}°', xoffset=-30, yoffset=10, box=False, line=False, height=16, color=color.white)
        
        self.accel_label = label(pos=vector(0, -7, 0), text='Acceleration: ', box=False, height=16)

    def build_ui(self):
        # כפתורי שליטה
        self.play_button = button(text="Play", bind=self.toggle_play)
        button(text="Reset", bind=self.reset_sim_from_ui)

        scene.append_to_caption('  ') 
        checkbox(bind=self.toggle_rope, text='Connect Rope', checked=True)

        # סליידרים למסות
        scene.append_to_caption('\n\nMass 1 (kg): ')
        self.m1_text = wtext(text=f'{self.m1_mass_val:.1f}')
        scene.append_to_caption('  ')
        slider(min=0.1, max=10, value=self.m1_mass_val, length=200, bind=self.set_m1_mass)

        if SLOPES > 1:
            scene.append_to_caption('\nMass 2 (kg): ')
            self.m2_text = wtext(text=f'{self.m2_mass_val:.1f}')
            scene.append_to_caption('  ')
            slider(min=0.1, max=10, value=self.m2_mass_val, length=200, bind=self.set_m2_mass)

    # --------------- אירועי ממשק (UI Callbacks) ----------------
    def toggle_play(self, b):
        if self.state == "RUNNING":
            self.state = "SETUP"
            b.text = "Play"
        elif self.state == "SETUP":
            self.state = "RUNNING"
            b.text = "Pause"
        elif self.state == "FINISHED":
            # אם הסימולציה הסתיימה ולוחצים פליי, מתבצע איפוס והתחלה מחדש
            self.reset_sim()
            self.state = "RUNNING"
            b.text = "Pause"

    def reset_sim_from_ui(self, b):
        self.reset_sim()

    def toggle_rope(self, c):
        self.has_rope = c.checked
        self.reset_sim()

    def set_m1_mass(self, s):
        self.m1_mass_val = s.value
        self.m1_text.text = f'{s.value:.1f}'
        self.reset_sim()

    def set_m2_mass(self, s):
        self.m2_mass_val = s.value
        self.m2_text.text = f'{s.value:.1f}'
        self.reset_sim()
    # ------------------------------------------------------------

    def reset_sim(self):
        """תואם לתיבה: reset בתרשים"""
        self.state = "SETUP"
        self.play_button.text = "Play"
        self.t = 0
        
        # החזרת מסה 1 לנקודת ההתחלה
        self.m1.x0 = M1_STARTING_POSITION
        self.m1.v0 = 0
        self.m1_wanted_pos = vector(self.m1.x0, 0, 0)
        
        # החזרת מסה 2 לנקודת ההתחלה
        if SLOPES > 1 and self.m2 is not None:
            self.m2.x0 = M2_STARTING_POSITION
            self.m2.v0 = 0
            self.m2_wanted_pos = vector(self.m2.x0, 0, 0)
            
        self.set_simulation_parameters()

    def set_simulation_parameters(self):
        """תואם לתיבה: set simulation parameters בתרשים"""
        
        # 1. עדכון המסות והנראות (רוחב) מהסליידרים
        self.m1.mass = self.m1_mass_val
        self.m1.width = self.m1_mass_val
        if self.m2 is not None:
            self.m2.mass = self.m2_mass_val
            self.m2.width = self.m2_mass_val

        # 2. חישוב תאוצות חדשות
        if self.m2 is not None:
            a1, a2 = calculate_accelerations(
                m1=self.m1.mass, theta1_deg=RIGHT_SLOPE, 
                m2=self.m2.mass, theta2_deg=LEFT_SLOPE, has_rope=self.has_rope
            )
            self.m1.acceleration = a1
            self.m2.acceleration = a2
        else:
            a1, _ = calculate_accelerations(
                m1=self.m1.mass, theta1_deg=RIGHT_SLOPE, 
                m2=0, theta2_deg=0, has_rope=False
            )
            self.m1.acceleration = a1

        # 3. אתחול הפוזיציה הגרפית מחדש
        self.m1.bottom_position = self.myRamp.right_slope_position(self.m1_wanted_pos)
        self.m1.mass_position()
        self.label_m1.pos = self.m1.get_top_center()

        if self.m2 is not None:
            self.m2.bottom_position = self.myRamp.left_slope_position(self.m2_wanted_pos)
            self.m2.mass_position()
            self.label_m2.pos = self.m2.get_top_center()
            
        # 4. ציור החוט מחדש בהתאם למצב
        if self.has_rope and self.rope is not None and self.m2 is not None:
            self.rope.visible = True
            self.rope.clear()
            self.rope.append([self.m1.get_top_center(), self.top_pulley_pos, self.m2.get_top_center()])
        elif self.rope is not None:
            self.rope.visible = False

        self.update_labels()

    def run_sim(self):
        """תואם לתיבה: run sim בתרשים"""
        # בדיקת גבולות תנועה
        m1_next_pos = self.myRamp.right_slope_position(self.m1_wanted_pos)
        m1_can_move = PULLEY_POSITION < m1_next_pos.x < self.xright and m1_next_pos.y > 0
        
        m2_can_move = False
        if self.m2 is not None:
            m2_next_pos = self.myRamp.left_slope_position(self.m2_wanted_pos)
            m2_can_move = -self.xleft < m2_next_pos.x < -PULLEY_POSITION and m2_next_pos.y > 0

        # תנועה מחוברת
        if self.has_rope and self.m2 is not None:
            if m1_can_move and m2_can_move:
                self.update_kinematics_m1()
                self.update_kinematics_m2()
                self.rope.modify(0, pos=self.m1.get_top_center())
                self.rope.modify(2, pos=self.m2.get_top_center())
            else:
                self.state = "FINISHED" # תואם לתיבה finish or reset
                
        # תנועה מנותקת
        else:
            moved_any = False
            if m1_can_move:
                self.update_kinematics_m1()
                moved_any = True
            if self.m2 is not None and m2_can_move:
                self.update_kinematics_m2()
                moved_any = True
                
            if not moved_any:
                self.state = "FINISHED" # תואם לתיבה finish or reset

        # קידום הזמן ועדכון תצוגה
        if self.state == "RUNNING":
            self.t += dt
            self.update_labels()
            
        if self.state == "FINISHED":
            self.play_button.text = "Play"

    def update_kinematics_m1(self):
        self.m1_wanted_pos.x = self.m1.x0 + (self.m1.v0 * self.t) + (0.5 * self.m1.acceleration * (self.t**2))
        self.m1.bottom_position = self.myRamp.right_slope_position(self.m1_wanted_pos)
        self.m1.mass_position()
        self.label_m1.pos = self.m1.get_top_center()

    def update_kinematics_m2(self):
        self.m2_wanted_pos.x = self.m2.x0 + (self.m2.v0 * self.t) + (0.5 * self.m2.acceleration * (self.t**2))
        self.m2.bottom_position = self.myRamp.left_slope_position(self.m2_wanted_pos)
        self.m2.mass_position()
        self.label_m2.pos = self.m2.get_top_center()

    def update_labels(self):
        if self.m2 is not None:
            self.accel_label.text = f'm1 Acceleration: {self.m1.acceleration:.2f} m/s²\nm2 Acceleration: {self.m2.acceleration:.2f} m/s²\nTime: {self.t:.2f} s'
        else:
            self.accel_label.text = f'm1 Acceleration: {self.m1.acceleration:.2f} m/s²\nTime: {self.t:.2f} s'

    def start(self):
        # הלולאה הראשית ששומרת על הסימולציה פועלת
        while True:
            rate(100)
            if self.state == "RUNNING":
                self.run_sim()

# הפעלת הסימולציה
if __name__ == "__main__":
    sim = Two_bodies_on_incline()
    sim.start()