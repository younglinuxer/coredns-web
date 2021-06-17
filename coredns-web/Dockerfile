FROM python:2.7
MAINTAINER younglinuxer younglinuxer@gamil.com

COPY requirements.txt /requirements.txt

COPY corednspy/ /corednspy

RUN pip install -r /requirements.txt

CMD [ "python", "/corednspy/run.py"]
