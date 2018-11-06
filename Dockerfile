FROM  ubuntu:latest
MAINTAINER Shashank Gupta "shashank31mar@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV FLASK_ENV=development JWT_SECRET_KEY=shashank
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run.py"]