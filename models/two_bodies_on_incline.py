#two_bodies_on_incline.py


from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley

#simulation parameters
LEFT_SLOPE = 20
RIGHT_SLOPE = 60
STARTING_POINT = 0.5
dt = 0.01


class Two_bodies_on_incline():


    def __init__(self):  # Constructor
        """
        this method constracts a simulation of Two_bodies_on_incline

        Args:
            base_position           : vector for locating the bottom of the base of the pulley

        Returns:
            none                    

        Raises:
            ValueError: none
        """     


    def start():

        #create scene
        scene.title = "2 Masses move on Double Ramp"
        scene.background = color.black
        scene.width = 800
        scene.height = 600 

        #create ramp
        myRamp = Ramp(LeftAngle=LEFT_SLOPE, 
                  RightAngle=RIGHT_SLOPE, 
                  DoubleRamp=True, 
                  RampColor=color.blue)


        #create masses
        m1 = Mass(name="m1",
                   tilted_degrees=-RIGHT_SLOPE,    #negative cause its a negative slope in relate to +x axis
                   tilt_axis=vector(0, 0, 1),    #tilt around z axis
                   length=2,
                   height=1,
                   width=1,
                   color = color.white,
                   )
        m1.x0 = STARTING_POINT
        m1.v0 = 0
        m1.acceleration = 10

        # 1. הגדרת המיקום כווקטור מקומי במערכת הצירים של המדרון
        m1_wanted_pos = vector(m1.x0, 0, 0)

        
        # 2. שליחת הווקטור המקומי לפונקציה כדי לקבל מיקום גלובלי, והצבת המסה
        m1.position = myRamp.right_slope_position(m1_wanted_pos)
        m1.mass_position()
       
        #create masses
        m2 = Mass( name="m2",
                    tilted_degrees=LEFT_SLOPE,
                    tilt_axis=vector(0, 0, 1),    #tilt around z axis
                    length=2,
                    height=1,
                    width=1,
                    color = color.white,
                    )

        m2.x0 = STARTING_POINT  
        m2.v0 = 0
        m2.acceleration = 10  

        # 1. הגדרת המיקום כווקטור מקומי במערכת הצירים של המדרון
        m2_wanted_pos = vector(m2.x0, 0, 0)

        
        # 2. שליחת הווקטור המקומי לפונקציה כדי לקבל מיקום גלובלי, והצבת המסה
        m2.position = myRamp.left_slope_position(m2_wanted_pos)
        m2.mass_position()

        #create pulley
        Mypulley = Pulley(base_position=myRamp.left_slope_position(vector(0,0,0))) 

        #--------------- Handle play/pause ---------------------------------------
        # משתנה בוליאני שקובע אם ההדמיה פועלת או לא
        running = False
        t = 0

        # הפונקציה שתופעל בעת לחיצה על הכפתור
        def toggle_play(b):
            nonlocal running
            running = not running # הפיכת המצב (אם שקר הופך לאמת, ולהיפך)
    
            # שינוי הטקסט על הכפתור בהתאם למצב
            if running: 
                b.text = "Pause"
            else:
                b.text = "Play"


        # יצירת הכפתור עצמו וקישור שלו לפונקציה
        play_button = button(text="Play", bind=toggle_play)
        #--------------------------------------------------------------------------



        #--------------- Handle Reset SIM ---------------------------------------
        def reset_sim(b):

            nonlocal running, t, m1_wanted_pos, m2_wanted_pos
            
            # 1. עצירת ההדמיה ועדכון כפתור ה-Play
            running = False
            play_button.text = "Play"
            t = 0
            
            # 2. איפוס משתני התנועה (חזרה לווקטורים מקומיים)
            m1.x0 = STARTING_POINT
            m2.x0 = STARTING_POINT

            m1_wanted_pos = vector(m1.x0, 0, 0)
            m2_wanted_pos = vector(m2.x0, 0, 0)
            
            # 3. החזרת הגופים למיקום ההתחלתי (בעזרת הווקטור)
            m1.position = myRamp.right_slope_position(m1_wanted_pos)
            m1.mass_position()
            
            m2.position = myRamp.left_slope_position(m2_wanted_pos)
            m2.mass_position()
        #----------------------------------------------------------------------


        # יצירת כפתור ה-Reset
        reset_button = button(text="Reset", bind=reset_sim)


        # main simulation loop:

        xleft, xright = myRamp.get_ramp_base_vertices()  #run until end of slope

        while True:

            if running:

                # עבור מסה 1
                if myRamp.right_slope_position(m1_wanted_pos).x < xright and myRamp.right_slope_position(m1_wanted_pos).y > 0:
                    
                    # חישוב הפיזיקה לאורך ציר ה-x של המדרון
                    m1_wanted_pos.x = m1.x0 + (m1.v0 * t) + (0.5 * m1.acceleration * (t**2))
                    
                    # עדכון המיקום הגלובלי וציור
                    m1.position = myRamp.right_slope_position(m1_wanted_pos)
                    m1.mass_position()

                # עבור מסה 2
                if myRamp.left_slope_position(m2_wanted_pos).x > -xleft and myRamp.left_slope_position(m2_wanted_pos).y > 0:
                    
                    # חישוב הפיזיקה לאורך ציר ה-x של המדרון
                    m2_wanted_pos.x = m2.x0 + (m2.v0 * t) + (0.5 * m2.acceleration * (t**2))
                    
                    # עדכון המיקום הגלובלי וציור
                    m2.position = myRamp.left_slope_position(m2_wanted_pos)
                    m2.mass_position()

                t = t + dt

            rate(100)                 
        
