# Running with docker

> **WARNING** Currently not working

```
# Build the docker container image
docker build -t matrixpi-image .

# Run the container
docker run --rm -p 5000:5000 ` -e DISABLE_MATRIX=1 `-v ${PWD}:/app `avans-matrix-board
```
