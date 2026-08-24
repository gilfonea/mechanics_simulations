FROM python:3.10

# הגדרת תיקיית העבודה בשרת
WORKDIR /app

# העתקת קובץ ההתקנות והתקנת הספריות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת כל שאר קבצי הפרויקט פנימה
COPY . .

# Render יודע לזהות את הפורט הזה באופן אוטומטי
EXPOSE 8080

# פקודת ההרצה של Voilà (ללא שם מחברת ספציפי, כדי להציג את התפריט הראשי)
CMD ["voila", "run_sim.ipynb", "--port=8080", "--no-browser", "--Voila.ip=0.0.0.0", "--enable_nbextensions=True"]