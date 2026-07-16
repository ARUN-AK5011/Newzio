  FROM python:3.8
  LABEL maintainer="Lionex , thedeveloper.arun@gmail.com@gmail.com"
  RUN apt-get update
  RUN mkdir /app
  WORKDIR /app
  COPY . /app
  RUN pip install -r requirements.txt
  EXPOSE 5000
  ENTRYPOINT [ "python" ]
  CMD [ "main.py" ]