import math
from constants import g

def calculate_accelerations(m1, theta1_deg, m2, theta2_deg, has_rope):
    """
    מחשב את תאוצות הגופים בהתאם למצב החוט (מחובר או מנותק).
    
    פרמטרים:
    m1, m2: המסות של הגופים (בק"ג)
    theta1_deg, theta2_deg: זוויות השיפוע של הגופים (במעלות)
    has_rope: ערך בוליאני המציין אם הגופים מחוברים (True) או מנותקים (False)
    
    מחזיר:
    (a1, a2) - תאוצות שני הגופים
    """
    # המרת זוויות למעלות (פונקציות טריגונומטריות ב-Python עובדות עם רדיאנים)
    theta1 = math.radians(theta1_deg)
    theta2 = math.radians(theta2_deg)
    
    if not has_rope:
        # תאוצה חופשית לכל גוף על המדרון שלו
        a1 = g * math.sin(theta1)
        a2 = g * math.sin(theta2)
        return a1, a2
        
    else:
        # חישוב תאוצה משותפת
        net_force = (m1 * g * math.sin(theta1)) - (m2 * g * math.sin(theta2))
        total_mass = m1 + m2
        
        a_system = net_force / total_mass
        
        # בהנחה שמערכת הצירים שלך דורשת סימנים הפוכים לגופים כשהם מחוברים
        # (המסה האחת יורדת והשנייה עולה, תלוי בכיווניות הוקטורים בסימולציה)
        return a_system, -a_system