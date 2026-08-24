FROM python:3.10
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /home/user/app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user . .
EXPOSE 7860
CMD ["voila", "run_sim.ipynb", "--port=7860", "--no-browser", "--Voila.ip=0.0.0.0", "--Voila.server_url=/"]
