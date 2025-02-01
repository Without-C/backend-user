# backend-user
## Run
```sh
docker build -t without-c-backend-user .
docker run --rm \
    -p 8000:8000 \
    -v $(pwd):/app \
    --name without-c-backend-user \
    without-c-backend-user
```
