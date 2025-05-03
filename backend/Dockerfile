FROM python:3.10-slim

WORKDIR /app

COPY ./DejaVuSans.ttf /usr/share/fonts/truetype/dejavu/

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt  --no-cache-dir

COPY . .

ENTRYPOINT [ "sh", "entrypoint.sh"]