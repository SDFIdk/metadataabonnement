FROM python:3.11.5-slim

RUN apt update \
	&& apt upgrade -y

ARG UNAME=niksk
ARG UID=2022
ARG GID=4004

RUN groupadd -g ${GID} -o ${UNAME}
RUN useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${UNAME}

USER ${UNAME}

WORKDIR /home/${UNAME}

COPY requirements.txt /home/${UNAME}

RUN pip install --no-cache-dir -r /home/${UNAME}/requirements.txt
