FROM python:2.7
MAINTAINER younglinuxer younglinuxer@gamil.com

COPY requirements.txt /requirements.txt

COPY corednspy/ /corednspy

RUN pip install -r /requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/

CMD [ "python", "/corednspy/run_etc.py"]
