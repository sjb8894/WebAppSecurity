FROM python:latest
RUN apt-get update && pip install bs4 && pip install lxml && mkdir /home/output/
COPY RequestAndParsing.py ~/RequestAndParsing.py
COPY act1step1.py ~/act1step1.py
ENTRYPOINT [ "python3" ]
CMD [ "~/act1step1.py" ]