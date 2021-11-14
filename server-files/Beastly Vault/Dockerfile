FROM python:slim AS app

RUN pip install --no-cache-dir Flask
RUN pip install --no-cache-dir pycryptodome 

WORKDIR /app

COPY . .
ENV FLASK_APP=beastlyblocks.py
CMD ["python", "-m", "flask",  "run",  "--host=0.0.0.0", "--port=2246"]
