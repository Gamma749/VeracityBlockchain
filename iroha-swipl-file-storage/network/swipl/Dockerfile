FROM deepnote/python:3.9
RUN apt update -y && apt install -y software-properties-common 
RUN apt-add-repository ppa:swi-prolog/stable
RUN apt install -y swi-prolog
RUN pip3 install --upgrade pip && pip3 install jupyter iroha
RUN mkdir swi-kernel
RUN cd swi-kernel && wget https://raw.githubusercontent.com/targodan/jupyter-swi-prolog/master/kernel.json
RUN jupyter kernelspec install swi-kernel --user
RUN rmdir --ignore-fail-on-non-empty swi-kernel
ENV DEFAULT_KERNEL_NAME SWI-Prolog
ENV BLOCKCHAIN_LOGGING 1
ENV FILE_TIMSTAMPING 1
ENV LOGGING_LEVEL 20
COPY run-notebook /usr/bin/run-notebook
COPY setup /setup
WORKDIR /setup
RUN pip install -r ./requirements.txt
WORKDIR /