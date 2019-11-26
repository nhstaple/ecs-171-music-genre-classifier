#Docker image that is used to run the code
#Author: Spencer Grossarth
FROM tensorflow/tensorflow:latest-py3
COPY requirements.txt /
RUN pip3 -V
RUN pip3 install -r /requirements.txt
RUN apt-get install --yes curl
RUN curl --silent --location https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install --yes nodejs
RUN apt-get install --yes build-essential
COPY . /app
WORKDIR /app/Front_End
RUN npm install
RUN npm run build
WORKDIR /app/Back_End
EXPOSE 8080
EXPOSE 3000
ENTRYPOINT [ "python" ]
CMD [ "backend.py" ]
