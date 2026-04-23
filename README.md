# game-backlog-tracker
Originally a project for a generative AI assignment for one of my courses at Valencia College. I decied to add more to it after subitting the assignment.

## What was the assignment about?

The assignment was to build a database-backed application using object-oriented software and use any gnerative AI like ChatGPT and Gemini as a partner to build this application.

## What AI did I use?

While I was already familar using ChatGPT and Gemini, I decided to use Claude. I know... There's so much news how great Claude is, but I have yet to personally use Claude for anything. So I decided to use Claude Sonnet 4.6 model. Mainly because I wanted to see how great the free teir models are as most of us already know how great the paid tiers are.

## The result? 

In the end I have a colsole-based application using CRUD operations to interact with a database that dose not need a server to be run separately. Of course, there was naturally a issue that was resolved rather quickly.

## What am I adding?

I wanted to do more outside of the assignment as I thought it was beyond the scope and not needed a website interface. I might add more overtime as long my interest see ot that way. And also to make this reproducable on other systems than just my own I made a docker image. But note this application can be run without a docker container.

## Required 
- Docker (**If** using containers)
- Python 3 (**If** running app without containers)
- Basic python knowlege.
- Basic HTML knowlege.
- Basic CSS knowlege.

## Installation
Installing and running this application is very simular but can differ slighty depending if you choose to run with python installed on your system or using docker. My recommendation is that you use docker unless you plan to make further modifications.

### Docker

Asuming you have docker and docker compose installed.

Clone this repo: `git clone https://github.com/aaronplayz-sys/game-backlog-tracker.git`

Enter the directory and then run `docker compose up -d`.

This will take a moment as the image will be built locally as I do not host pre-built images.

This application will be running on port **5000**.

Optional: 

Import sample data, by doing `docker compose exec backlog-tracker python load_sample_data.py`

#### Making modifications

If wish to make modifications with docker, you need to rebuild the image each time you make a change, this is why I recommend that you have python installed on your system to see changes instantly without needed to build an image.

### Native python

This is the best method to run the console-based application (no webpage) and the web version. This is also the easist way to make changes and see them instantly.

Clone this repo: `git clone https://github.com/aaronplayz-sys/game-backlog-tracker.git`

Enter the directory and then run `python app.py` if you want the webpage interface. If you want to run the console-based app then run `python main.py`.

## Checklist
- [x] Import project files
- [x] Create pages
- [x] Add Flask routes
- [x] Create Dockerfile
- [x] Create docker-compose.yml
- [x] Write installation instructions
- [ ] Documentation
