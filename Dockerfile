FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV DOC_PROJECT_URL="https://github.com/tttttx2/SimpleSignageProxy" 
ENV DOC_PROJECT_NAME="SimpleSignageProxy"

COPY app /app/

CMD [ "python3", "/app/main.py"]
