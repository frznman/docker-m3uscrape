Docker m3u Scraper
=================

How to use this image
---------------------

### Run on host networking

This example uses host networking for simplicitly. Also note the `-v` argument. This directory will be used to output the resulting videos

```
sudo docker run -d --net="host" --name m3u-scraper shuaiscott/m3u-scraper
```

### Submitting a URL to scrape

Downloads can be triggered by supplying the `{{url}}` of the requested video through the Web UI or through the REST interface via curl, etc.

#### HTML

Just navigate to `http://{{address}}:9009/m3uscrape?url={{url}}` and enter the requested `{{url}}`.

#### Curl

```
curl -X POST --data-urlencode "url={{url}}" http://{{address}}:9009/m3uscrape
```

Implementation
--------------

The server uses [`bottle`](https://github.com/bottlepy/bottle) for the web framework

This docker image is based on [`python:3-alpine`](https://registry.hub.docker.com/_/python/) 

There is now a start-up script that updates all pip libraries so you'll always have the latest version of youtube-dl. To update, just restart the docker container.
