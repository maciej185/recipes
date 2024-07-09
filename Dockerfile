FROM python:3.12

WORKDIR /recipes

COPY ./src/requirements.txt /recipes/src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /recipes/src/requirements.txt

COPY . /recipes

CMD ["fastapi", "run", "src/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]