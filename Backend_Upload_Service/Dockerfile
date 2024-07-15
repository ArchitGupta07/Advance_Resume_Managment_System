FROM python:3.11

WORKDIR /app

COPY dockerRequirements.txt dockerRequirements.txt
RUN pip install -r dockerRequirements.txt

RUN apt-get update && apt-get install -y openjdk-17-jre-headless

RUN apt-get install -y tesseract-ocr 
# libtiff5 libjbig0 liblcms2-2 libjpeg62-turbo libopenjp2-7 libwebp6

COPY . .

EXPOSE 8001

CMD [ "python", "main.py"]