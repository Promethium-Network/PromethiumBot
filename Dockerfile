FROM python:3.11

ADD PromethiumBot.py .
ADD transcriptForwarder.py .
ADD welcomeMessage.py .

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

CMD [ "python", "./PromethiumBot.py" ]