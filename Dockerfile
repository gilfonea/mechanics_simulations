FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# התקנת גרסה תואמת של notebook שתומכת במנגנון התקשורת של VPython
RUN pip install --no-cache-dir "notebook<7"

# רישום והפעלה של ערוץ התקשורת של VPython (ה-'glow')
RUN jupyter nbextension install --py vpython --sys-prefix
RUN jupyter nbextension enable --py vpython --sys-prefix

# העתקת כל שאר קבצי הפרויקט
COPY . .

# הגדרת המחברת כ"בטוחה" כדי להעלים אזהרות אבטחה
RUN jupyter trust run_sim.ipynb

EXPOSE 8080

CMD ["voila", "run_sim.ipynb", "--port=8080", "--no-browser", "--Voila.ip=0.0.0.0", "--enable_nbextensions=True"]