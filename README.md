# Intro
This is an unfinished toy project for visualizing construction activity in San Jose California. Uses Django for the backend, and React for the frontend.

San Jose City API located here: http://data.sanjoseca.gov/developers/

## Active Building permits

(example using httpie https://github.com/jkbrzt/httpie API key available at link above)
```sh
http http://api.data.sanjoseca.gov/api/v2/datastreams/ACTIV-BUILD-PERMI/data.json/ auth_key==xxyyzz limit==50
```

In the end I just downloaded the CSV from here http://data.sanjoseca.gov/dataviews/230622/active-building-permits/ and created a (django) management command to import into mysql


# Setup

1. Install docker
2. `docker pull mysql`
3. `docker pull python`
4. Log into python container (eg. `docker exec -it <container-id> bash`) and run `python manage.py migrate`
5. Get an API key from mapbox, and modify in `main.js` and in `importconstruction.py` files (search for `<api key>`)
6. Download csv (http://data.sanjoseca.gov/dataviews/230622/active-building-permits/ ) and run `python manage.py importconstruction <csv file>`
7. View on `http://localhost:8000`

## Dev Log

1. Installed docker for OS X
2. `docker pull mysql`
3. `docker pull python`
4. created the `src/` subdir for django files, and `docker_env/` dir for docker setup
5. Added the `Dockerfile` that describes the python container, and the `docker-compose.yml` that describes the two dependant containers (python & db)
6. Ran `python manage.py migrate` for django, started "mapview" app. 
7. Created the model for building permit data, ran `python manage.py makemigrations mapview`, then ran `migrate` again to sync
8. Set up managed volume for db to preserve data across restarts
9. Set up the import script, and ran with `python manage.py importconstruction sjcitydata.csv`
10. Got a basic index page going from Django, then added javascript libraries for front-end work (mapbox, react, bable for JSX, axios for http requests & my own main.js) as wells as basic bootstrap CSS.
11. Set up the mapbox window centered on San Jose
12. Created an init view to return a simple JSON response
