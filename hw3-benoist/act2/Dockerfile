FROM python:latest
RUN apt-get update && pip install bs4 && pip install lxml && mkdir /home/output/
COPY RequestAndParsing.py ~/RequestAndParsing.py
COPY act2.py ~/act2.py
ENTRYPOINT [ "python3" ]
CMD [ "~/act2.py" ]