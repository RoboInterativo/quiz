FROM python:3.6-slim
RUN mkdir /home/bot &&\
    pip install virtualenv
COPY files/bot.py files/config.yml files/quest.txt  files/requirements.txt /hom$
RUN chown 1001:1001 /home/bot/* -R && chmod 777 /home/bot/
USER 1001
RUN cd /home/bot && mkdir /home/bot/venv && python -m virtualenv venv &&\
    . ./venv/bin/activate && pip install -r requirements.txt
WORKDIR /home/bot/

CMD . ./venv/bin/activate &&python bot.py
