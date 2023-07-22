FROM apache/nifi:latest

RUN addgroup --gid 20 mygroup
RUN adduser --disabled-password --gecos "" --force-badname --ingroup 20 myuser 
USER myuser

CMD ["/bin/bash"]