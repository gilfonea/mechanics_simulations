FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["voila", "run_sim.ipynb", "--port=8080", "--no-browser", "--Voila.ip=0.0.0.0", "--enable_nbextensions=True"]