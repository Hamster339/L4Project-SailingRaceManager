FROM python:3.11

WORKDIR SailingRaceManagerImage/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "SailingRaceManager_project/manage.py","runserver","0.0.0.0:8000"]
