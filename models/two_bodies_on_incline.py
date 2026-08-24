from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley
from utils.physics import calculate_accelerations, calculate_tension
from constants import g
import asyncio

# simulation parameters
LEFT_SLOPE = 30
RIGHT_SLOPE = 40
PULLEY_POSITION = 0.5
M1_STARTING_POSITION = 2     # must be greater than PULLEY_POSITION
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
        scene.width = 700
        scene.height = 500 
        scene.align = 'left' # <--- תוספת: הצמדת ההדמיה לשמאל

        # --- תוספת: חלונות הגרפים ---
        # הקטנתי את הגובה ל-250 כדי ששניהם יכנסו יחד בצד ימין
        self.v_graph = graph(title='Velocity vs. Time', xtitle='t [s]', ytitle='v [m/s]', 
                             align='right', width=450, height=250)
        
        # עקומה למסה 1 - מהירות
        self.v_curve1 = gcurve(graph=self.v_graph, color=color.cyan, label='m1 Velocity')
        self.v_curve2 = None 

        # --- יצירת גרף המיקום ---
        self.x_graph = graph(title='Position vs. Time', xtitle='t [s]', ytitle='x [m]', 
                             align='right', width=450, height=250)
        
        # עקומה למסה 1 - מיקום
        self.x_curve1 = gcurve(graph=self.x_graph, color=color.cyan, label='m1 Position')
        self.x_curve2 = None
        # -------------------------

        # מסילה
        self.myRamp = Ramp(LeftAngle=LEFT_SLOPE, RightAngle=RIGHT_SLOPE, num_slopes=SLOPES, RampColor=color.blue)
        self.xleft, self.xright = self.myRamp.get_ramp_base_vertices()

        # מסה 1
        self.m1 = Mass(name="m1", mass=self.m1_mass_val, tilted_degrees=-RIGHT_SLOPE, tilt_axis=vector(0, 0, 1), 
                       length=2, height=1, width=self.m1_mass_val, color=color.cyan)
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
                           length=2, height=1, width=self.m2_mass_val, color=color.orange)
            self.label_m2 = label(text='m2', box=False, opacity=0, line=False, height=14, yoffset=15)
            
            # עקומה למסה 2 על גרף המהירות
            self.v_curve2 = gcurve(graph=self.v_graph, color=color.orange, label='m2 Velocity')
            # תוספת: עקומה למסה 2 על גרף המיקום
            self.x_curve2 = gcurve(graph=self.x_graph, color=color.orange, label='m2 Position')

            # גלגלת וחוט
            self.Mypulley = Pulley(base_position=self.myRamp.left_slope_position(vector(0,0,0))) 
            self.top_pulley_pos = self.Mypulley.get_top_wheel_position()
            self.rope = curve(color=color.white, radius=0.02)
            
        # תוויות קבועות במסך (זוויות ותאוצה)
        label(pos=vector(-self.xleft, 0, 0), text=f'{LEFT_SLOPE}°', xoffset=30, yoffset=10, box=False, line=False, height=16, color=color.white)
        label(pos=vector(self.xright, 0, 0), text=f'{RIGHT_SLOPE}°', xoffset=-30, yoffset=10, box=False, line=False, height=16, color=color.white)
        
        self.accel_label = label(pos=vector(0, -7, 0), text='Acceleration: ', box=False, height=16)

        self.tension_label = label(pos=vector(0, -13, 0), text='Tension (T): ', box=False, height=16, color=color.yellow)

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
        
        # --- תוספת: איפוס נתוני הגרף ---
        if hasattr(self, 'v_curve1'):
            self.v_curve1.data = []
        if hasattr(self, 'v_curve2') and self.v_curve2 is not None:
            self.v_curve2.data = []
            
        # איפוס נתוני גרף המיקום החדש
        if hasattr(self, 'x_curve1'):
            self.x_curve1.data = []
        if hasattr(self, 'x_curve2') and self.x_curve2 is not None:
            self.x_curve2.data = []
        # -------------------------------

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

