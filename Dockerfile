FROM python:3.14-slim

WORKDIR /app

COPY VulnerableLogin.py .
COPY FixedLogin.py .
COPY templates/ ./templates/
COPY static/ ./static/

RUN pip install flask

EXPOSE 5000 5001

CMD ["python", "VulnerableLogin.py"]