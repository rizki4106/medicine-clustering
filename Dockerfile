FROM python:3.9.16

WORKDIR /medicine

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8502

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false", "--server.enableWebsocketCompression=false"]