# 2. חישוב תאוצות חדשות ומתיחות
        if self.m2 is not None:
            a1, a2 = calculate_accelerations(
                m1=self.m1.mass, theta1_deg=RIGHT_SLOPE, 
                m2=self.m2.mass, theta2_deg=LEFT_SLOPE, has_rope=self.has_rope
            )
            self.m1.acceleration = a1
            self.m2.acceleration = a2
            
            # קריאה לפונקציה החיצונית לחישוב המתיחות
            self.tension = calculate_tension(self.m1.mass, RIGHT_SLOPE, a1, self.has_rope)
            
        else:
            a1, _ = calculate_accelerations(
                m1=self.m1.mass, theta1_deg=RIGHT_SLOPE, 
                m2=0, theta2_deg=0, has_rope=False
            )
            self.m1.acceleration = a1
            self.tension = 0

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
        # בדיקת גבולות תנועה
        m1_next_pos = self.myRamp.right_slope_position(self.m1_wanted_pos)
        m1_can_move = PULLEY_POSITION < m1_next_pos.x < self.xright and m1_next_pos.y > 0
        
        m2_can_move = False
        if self.m2 is not None:
            m2_next_pos = self.myRamp.left_slope_position(self.m2_wanted_pos)
            m2_can_move = -self.xleft < m2_next_pos.x < -PULLEY_POSITION and m2_next_pos.y > 0

        # משתנים זמניים המייצגים את המהירות והתאוצה הרגעית
        # אם המסות בתנועה - הם יחושבו כרגיל. אם מסה תעצור - נאפס אותם.
        current_a1 = self.m1.acceleration
        current_v1 = self.m1.v0 + self.m1.acceleration * self.t
        current_a2 = self.m2.acceleration if self.m2 else 0
        current_v2 = self.m2.v0 + self.m2.acceleration * self.t if self.m2 else 0

        # תנועה מחוברת
        if self.has_rope and self.m2 is not None:
            if m1_can_move and m2_can_move:
                self.update_kinematics_m1()
                self.update_kinematics_m2()
                self.rope.modify(0, pos=self.m1.get_top_center())
                self.rope.modify(2, pos=self.m2.get_top_center())
            else:
                # אם אחת המסות הגיעה לקצה, כל המערכת המחוברת נעצרת
                self.state = "FINISHED" 
                current_a1 = current_a2 = 0
                current_v1 = current_v2 = 0
                
        # תנועה מנותקת
        else:
            moved_any = False
            if m1_can_move:
                self.update_kinematics_m1()
                moved_any = True
            else:
                # מסה 1 הגיעה לקצה ונעצרה
                current_a1 = 0
                current_v1 = 0
                
            if self.m2 is not None:
                if m2_can_move:
                    self.update_kinematics_m2()
                    moved_any = True
                else:
                    # מסה 2 הגיעה לקצה ונעצרה
                    current_a2 = 0
                    current_v2 = 0
                
            if not moved_any:
                self.state = "FINISHED" 

        # עדכון גרפים ותוויות
        if self.state == "RUNNING":
            # הגרף מקבל עכשיו את המהירות המעודכנת
            self.v_curve1.plot(self.t, current_v1)
            # תוספת: הגרף השני מקבל את המיקום הנוכחי
            self.x_curve1.plot(self.t, self.m1_wanted_pos.x)
            
            if self.m2 is not None and self.v_curve2 is not None:
                self.v_curve2.plot(self.t, current_v2)
                # תוספת: מיקום מסה 2
                self.x_curve2.plot(self.t, self.m2_wanted_pos.x)

            self.t += dt

            # התוויות מקבלות את התאוצה המעודכנת
            self.update_labels(current_a1, current_a2)


            
        if self.state == "FINISHED":
            self.play_button.text = "Play"
            # וידוא שבסיום הסימולציה התוויות מתאפסות ל-0
            self.update_labels(0, 0)

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

    def update_labels(self, current_a1=None, current_a2=None):
        # אם לא הועברו פרמטרים (למשל בזמן reset), נשתמש בתאוצה המקורית
        if current_a1 is None: current_a1 = self.m1.acceleration
        if current_a2 is None: current_a2 = self.m2.acceleration if self.m2 else 0

        # עדכון תווית התאוצה והזמן בהתאם לערכים העדכניים
        if self.m2 is not None:
            self.accel_label.text = f'm1 Acceleration: {current_a1:.2f} m/s²\nm2 Acceleration: {current_a2:.2f} m/s²\nTime: {self.t:.2f} s'
        else:
            self.accel_label.text = f'm1 Acceleration: {current_a1:.2f} m/s²\nTime: {self.t:.2f} s'
            
        # עדכון תווית המתיחות בחוט
        if self.has_rope and self.m2 is not None:
            self.tension_label.text = f'Tension (T): {abs(self.tension):.2f} N'
            self.tension_label.visible = True
        else:
            self.tension_label.visible = False

    def start(self):
        # הלולאה הראשית ששומרת על הסימולציה פועלת
        while True:
            rate(100)
            if self.state == "RUNNING":
                self.run_sim()

    async def start_web(self):
        """לולאת אנימציה אסינכרונית המותאמת להרצה ב-Voilà"""
        while True:
            rate(100)
            if self.state == "RUNNING":
                self.run_sim()
            
            # פקודה זו אומרת לפייתון לשחרר שבריר שנייה לדפדפן כדי לרנדר את המסך
            await asyncio.sleep(0.01)


# הפעלת הסימולציה
if __name__ == "__main__":
    sim = Two_bodies_on_incline()
    sim.start()