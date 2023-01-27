# To Do Application
> This application is user task manager for management daily workflow.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)


## General Information
- This project was created because I wanted to connect Flask with mongo database.
- I wanted to create simple web app.


## Technologies Used
- Python - version 3.10.6
- Flask - version 2.2.2


## Features
List the ready features here:
- database for user and tasks
- register and login user
- implementation in docker


## Setup
For start application with docker you need [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).


## Usage
The application can be build from sources or can be run in docker.

##### Build from sources
```bash
$ # Move to directory
$ cd folder/to/clone-into/
$
$ # Clone the sources
$ git clone https://github.com/mateuszgua/to-do-app.git
$
$ # Move into folder
$ cd to-do-app
$
$ # Create virtual environment
$ python3 -m venv my_env
$
$ # Activate the virtual environment
$ source my_env/bin/activate
$
$ # Start app
$ flask --app run.py run
$ # ...
$ # * Running on http://127.0.0.1:5000 
```

##### Start the app in Docker
```bash
$ # Move to directory
$ cd folder/to/clone-into/
$
$ # Clone the sources
$ git clone https://github.com/mateuszgua/to-do-app.git
$
$ # Move into folder
$ cd to-do-app
$
$ # Start app
$ docker-compose up --build
$ # ...
$ # frontend_1  |  * Running on http://127.0.0.1:5000
```

## Project Status
Project is: complete 


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Improve the frontend
