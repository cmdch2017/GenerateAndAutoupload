docker build -t autoupload .
docker run -it --rm -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix autoupload
