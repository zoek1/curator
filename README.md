# Curator

Curator is a tinder-like app to facilitate the curation of grants in the Gitcoin ecosystem allowing the user to enter “Yes”, “Unsure”, or “No” for each of the various requirements. Also for every curated grant one 0.1 GTC is rewarded to the user.

## 1. Setup
This will setup one enviroment with the server, db, and client.
```
docker-compose up
```

## 2. Seed
Download and format as the specified in the docs documents the grant information:

```
docker-compose run --rm server python scripts/seed.py 
```

## Demo

You can see the UI working on [http://localhost:8080/](http://localhost:8080/)

The list of grants of the current cycle can be consulted here: [http://localhost:5000/harvest](http://localhost:5000/harvest)

One specific grant curation can be consulted by the api here: [http://localhost:5000/harvest/3380](http://localhost:5000/harvest/3380)


https://www.loom.com/share/3d74629966e54d8ca7d878ff8ba4d03d


