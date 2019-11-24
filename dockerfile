FROM python:3-alpine

WORKDIR /root

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "*/10    *       *       *       *       python acgwatch.py" >> /etc/crontabs/root

RUN printf "output_dir = \"csv/\"\ntimestamp_persist_file=\"persist/timestamp\"" >> "config.toml"
RUN mkdir persist

VOLUME [ "persist", "csv" ]

COPY *.py ./

CMD [ "crond", "-f" ]
