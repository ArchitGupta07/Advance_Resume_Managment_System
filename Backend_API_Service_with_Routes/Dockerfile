FROM python:3.11

WORKDIR /app

COPY dockerRequirements.txt dockerRequirements.txt
RUN pip install -r dockerRequirements.txt

RUN apt-get update && apt-get install -y openjdk-17-jre-headless


COPY . .

EXPOSE 8000

CMD [ "python", "main.py"]