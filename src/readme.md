# Readme

Source code is located under "SailingRaceManger_project". Within this:

HTML pages are foun duner "templates"

Django bakend files are found under "Sailing Race Manager"

Bundeled JavaScript libaries are found under "Sailing Race Manager/static/Sailing Race Manager/Libraries"

## Build instructions
### Requirements
* Python 3
* Modern Web-Browser
* Packages: listed in `requirements.txt` 
* Tested on Windows 10 + Ubuntu Linux


### Build steps

1. Install the required packages with the command:

	pip install -r rquirements.txt

or open the file and install them manually.

2. To create and populate the database with the 2023 Portsmouth Yardstick hanidcap numbers, run the following command from the "SailingRaceManager" folder:

	python populate.py

### Run steps

1. To run the Web App localy, run the following command from the same place:

	python manage.py runserver

2. Navigate to the Url that is given to open the Web App.

### Test steps

1. Follow the steps above in "Run steps", and navigate any web browser to the given URL. If the leader Board page is displayed, the software is working correctly.

2. To run the Automated unit tests, run the following command:

 python manage.py test

### Public hosting

You can easily host the web-App publicly by building a docker image useing the suplyed docker file.

The image can be used to host on a provider of your choice.

## Embeding Leaderbord on another website

To embed the leader board of any series on another website, use an <iframe> html tag and link it to the following URL:

	<Top LevelDomain>/embedded-leaderboard/<Series Name>

To ensure the correct series name is used, navigate to the Sereis editor on your chosen, and get the Series name form the end of the URL. e.g.:


	<Top LevelDomain>/admin-home/series-editor/<Series name is here>


