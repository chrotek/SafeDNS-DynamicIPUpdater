# server Dockerfile
FROM python:3

# ADD safedns-ddns-configuration.py /
# ADD safedns-ddns-updater.py /
# ADD config.ini /
# ADD safedns-ddns-updater.log /

RUN pip install --upgrade pip && \
    pip install requests pick dnspython

CMD [ "python","-u","/safedns-ddns-updater.py" ]


