FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# expose default flask port
EXPOSE 5000 

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]