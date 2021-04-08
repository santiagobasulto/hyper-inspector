FROM python:3.8-buster

RUN pip install hyper-inspector==0.0.4

WORKDIR /app

EXPOSE 5555

ENTRYPOINT ["hyper", "--ip", "0.0.0.0"]
