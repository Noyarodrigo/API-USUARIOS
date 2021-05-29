#base image
FROM python:3.6-slim

#working dir
WORKDIR /app/src

#copying all files
COPY ./requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install -r requirements.txt

COPY ./ ./
CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "wsgi:app"]
