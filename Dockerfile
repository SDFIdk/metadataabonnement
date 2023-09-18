FROM python:3.11.5-slim

ARG UNAME=niksk
ARG UID=2022
ARG GID=4004

RUN groupadd -g ${GID} -o ${UNAME}
RUN useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${UNAME}

USER ${UNAME}

WORKDIR /home/${UNAME}

RUN pip install Django==4.2.5
