#base image
FROM python:3.6-stretch

#working dir
WORKDIR /app/src

#copying all files
COPY ./requeriments.txt ./
RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requeriments.txt

#port
EXPOSE 5000
COPY ./app.py ./
CMD ["python", "app.py"]
