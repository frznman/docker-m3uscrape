#!/bin/bash
docker stop m3u-test && docker rm m3u-test && docker rmi m3u-test
docker build ./ -t m3u-test && docker run -d --name m3u-test -p 9009:9009 m3u-test
