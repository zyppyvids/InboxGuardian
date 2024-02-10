FROM python:3.7.9
ENV DockerHOME=/home/app/modelswrapper
  
RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip  

COPY . $DockerHOME

RUN pip install -r requirements.txt  

CMD python models_wrapper.py