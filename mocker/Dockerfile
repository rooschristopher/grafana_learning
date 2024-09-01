FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=.py
EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080", "--debug"]
