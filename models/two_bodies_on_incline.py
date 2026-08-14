from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley
from constants import g

# simulation parameters
LEFT_SLOPE = 20
RIGHT_SLOPE = 60
PULLEY_POSITION = 0.5
M1_STARTING_POSITION = 1     # must be greater than PULLEY_POSITION
M2_STARTING_POSITION = 3     # must be greater than PULLEY_POSITION

# תאוצות כשהחוט מחובר (מערכת משותפת)
M1_COUPLED_ACCEL = 10
M2_COUPLED_ACCEL = -10

# תאוצות כשהחוט מנותק (נפילה חופשית על המדרון, יש להזין את הערכים הפיזיקליים הנכונים)
M1_FREE_ACCEL =  g * sin(radians(RIGHT_SLOPE))
M2_FREE_ACCEL =  g * sin(radians(LEFT_SLOPE))

dt = 0.01

class Two_bodies_on_incline():

    def __init__(self):
        pass

    def start(self):

        # create scene
        scene.title = "2 Masses move on Double Ramp"
        scene.background = color.black
        scene.width = 800
        scene.height = 600 

        # create ramp
        myRamp = Ramp(LeftAngle=LEFT_SLOPE, 
                      RightAngle=RIGHT_SLOPE, 
                      DoubleRamp=True, 
                      RampColor=color.blue)

        # create masses
        m1 = Mass(name="m1",
                   tilted_degrees=-RIGHT_SLOPE,
                   tilt_axis=vector(0, 0, 1),      #tilt around z axis
                   length=2,
                   height=1,
                   width=1,
                   color=color.white)
        m1.x0 = M1_STARTING_POSITION
        m1.v0 = 0
        m1.acceleration = M1_COUPLED_ACCEL # תאוצה התחלתית (עם חוט)

        m1_wanted_pos = vector(m1.x0, 0, 0)
        m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
        m1.mass_position()
       
        m2 = Mass(name="m2",
                   tilted_degrees=LEFT_SLOPE,
                   tilt_axis=vector(0, 0, 1),
                   length=2,
                   height=1,
                   width=1,
                   color=color.white)
        m2.x0 = M2_STARTING_POSITION  
        m2.v0 = 0
        m2.acceleration = M2_COUPLED_ACCEL # תאוצה התחלתית (עם חוט)

        m2_wanted_pos = vector(m2.x0, 0, 0)
        m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
        m2.mass_position()

        # create pulley
        Mypulley = Pulley(base_position=myRamp.left_slope_position(vector(0,0,0))) 
        top_pulley_pos = Mypulley.get_top_wheel_position()

        # יצירת החוט
        rope = curve(pos=[m1.get_top_center(), top_pulley_pos, m2.get_top_center()], color=color.white, radius=0.02)


        # משתנים גלובליים למצב המערכת
        running = False
        has_rope = True # משתנה חדש ששומר את מצב החוט
        t = 0

        # --------------- Handle play/pause ---------------------------------------
        def toggle_play(b):
            nonlocal running
            running = not running
            if running: 
                b.text = "Pause"
            else:
                b.text = "Play"

        play_button = button(text="Play", bind=toggle_play)
        
        # --------------- Handle Reset SIM ---------------------------------------
        def reset_sim(b=None):
            nonlocal running, t, m1_wanted_pos, m2_wanted_pos
            
            running = False
            play_button.text = "Play"
            t = 0
            
            m1.x0 = M1_STARTING_POSITION
            m2.x0 = M2_STARTING_POSITION

            m1_wanted_pos = vector(m1.x0, 0, 0)
            m2_wanted_pos = vector(m2.x0, 0, 0)
            
            m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
            m1.mass_position()
            
            m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
            m2.mass_position()

            # עדכון החוט והתאוצות בהתאם למצב הנוכחי של המתג
            if has_rope:
                rope.visible = True
                rope.modify(0, pos=m1.get_top_center())
                rope.modify(2, pos=m2.get_top_center())
                m1.acceleration = M1_COUPLED_ACCEL
                m2.acceleration = M2_COUPLED_ACCEL
            else:
                rope.visible = False
                m1.acceleration = M1_FREE_ACCEL
                m2.acceleration = M2_FREE_ACCEL

        reset_button = button(text="Reset", bind=reset_sim)

        # --------------- Handle Rope Switch ---------------------------------------
        scene.append_to_caption('  ') # קצת רווח ב-UI

        def toggle_rope(c):
            nonlocal has_rope
            has_rope = c.checked # קורא האם התיבה מסומנת (True/False)
            # מכיוון ששינוי תאוצה מצריך איפוס של משוואת הזמן, נפעיל אוטומטית Reset
            reset_sim()

        # הוספת מתג בוליאני לבחירת מצב החוט
        rope_checkbox = checkbox(bind=toggle_rope, text='Connect Rope', checked=True)
        # -------------------------------------------------------------------------


        # main simulation loop:
        xleft, xright = myRamp.get_ramp_base_vertices() 

        while True:
            if running:
                m1_next_pos = myRamp.right_slope_position(m1_wanted_pos)
                m2_next_pos = myRamp.left_slope_position(m2_wanted_pos)

                m1_can_move = PULLEY_POSITION < m1_next_pos.x < xright and m1_next_pos.y > 0
                m2_can_move = -xleft < m2_next_pos.x < -PULLEY_POSITION and m2_next_pos.y > 0

                if has_rope:
                    # מחוברים: זזים ביחד ועוצרים ביחד
                    if m1_can_move and m2_can_move:
                        # מסה 1
                        m1_wanted_pos.x = m1.x0 + (m1.v0 * t) + (0.5 * m1.acceleration * (t**2))
                        m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
                        m1.mass_position()

                        # מסה 2
                        m2_wanted_pos.x = m2.x0 + (m2.v0 * t) + (0.5 * m2.acceleration * (t**2))
                        m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
                        m2.mass_position()

                        # חוט
                        rope.modify(0, pos=m1.get_top_center())
                        rope.modify(2, pos=m2.get_top_center())

                        t = t + dt
                    else:
                        running = False

                else:
                    # מנותקים: כל גוף זז ועוצר בפני עצמו
                    if m1_can_move or m2_can_move:
                        if m1_can_move:
                            m1_wanted_pos.x = m1.x0 + (m1.v0 * t) + (0.5 * m1.acceleration * (t**2))
                            m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
                            m1.mass_position()
                        
                        if m2_can_move:
                            m2_wanted_pos.x = m2.x0 + (m2.v0 * t) + (0.5 * m2.acceleration * (t**2))
                            m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
                            m2.mass_position()

                        t = t + dt
                    else:
                        # שניהם הגיעו לקצה
                        running = False

            rate(100)