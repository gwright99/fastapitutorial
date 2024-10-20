FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

ENV ghcontent=/ghcontent
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# https://fastapi.tiangolo.com/deployment/docker/#behind-a-tls-termination-proxy
# Tells uvicorn to trust headers since they'll come from the Gateway TLS 
# CMD [ "fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8081" ]
# CMD [ "bash", "-c", "fastapi run $ghcontent/app/main.py --proxy-headers --port 8081" ]
CMD [ "bash", "-c", "fastapi run $ghcontent/src/app/app.py --proxy-headers --port 8081" ]
