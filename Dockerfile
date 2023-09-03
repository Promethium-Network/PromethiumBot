FROM python:3.11.4

ADD main.py .
ADD blockhuntstats.py .
ADD sand.py .
ADD serverembeds.py .
ADD serverstatusembeds.py .
ADD skillstop.py .
ADD transcriptforwarder.py .
ADD sand.mp3 .
ADD requirements.txt .

RUN apt update
RUN apt-get install -y ffmpeg
RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]