#two_bodies_on_incline.py


from vpython import *
from entities.mass import Mass
from entities.ramp import Ramp
from entities.pulley import Pulley

#simulation parameters
LEFT_SLOPE = 20
RIGHT_SLOPE = 60
PULLEY_POSITION = 0.5
M1_STARTING_POSITION = 1     #must be greater than PULLEY_POSITION
M2_STARTING_POSITION = 3     #must be greater than PULLEY_POSITION
M1_ACCELERATION = 10
M2_ACCELERATION = -10
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
        m1.x0 = M1_STARTING_POSITION
        m1.v0 = 0
        m1.acceleration = M1_ACCELERATION

        # 1. הגדרת המיקום כווקטור מקומי במערכת הצירים של המדרון
        m1_wanted_pos = vector(m1.x0, 0, 0)

        
        # 2. שליחת הווקטור המקומי לפונקציה כדי לקבל מיקום גלובלי, והצבת המסה
        m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
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

        m2.x0 = M2_STARTING_POSITION  
        m2.v0 = 0
        m2.acceleration = M2_ACCELERATION 

        # 1. הגדרת המיקום כווקטור מקומי במערכת הצירים של המדרון
        m2_wanted_pos = vector(m2.x0, 0, 0)

        
        # 2. שליחת הווקטור המקומי לפונקציה כדי לקבל מיקום גלובלי, והצבת המסה
        m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
        m2.mass_position()

        #create pulley
        Mypulley = Pulley(base_position=myRamp.left_slope_position(vector(0,0,0))) 

        top_pulley_pos = Mypulley.get_top_wheel_position()

        # יצירת החוט. הוא מקבל רשימה של 3 מיקומים התחלתיים
        rope = curve(pos=[m1.get_top_center(), top_pulley_pos, m2.get_top_center()], color=color.white, radius=0.02)



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
            m1.x0 = M1_STARTING_POSITION
            m2.x0 = M2_STARTING_POSITION

            m1_wanted_pos = vector(m1.x0, 0, 0)
            m2_wanted_pos = vector(m2.x0, 0, 0)
            
            # 3. החזרת הגופים למיקום ההתחלתי (בעזרת הווקטור)
            m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
            m1.mass_position()
            
            m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
            m2.mass_position()


            # 4. איפוס מיקום החוט (קצוות החבל) למיקום ההתחלתי של המסות
            rope.modify(0, pos=m1.get_top_center())
            rope.modify(2, pos=m2.get_top_center())


        #----------------------------------------------------------------------


        # יצירת כפתור ה-Reset
        reset_button = button(text="Reset", bind=reset_sim)


        # main simulation loop:
        xleft, xright = myRamp.get_ramp_base_vertices()  #run until end of slope

        while True:
            
            if running:
                # חישוב המיקומים העתידיים לשני הגופים מראש
                m1_next_pos = myRamp.right_slope_position(m1_wanted_pos)
                m2_next_pos = myRamp.left_slope_position(m2_wanted_pos)

                # הגדרת תנאי הגבול לכל מסה במשתנים בוליאניים
                m1_can_move = PULLEY_POSITION < m1_next_pos.x < xright and m1_next_pos.y > 0
                m2_can_move = -xleft < m2_next_pos.x < -PULLEY_POSITION and m2_next_pos.y > 0

                # התנועה מתבצעת *רק* אם שני הגופים בתוך הגבולות
                if m1_can_move and m2_can_move:
                    
                    # --- עבור מסה 1 ---
                    m1_wanted_pos.x = m1.x0 + (m1.v0 * t) + (0.5 * m1.acceleration * (t**2))
                    m1.bottom_position = myRamp.right_slope_position(m1_wanted_pos)
                    m1.mass_position()

                    # --- עבור מסה 2 ---
                    m2_wanted_pos.x = m2.x0 + (m2.v0 * t) + (0.5 * m2.acceleration * (t**2))
                    m2.bottom_position = myRamp.left_slope_position(m2_wanted_pos)
                    m2.mass_position()

                    # --- עדכון מיקום החוט ---
                    rope.modify(0, pos=m1.get_top_center())
                    rope.modify(2, pos=m2.get_top_center())

                    # קידום הזמן
                    t = t + dt
                
                else:
                    # ברגע שאחד התנאים לא מתקיים (אחד הגופים הגיע לקצה), עוצרים את הסימולציה
                    running = False

            rate(100)            
        

#TODO: position the rope in the top of the masses
#and take care in generic case where no rope in the situation