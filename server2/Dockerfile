############################################################
# Dockerfile to build a simple Flask Application Container
############################################################

FROM orchardup/python:2.7
ADD /hello-flask /hello-flask
RUN pip install -r /hello-flask/requirements.txt
WORKDIR /hello-flask
CMD ["python","app.py"]
EXPOSE 80