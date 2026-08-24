FROM python:3.10

WORKDIR /app

# התקנת הספריות הבסיסיות בלבד (vpython, voila)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קבצי הפרויקט
COPY . .

EXPOSE 8080

# הרצת השרת בגרסה הנקייה ביותר
CMD ["voila", "run_sim.ipynb", "--port=8080", "--no-browser", "--Voila.ip=0.0.0.0"]